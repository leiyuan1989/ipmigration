# -*- coding: utf-8 -*-
"""

@author: leiyuan
"""
import json
import pandas as pd
import matplotlib.pyplot as plt
from z3 import Optimize,Solver
from z3 import Int, Bool, Or, And, Not, Distinct, If, is_true,sat

from itertools import combinations, chain
import itertools

import math
import time

import logging
logger = logging.getLogger(__name__)

#ipmigration\cell\apr\pr\__pycache__\place\queue.json
queue_data = 'ipmigration/cell/apr/pr/place/queue.json'


output_mappings = {
    frozenset({'out_Q', 'out_QN', 'out_Q_2'}): [['out_Q_2'], ['out_Q', 'out_QN']],
    frozenset({'out_Q', 'out_Q_2'}): [['out_Q_2', 'out_Q']],
    frozenset({'out_Q', 'out_QN'}): [['out_Q', 'out_QN']],
    frozenset({'out_Q'}): [['out_Q']],
    frozenset({'out_QN'}): [['out_QN']],
    frozenset({'out_ECK'}): [['out_ECK']]
}



'''
Based on the design objectives, to better preserve the design intent, 
an enumeration method is employed here. 
In the case of new netlists, they need to be optimized according to the design.
'''

class PatternAPR:
    def __init__(self,ckt,sub_ckts,place_file,load=False):
        self.name = ckt.name
        self.ckt = ckt
        self.sub_ckts = sub_ckts
        self.place_file = place_file
        self.load = load
        self.placement = []
        #combo                
        #temp 
        if load:
            self.queue = self.place_file[self.name]
            self.ready=True
                    
        else:
            # sub_ckts_names = [k + ': ' + v.ckt.name for k,v in self.sub_ckts.items()]
            queue = self.cal_queue()
            self.write_place_file(queue)
            self.ready=False

    
    def place(self):
        self.queue = split_list_elements(self.queue) 
        for combo in self.queue:
            if len(combo) ==1:
                p = self.sub_ckts[combo[0]]
                self.placement.append(p.place)
                
            else:
                if type(combo[0]) is list:
                    t_placement = []
                    if len(combo[0]) == 1:
                        p = self.sub_ckts[combo[0][0]]
                        t_placement += p.place
                    else:
                        p1 = self.sub_ckts[combo[0][0]]
                        p2 = self.sub_ckts[combo[0][1]]    
                        t_placement += p1.flip_place() + p2.place
                    t_placement.append({'P':None,'N':None})
                    if len(combo[1]) == 1:
                        p = self.sub_ckts[combo[1][0]]
                        t_placement += p.place
                    else:
                        p1 = self.sub_ckts[combo[1][0]]
                        p2 = self.sub_ckts[combo[1][1]]                  
                        t_placement += p1.flip_place() + p2.place                 
                        
                    self.placement.append(t_placement)  
                    
                    
                else:
                    p1 = self.sub_ckts[combo[0]]
                    p2 = self.sub_ckts[combo[1]]                  
                    self.placement.append(p1.flip_place() + p2.place)
        
        self.net_loc = {}
        loc = 0
        for blk in self.placement:      
            for pn in blk:
                p = pn['P']
                n = pn['N']
                if not(p) and not(n):
                    loc +=1
                else:
                    if p:
                        self.net_loc[(p,'S')] = (loc,4,1)
                        self.net_loc[(p,'G')] = (loc+1,4,0)
                        self.net_loc[(p,'D')] = (loc+2,4,1)                        
                    if n:
                        self.net_loc[(n,'S')] = (loc,1,1)
                        self.net_loc[(n,'G')] = (loc+1,1,0)
                        self.net_loc[(n,'D')] = (loc+2,1,1)       
                    loc+=2
            loc+=1
        
        self.grid_size = (max([t[0] for t in self.net_loc.values()]),6)
        #6 is for init-place, more vertical grid can be add during routing.
        self.vdd_nets = []
        self.vss_nets = []
        self.abut_nets = []
        self.gg_nets = []
        self.nets = {}
        
        
        
        # print(self.net_loc,self.ckt.nets)
        
        for k,v in self.ckt.nets.items():
            if k == 'VDD':
                self.vdd_nets = [self.net_loc[t] for t in v]
            elif k == 'VSS':
                self.vss_nets = [self.net_loc[t] for t in v]        
            else:
                nets = [self.net_loc[t] for t in v]  
                if len(set(nets)) == 1:
                    self.abut_nets.append(nets)
                else:
                    to_extract = set()
                    gg_nets = []
                    for e1, e2 in combinations(nets, 2):
                        if e1[0] == e2[0] and e1[2] == 0 and e2[2] == 0:
                            to_extract.add(e1)
                            to_extract.add(e2)
                            self.gg_nets.append([e1,e2])
                            gg_nets.append((e1[0],2.5,e1[2]))
                            
                    filtered_data = [item for item in nets if item not in to_extract] + gg_nets

                    # filtered_data = [item for item in nets if item not in set(to_extract)]                    
                    
                    self.nets[k] = list(set(filtered_data))

        
        # x_coordinates = extract_x_coordinates(self.nets)
        self.crossings = calculate_crossings(self.nets)
        # edges = [
        #     ((10, 4, 0), (10, 1, 0)),  # 连接点 (1,1) 到 (1,2)
        #     # ((2, 0, 0), (3, 1, 0)),  # 连接点 (2,0) 到 (3,1)
        #     # 添加更多连接...
        # ]
        # fig, ax = visualize_pins(self.name, self.crossings,edges)
        # plt.show() 
                
        self.show_placement()
        # print(self.placement)
            
        
    def route(self):
        self.router = IPRouter(self.grid_size ,self.crossings, vertical_tracks = 6)
        self.router.route()
        
        
        
        
    def show_placement(self):
        line_p = ''
        line_n = ''
        for blk in self.placement:
            line_p = line_p + ' ## '
            line_n = line_n + ' ## '            
            for pn in blk:
                p = pn['P']
                n = pn['N']
                if not(p) and not(n):
                    line_p = line_p + ' ## '
                    line_n = line_n + ' ## '
                else:
                    if p:
                        line_p = line_p + '| %6s %6s %6s |'%(p.S,p.G,p.D)
                    else:
                        line_p = line_p + '| %6s %6s %6s |'%('','','')
                    if n:
                        line_n = line_n + '| %6s %6s %6s |'%(n.S,n.G,n.D)
                    else:
                        line_n = line_n + '| %6s %6s %6s |'%('','','')
        logger.info(line_p)
        logger.info(line_n) 
        # print(line_p+'\n'+line_n+'\n')
    
    
    def cal_queue(self):
        with open(queue_data, 'r') as f:
            data = json.load(f)
        ckt_type = self.ckt.ckt_type 
        if ckt_type == 'latch':
            init_queue = data['queue_la']
        elif ckt_type == 'clockgate':
            init_queue = data['queue_cg']
        elif ckt_type == 'ff':
            init_queue = data['queue_ff']  
        elif ckt_type == 'scanff':
            init_queue = data['queue_sf']
        else:
            raise ValueError('ckt type error!')

        queue_t = {t:[] for t in init_queue}
        ininv = []
        out = []
        #cal queue and out and ininv
        for ckt_name in self.sub_ckts:
            for key in queue_t:
                if ckt_name == key:
                    queue_t[key].append(ckt_name)

            if 'ininv' in ckt_name:
              ininv.append(ckt_name)  
            if 'out' in ckt_name:
                out.append(ckt_name)
        
        out0=[]
        out1=[]
        #process out
        out_set = frozenset(out)
        if out_set in output_mappings:
            out_queue = output_mappings[out_set]
            if len(out_queue) == 1:
                out1 = out_queue[0]
            elif  len(out_queue) == 2:
                out1 = out_queue[1]
                out0 = out_queue[0]

        else:
            raise ValueError(out_set)

        #insert ininv to queue  
        #ininv_r0 is merge with output
        if 'ininv_RN_0' in ininv:
            ininv.remove('ininv_RN_0')
            if len(out1) == 2:
                out0 = ['ininv_RN_0']  + out0
            elif len(out1) == 1:
                out1 = out1 + ['ininv_RN_0']  
        
        if 'ininv_SN_0' in ininv:
            ininv.remove('ininv_SN_0')
            queue_t['cross1'] = ['ininv_SN_0','cross1']
            
        if 'ininv_SE_0' in ininv:
            ininv.remove('ininv_SE_0')
            queue_t['sesi'] = ['ininv_SE_0','sesi']            
       
        if 'ininv_E_0' in ininv:
            ininv.remove('ininv_E_0')
            # print('test1',queue_t)
            out1 = out1  + ['ininv_E_0']           
        
        queue_t['ininv'] = ininv
        for k,v in queue_t.items():
            if not v:
                queue_t[k] = 'NA'
            elif len(v) == 1:
                queue_t[k] = v[0]
            else:
                queue_t[k]  = '-'.join(v)
        

        out0 = '-'.join(out0) if len(out0) > 1 else ''.join(out0) 
        out1 = '-'.join(out1) if len(out1) > 1 else ''.join(out1) 
        if out0:
            queue_t['out'] = out0+'|'+out1 
        else:
            queue_t['out'] = out1 
        
        queue = [v for k,v in queue_t.items() if v != 'NA']
        
        return queue
        
        # print(queue_t,ininv)
    
    
    def cal_ext_net_mat(self):
        ext_net_mat = [[0 for _ in range(len(self.sub_ckts))] for _ in range(len(self.sub_ckts))]
        ext_net_mat_dict = {}
        for k1,v1 in self.sub_ckts.items():
            for k2,v2 in self.sub_ckts.items():
                if k1 != k2:
                    ext_net_mat_dict[(k1,k2)] = self.extract_ext_nets(v1.net_map, v2.net_map)
    
        self.ext_net_mat_dict = ext_net_mat_dict
        for k,v in ext_net_mat_dict.items():
            n1 = self.sub_ckts_num[k[0]]
            n2 = self.sub_ckts_num[k[1]]
            ext_net_mat[n1][n2] = len(v)
        self.ext_net_mat = ext_net_mat

        
    def extract_ext_nets(self,net_map1,net_map2):
        ext_nets = []
        for k1,v1 in net_map1.items():
            for k2,v2 in net_map2.items():
                if k1 != 'VDD' and k1 != 'VSS':
                    if v1 == v2:
                        if not(v1 in ext_nets):
                            ext_nets.append(v1)
        return ext_nets


            

    def write_place_file(self,queue):
        with open(self.place_file,'a+') as f:
            line = '%-10s,'%(self.name)
            ql = len(queue) 
            for i in range(10):
                if i < ql:
                    name = queue[i]
                else:
                    name = 'NA'
                
                line += '%-30s,'%(name)
            f.write(line[:-1]+'\n')



