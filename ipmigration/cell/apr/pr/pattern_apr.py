# -*- coding: utf-8 -*-
"""

@author: leiyuan
"""
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import networkx as nx
from collections import OrderedDict
from ipmigration.cell.apr.pr.analog_router import AnalogRouter1

import z3
from z3 import Optimize,Solver
from z3 import Int, Bool, Or, And, Not, Distinct, If, is_true,sat,Abs

from itertools import combinations, chain
import itertools

import math
import time

import logging
logger = logging.getLogger(__name__)

DEBUG=False

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
        
        #process cross here
        
        
        
        self.net_loc = {}
        loc = 0
        for blk in self.placement:      
            for i,pn in enumerate(blk):
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
                    
                    if i != len(blk)-1:
                        #next is pn
                        p2 = blk[i+1]['P']
                        n2 = blk[i+1]['N'] 
                        if p2 and n2 and p and n:
                            # print(p,p2,n,n2)
                            if p.G == n2.G and n.G == p2.G:
                                #cross
                                # print('11111111111111')
                                self.net_loc[(p,'S')] = (loc,4,1)
                                self.net_loc[(p,'G')] = (loc+1,4,0)
                                self.net_loc[(p,'D')] = (loc+3,4,1)  
                                    
                                self.net_loc[(n,'S')] = (loc,1,1)
                                self.net_loc[(n,'G')] = (loc+1,1,0)
                                if p.D == n.D:
                                    self.net_loc[(n,'D')] = (loc+3,4,1)#same with pD 
                                else:
                                    self.net_loc[(n,'D')] = (loc+3,1,1)
                                
                                loc+=1
                    
                    if i != 0:
                        #next is pn
                        p2 = blk[i-1]['P']
                        n2 = blk[i-1]['N'] 
                        if p2 and n2 and p and n:
                  
                            if p.G == n2.G and n.G == p2.G:
                                #cross
                                # print('2222222222222')
                                self.net_loc[(p,'S')] = (loc,4,1)
                                self.net_loc[(p,'G')] = (loc+1,4,0)
                                self.net_loc[(p,'D')] = (loc+2,4,1)  
                                    
                                if p.S == n.S:
                                    self.net_loc[(n,'S')] = (loc,4,1)
                                else:
                                    self.net_loc[(n,'S')] = (loc,1,1)
                                self.net_loc[(n,'G')] = (loc+1,1,0)
                                self.net_loc[(n,'D')] = (loc+2,4,1) 
                                # print()
                                # loc+=1                                
                                
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
        self.show_placement()
        self.x_coordinate_dict = process_nets(self.nets)


        
    def route(self):
        self.router = IPRouter( self.ckt, self.x_coordinate_dict, vertical_tracks = 6)
        self.router.route()
        # fig, ax = visualize_pins(self.name, self.router.m1_pins)
        # plt.show()
    

        
        
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
    def __init__(self,ckt, x_nets, vertical_tracks):
        self.ckt = ckt
        self.x_nets = x_nets
        self.x_lim = max(x_nets.keys()) + 1
        self.y_lim = vertical_tracks

    
    def route(self):
        # s = Optimize() 
        s = Solver()
        self.poly_constraints(self.x_nets)

        t = replace_points(self.x_nets,self.crossing_pairs)
        t = replace_points(t,self.hshape_pairs)
        
        self.m1_pins = t
        
            #(26, [['N_4', (26, 2, 0)], ['N_6', (26, 5, 0)]]),
            
        # self.m1_pins[26] =  [['N_4', (26, 2, 0)]]
        
        
        self.cross_nets = generate_interval_dict(self.m1_pins)
    
        self.ip_route(s, self.m1_pins, self.cross_nets)    
        # self.solver = s
        
        if self.result:
            print('-----Success!------')
            fig, ax = visualize_pins(self.ckt.name, self.m1_pins,edges=self.edges)
            plt.show()
            
            #process edges
            
            
        else:
            if DEBUG:
                #begin debug
                print('--Begin Debug--')
                increment = 5
                m1_pins_list = split_dict_by_increment(self.m1_pins, increment=increment)
                col = 0
                for m1_pins in m1_pins_list:
                    col = col + increment
                    s = Solver()
                    cross_nets =  generate_interval_dict(m1_pins)
                    self.ip_route(s, m1_pins, cross_nets)    
                    
                    if self.result:
                        print("Pass: %d"%(col))
                        
                    else:
                        print("Failed at %d"%(col))
                        m1_pins_list2 = split_dict_by_increment(self.m1_pins, increment=1)
                        last_pass_m1_pins = {}
                        for k, m1_pins2 in enumerate(m1_pins_list2):
                            if k < col - increment:
                                pass
                                last_pass_m1_pins= m1_pins2
                            else:
                                s = Solver()
                                cross_nets2 =  generate_interval_dict(m1_pins2)
                                self.ip_route(s, m1_pins2, cross_nets2)    
                                if self.result:
                                    print("Pass: %d"%(k+1))
                                    last_pass_m1_pins = m1_pins2
                                else:
                                    self.cross_nets_debug1 = cross_nets2
                                    self.m1_pins_debug1 = m1_pins2
                                    print("Failed at %d"%(k+1))
                                    # print(m1_pins2)
                                
                                    break        
                        break
                s = Solver()
                cross_nets =  generate_interval_dict(last_pass_m1_pins)
                self.cross_nets_debug2 = cross_nets
                self.m1_pins_debug2 = last_pass_m1_pins
                self.ip_route(s, last_pass_m1_pins, cross_nets)  
                if self.result:
                    fig, ax = visualize_pins(self.ckt.name, self.m1_pins,edges=self.edges)
                    plt.show()
            # print(self.result)
            # self.gen_edges()
            # print(self.result)
    
    def optimize_edges(self,edges,m1_pins):
        pass
        
        
        
        
        




    def ip_route(self, s, m1_pins, cross_nets):
                
        var = {}
        # nodes = {}
    
        #init constraints
        # for k,col in m1_pins.items():
        #     nodes[k] = {}
        #     for i in range(self.y_lim):
                
        #         node = Int('%d_%d_node'%(k,i))
        #         s.add(node>=0)
        #         s.add(node<=1)
        #         # nodes[(k,i)] = node
        #         nodes[k][i] = node
  
        for (x1,x2),nets in cross_nets.items():
            dist = []
            var[(x1,x2)] = {}
            for net in nets:
                v = Int('%d_%d_%s'%(x1,x2,net))
                var[(x1,x2)][net] = v
                s.add(v>=0)
                s.add(v<=5)
                dist.append(v)
            if dist:
                s.add(Distinct(dist)) 
                
        
        self.pins_const = self.add_pins_const(s,m1_pins)
        
        #add constraints
        
        for k,col in m1_pins.items():
            if k==0:
                pre_nets = {}
            else:
                pre_nets = var[k-1,k]
            next_nets = var[k,k+1]
            col_nets = {key[1]: value for key, value in self.pins_const.items() if key[0] == k}
            
            all_nets = list(set( list(pre_nets.keys()) + list(col_nets.keys()) +list(next_nets.keys()) ))
            net_range = {}
            for net in all_nets:
                t1 = net in pre_nets
                t2 = net in next_nets
                t3 = net in col_nets
                if t1 and t2 and t3:
                    r1 = pre_nets[net]
                    r2 = col_nets[net]
                    r3 = next_nets[net]
                    r = self.merge_range(r1, r2)
                    r = self.merge_range(r3, r)
 
                    
                elif t1 and t3:
                    r1 = pre_nets[net]
                    r2 = col_nets[net]
                    r = self.merge_range(r1, r2)
                    
                elif t1 and t2:
                    r1 = pre_nets[net]
                    r2 = next_nets[net]
                    r = self.merge_range(r1, [r2])
                    
                elif t2 and t3:
                    r1 = col_nets[net]
                    r2 = next_nets[net]
                    r = self.merge_range(r2, r1)
                elif t3:
                    r = col_nets[net]
                    r = [r[0],r[0]]
                    
                    #一个dict 包含上下表，要求互相不覆盖
                    
                    
                else:
                    print(m1_pins,self.pins_const)
                    print(pre_nets,col_nets,next_nets)
                    print(k,net,t1,t2,t3)
                    raise ValueError
                net_range[net] = r
            for net1, range1 in net_range.items():
                for net2, range2 in net_range.items():
                    if net1 != net2:
                        r1l,r1u = range1
                        r2l,r2u = range2
                        # print(range1,range2)
                        s.add(Or(r1l>r2u,r1u<r2l))
              
            
        self.variables = var
        # cross_nets = {}
        # for loc,nets in self.variables.items():
        #     for net, v in nets.items():
        #         x1,x2=loc
        #         if net in cross_nets:
        #             cross_nets[net].append( v )
        #         else:
        #             # print(edges)
        #                 cross_nets[net] = [v]
        # abs_sum = Int('Abs_sum')
        # for net, vs in cross_nets.items():
        #     l = len(vs)
        #     if l>=2:
        #         for i in range(l-1):
        #             abs_sum += Abs(vs[i] - vs[i+1])
        # self.cross_nets = cross_nets     
                
                
        # s.minimize(abs_sum)
        
        if s.check() == sat:
            m = s.model()
            edges = {}
            variables = self.variables.copy()
            for loc,nets in self.variables.items():
                for net, v in nets.items():
                    x1,x2=loc
                    y = m[v].as_long()
                    variables[loc][net] = y
                    if net in edges:
                        edges[net].append( [(x1,y), (x2,y)] )
                    else:
                        # print(edges)
                        edges[net] = [[(x1,y), (x2,y)]]
            self.variables= variables
            self.edges = edges
            self.result = True
            # self.result = {k:m[v] for k,v in self.variables.items()}
            # self.result = [(d.name(), m[d]) for d in m.decls()] 
        else:
            #not satisfied
            self.result = False
            
    def poly_constraints(self,x_nets):
        poly_pins = []
        for key in x_nets:
            pins = {}
            for pin in x_nets[key]:
                # print(pin)
                if pin[1][2] == 0:
                    pins[pin[0]] = pin[1]
            if pins:
                poly_pins.append(pins)
        self.poly_pins = poly_pins
        crossing_pairs = {}
        hshape_pairs = {}
        poly_connect = {}
        # poly_ct = {}
        top_clock = None
        
        for i in range(len(poly_pins) - 1):
            current = poly_pins[i]
            next_row = poly_pins[i + 1]
            #cross
            if len(current) == 2 and len(next_row) == 2:
                current_lines = set(current.keys())
                next_lines = set(next_row.keys())          
                if current_lines == next_lines:
                    net1,net2 = list(current.keys())
                    p1 = current[net1]
                    p2 = current[net2]
                    p3 = next_row[net1]
                    p4 = next_row[net2]                    
                    if (p1[1] == p4[1] and p2[1] == p3[1]):
                        if p1[1] == 4:
                            if top_clock:
                                pass
                            else:
                                top_clock = net1
                        if p2[1] == 4:
                            if top_clock:
                                pass
                            else:
                                top_clock = net2
                        #
                        if net1 == top_clock:
                            if p1[1] == 4: #p3[1]==1 p4[1]==4 p2[1]=1
                                crossing_pairs[(net1,p1)] = (p1[0],5,0)
                                crossing_pairs[(net1,p3)] = None
                                
                                crossing_pairs[(net2,p2)] = (p2[0],2,0)
                                crossing_pairs[(net2,p4)] = (p4[0],3,0)
                                
                                
                            else:
                                #p3[1]==
                                crossing_pairs[(net1,p1)] = None   
                                crossing_pairs[(net1,p3)] = (p3[0],5,0)
                                
                                crossing_pairs[(net2,p2)] = (p2[0],3,0)
                                crossing_pairs[(net2,p4)] = (p4[0],2,0)
                                
                            poly_connect[(net1,p1)] = (p1,p3) 
                                                    

                            
                        else:
                            #net2 is top
                            if p2[1] == 4: #p3[1]==4 p4[1]==1 p1[1]=1
                                crossing_pairs[(net1,p1)] = (p1[0],2,0)
                                crossing_pairs[(net1,p3)] = (p3[0],3,0)
                                
                                crossing_pairs[(net2,p2)] = (p2[0],5,0)
                                crossing_pairs[(net2,p4)] = None
                                
                                
                            else:
                                # p2[1] == 1 p3[1]==1 p4[1]==4 p1[1]=4
                                crossing_pairs[(net1,p1)] = (p1[0],3,0)
                                crossing_pairs[(net1,p3)] = (p3[0],2,0)  
                                
                                crossing_pairs[(net2,p2)] = None
                                crossing_pairs[(net2,p4)] = (p4[0],5,0)
                                
                            poly_connect[(net2,p2)] = (p2,p4)
                        
                        
                        
                        
                      
            #connect poly
            if len(current) == 1 and len(next_row) == 1:
                net1 = list(current.keys())[0]
                net2 = list(next_row.keys())[0]
                if net1 == net2:
                    # print(net1,net2)
                    p1 = current[net1]
                    p2 = current[net2]
                    if net1 == net2:
                        poly_connect[(net1,p1)] = (p1,p2)
                        hshape_pairs[(net2,p2)] = None  

                
            
        self.crossing_pairs = crossing_pairs
        self.hshape_pairs = hshape_pairs
        self.poly_connect = poly_connect
            

    
    def add_pins_const(self,solver,m1_pins,aa_range = 3):
        pins_const = {}
        for k,col in m1_pins.items():
            if len(col) == 2:
                n1,p1 = col[0]
                n2,p2 = col[1]
            
                #common AA
                if n1==n2 and p1[2]==1 and p2[2]==1:
                    t1 = Int('%d_%s_paa'%(k,n1))
                    t2 = Int('%d_%s_naa'%(k,n1))
                    eqs1 = []
                    eqs2 = []
                    
                    #t1 t2 range
                    for i in range(aa_range):
                        eqs1.append(t1==6-i)
                        eqs2.append(t2==0+i)
                    solver.add(Or(*eqs1))
                    solver.add(Or(*eqs2))
                    pins_const[(k,n1)] = [t2,t1]
                    # range_ = (t2,t1) 
                    # lb= t1
                    # ub = t1
                                    
                    # if n1 in pre_nets:
                    #     pre_net = pre_nets[n1]
                    #     lb,ub = self.merge_range(pre_net, [lb,ub])
                                       
                    # for name,v in col_nets.items():
                    #     if name != n1:
                    #         #common a and its net (maybe top or bottm), all the range are blocked
                    #         solver.add(Or(v < lb, v > ub))
                elif n1!=n2 and p1[2]==0 and p2[2]==0:
                    t1 = Int('%d_%s_gt'%(k,n1))
                    solver.add(t1 == 2)
                    t2 = Int('%d_%s_gt'%(k,n2))
                    solver.add(Or(t2 == 5,t2==3))
                    pins_const[(k,n1)] = [t1]
                    pins_const[(k,n2)] = [t2]
    
                elif n1!=n2 and p1[2]==1 and p2[2]==1:
                    #diff AA                      
                    t1 = Int('%d_%s_naa'%(k,n1))
                    t2 = Int('%d_%s_paa'%(k,n2))
                    eqs1 = []
                    eqs2 = []
                    
                    #t1 t2 range
                    for i in range(aa_range):
                        eqs1.append(t2==6-i)
                        eqs2.append(t1==0+i)
                    solver.add(Or(*eqs1))
                    solver.add(Or(*eqs2))
                    
                    pins_const[(k,n1)] = [t1]
                    pins_const[(k,n2)] = [t2]
                             
                else:
                    print(col)
                    raise ValueError

            elif len(col) == 1:
                n1,p1 = col[0]
                if p1[2] ==0:
                    if p1[1] == 2.5:
                        #common gt
                        t1 = Int('%d_%s_gt'%(k,n1))
                        solver.add(Or(t1 == 2, t1 == 3))
                    elif p1[1] == 2:
                        t1 = Int('%d_%s_gt'%(k,n1))
                        solver.add(t1 == 2)
                    elif p1[1] == 3:
                        t1 = Int('%d_%s_gt'%(k,n1))
                        solver.add(t1 == 3)                    
                    elif p1[1] == 5:
                        t1 = Int('%d_%s_gt'%(k,n1))
                        solver.add(t1 == 5)                    
                    else:
                          print(col)
                          raise ValueError 
                else:
                    if p1[1] == 1:
                        t1 = Int('%d_%s_naa'%(k,n1))
                        solver.add(Or(t1 == 2, t1 == 3))
                        eqs1 = []
                        
                        for i in range(aa_range):
                            eqs1.append(t1==0+i)
                        solver.add(Or(*eqs1))
                    elif p1[1] ==4:
                        t1 = Int('%d_%s_paa'%(k,n1))
                        eqs1 = []
                        #t1 t2 range
                        for i in range(aa_range):
                            eqs1.append(t1==6-i)
                        solver.add(Or(*eqs1))
                    else:
                        print(col)
                        raise ValueError    
                pins_const[(k,n1)] = [t1]       
      
        return pins_const
    
    @staticmethod
    def merge_range(x, range_):
        if len(range_)==2:
            a_min,a_max = range_
            lower_bound = If(x < a_min, If(x < a_max, x, a_max), If(a_min < a_max, a_min, a_max))
            upper_bound = If(x > a_max, If(x > a_min, x, a_min), If(a_max > a_min, a_max, a_min))
        else:#len(range)==1
            y = range_[0]
            lower_bound = If(x < y, x, y)
            upper_bound = If(x > y, x, y) 
        
        return (lower_bound,upper_bound)
    
    @staticmethod
    def cover(range_a, range_b, solver=None):
        """
        为两个范围参数添加 Z3 约束条件，确保它们存在重叠部分。
        
        参数:
            range_a, range_b: 可以是单个整数（表示点）或元组 (lower, upper) 表示区间。
            solver: 可选的 Z3 求解器实例，若提供则直接添加约束，否则返回约束列表。
        
        返回:
            若提供 solver，返回 True（约束添加成功）或 False（输入无效）；
            若未提供 solver，返回约束列表或 None（输入无效）。
        """
        # 检查输入有效性
        if not IPRouter.is_valid_range(range_a) or not IPRouter.is_valid_range(range_b):
            return False if solver else None
        
        # 将点转换为区间表示
        a_low, a_high = IPRouter.normalize_range(range_a)
        b_low, b_high = IPRouter.normalize_range(range_b)
        
        # 创建 Z3 表达式
        a_low_expr = z3.IntVal(a_low) if isinstance(a_low, int) else a_low
        a_high_expr = z3.IntVal(a_high) if isinstance(a_high, int) else a_high
        b_low_expr = z3.IntVal(b_low) if isinstance(b_low, int) else b_low
        b_high_expr = z3.IntVal(b_high) if isinstance(b_high, int) else b_high
        
        # 生成约束条件
        overlap_low = z3.If(a_low_expr >= b_low_expr, a_low_expr, b_low_expr)
        overlap_high = z3.If(a_high_expr <= b_high_expr, a_high_expr, b_high_expr)
        overlap_constraint = overlap_low <= overlap_high
        
        # 添加到求解器或返回约束
        if solver:
            solver.add(overlap_constraint)
            return True
        else:
            return [overlap_constraint]
    
    @staticmethod
    def is_valid_range(r):
        """检查输入是否为有效的点或区间"""
        if isinstance(r, int):
            return True  # 点是有效的
        elif isinstance(r, tuple) and len(r) == 2:
            lower, upper = r
            # 允许 Z3 变量或整数
            valid_lower = isinstance(lower, int) or isinstance(lower, z3.ArithRef)
            valid_upper = isinstance(upper, int) or isinstance(upper, z3.ArithRef)
            if valid_lower and valid_upper:
                # 如果都是整数，检查 lower <= upper
                if isinstance(lower, int) and isinstance(upper, int):
                    return lower <= upper
                return True
            return False
        return False
    @staticmethod
    def normalize_range(r):
        """将点或区间统一转换为 (lower, upper) 格式"""
        if isinstance(r, int):
            return (r, r)  # 点转换为相同上下界的区间
        else:
            return r  # 区间直接返回






    def gen_edges(self):
        net_loc = {}
        for (x,net),y_z3 in self.result.items():
            y = int(y_z3.as_long())
            if net in net_loc:
                net_loc[net].append(((x,y),(x+1,y)))
            else:
                net_loc[net] = [((x,y),(x+1,y))]

        self.edges = net_loc     
        
        # self.edges = generate_edges(net_loc)



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




