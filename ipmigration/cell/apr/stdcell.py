#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: leiyuan
"""

from ipmigration.cell.apr.cir.decompose import DeCKT
from ipmigration.cell.apr.pr.pattern_placer import Placer
from ipmigration.cell.apr.cir.graph import RouteGraph
from ipmigration.cell.apr.tech import VMode
from ipmigration.cell.apr.pr.smt_router import MIPGraphRouter

class StdCell:
    def __init__(self, ckt, tech, cfgs, patterns):
        self.ckt = ckt
        self.tech = tech
        self.cfgs = cfgs
        self.patterns= patterns
        
        
        
        
    def run(self):
        self.init_layout()
        self.global_pr()
    
    def init_layout(self):
        pass
    
    def global_pr(self):
        self.ckt.combine_parallel()
        self.de_ckt = DeCKT(self.ckt, 
                            self.patterns, 
                            self.tech.tech_name, 
                            self.cfgs.output_dir)
        result = self.de_ckt.run()
        if result:
            print('Success: ', self.ckt.name)
            pat_placer = Placer(self.de_ckt.sub_ckts)
            queue = pat_placer.find_opt_perm(self.ckt.ckt_type)
            self.queue = [self.de_ckt.sub_ckts[t] for t in queue]
            #TODO: Visualization this part with multi-graph
            self.extract_ext_net(self.queue)
            
            left_nets = {}
            for loc,pattern in enumerate(self.queue):
                pattern.set_vmode(self.tech)
                self.pattern_route(pattern, loc, left_nets)

                
            
            
            
            #auto-folding
            
            
            
            # self.pat_placer = pat_placer

        else:
            print('Fail: ', self.ckt.name)
        
 
    
    def pattern_route(self,pattern, pattern_loc, left_nodes):
        # G = RouteGraph(self)
        aa_m1_y_p = self.tech.median+2
        aa_m1_y_n = self.tech.median-2
        
        route_nets = {k:[] for k in pattern.net_map_r}
        
        if len(left_nodes) ==0:
            start_loc=0 
        else:
            start_loc=2        
        #creat M1 nets
        grid_columns = start_loc + sum(pattern.grid_columns)
        m1_nodes = VMode.gen_m1_grids(self.tech, grid_columns)
 
        pt_gt_nodes = {}
        pt_ct_nodes = {}
        pt_edges = []
        pt_connected = {}
    
        
    
        left_gt = []
        left_ct = []
        loc = start_loc -1
        for i, pn_pair in enumerate(pattern.place):
            pmos = pn_pair['P']
            nmos = pn_pair['N']
            vmode = pattern.vmode[i]
            pn_colums = pattern.grid_columns[i]
                        
            if vmode.vmode==0:
                loc+=1
                gt_nodes,ct_nodes,gt_nets,connected,edges = vmode.gen_grids(loc)
                
            else:
                loc+=2
                gt_nodes,ct_nodes,gt_nets,connected,edges = vmode.gen_grids(loc)
                if len(left_gt)==0:
                    common_gt = gt_nodes['s']
                else:
                    common_gt = list(set(left_gt)&set(gt_nodes['s']))
                    # print(left_gt, gt_nodes['s'])
                    assert len(common_gt)>0
                
                if len(left_ct)==0:
                    common_ct = ct_nodes['s']
                else:
                    common_ct = list(set(left_ct)&set(ct_nodes['s']))       
                
                for node in common_gt:
                    pt_gt_nodes[node] = {'net':'',
                                         'loc':(node[0]+0.3, node[1]+0.3),
                                         'color':'blue'}
                for node in common_ct:
                    pt_ct_nodes[node] = {'net':'',
                                         'loc':(node[0]+0.15, node[1]+0.15),
                                         'color':'cyan'}            
            
                if pmos:
                    m1_nodes[(loc-1,aa_m1_y_p,1)]['net'] = pmos.D
                    route_nets[pmos.D].append((loc-1,aa_m1_y_p,1))
                if nmos:
                    m1_nodes[(loc-1,aa_m1_y_n,1)]['net'] = nmos.D
                    route_nets[nmos.D].append((loc-1,aa_m1_y_n,1))                
                
                
                if pn_colums==3:
                    for node in gt_nodes['d']:
                        pt_gt_nodes[node] = {'net':'',
                                             'loc':(node[0]+0.3, node[1]+0.3),
                                             'color':'blue'}
                    for node in ct_nodes['d']:
                        pt_ct_nodes[node] = {'net':'',
                                             'loc':(node[0]+0.15, node[1]+0.15),
                                             'color':'cyan'} 
                        
                    if pmos:
                        m1_nodes[(loc+1,aa_m1_y_p,1)]['net'] = pmos.D
                        route_nets[pmos.D].append((loc+1,aa_m1_y_p,1))
                    if nmos:
                        m1_nodes[(loc+1,aa_m1_y_n,1)]['net'] = nmos.D
                        route_nets[nmos.D].append((loc+1,aa_m1_y_n,1))    
                        
                    loc += 1  
                    
                    
            for node in gt_nodes['g']:
                pt_gt_nodes[node] = {'net':'',
                                     'loc':(node[0]+0.3, node[1]+0.3),
                                     'color':'blue'}
            for node in ct_nodes['g']:
                pt_ct_nodes[node] = {'net':'',
                                     'loc':(node[0]+0.15, node[1]+0.15),
                                     'color':'cyan'}  

            
            for k,v in gt_nets.items():        
                pt_gt_nodes[k]['net'] = pn_pair[v].G
                route_nets[pn_pair[v].G].append(k)
                
            
            pt_edges = pt_edges + edges
            for k,v in connected.items():
                pt_connected[k] = v

    

        G = RouteGraph(pattern, pt_connected, pt_edges)
        G.add_nodes(m1_nodes, pt_gt_nodes, pt_ct_nodes)
        G.add_edges()
        pattern.G = G
        
        pattern.route_nets = route_nets
        route_G = G.gen_routing_graph()
        
        signals,cost_edge = route_G.gen_routing_signals(route_nets,route_G)
        G.cost_edge = cost_edge

        print('Begin Routing',pattern.pattern_name,signals)
        route_G.plot(grid_columns)
        G.plot(grid_columns)

        router = MIPGraphRouter()
        routing_trees = router.min_steiner_tree(route_G, signals,
                                         node_cost_fn=None,
                                         edge_cost_fn=cost_edge)
        #
        print('aaa',routing_trees)
        
        
        
        
        

            # vmode.gt_nodes  
            # vmode.gt_nets 
            # vmode.connected  
            # vmode.ct_nodes 
            # vmode.edges
            
            # t = vmode.gen_grids(pn_pair)
            # print(t)
            # s_grid = {(loc-1,i,1):'none' for i in range(tech.M1_tracks_num)}
            # g_grid = {( loc  ,i,1):'none' for i in range(tech.M1_tracks_num)}
            # d_grid = {( loc+1,i,1):'none' for i in range(tech.M1_tracks_num)}

    

    def detail_place(self):
        pass
    
    def detail_route(self):
        pass    
    
    
    def pre_process(self, ckt, right, left=0, m2_tracks=False):
        pass

     

    def extract_ext_net(self,queue):
        for pattern in queue: 
            signal_nets = list(pattern.net_map.values())
            if 'VDD' in signal_nets:
                signal_nets.remove('VDD')
            if 'VSS' in signal_nets:
                signal_nets.remove('VSS')
            pattern.signal_nets  = signal_nets
        nets_loc = {}
        for net in self.ckt.nets:
            if net != 'VDD' and net != 'VSS':
                nets_loc[net] = []
                for i, pattern in enumerate(queue):
                    if net in pattern.signal_nets:
                        nets_loc[net].append(i)
        
        for i, pattern in enumerate(queue):
            for net, loc in nets_loc.items():
                if len(loc) ==1:
                    if loc[0] == i:
                        pattern.internal_nets.append(net)

                else: #len loc >1
                    if min(loc) == i:
                        pattern.right_nets.append(net)
                    elif max(loc) == i:
                        pattern.left_nets.append(net)
                    elif min(loc) < i and max(loc) > i:
                        pattern.cross_nets.append(net)


                
                
    def gen_graph(self):
        pass


    def apr(self, ckt, file):
        #init ckt layout
        ckt.preprocess(self.layout,self.layout_layers)
        
        #TODO maybe more complicated here
        structs_queue = [ckt.de.struct_clk]   + \
                        [ckt.de.struct_input] + \
                         ckt.de.struct_queue  + \
                        [ckt.de.struct_out]
        

        line = self.tech.tech_name +  ' '  + ckt.name + ': '
        for s in structs_queue:
            line = line + s.struct_ckt_name + ' '
        print(line)
        file.write(line + '\n')

        #examine struct
        for struct in structs_queue:
            if not(struct.struct_ckt.name in self.ready_structs):
                logger.info('%s not in ready struct'%(struct.struct_ckt.name))
                return False, struct.struct_ckt.name        
        
        #TODO delete these
        pin_locs = json.load(open('src/lego/layout/pin_loc.json','r'))
        struct_names = [t.struct_ckt.name for t in structs_queue]
        pin_locs = {k:v for k,v in pin_locs.items() if k in struct_names}
                
        channels = Channels(structs_queue, ckt, pin_locs)
        result, channel_nets_routed,pin_locs = channels.graph_route()

        if not(result):
            logger.info('%s can not be channel routed '%(ckt.name))
            return False, ckt.name
        
        for i, struct in enumerate(structs_queue):
            # if i == 0:        
            struct.global_pr_7T(ckt,start_x=0)
        

        side_space =  self.cell_offset_x + self.tech.CT_E_AA.v + self.tech.CT_W_half 
        x = side_space
        
        for i, struct in enumerate(structs_queue):   
            x1 = struct.detail_pr_7T(ckt, self.tech, self, start_x=x)       
            
            if i != len(structs_queue)-1:
                if not(struct.struct_ckt_name in merge_structs()):
                    x1 = channels.detail_route(self.tech, self, i, x1)
            struct.draw(ckt)
            x = x1
        channels.draw(ckt)   
            
        self.post_process_layout(ckt,x1 + side_space)  
        
        return True, ''
   
    def post_process(self, ckt, right, left=0, m2_tracks=False):
        #TODO add merge shapes
        
        
        #draw power ground rail
        m1_rails  = M1_Rails(self, left, right)
        m1_rails.draw(ckt)
        ckt.border = m1_rails.border_box
        
        if m2_tracks:
            m2_tracks = M2_Tracks(self, left, right)
            m2_tracks.draw(ckt)
        
        #border and diffusion
        border = ckt.border
        ckt.SP_box = Box([border.l - self.np_ext_border,
                           self.middle,
                           border.r + self.np_ext_border,
                           border.t + self.np_ext_border])
        
        ckt.NW_box = Box([ ckt.SP_box.l - self.nw_ext_np,
                           self.middle,
                           ckt.SP_box.r + self.nw_ext_np,
                           ckt.SP_box.t + self.nw_ext_np])     
        
        ckt.SN_box = Box([border.l - self.np_ext_border,
                           border.b - self.np_ext_border,
                           border.r + self.np_ext_border,
                           self.middle])      
        
        ckt.db_shapes[self.tech.NW].insert( ckt.NW_box.to_dbBox())
        ckt.db_shapes[self.tech.SP].insert( ckt.SP_box.to_dbBox())
        ckt.db_shapes[self.tech.SN].insert( ckt.SN_box.to_dbBox())    
    