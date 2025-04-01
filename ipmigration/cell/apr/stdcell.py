#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: leiyuan
"""
import os
import json

from ipmigration.cell.apr.cir.decompose import DeCKT
from ipmigration.cell.apr.pr.pattern_placer import Placer
from ipmigration.cell.apr.cir.graph import RouteGraph
from ipmigration.cell.apr.tech import VMode
from ipmigration.cell.apr.pr.smt_router import MIPGraphRouter
from ipmigration.cell.apr.pr.analog_router import AnalogRouter1
from ipmigration.cell.apr.io.route_loader import load_routing_expertise,save_routing_expertise,list_to_tuple
from ipmigration.cell.apr.utils.utils import concatenate_images

from  ipmigration.cell.apr.lyt.instance import GT_AA, CT_GT, CT_Nodes, EdgeRoute ,AA_SD,POWER


class StdCell:
    def __init__(self, ckt, tech, cfgs, patterns, route_data_path):
        self.ckt = ckt
        self.tech = tech
        self.cfgs = cfgs
        self.patterns= patterns
        self.route_data_path = route_data_path
        self.route_path = []
        

        
    def run(self,top_layout,db_layers):
       
        result = self.global_pr()
        if result:
            save_fig_path = os.path.join(self.cfgs.output_dir,'route','%s.png'%(self.ckt.name))
            print(self.route_path)
            concatenate_images(self.route_path, save_fig_path)
            
            #detail pr
            self.init_layout(top_layout,db_layers)
            result = self.detail_pr()
        if result:
            pass
            # self.post_process()
            
        
        
        return result
    
    def init_layout(self,top_layout,db_layers):
        self.db_layout = top_layout.create_cell(self.ckt.name)
        self.db_shapes = {}
        for name in db_layers:
            self.db_shapes[name] = self.db_layout.shapes(db_layers[name]) 
    
    def global_pr(self):
        self.ckt.combine_parallel()
        self.de_ckt = DeCKT(self.ckt, 
                            self.patterns, 
                            self.tech.tech_name, 
                            self.cfgs.output_dir)
        result = self.de_ckt.run()
        if result:          
            pat_placer = Placer(self.de_ckt.sub_ckts)
            queue = pat_placer.find_opt_perm(self.ckt.ckt_type)
            self.queue = [self.de_ckt.sub_ckts[t] for t in queue]
            print(self.ckt.name,self.queue)
            #TODO: Visualization this part with multi-graph
            
            self.clk_loc = {self.ckt.c_net: self.tech.M1_tracks_num-1, self.ckt.cn_net:0}
            self.extract_ext_net(self.queue)
            aa_pos = [ (self.tech.median+2, self.tech.median-2),(self.tech.M1_tracks_num-2, 1)]
            
            
            try:
                with open(self.route_data_path, 'r', encoding='utf-8') as file:
                    route_data = json.load(file)
            except FileNotFoundError:
                route_data = {}

            try:
                #right nodes, only read
                path = self.route_data_path[:-5] + '_rn.json'
                with open(path, 'r', encoding='utf-8') as file:
                    route_data_rn = json.load(file)
            except FileNotFoundError:
                route_data_rn = {}

            left_nodes_ex = {}
            # right_nodes_in = {}
            # right_nodes_ex = {}
            
            for loc,pattern in enumerate(self.queue):
                print('\n\n\nBegin Routing',pattern.pattern_name)

                if loc ==0 :
                    pattern.is_first = True
                else:
                    pattern.is_first = False
                
                if loc == len(self.queue) - 1:
                    pattern.is_last = True
                else:
                    pattern.is_last = False
                
                #set vmodes for each pn pair
                pattern.set_vmode(self.tech)
                
                if pattern.is_first:    
                    left_nodes_in = {}
                    net_map= pattern.net_map
                    '''
                        TODO: need consider load, but initial load may lead to clk net problem for clk at first, 
                        maybe use a for loop to find the suitable case
                        load_routing_expertise(data, name, left_nodes, right_nodes_names, node_match=True):
                    '''
                else:
                    left_nodes_in, net_map = pattern.gen_left_nodes_in(left_nodes_ex)
                
                right_nodes_ex,right_nodes_in = pattern.gen_right_nodes(self.tech,left_nodes_ex,net_map,self.clk_loc)
                #try load right nodes first, if not found, generate them. 
                print('1------------------------------')
                match_rn = load_routing_expertise(route_data, pattern.pattern_name, left_nodes_in, right_nodes_in,only_left=True)
                matches=[]
                for match in match_rn:
                    print('load right nodes successfully')
                    right_nodes_in = match['right_nodes']
                    print(right_nodes_in)
                    print('2------------------------------')
                    matches = load_routing_expertise(route_data, pattern.pattern_name, left_nodes_in, right_nodes_in)
                    if len(matches)>0:
                        break
  
                # print('3',matches)
                if len(matches)==0:
                    edges = {}
                    m2_edges = {}
                    pattern.aa_pos = aa_pos[1]
                else:
                    edges = matches[0]['edges']
                    m2_edges = matches[0]['m2_edges']
                    # right_nodes_in =  matches[0]['right_nodes']
                    pattern.aa_pos = matches[0]['aa_pos']
                    #TODO, this may be more detail next version. 
                    # print('%%%%',edges,m2_edges)
               
                # result = self.pattern_route(pattern, left_nodes_in, right_nodes_in, 
                #                             aa_pos[0], load_edges=edges,m2_edges=m2_edges)
                # if not(result):
                result = self.pattern_route(pattern, left_nodes_in, right_nodes_in, 
                                            aa_pos[1], load_edges=edges,m2_edges=m2_edges)
                # pattern.aa_pos =aa_pos[1]  
                if result:
                    pattern.aa_pos =aa_pos[1]     
                else:
                    not_route = True
                    count = 5
                    while(not_route):
                        if 'cross_%d'%(count) in left_nodes_in:
                            m2_edges['cross_%d'%(count)] = [left_nodes_in['cross_%d'%(count)], 
                                                            right_nodes_in['cross_%d'%(count)] ]
                            
     
                            result = self.pattern_route(pattern, left_nodes_in, 
                                                        right_nodes_in, aa_pos[1],
                                                        load_edges=edges,m2_edges=m2_edges)
                            if result:
                                not_route=False
                            else:
                                count = count-1
                                
                        else:
                            count = count-1
                        if count<0:
                            not_route=False
                            result = False

                #save 
                if result:
                    new_item = {'left_nodes':left_nodes_in,
                                'right_nodes':right_nodes_in,
                                'edges':pattern.routed_edges,
                                'm2_edges':pattern.m2_edges,
                                # 'max_col':pattern.max_col,
                                'aa_pos': pattern.aa_pos
                                }
                    save_routing_expertise(self.route_data_path, route_data, pattern.pattern_name, new_item)
                        
                
        
                  
                if result:
                   print('Success: %s->%s'%(self.ckt.name,pattern.pattern_name))
                   left_nodes_ex = pattern.gen_right_nodes_ex(right_nodes_in,net_map)
                  
                   pattern.save_fig_path = os.path.join(self.cfgs.output_dir,'route','temp_%s-%s_%d.png'%(self.ckt.name,pattern.pattern_name,loc))
                   self.route_path.append(pattern.save_fig_path)
                   # print('t1',left_nodes_ex,left_nodes_in)
                   # print('t2',right_nodes_ex,right_nodes_in)
                   # print(pattern.routed_edges)
                   # print(pattern.route_G.nodes,  list(pattern.routed_edges.values()))
                   m2_edge_list = []
                   for net in pattern.m2_edges.values():
                       m2_edge_list.append([tuple(net)])
                   pattern.route_G.plot(list(pattern.routed_edges.values()),
                                        m2_edge_list,
                                        savepath= pattern.save_fig_path )
            
                else:
                    raise ValueError
                    print('------------------Fail: %s------------------'%(self.ckt.name))
                    return 0
            print('------------------All Success: %s------------------'%(self.ckt.name))
            return 1
        else:
            print('------------------Fail: %s------------------'%(self.ckt.name))
            return 0
        

    
    def detail_pr(self):
        cfgs = self.cfgs
        tech = self.tech
        #init db layout and cell and shapes of cell, then we can use insert function.

        x =  cfgs.cell_offset_x + tech.CT_E_AA.v + tech.CT_W.hv        
        for i, pattern in enumerate(self.queue):   
            pass
            x = self.pattern_draw(pattern, x)       
            self.draw(pattern)
            # if i != len(structs_queue)-1:
            #     if not(struct.struct_ckt_name in merge_structs()):
            #         x1 = channels.detail_route(self.tech, self, i, x1)
            
            
            # struct.draw(ckt)
            # x = x1
            # channels.draw(ckt)   
            
        # self.post_process_layout(ckt,x1 + side_space)  
        
    def pattern_draw(self, pattern, start_x):
        #initial
        pattern.data = []
        tech = self.tech
        
        # make node_attr:
        nodes_attr = {}
        cols = pattern.max_col + 1 #
        rows = tech.M1_tracks_num
        for i in range(cols):
            for j in range(rows):
                nodes_attr[(i,j)] = {'net':'','is_gt_ct':False,'is_aa_ct':False,
                                     'is_pin':False,'is_m1':False,'is_m2':False,
                                     'is_gt':False,
                                     'eol':'no','col_t':'','pn':{}}
        #TODO maybe add is_power
        
        aa_pos_p,aa_pos_n = pattern.aa_pos
       
        routed_edges = pattern.routed_edges
        m2_edges = pattern.m2_edges
           
        
        route_nets = pattern.route_nets
        v_mode = pattern.vmode
        m1_tracks = tech.M1_tracks        
        pin_map = pattern.master_ckt.pin_map #netlist to ascell
        
        route_nets = pattern.route_nets
        node_net = {}
        for key, values in route_nets.items():
            for value in values:
                node_net[value] = key
        
    
        #process edges:
        gt_cts = []
        aa_cts = []
        m1_edges = []
        gt_edges = []
        pins = {}           
        preconnect_nodes = {}

        for node,nodes in pattern.route_G.pt_connected.items():
            net = node_net[node]
            preconnect_nodes[node] = []
            for n0,n1 in nodes:
                if n0[2] == 0.5 or n1[2] ==0.5:
                    gt_cts.append((n0[0],n0[1]))
                    preconnect_nodes[node].append( (n0[0],n0[1],0) ) 
                    preconnect_nodes[node].append( (n0[0],n0[1],1) ) 
                    nodes_attr[ (n0[0],n0[1]) ]['net'] =  net
                    nodes_attr[ (n0[0],n0[1]) ]['is_gt_ct'] = True
                    nodes_attr[ (n0[0],n0[1]) ]['is_gt'] = True
                    nodes_attr[ (n0[0],n0[1]) ]['is_m1'] = True
                else:
                    preconnect_nodes[node].append( n0 ) 
                    preconnect_nodes[node].append( n1 ) 
                    if n0[2] == 1 and n1[2] == 1:
                        m1_edges.append( ( (n0[0],n0[1]), (n1[0],n1[1]) ) )
                        nodes_attr[ (n0[0],n0[1]) ]['net'] = net
                        nodes_attr[ (n1[0],n1[1]) ]['net'] = net
                        nodes_attr[ (n0[0],n0[1]) ]['is_m1'] = True
                        nodes_attr[ (n1[0],n1[1]) ]['is_m1'] = True
                    elif  n0[2] == 0 and n1[2] == 0:
                        gt_edges.append( ( (n0[0],n0[1]), (n1[0],n1[1]) ) )
                        nodes_attr[ (n0[0],n0[1]) ]['net'] = net
                        nodes_attr[ (n1[0],n1[1]) ]['net'] = net
                        nodes_attr[ (n0[0],n0[1]) ]['is_gt'] = True
                        nodes_attr[ (n1[0],n1[1]) ]['is_gt'] = True
            preconnect_nodes[node] = list(set( preconnect_nodes[node] ))
                        
        #process preconnect nodes
        routed_edges_t = {}
        for net, nodes in routed_edges.items():
            routed_edges_t[net] = []
            for n0,n1 in nodes:
                if n0 in preconnect_nodes:
                    nearest_node, min_distance = find_nearst_nodes(preconnect_nodes[n0], n1)
                    assert min_distance == 1
                    routed_edges_t[net].append((nearest_node,n1))
                    
                elif n1 in preconnect_nodes:
                    nearest_node, min_distance = find_nearst_nodes(preconnect_nodes[n1], n0)
                    assert min_distance == 1
                    routed_edges_t[net].append((nearest_node,n0))
                else:
                    routed_edges_t[net].append((n0,n1))
        
        #compare difference with following
        # pattern.route_G.plot(list(routed_edges.values()))
        # pattern.G.plot(list(routed_edges_t.values()))
        
        for net, nodes in route_nets.items():
            if net == 'VDD':
                vdd_net = nodes
            elif net == 'VSS':
                vss_net = nodes
            elif 'cross' in net:
                pass
            else:
                if pattern.net_map[net] in pin_map:
                    pins[net] = (node[0],node[1])
                    nodes_attr[ (node[0],node[1]) ]['net'] =  net
                    nodes_attr[ (node[0],node[1]) ]['is_gt_ct'] = True
                    nodes_attr[ (node[0],node[1]) ]['is_gt'] = True
                    nodes_attr[ (node[0],node[1]) ]['is_m1'] = True
                    nodes_attr[ (node[0],node[1]) ]['is_pin'] = True
   
                if len(nodes)>1:
                    for node in nodes:
                        if node[2] == 1 and node[0] !=0 and node[0] !=pattern.max_col:
                            aa_cts.append( (node[0],node[1]) )
 
        for net, nodes in m2_edges.items():
            for node in nodes:
                nodes_attr[ (node[0],node[1]) ]['net'] =  net
                nodes_attr[ (node[0],node[1]) ]['is_m2'] = True
                
    
        for net, nodes in routed_edges_t.items():
            for n0,n1 in nodes:
                if n0[2] == 0.5 or n1[2] ==0.5:
                    gt_cts.append((n0[0],n0[1]))
                    nodes_attr[ (n0[0],n0[1]) ]['net'] =  net
                    nodes_attr[ (n0[0],n0[1]) ]['is_gt_ct'] = True
                    nodes_attr[ (n0[0],n0[1]) ]['is_gt'] = True
                    nodes_attr[ (n0[0],n0[1]) ]['is_m1'] = True
                else:
                    if n0[2] == 1 and n1[2] == 1:
                        m1_edges.append( ( (n0[0],n0[1]), (n1[0],n1[1]) ) )
                        nodes_attr[ (n0[0],n0[1]) ]['net'] = net
                        nodes_attr[ (n1[0],n1[1]) ]['net'] = net
                        nodes_attr[ (n0[0],n0[1]) ]['is_m1'] = True
                        nodes_attr[ (n1[0],n1[1]) ]['is_m1'] = True
                    elif  n0[2] == 0 and n1[2] == 0:
                        gt_edges.append( ( (n0[0],n0[1]), (n1[0],n1[1]) ) )
                        nodes_attr[ (n0[0],n0[1]) ]['net'] = net
                        nodes_attr[ (n1[0],n1[1]) ]['net'] = net
                        nodes_attr[ (n0[0],n0[1]) ]['is_gt'] = True
                        nodes_attr[ (n1[0],n1[1]) ]['is_gt'] = True

            
        pn_attr = {0:'space', pattern.max_col:'space'}
        pn_l_attr =  {}
        loc = 1
        for i,n in enumerate(pattern.grid_columns):
            if n==1:
                pn_attr[loc] = 'space'
                loc += 1
            elif n==2:
                pn_attr[loc] = 'aa'
                pn_attr[loc+1] = 'gt'            
                pn_l_attr[loc+1] =  pattern.place[i]
                loc += 2
            elif n==3:
                pn_attr[loc] = 'aa'
                pn_attr[loc+1] = 'gt'
                pn_attr[loc+2] = 'aa'
                pn_l_attr[loc+1] =  pattern.place[i]
                loc += 3                
                

        for node,attr in nodes_attr.items():
            for i in range(cols):
                if node[0] == i:
                    nodes_attr[node]['col_t'] = pn_attr[i]
                    if pn_attr[i] == 'gt':
                        nodes_attr[node]['pn'] = pn_l_attr[i]
                
        #TODO   
        col_axis = self.col_space(pattern, start_x, nodes_attr, tech)
        
        
        row_axis = [t.c for t in m1_tracks]
        
        
        node_loc = {}
        for c, x in enumerate(col_axis):
            for r,y in enumerate(row_axis):
                node_loc[(c,r)] = (x,y)
        
 
        #1 CT nodes
        ct_lyt = CT_Nodes(tech, gt_cts, aa_cts, node_loc, nodes_attr)
        pattern.data.append(ct_lyt.data)
        
        #2 edges route
        edge_lyt = EdgeRoute(tech, gt_edges, m1_edges, node_loc, nodes_attr)
        pattern.data.append(edge_lyt.data)
        
        #3 GTs
        #GTs 
        #AA
        
        
        for i,pn in enumerate(self.mos_loc):
            if len(pn) >0:
                pmos = pn['P']
                nmos = pn['N']
                x = matrix[i][0][0]
                if pmos:
                    gt_aa = GT_AA(tech, x, gt_range_p, aa_range_p, pmos)
                    self.add_data(pmos.name,gt_aa.data)
                if nmos:
                    gt_aa = GT_AA(tech, x, gt_range_n, aa_range_n, nmos)
                    self.add_data(nmos.name,gt_aa.data)
   
        
        return col_axis[-1]
        
        
        

        # pattern.match_devices() 
        ct_nodes = {}
        m1_edges = {}
        gt_edges = {}
        

        

        
        return True     

        # self.end_of_line_examine()
        # self.tech_process(start_x,tech,cells)
        
   
        
        
        #3 MOS
        for i,pn in enumerate(self.mos_loc):
            if len(pn) >0:
                pmos = pn['P']
                nmos = pn['N']
                x = matrix[i][0][0]
                if pmos:
                    gt_aa = GT_AA(tech, x, gt_range_p, aa_range_p, pmos)
                    self.add_data(pmos.name,gt_aa.data)
                if nmos:
                    gt_aa = GT_AA(tech, x, gt_range_n, aa_range_n, nmos)
                    self.add_data(nmos.name,gt_aa.data)
        
        #4 AA SD
        for i,pn in enumerate(self.mos_loc):
            ct_nodes_p = [t for t in self.ct_aa_nodes if t[1]>(self.v_tracks_num/2) and t[0] == i]
            ct_nodes_n = [t for t in self.ct_aa_nodes if t[1]<=(self.v_tracks_num/2) and t[0] == i]
            ##????
            
            if i == 0:
                mos_l_p = None
                mos_l_n = None
                pn = self.mos_loc[i+1]
                if len(pn)>0:
                    if pn['P']:
                        mos_r_p = self.data[pn['P'].name]
                    else:
                        mos_r_p = None
                    if pn['N']:
                        mos_r_n = self.data[pn['N'].name]
                    else:
                        mos_r_n = None
                else:
                    mos_r_p = None
                    mos_r_n = None
            elif i >0 and i != len(self.mos_loc) - 1:
                pn = self.mos_loc[i-1]

                if len(pn)>0:
                    if pn['P']:
                        mos_l_p = self.data[pn['P'].name]
                    else:
                        mos_l_p = None
                    if pn['N']:
                        mos_l_n = self.data[pn['N'].name]               
                    else:
                        mos_l_n = None
                else:
                    mos_l_p = None
                    mos_l_n = None
                pn = self.mos_loc[i+1]

                if len(pn)>0:
                    if pn['P']:
                        mos_r_p = self.data[pn['P'].name]
                    else:
                        mos_r_p = None
                    if pn['N']:
                        mos_r_n = self.data[pn['N'].name]               
                    else:
                        mos_r_n = None
                else:
                    mos_r_p = None
                    mos_r_n = None                
            else: 
                mos_r_p = None
                mos_r_n = None
                pn = self.mos_loc[i-1]
                if len(pn)>0:
                    if pn['P']:
                        mos_l_p = self.data[pn['P'].name]
                    else:
                        mos_l_p = None
                    if pn['N']:
                        mos_l_n = self.data[pn['N'].name]
                    else:
                        mos_l_n = None
                else:
                    mos_l_p = None
                    mos_l_n = None          
                
            if mos_l_p or mos_r_p:
                
                aa_sd = AA_SD(tech, 'P', i , mos_l_p, mos_r_p, matrix, ct_nodes_p)
                
                self.add_data(('P',i),aa_sd.data)
            
            if mos_l_n or mos_r_n:
                aa_sd = AA_SD(tech, 'N', i , mos_l_n, mos_r_n, matrix, ct_nodes_n)
                self.add_data(('N',i),aa_sd.data)        
        
        #5 power   
        power = POWER(tech, cells, self.power_nodes_prop, matrix, aa_range_p, aa_range_n)
        self.add_data('power',power.data)    
        

        #may move to ascell for merge
        
        return self.h_tracks[-1]

     

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
    
    def draw(self, ckt):
        for k,v in self.data.items():
            for layer in v:    
                for box in v[layer]:
                    ckt.db_shapes[layer].insert(box.to_dbBox())

    
    def pattern_route(self, pattern, left_nodes, right_nodes, aa_pos, load_edges={}, m2_edges={}):
        #TODO: move to pattern in next version
        # G = RouteGraph(self)
        aa_m1_y_p = aa_pos[0]
        aa_m1_y_n = aa_pos[1]
        
        # if is_first:
        #     start_loc=0 
        # else:
        #     start_loc=1
        start_loc=1
        if len(m2_edges)>0:
            # pattern.m2_edges=m2_edges
            left_nodes_t = left_nodes.copy()
            right_nodes_t = right_nodes.copy()
            for k in m2_edges:
                left_nodes_t.pop(k)
                right_nodes_t.pop(k)
            left_nodes_o = left_nodes
            right_nodes_o = right_nodes                
            left_nodes = left_nodes_t
            right_nodes = right_nodes_t
  
        #creat M1 nets
        grid_columns = start_loc + sum(pattern.grid_columns)
        m1_nodes = VMode.gen_m1_grids(self.tech, grid_columns)
 
        pt_gt_nodes = {}
        pt_ct_nodes = {}
        pt_edges = []
        pt_connected = {}
    
        left_gt = []
        left_ct = []
        
        route_nets = {k:[] for k in pattern.net_map}
        
              
                
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
                    m1_nodes[(loc-1,aa_m1_y_p,1)]['net'] = pattern.net_map_r[pmos.S]
                    route_nets[pattern.net_map_r[pmos.S]].append((loc-1,aa_m1_y_p,1))
                if nmos:
                    m1_nodes[(loc-1,aa_m1_y_n,1)]['net'] = pattern.net_map_r[nmos.S]
                    route_nets[pattern.net_map_r[nmos.S]].append((loc-1,aa_m1_y_n,1))                
                
                
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
                        m1_nodes[(loc+1,aa_m1_y_p,1)]['net'] = pattern.net_map_r[pmos.D]
                        route_nets[pattern.net_map_r[pmos.D]].append((loc+1,aa_m1_y_p,1))
                    if nmos:
                        m1_nodes[(loc+1,aa_m1_y_n,1)]['net'] = pattern.net_map_r[nmos.D]
                        route_nets[pattern.net_map_r[nmos.D]].append((loc+1,aa_m1_y_n,1))    
                        
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
                pt_gt_nodes[k]['net'] = pattern.net_map_r[pn_pair[v].G]
                route_nets[pattern.net_map_r[pn_pair[v].G]].append(k)
                
            pt_edges = pt_edges + edges
            for k,v in connected.items():
                pt_connected[k] = v

        G = RouteGraph()
        G.init(pattern, pt_connected, pt_edges)
        G.add_nodes(m1_nodes, pt_gt_nodes, pt_ct_nodes)
        G.add_edges()
      
        
        median = self.tech.median
        max_r = self.tech.M1_tracks_num-1
        min_r = 0
        min_c = 0
        max_c = G.max_col

        
        # if not(is_last):
        G.add_right_nodes(median)
        max_c = G.max_col
        for net,v in right_nodes.items():
            if net in route_nets:
                route_nets[net].append((max_c,v[0],v[1]))
            else:
                route_nets[net]= [(max_c,v[0],v[1])]

            G.nodes[(max_c,v[0],v[1])]['net'] = net
                           
        # if not(is_first):
        G.add_left_nodes(median)
        for net,v in left_nodes.items():
                route_nets[net].append((min_c,v[0],v[1]))
                G.nodes[(min_c,v[0],v[1])]['net'] = net
        
        if len(m2_edges)>0:
            m2_edges_t = {}
            for k,v in m2_edges.items():
                t1 = left_nodes_o[k]
                t2 = right_nodes_o[k]
                # print('jkl',k,v)
                m2_edges_t[k]=[(min_c,t1[0],2),(max_c,t2[0],2)]
            
            pattern.m2_edges=m2_edges_t
        else:
            pattern.m2_edges = {}
            
        pattern.max_col = max_c  
        pattern.route_nets = route_nets
        route_G = G.gen_routing_graph()
        
        signals,route_G_wo_inputs = route_G.gen_routing_signals(route_nets,route_G)
        # G.cost_edge = cost_edge
        

        pattern.G = G   
        pattern.route_G = route_G  
        pattern.route_G_wo_inputs = route_G_wo_inputs  
        # print('a',pattern.left_nets, pattern.right_nets,pattern.cross_nets)
        # print('b',left_nodes)
        # print('c',right_nodes)
        # print('d',pattern.m2_edges)
        
        '''
        analogrouter is not very stable now!
        router = AnalogRouter1(pattern,route_G, signals, M2=False)
        result, paths,terminal_sets = router.run(block_pins)
        '''
        # G.plot()
        route_G.plot()
        
        result = False   
        pattern.routed_edges = {}
        
        #loaded 
        if len(load_edges)>0:
            
            convert_load_edges = {}
            for k,v in load_edges.items():
                convert_load_edges[k] = [list_to_tuple(t) for t in v]
            pattern.routed_edges = convert_load_edges 
            #TODO: examine edges inlcude all signals
            result = True

        #
        
        if not(result):
            # result = True
            #use router
            router = MIPGraphRouter()
            result, paths = router.route(route_G_wo_inputs, signals,
                                              node_cost_fn=None,
                                              edge_cost_fn=lambda e: 1)

            if result:
                #TODO: need revise this
                for path, signal in zip(paths,signals):
                    for k,v in pattern.route_nets.items():
                    
                        if set(v)== signal:
                            pattern.routed_edges[k] = list(path.edges())
    
        return  result


    def col_space(self,pattern, start_x, nodes_attr, tech ):
        x_axis = []
        for i in range(pattern.max_col+1):
            x_axis.append(start_x + 366*i)
        #return list of detail axis
        return x_axis


    def draw(self,pattern):
        for v in pattern.data:
            for layer in v:    
                for box in v[layer]:
                    self.db_shapes[layer].insert(box.to_dbBox())



def edges_on_col(edges,col):
    for name, net_edges in edges.items():
        for n1,n2 in net_edges:
            pass
            


def end_of_line_examine(edges, aa_cts):
    #TODO L shape on ct
    eol_nodes = {}
    for net, values in edges.items():
        nodes = []
        for t1,t2 in values:
            nodes.append(t1)
            nodes.append(t2)
        nodes = list(set(nodes))
        
        for node in nodes:
            t = []
            t2 = []
            
            x,y,z = node
            if (x+1,y,z) in nodes:
                t.append((x+1,y,z))
                t2.append('e')
            if (x-1,y,z) in nodes:
                t.append((x-1,y,z)) 
                t2.append('w')
            if (x,y+1,z) in nodes:
                 t.append((x,y+1,z))     
                 t2.append('n')
            if (x,y-1,z) in nodes:
                t.append((x,y-1,z)) 
                t2.append('s')
            if len(t) == 1:
                if node in self.ct_aa_nodes or  node in self.gt_ct_nodes:
                   self.eol_nodes[node] = t2[0]
                   
                   

def find_nearst_nodes(nodes, node):

    min_distance = float('inf')
    nearest_node = None
    for current_node in nodes:
        distance = (current_node[0] - node[0]) ** 2 +\
                   (current_node[1] - node[1]) ** 2 +\
                   (current_node[2] - node[2]) ** 2
        
        if distance < min_distance:
            min_distance = distance
            nearest_node = current_node
    return nearest_node, min_distance