def process_nets(data):
    """处理原始数据，生成按x坐标排序的点集合"""
    x_coordinate_dict = {}
    
    # 遍历每个网络和对应的坐标点
    for net, points in data.items():
        for point in points:
            x, y, z = point
            # 如果x坐标尚未作为键存在，创建新列表
            if x not in x_coordinate_dict:
                x_coordinate_dict[x] = []
            # 添加点信息到对应x坐标的列表中
            x_coordinate_dict[x].append([net, point])
    
    # 对每个x坐标下的点按y值从小到大排序
    for x in x_coordinate_dict:
        x_coordinate_dict[x].sort(key=lambda p: p[1][1])
    
    # 确定x坐标的范围
    if x_coordinate_dict:
        min_x = min(x_coordinate_dict.keys())
        max_x = max(x_coordinate_dict.keys())
        # 确保从min_x到max_x的每个整数x都在字典中，没有pin的x对应空列表
        for x in range(min_x, max_x + 1):
            if x not in x_coordinate_dict:
                x_coordinate_dict[x] = []
    
    # 按x坐标从小到大排序字典
    sorted_x = sorted(x_coordinate_dict.keys())
    x_coordinate_dict = OrderedDict((x, x_coordinate_dict[x]) for x in sorted_x)
    
    return x_coordinate_dict