#Integer Programming, IP
class IPRouter:
    #satisfiability modulo theories 
    def __init__(self,shape, crossings, vertical_tracks):
        self.crossings = crossings
        self.x_lim,self.y_lim = shape

    
    def route(self):
        self.gen_constraints(self.crossings)
    
    def gen_constraints(self,crossings):
        var = {}
        const = {}
        s = Solver() 
        for k,col in crossings.items():
            dist = {}
            for net in col['cross']:
                v = Int('%d_%s'%(k,net))
                var[(k,net)] =v
                s.add(v>=0)
                s.add(v<=5)
                dist[net] = v
                
                if 
                
            s.add(Distinct(list(dist.values()) ) )        
            
            for net
            
            
            
            new_const = self.col_constriants(s,col,dist)

            
            

        
        
        
        # Constraint 1: Positions are bounded.   
    
        self.variables = var
        # for k,v in self.variables.items():
        #     s.add(v>=0)
        #     s.add(v<=5)
    
        if s.check() == sat:
            m = s.model()
            self.result = {k:m[v] for k,v in self.variables.items()}
            # self.result = [(d.name(), m[d]) for d in m.decls()] 
        else:
            #not satisfied
            pass
    def col_constriants(self, solver,col,dist):
        
        #TODO: need return info like 'common AA' to detial pr 
        const = {}
        if len(col['pin']) == 2:
             n1,p1 = col['pin'][0]
             n2,p2 = col['pin'][1]
             if n1==n2 and p1[2]==1 and p2[2]==1:
                #common AA
                a_max = p2[1]-1 
                a_min = p1[1]+1
                x = dist[n1]
                lower_bound,upper_bound = self.merge_range(x, (a_min,a_max))
                
                # lower_bound = If(x < a_min, If(x < a_max, x, a_max), If(a_min < a_max, a_min, a_max))
                # upper_bound = If(x > a_max, If(x > a_min, x, a_min), If(a_max > a_min, a_max, a_min))
                for name,v in dist.items():
                    if name != n1:
                        #common a and its net (maybe top or bottm), all the range are blocked
                        solver.add(Or(v < lower_bound, v > upper_bound))
                        const[n1] = (lower_bound,upper_bound)
             
             elif n1!=n2 and p1[2]==0 and p2[2]==0:
                 #diff poly
                 pass
             elif n1!=n2 and p1[2]==1 and p2[2]==1:
                 #diff AA
                 print(col)
                 pass
             else:
                 print(col)
                 raise ValueError
             # if p1[2] == 1 and 
             
             
            
        elif len(col['pin']) == 1:
             n1,p1 = col['pin'][0]
             if p1[1] == 2.5:
                 #common gt
                 pass
             elif p1[1] == 4:
                 pass
             elif p1[1] == 1:
                 pass                
             else:
                 print(col)
                 raise ValueError    
        return const      
    @staticmethod
    def merge_range(x, range_):
        a_min,a_max = range_
        lower_bound = If(x < a_min, If(x < a_max, x, a_max), If(a_min < a_max, a_min, a_max))
        upper_bound = If(x > a_max, If(x > a_min, x, a_min), If(a_max > a_min, a_max, a_min))
        return (lower_bound,upper_bound)

    def _place(self, pmos_list, nmos_list, cell_width, pairs, vertical_tracks_pmos = 1, vertical_tracks_nmos = 1):
        #TODO find relationship before run this and try decrease the running time
        
        # Wrapper arount solver.add

            
        assert len(nmos_list) <= cell_width 
        assert len(pmos_list) <= cell_width 
        #how to add some constraints to generate more 
        # transistors = []
        # transistors.extend(nmos_list)
        # transistors.extend(pmos_list)

        solver = Optimize()

        # Create symbols for transistor positions.
        pmos_loc = {t: (Int("pmos_{}_x".format(t.name)), Int("pmos_{}_y".format(t.name))) for t in pmos_list}
        nmos_loc = {t: (Int("nmos_{}_x".format(t.name)), Int("nmos_{}_y".format(t.name))) for t in nmos_list}
        # Create boolean symbols for transistor flips.
        pmos_flipped = {t: Bool("pmos_{}_flipped".format(t.name)) for t in pmos_list}     
        nmos_flipped = {t: Bool("nmos_{}_flipped".format(t.name)) for t in nmos_list}          
        
        # transistor_positions = {t: (Int("transistor_{}_x".format(i)), Int("transistor_{}_y".format(i)))
        #                         for i, t in enumerate(transistors)}
        # # Create boolean symbols for transistor flips.
        # # Each transistor can be flipped (source/drain swapped).
        # transistor_flipped = {t: Bool("transistor_{}_flipped".format(i))
        #                       for i, t in enumerate(transistors)}

        # Constraint 1: Positions are bounded.      
        for x, y in pmos_loc.values():
            # Add bounds on positions.
            solver.add(x > 0)# begin from 1
            solver.add(y > 0)
            # Add upper bounds on transistor positions.
            solver.add(x <= cell_width)
            solver.add(y <= vertical_tracks_pmos)
        for x, y in nmos_loc.values():
            # Add bounds on positions.
            solver.add(x > 0)
            solver.add(y > 0)
            # Add upper bounds on transistor positions.
            solver.add(x <= cell_width) # <=
            solver.add(y <= vertical_tracks_nmos)            
            
        # Constraint 2: No same x positions
        d_pmos = Distinct([x for x,y in pmos_loc.values()])
        d_nmos = Distinct([x for x,y in nmos_loc.values()])       
        solver.add(d_pmos)
        solver.add(d_nmos)        

        # Constraint 3: PN pair
        # for tn in nmos_list:
        #     for tp in pmos_list:
        #         if tn.gate_net == tp.gate_net:
        #             (xn, yn) = nmos_loc[tn]
        #             (xp, yp) = pmos_loc[tp]
        #             same_x = xn == xp
        #             solver.add_soft(same_x,weight=3)
        for p,n in pairs:
            (xn, yn) = nmos_loc[n]
            (xp, yp) = pmos_loc[p]
            # print(xn,xp,p,n)
            
            solver.add(xn == xp)
        # print(solver)                  
        # Constraint 4: Abutment, Diffusion sharing
        # If two transistors are placed side-by-side then the abutted sources/drain nets must match.

        # Loop through all potential (left, right) pairs.
        for a, b in combinations(pmos_list, 2):
            for t_left, t_right in [(a, b), (b, a)]:
                xl, yl = pmos_loc[t_left]
                xr, yr = pmos_loc[t_right]

                # Checks if t_left is left neighbor of t_right.
                are_neighbors = And(
                    yl == yr,
                    xl + 1 == xr
                )

                # Go through all combinations of flipped transistors
                # and check if they are allowed to be directly abutted if flipped
                # in a specific way.
                flip_combinations = [[False, False], [False, True], [True, False], [True, True]]
                for flip_l, flip_r in flip_combinations:
                    l = t_left.flipped() if flip_l else t_left
                    r = t_right.flipped() if flip_r else t_right

                    if l.drain_net != r.source_net:
                        # Drain/Source net mismatch.
                        # In case the transistors are flipped that way,
                        # they are not allowed to be direct neighbors.
                        solver.add(
                            Implies(
                                And(pmos_flipped[t_left] == flip_l,
                                    pmos_flipped[t_right] == flip_r),
                                Not(are_neighbors)
                            )
                        )
        for a, b in combinations(nmos_list, 2):
            for t_left, t_right in [(a, b), (b, a)]:
                xl, yl = nmos_loc[t_left]
                xr, yr = nmos_loc[t_right]

                # Checks if t_left is left neighbor of t_right.
                are_neighbors = And(
                    yl == yr,
                    xl + 1 == xr
                )

                # Go through all combinations of flipped transistors
                # and check if they are allowed to be directly abutted if flipped
                # in a specific way.
                flip_combinations = [[False, False], [False, True], [True, False], [True, True]]
                for flip_l, flip_r in flip_combinations:
                    l = t_left.flipped() if flip_l else t_left
                    r = t_right.flipped() if flip_r else t_right

                    if l.drain_net != r.source_net:
                        # Drain/Source net mismatch.
                        # In case the transistors are flipped that way,
                        # they are not allowed to be direct neighbors.
                        solver.add(
                            Implies(
                                And(nmos_flipped[t_left] == flip_l,
                                    nmos_flipped[t_right] == flip_r),
                                Not(are_neighbors)
                            )
                        )
        
        # Constraint 5: Route Congestion
        # Extract all net names.
        nets = set(chain(*(t.terminals() for t in pmos_list + nmos_list)))  #clear vdd vss

        # Create net bounds. This will be used to optimize
        # the bounding box perimeter of the nets (for wiring length optimization).
        net_max_x = {net: Int("net_max_x_{}".format(net))
                     for net in nets}

        net_min_x = {net: Int("net_min_x_{}".format(net))
                     for net in nets}

        net_max_y = {net: Int("net_max_y_{}".format(net))
                     for net in nets}

        net_min_y = {net: Int("net_min_y_{}".format(net))
                     for net in nets}

        for t in pmos_list:
            x, y = pmos_loc[t]

            # TODO: Net positions dependent on transistor terminal.
            #       Now, the net position equals the transistor position.
            #       Make it dependent on the actual terminal (drain, gate, source).
            #       Also depends on transistor flips.
            for net in t.terminals():
                solver.add(x <= net_max_x[net])
                solver.add(x >= net_min_x[net])
                # add_assertion(y <= net_max_y[net])
                # add_assertion(y >= net_min_y[net])

        for t in nmos_list:
            x, y = nmos_loc[t]

            # TODO: Net positions dependent on transistor terminal.
            #       Now, the net position equals the transistor position.
            #       Make it dependent on the actual terminal (drain, gate, source).
            #       Also depends on transistor flips.
            for net in t.terminals():
                solver.add(x <= net_max_x[net])
                solver.add(x >= net_min_x[net])
                # add_assertion(y <= net_max_y[net])
                # add_assertion(y >= net_min_y[net])

        # Optiimization goals
        # Note: z3 uses lexicographic priorities of objectives by default.
        # Here, the cell width is optimized first.
        # Could be interesting: z3 could also find pareto fronts.

        # # Optimization objective 1
        # # Minimize cell width.
        # solver.minimize(max_x)

        # Optimization objective 2
        # Minimize wiring length (net bounding boxes)
        # TODO: sort criteria by what? Number of terminals?

        for net in nets:
            # TODO: skip VDD/GND nets
            solver.minimize(net_max_x[net] - net_min_x[net])
            solver.minimize(net_max_y[net] - net_min_y[net])

        # TODO: optimization objective for pin nets.


        #
        logger.info("smt_placer-> Run SMT optimizer")
        is_sat = solver.check() == sat

        logger.info("smt_placer-> Is satisfiable: %s", is_sat)
        
        if is_sat:
            model = solver.model()
            # print(solver,model)
            assert len(model) > 0, "model is empty"
            #return model
        
            placements = Placement(cell_width)
            # cell = Cell(cell_width)
            # rows = [cell.lower, cell.upper]
            for p,n in pairs:
                (xn, yn) = nmos_loc[n]
                (xp, yp) = pmos_loc[p]
                # print('xx', model[xn],model[xp])
                
            for t in pmos_list:
                x, y = pmos_loc[t]
                x = model[x].as_long()
                # y = model[y].as_long()  
                flip = is_true(model[pmos_flipped[t]])
                transistor = t.flipped() if flip else t
                placements.upper[x - 1] = transistor
    
            for t in nmos_list:
                x, y = nmos_loc[t]
                x = model[x].as_long()
    
                # y = model[y].as_long()  
                flip = is_true(model[nmos_flipped[t]])
                transistor = t.flipped() if flip else t
                placements.lower[x - 1] = transistor        
            
            return [placements]
        else:
            return [] # No solution found

    def pn_relation(self,pmos,nmos):
        p_g = pmos.gate_net
        p_s = pmos.source_net
        p_d = pmos.drain_net
        n_g = nmos.gate_net
        n_s = nmos.source_net
        n_d = nmos.drain_net        
        
        common_g = int(p_g == n_g)
        
        if (p_s == n_s) and (p_d == n_d):
            common_ds1 = 2
        elif(p_s == n_s) or (p_d == n_d):
            common_ds1 = 1
        else:
            common_ds1 = 0
        
        if (p_s == n_d) and (p_d == n_s):
            common_ds2 = 2
        elif(p_s == n_d) or (p_d == n_s):
            common_ds2 = 1
        else:
            common_ds2 = 0        
        
        #6 = 4 + 2 5 = 4 + 1 4 = 4 + 0  2 = 0 + 2 1 = 0 + 1 0 = 0 + 0
        return 4*common_g + max(common_ds1,common_ds2)
            


    def pn_pairs(self, pmos_list, nmos_list):
        pairs_score = {}
        mos_list = pmos_list +  nmos_list
        for p in pmos_list:
            for n in nmos_list:
                pairs_score[(p,n)] = self.pn_relation(p, n)
        
        pn_pairs = []
        # paired = []
        
        pairs_score = sorted(pairs_score.items(), key=lambda x: x[1],reverse=True)    
        for pair, score in pairs_score:
            if score >=2:
                p,n  = pair
                if (p in pmos_list) and (n in nmos_list):
                    pn_pairs.append(pair)
                    pmos_list.remove(p)
                    nmos_list.remove(n)

        return pn_pairs,pmos_list,nmos_list
        
    def place(self, devices, vertical_tracks_pmos = 1, vertical_tracks_nmos = 1):
        """
        Place transistors using an SMT solver (Z3).
        :param transistors list
        :return: Placement.
        """
        nmos_list = [t for t in devices if t.t == 'N']
        pmos_list = [t for t in devices if t.t == 'P']

        minimal_cell_width = math.ceil(max(len(nmos_list), len(pmos_list)))
        maximal_cell_width = max(len(nmos_list), len(pmos_list)) * 3 #?
        
        time_start = time.time()
        self.pairs,self.no_paires_p,self.no_paires_n  = self.pn_pairs(pmos_list, nmos_list)
        nmos_list = [t for t in devices if t.t == 'N']
        pmos_list = [t for t in devices if t.t == 'P']
        # print(self.pairs)
        for cell_width in range(minimal_cell_width, maximal_cell_width):
            logger.info("smt_placer-> Try cell width: %d"%(cell_width))
            print("smt_placer-> Try cell width: %d"%(cell_width))
            placements = self._place(pmos_list, nmos_list, cell_width, self.pairs, vertical_tracks_pmos = 1, vertical_tracks_nmos = 1)
            logger.info("smt_placer-> Placement of width %d cost %d seconds"%(cell_width, int(time.time() - time_start)))
            if len(placements) > 0:
                yield placements[0]
            else:
                logger.info("smt_placer-> Placement of width %d is impossible"%(cell_width))
        