def generate_interval_dict(x_coordinate_dict):
    """根据x_coordinate_dict生成区间到网络的映射"""
    interval_dict = {}
    
    # 收集所有存在点的x坐标
    existing_x = list(range(max(x_coordinate_dict.keys())+1))
    # 如果没有任何点，直接返回空的interval_dict
    if not existing_x:
        return interval_dict
    
    # 为每个存在点的x值创建区间(x, x+1)
    for x in existing_x:
        interval = (x, x + 1)
        interval_dict[interval] = []
    
    # 构建网络到其x坐标范围的映射
    net_x_range = {}
    # 遍历x_coordinate_dict中的每个x坐标
    for x, points in x_coordinate_dict.items():
        # 遍历每个点的信息
        for point_info in points:
            net, point_list = point_info
            if not point_list:
                continue
            # 提取点的x坐标
            point_x = point_list[0]
            # 更新网络的x坐标范围
            if net not in net_x_range:
                net_x_range[net] = (point_x, point_x)
            else:
                current_min, current_max = net_x_range[net]
                net_x_range[net] = (min(current_min, point_x), max(current_max, point_x))
    
    # 确定哪些网络属于每个区间
    for interval, _ in interval_dict.items():
        x, x_plus_1 = interval
        for net, (min_x, max_x) in net_x_range.items():
            # 检查网络是否跨越区间(x, x+1)
            if min_x <= x and max_x >= x_plus_1:
                interval_dict[interval].append(net)
    
    return interval_dict