def split_list_elements(input_list):
    result = []
    for item in input_list:
        if '|' in item:
            sub_items = item.split('|')
            temp = []
            for sub in sub_items:
                temp.append(sub.split('-'))
            result.append(temp)
        elif '-' in item:
            result.append(item.split('-'))
        else:
            result.append([item])
    return result


def extract_x_coordinates(nets):
    x_coordinates = {}
    for net_name, points in nets.items():
        for point in points:
            x, y, direction = point
            if x not in x_coordinates:
                x_coordinates[x] = []
            x_coordinates[x].append((net_name, (x, y, direction)))
    
    return x_coordinates



def calculate_crossings(nets):
    """Calculate the number of lines crossing and pins at each integer x position
    
    Args:
    nets: Dictionary of line data
    
    Returns:
    crossings: Dictionary containing crossing and pin data for each x position
    """
    # Find all possible integer x positions
    all_x = set()
    for line_name, points in nets.items():
        for point in points:
            x, y, direction = point
            all_x.add(x)
    
    # Calculate min and max x coordinates
    min_x = min(all_x)
    max_x = max(all_x)
    
    # Generate all integer x positions (including min and max)
    integer_x = list(range(min_x, max_x + 1))
    
    # Initialize crossing data dictionary
    crossings = {x: {'cross': [], 'pin': []} for x in integer_x}
    
    # Check each line for pins
    for line_name, points in nets.items():
        for point in points:
            x, y, direction = point
            if x in integer_x:
                # Store the line name, y-coordinate, and direction for pins
                crossings[x]['pin'].append((line_name,point))
    
    # Check each line for crossings using min and max x of the entire line
    for line_name, points in nets.items():
        # Extract all x coordinates of the line
        x_coords = [point[0] for point in points]
        if not x_coords:
            continue
            
        line_min_x = min(x_coords)
        line_max_x = max(x_coords)
        
        # Check each integer x position
        for x in integer_x:
            # A line crosses x if x is between its min and max x (excluding endpoints)
            if line_min_x <= x <= line_max_x:                
                # Store the line name, approximate start y-coordinate, end y-coordinate, and direction
                crossings[x]['cross'].append(line_name)
    
    for k,v in crossings.items():
        v['pin'].sort(key=lambda x: x[1][1])
    return crossings