def visualize_pins(name, data, edges_points=None, edges=None):
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
        for pin in value:
            if pin[1][2] == 0:
                filtered_pins1.append(pin)
            else:
                filtered_pins2.append(pin)
    
    fig, ax = plt.subplots(figsize=(20, 6))
    
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
    all_x = x1 + x2
    max_x = max(all_x) if all_x else 0  # 提前计算max_x
    for i, pin in enumerate(filtered_pins2):
        ax.annotate(pin[0],
                    (x2[i], y2[i]),
                    textcoords="offset points",
                    xytext=(0, -20),
                    ha='center',
                    va='top')
    
    # Plot edge_points with smaller markers and labels
    if edges_points:
        edge_x = []
        edge_y = []
        edge_labels = []
        
        for label, points in edges_points.items():
            for point in points:
                x, y = point
                edge_x.append(x)
                edge_y.append(y)
                edge_labels.append(label)
        
        # Plot small gray points for edges_points
        ax.scatter(edge_x, edge_y, color='gray', marker='.', s=10, label='Edge Points')
        
        # Add small labels for edges_points
        for x, y, label in zip(edge_x, edge_y, edge_labels):
            ax.annotate(label,
                        (x, y),
                        textcoords="offset points",
                        xytext=(5, 5),  # Smaller offset than data points
                        ha='left',
                        va='bottom',
                        fontsize=6)  # Smaller font size
    
    # Plot edges (支持字典格式，不同key用不同颜色)
    if edges and isinstance(edges, dict):
        # 生成颜色映射
        cmap = plt.cm.get_cmap('tab20', len(edges))  # 支持最多20种颜色
        
        for i, (line_name, line_edges) in enumerate(edges.items()):
            color = cmap(i)  # 获取当前线的颜色
            
            # 绘制所有边
            for j, (start, end) in enumerate(line_edges):
                ax.plot([start[0], end[0]], [start[1], end[1]], 
                        color=color, alpha=0.8, linewidth=1.5)

                # 计算线的中点
                mid_x = (start[0] + end[0]) / 2
                mid_y = (start[1] + end[1]) / 2
                
                # 添加标签（字体大小减半，位置在线上面）
                ax.annotate(line_name, 
                            (mid_x, mid_y),
                            color='black',
                            fontweight='bold',
                            fontsize=plt.rcParams['font.size'] ,  # 字体大小减半
                            alpha=0.8,
                            ha='center',
                            va='bottom',  # 位置在线上面
                            xytext=(0, 5),  # 垂直偏移量
                            textcoords='offset points')

    # 设置网格：每个点都有虚线网格，半透明
    ax.set_xticks(np.arange(-1, max_x + 2, 1))  # 确保x轴刻度覆盖所有点
    ax.set_yticks(np.arange(-1, 7, 1))          # 确保y轴刻度覆盖所有点
    ax.grid(True, which='both', linestyle='--', alpha=0.3)  # 细虚线，半透明
    
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
    
    plt.tight_layout()
    plt.rcParams['axes.unicode_minus'] = False
    return fig, ax