def visualize_pins(name, data, edges=None):
    """
    Visualize pins and optional connections between them.
    
    Args:
        name (str): Chart title
        data (dict): Data structure containing pin information
        edges (list, optional): List of tuples representing connections 
            between points ((start_x, start_y, start_z), (end_x, end_y, end_z))
    
    Returns:
        fig, ax: matplotlib figure and axis objects
    """
    filtered_pins1 = []  # Pins with third element 0
    filtered_pins2 = []  # Pins with third element 1
    
    for key, value in data.items():
        for pin in value['pin']:
            if pin[1][2] == 0:
                filtered_pins1.append(pin)
            else:
                filtered_pins2.append(pin)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot blue pins (third element 0)
    x1 = [pin[1][0] for pin in filtered_pins1]
    y1 = [pin[1][1] for pin in filtered_pins1]
    ax.scatter(x1, y1, color='blue', marker='o', s=100, label='Poly Pins')
    
    for i, pin in enumerate(filtered_pins1):
        ax.annotate(pin[0],
                    (x1[i], y1[i]),
                    textcoords="offset points",
                    xytext=(0, 10),
                    ha='center')
    
    # Plot red pins (third element 1)
    x2 = [pin[1][0] for pin in filtered_pins2]
    y2 = [pin[1][1] for pin in filtered_pins2]
    ax.scatter(x2, y2, color='red', marker='o', s=100, label='M1 Pins')
    
    for i, pin in enumerate(filtered_pins2):
        ax.annotate(pin[0],
                    (x2[i], y2[i]),
                    textcoords="offset points",
                    xytext=(0, -20),
                    ha='center',
                    va='top')
    
    # Plot edges
    if edges:
        for edge in edges:
            start_point, end_point = edge
            start_x, start_y = start_point[0], start_point[1]
            end_x, end_y = end_point[0], end_point[1]
            
            # # Check if points exist in dataset
            # point_exists = any(
            #     (pin[1][0] == start_x and pin[1][1] == start_y) for pin_list in [filtered_pins1, filtered_pins2] for pin in pin_list
            # ) and any(
            #     (pin[1][0] == end_x and pin[1][1] == end_y) for pin_list in [filtered_pins1, filtered_pins2] for pin in pin_list
            # )
            
            # if point_exists:
            ax.plot([start_x, end_x], [start_y, end_y], 'g-', alpha=0.6, linewidth=1.5)
    
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    ax.set_title(f'Visualization of Pins: {name}')
    
    all_x = x1 + x2
    max_x = max(all_x) if all_x else 0
    ax.set_xlim(-1, max_x + 1)
    ax.set_ylim(-1, 6)
    
    ax.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
    ax.axhline(y=1, color='gray', linestyle='-', alpha=0.3)
    ax.axhline(y=2, color='gray', linestyle='-', alpha=0.3)
    
    ax.legend()
    plt.tight_layout()
    plt.rcParams['axes.unicode_minus'] = False
    return fig, ax


def generate_range(a, b):
    if a <= b:
        return list(range(a, b + 1))  # 升序：a ≤ b
    else:
        return list(range(a, b - 1, -1))  # 降序：a > b