def generate_range(a, b):
    if a <= b:
        return list(range(a, b + 1))  # 升序：a ≤ b
    else:
        return list(range(a, b - 1, -1))  # 降序：a > b
    
    
def replace_points(x_coordinate_dict, replacement_map):
    """根据替换映射修改x_coordinate_dict中的点"""
    # 遍历每个x坐标下的所有点信息
    for x, points in x_coordinate_dict.items():
        # 对每个点信息进行处理
        for i in range(len(points)):
            net, point_list = points[i]  # point_list是包含一个元组的列表
            if not point_list:
                continue

            key = (net, point_list)
            if key in replacement_map:
                new_point = replacement_map[key]
                if new_point is not None:
                    # 更新点信息，保持[net, [(x, y, z)]]的格式
                    points[i] = [net, new_point]
                else:
                    # 如果替换值为None，移除该点
                    points[i] = None
        # 过滤掉被移除的点（值为None的项）
        x_coordinate_dict[x] = [p for p in points if p is not None]
    return x_coordinate_dict


def generate_edges(data):
    """
    根据点坐标生成水平和垂直的edges
    
    参数:
    data (dict): 包含线名称和对应点坐标的字典
    
    返回:
    dict: 包含线名称和对应edges的字典
    """
    edges_result = {}
    
    for line_name, points_dict in data.items():
        # 提取并排序点
        points = []
        for key in sorted(points_dict.keys()):
            points.extend(points_dict[key])
        
        edges = []
        
        # 处理每个相邻点对
        for i in range(len(points) - 1):
            start = points[i]
            end = points[i + 1]
            
            # 如果x坐标相同，直接垂直连接
            if start[0] == end[0]:
                edges.append((start, end))
            # 如果y坐标相同，直接水平连接
            elif start[1] == end[1]:
                edges.append((start, end))
            # 否则，通过中间点生成水平和垂直edges
            else:
                mid_point = (end[0], start[1])  # 中间点：(end_x, start_y)
                edges.append((start, mid_point))
                edges.append((mid_point, end))
        
        edges_result[line_name] = edges
    
    return edges_result


def split_dict_by_increment(original_dict, increment=5):
    """
    按递增间隔拆分OrderedDict
    
    参数:
    original_dict - 原始OrderedDict
    increment - 每次增加的间隔
    
    返回:
    拆分后的字典列表
    """
    result = []
    keys = list(original_dict.keys())
    
    # 计算最大key值
    max_key = max(keys) if keys else 0
    
    # 生成间隔列表
    intervals = [i for i in range(increment, max_key + 1, increment)]
    
    # 如果最大值不是间隔的倍数，添加一个额外的间隔
    if max_key % increment != 0:
        intervals.append(max_key)
    
    # 为每个间隔创建一个新字典
    for interval in intervals:
        new_dict = OrderedDict()
        for key in keys:
            if key <= interval:
                new_dict[key] = original_dict[key]
        result.append(new_dict)
    
    return result

