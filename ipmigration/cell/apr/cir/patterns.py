# -*- coding: utf-8 -*-
"""
@author: LEI Yuan
"""
import os
import json
import itertools
import copy
from datetime import datetime

from ipmigration.cell.apr.cir.netlist import Netlist
from ipmigration.cell.apr.cir.graph import MosGraph,PatternGraph

from ipmigration.cell.apr.tech import VMode
from ipmigration.cell.apr.pr.smt_router import MIPGraphRouter
from ipmigration.cell.apr.io.route_loader import RouteDB, convert_tuples_to_lists


pt_list = ['FCROSS_4','PCROSS_2','INV']
# pt_list = ['INV']
class Patterns:
    def __init__(self):
        model = 'ipmigration/cell/apr/cir/pattern_cdl/model.cdl'
        netlist = 'ipmigration/cell/apr/cir/pattern_cdl/patterns.cdl'

        
        self.ckt_dict = {}
        self.ckt_place = {}
        self.ckt_graph = {}

        self.pattern_route_dict = {}

        self.clk_dict = {}
        self.logic2_dict = {}
        self.mux_dict = {}
        
        self.fcross_dict = {}
        self.pcross_dict = {}
        self.rscross_dict = {'FRS':{},'FR':{},'FS':{},
                             'PRS':{},'PR':{},'PS':{} }#Asynchronous RN/SN
        
        # self.out_dict = {}


        self.backtrack3_dict  = {}
        self.backtrack2_dict  = {}
        self.backtrack1_dict  = {}
        
        self.pull_dict  = {}



        pdk_lib, ckt_dict = Netlist.load_netlist(model, netlist)
        
        self.ckt_dict = self.sort_dict(ckt_dict)
        
        for k,v in self.ckt_dict.items():
            if 'CLK' in k:
                self.clk_dict[k] = v
            if 'LOGIC2' in k:
                self.logic2_dict[k] = v 
            if 'MUX' in k:
                self.mux_dict[k] = v           
            if 'FCROSS' in k:
                self.fcross_dict[k] = v
            if 'PCROSS' in k:
                self.pcross_dict[k] = v   
            
            if 'FRSCROSS' in k:
                self.rscross_dict['FRS'][k] = v  
            if 'FRCROSS' in k:
                self.rscross_dict['FR'][k] = v                  
            if 'FSCROSS' in k:
                self.rscross_dict['FS'][k] = v  
            if 'PRSCROSS' in k:
                self.rscross_dict['PRS'][k] = v  
            if 'PRCROSS' in k:
                self.rscross_dict['PR'][k] = v                  
            if 'PSCROSS' in k:
                self.rscross_dict['PS'][k] = v                  
                       
            if 'BACKTRACK3' in k:
                self.backtrack3_dict[k] = v  
            if 'BACKTRACK2' in k:
                self.backtrack2_dict[k] = v              
            if 'LOGIC2' in k:
                self.backtrack2_dict[k] = v 
            if 'INV' in k:
                self.backtrack1_dict[k] = v            
            
            # if 'PULL' in k:
            #     self.pull_dict[k] = v                 

            self.ckt_graph[k] = MosGraph(v)
        self.pattern_augment()
            # print(chain)
        
        # self.examine_structs(self.cross_dict)

    def sort_dict(self, di):
        return  dict(sorted(di.items(), key=lambda item: len(item[1]),reverse=True))

    def pattern_augment(self):
        self.fcross_aug_dict = {}
        self.pcross_aug_dict = {}
        self.backtrack3_aug_dict = {}
        self.backtrack2_aug_dict = {}
        self.backtrack1_aug_dict = {}
        
        aug_types = {'_noVDD':[True,False],'_noVSS':[False,True],'_noVDDVSS':[True,True]}
        for ckt_name,ckt in self.fcross_dict.items():
            for aug_type,vddvss in aug_types.items():
                aug_ckt = ckt.copy()
                vdd,vss = vddvss
                aug_ckt_name = ckt_name+aug_type
                aug_ckt.name = aug_ckt_name
                self.clear_vddvsss(aug_ckt,VDD=vdd, VSS=vss)
                self.fcross_aug_dict[aug_ckt_name] = aug_ckt
                self.ckt_graph[aug_ckt_name] = MosGraph(aug_ckt)
                self.ckt_dict[aug_ckt_name] = aug_ckt
        for ckt_name,ckt in self.pcross_dict.items():
            for aug_type,vddvss in aug_types.items():
                aug_ckt = ckt.copy()
                vdd,vss = vddvss
                aug_ckt_name = ckt_name+aug_type
                aug_ckt.name = aug_ckt_name
                self.clear_vddvsss(aug_ckt,VDD=vdd, VSS=vss)
                self.pcross_aug_dict[aug_ckt_name] = aug_ckt
                self.ckt_graph[aug_ckt_name] = MosGraph(aug_ckt)
                self.ckt_dict[aug_ckt_name] = aug_ckt    
        
        for ckt_name,ckt in self.backtrack3_dict.items():
            for aug_type,vddvss in aug_types.items():
                aug_ckt = ckt.copy()
                vdd,vss = vddvss
                aug_ckt_name = ckt_name+aug_type
                aug_ckt.name = aug_ckt_name
                self.clear_vddvsss(aug_ckt,VDD=vdd, VSS=vss)
                self.backtrack3_aug_dict[aug_ckt_name] = aug_ckt
                self.ckt_graph[aug_ckt_name] = MosGraph(aug_ckt)
                self.ckt_dict[aug_ckt_name] = aug_ckt    
        for ckt_name,ckt in self.backtrack2_dict.items():
            for aug_type,vddvss in aug_types.items():
                aug_ckt = ckt.copy()
                vdd,vss = vddvss
                aug_ckt_name = ckt_name+aug_type
                aug_ckt.name = aug_ckt_name
                self.clear_vddvsss(aug_ckt,VDD=vdd, VSS=vss)
                self.backtrack2_aug_dict[aug_ckt_name] = aug_ckt
                self.ckt_graph[aug_ckt_name] = MosGraph(aug_ckt)
                self.ckt_dict[aug_ckt_name] = aug_ckt    
        for ckt_name,ckt in self.backtrack1_dict.items():
            for aug_type,vddvss in aug_types.items():
                aug_ckt = ckt.copy()
                vdd,vss = vddvss
                aug_ckt_name = ckt_name+aug_type
                aug_ckt.name = aug_ckt_name
                self.clear_vddvsss(aug_ckt,VDD=vdd, VSS=vss)
                self.backtrack1_aug_dict[aug_ckt_name] = aug_ckt
                self.ckt_graph[aug_ckt_name] = MosGraph(aug_ckt)
                self.ckt_dict[aug_ckt_name] = aug_ckt    
    
    
    
    def clear_vddvsss(self,ckt,VDD,VSS):
        for d in ckt.devices:
            if VDD:
                if d.G == 'VDD':
                    d.G = 'NETP'
                if d.S == 'VDD':
                    d.S = 'NETP'                
                if d.D == 'VDD':
                    d.D = 'NETP'                
            if VSS:
                if d.G == 'VSS':
                    d.G = 'NETG'
                if d.S == 'VSS':
                    d.S = 'NETG'                
                if d.D == 'VSS':
                    d.D = 'NETG'             
            


    def examine_structs(self,ckt_dict):
        for name1,ckt1 in ckt_dict.items():
            for name2,ckt2 in ckt_dict.items():
                if name1 != name2:
                    graph1 = MosGraph(ckt1)
                    graph2 = MosGraph(ckt2)
                    if graph1.is_isomorphic(graph2):
                        print('Two struct with same graph: %s, %s !!'%(name1,name2))

    


    # For future
    # def pattern_routing(self, track_num):

    #     route_db = RouteDB(track_num)
    #     for name, ckt in self.ckt_dict.items():
    #         if name in pt_list:
    #             # print(name,ckt)
    #             pt_router = PatternRouter(ckt, track_num, route_db)
    #             pt_router.gen_graph()
    #             side_nodes = gen_side_nodes(pt_router)
    #             for l_nodes,r_nodes,m2_nodes in side_nodes:
    #             #can use left from right to gen 
    #                 results= route_db.find(name,l_nodes,r_nodes,m2_nodes)
    #                 result, graph_index, routed_edges, io_pins, pw_pins, m2_edges = results
    #                 print(results)
    #                 if result:
    #                     print('YY %s found in RouteDB!'%(name))
    #                     graph,route_nets = pt_router.graph[graph_index]
    #                     pt_router.routing(graph,route_nets,
    #                                       l_nodes,r_nodes,m2_nodes,
    #                                       is_load=True, 
    #                                       load=[routed_edges, io_pins, pw_pins, m2_edges]) 
                        
                        
                        
                        
    #                 else:
    #                     for graph_index, (graph,route_nets) in pt_router.graph.items():      
    #                         print('XX %s is not found in RouteDB! Route by Router'%(name))
    #                         results = pt_router.routing(graph,route_nets,l_nodes,r_nodes,m2_nodes) 
    #                         result, routed_edges, io_pins, pw_pins,m2_edges = results                         
    #                         if result:
    #                             route_db.update(name, l_nodes, r_nodes,m2_nodes, graph_index, 
    #                                     routed_edges, io_pins, pw_pins, m2_edges, save=True)
    #                     #break; add in routing and break in searching                            

                            
                            
    #                     # pt_router.G.plot()
                
    #             self.pattern_route_dict[name] = pt_router


pattern_type = {}


class Pattern:
    def __init__(self, pattern_ckt, master_ckt, match_table):
        '''
        pattern_ckt
        master_ckt
        match_table: 
        '''
        
        self.pattern_name = pattern_ckt.name
        self.pattern_ckt = pattern_ckt
        self.master_ckt = master_ckt
        #for global routing
        # self.pins = []

        self.signal_nets = []
        self.left_nets = []
        self.right_nets = []
        self.cross_nets = []
        
        self.internal_nets = []
        
        self.place = []
        self.vmode = []
        
        self.map_ckt(match_table) #map and flipped
        #load from saved
        self.load_from_saved = True

        self.m2_edges = {}
        
        #
        # self.left_pins  = {}
        # self.right_pins = {}




    def __repr__(self):
        return "pattern: %s in %s"%(self.pattern_name, self.master_ckt.name)



    def map_ckt(self, match_table):
        self.device_map = {}     #pattern ckt to master ckt
        self.device_map_r = {}   #master ckt to pattern ckt
        self.net_map = {}        #pattern ckt to master ckt
        self.net_map_r = {}      #master ckt to pattern ckt
        
        match_devices = {}
        for k,v in match_table.items():
            if (':S' in k) or (':G' in k) or (':D' in k): #device
                t1,t2 = k.split(':')
                t3,t4 = v.split(':')
                if t1+':'+t3 in match_devices:
                    match_devices[t1+':'+t3].append(t2+':'+t4)
                else:
                    match_devices[t1+':'+t3]=[t2+':'+t4]              
            
            else: #net 
                self.net_map[k] = v
                self.net_map_r[v] = k               

        #flipped
        loc = {}
        devices = []
        for k,v in match_devices.items():
            if 'G:G' in v:
                t1,t2 = k.split(':')
                self.device_map[t1] = t2
                self.device_map_r[t2] = t1
                device = self.master_ckt[t2]      
                loc[device] = self.pattern_ckt[t1].COL
                devices.append(device)
                
                #flipped device
                if 'S:D' in v and 'D:S' in v:
                    device.flipped()    
            else:
                raise ValueError(k,v) 
        #sub ckts
        self.ckt = self.master_ckt.sub_ckt(devices)
        self.ckt.name = self.pattern_name 
        
        #folding applied on pn_pairs
        #place/vmode/grid_columns
        
        for i in range(max(loc.values())):
             self.place.append({'P':None,'N':None})
        for device,loc in loc.items():
            self.place[loc-1][device.T] = device
        
        #get total grid columns
        grid_columns = []
        for i, pn_pair in enumerate(self.place):
            pmos = pn_pair['P']
            nmos = pn_pair['N']
            if not(pmos) and not(nmos):
                grid_columns.append(1)
            else:
                if i != len(self.place)-1:
                    next_pair = self.place[i+1]
                    if not(next_pair['P']) and not(next_pair['N']):
                        grid_columns.append(3)
                    else:
                        grid_columns.append(2)
                else:
                    grid_columns.append(3)
    
        self.grid_columns =grid_columns

    
    def draw(self, start_x):
        return 1
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
    
    def map_ext_nets(self):
        self.left_nets_in = [self.net_map_r[net] for net in self.left_nets]
        self.right_nets_in = [self.net_map_r[net] for net in self.right_nets]
        self.cross_nets_in = []
        for i,net in enumerate(self.cross_nets):
            self.cross_nets_in.append('CR%d'%(i+1))

    
    
    
    # def set_vmode(self,tech):
    #     for pn_pair in self.place:
    #         vmode = VMode.get_vmode(pn_pair,self.master_ckt.pin_map)
    #         self.vmode.append(tech.vmode[vmode])

    # def gen_left_nodes_in(self,left_nodes_ex):
    #     left_node_in = {}
    #     net_map = {}
    #     count=0
    #     for net,v in left_nodes_ex.items():
    #         if net in self.net_map_r:
    #             net_r = self.net_map_r[net]
    #             net_map[net_r] = net
    #             left_node_in[net_r]=v
            
    #         else:
    #             # cross net 
    #             left_node_in['cross_%d'%(count)] = left_nodes_ex[net]
    #             net_map['cross_%d'%(count)] = net
    #             count+=1  

    #     return left_node_in,net_map

    # def gen_right_nodes_ex(self,right_nodes_in,net_map):
    #     right_nodes_ex = {}
    #     for net,v in right_nodes_in.items():
    #         right_nodes_ex[net_map[net]] = v
    #     return right_nodes_ex    




    # def gen_right_nodes(self, tech, left_nodes_ex,net_map,clk_loc):
    #     median = tech.median
    #     # possible_locs = [median-1,median+1,median+2]
    #     right_nodes_ex = {}
    #     right_nodes_in = {}
        
        
        
    #     net_map_r = {v:k for k,v in net_map.items()}
    #     for net in self.right_nets + self.cross_nets:   
    #         if net in self.net_map_r: #C/CN also in pattern
    #             net_r = self.net_map_r[net]
    #             net_map[net_r] = net
    #             if net in clk_loc:
    #                 if net in left_nodes_ex:
    #                     right_nodes_ex[net] = left_nodes_ex[net]
    #                     right_nodes_in[net_r] = left_nodes_ex[net]
    #                 else:
    #                     right_nodes_ex[net] = [clk_loc[net],1]
    #                     right_nodes_in[net_r] = [clk_loc[net],1]
    #             elif net_r == 'OUT1':
    #                 right_nodes_ex[net] = [median,1]
    #                 right_nodes_in[net_r] = [median,1]
    #             elif net_r == 'D1':
    #                 right_nodes_ex[net] = [median+1,0]
    #                 right_nodes_in[net_r] = [median+1,0]
    #             elif net_r == 'IN1':
    #                 right_nodes_ex[net] = [median+1,0]
    #                 right_nodes_in[net_r] = [median+1,0]
    #             else:
    #                 t = set([v[0] for k,v in right_nodes_in.items()])
    #                 possible_locs = list(set(range(tech.M1_tracks_num)) - t)
    #                 possible_locs.sort()
    #                 loc = possible_locs.pop()
    #                 # print(self.right_nets + self.cross_nets)
    #                 right_nodes_ex[net] = [loc,1]
    #                 right_nodes_in[net_r] = [loc,1]
    #         else:
    #             # cross net 
    #             t = [v[0] for k,v in right_nodes_in.items()]
    #             if left_nodes_ex[net][0] in t:
    #                 possible_locs = list(set(range(tech.M1_tracks_num)) - set(t))
    #                 possible_locs.sort()
    #                 loc = possible_locs.pop()
    #                 right_nodes_ex[net] = [loc,1]
    #                 right_nodes_in[net_map_r[net]] = [loc,1]
    #             else:
    #                 right_nodes_ex[net] = left_nodes_ex[net]
    #                 right_nodes_in[net_map_r[net]] = left_nodes_ex[net]
   
    #     #TODO: future can use generate a list of possible right nodes.      
    #     return right_nodes_ex,right_nodes_in
    
    
    
    
    
class PatternRouter:
    def __init__(self, ckt, track_num, route_db):
        self.ckt = ckt
        self.track_num = track_num
        
        self.median_u = track_num // 2
        self.median_d = self.median_u - 1
        if track_num % 2 == 0:
            self.median = self.median_d
        else:
            self.median = self.median_u
        
        self.route_db = route_db
        
    def load(self,l_nodes,r_nodes):
        pass
    
    def routing(self,graph,route_nets_wo_side,l_nodes,
                    r_nodes,m2_nodes,v1_nodes, is_load=False, load=[],
                    savefig=None):
        G = graph.add_side_nodes(l_nodes,r_nodes)
        route_nets = copy.deepcopy(route_nets_wo_side)
        self.G = G
        #route_nets not including l and r
        l = 0  
        r = G.max_col
        for k,v in l_nodes.items():
            if k in route_nets:
                route_nets[k].append( (l,v[0],v[1]) )
            else:
                route_nets[k] = [ (l,v[0],v[1]) ]
        
        for k,v in r_nodes.items():
            if k in route_nets:
                route_nets[k].append( (r,v[0],v[1]) )
            else:
                route_nets[k] = [ (r,v[0],v[1]) ]            
        m2_edges = {}
        m2_pins = []    
        for k,v in m2_nodes.items():
            m2_pins.append((l,v[0],v[1]))
            m2_pins.append((r,v[0],v[1]))
            m2_edges[k] = [(l,v[0],v[1]), (r,v[0],v[1])]
        
        v1_pins = []
        for k,vs in v1_nodes.items():
            for v in vs:
                if v[0] == 0:
                    t = (l,v[1],v[2])
                    if t in m2_pins:
                        m2_pins.remove(t)
                    v1_pins.append((l,v[1],v[2]))
                if v[0] == 1:
                    t = (r,v[1],v[2])
                    if t in m2_pins:
                        m2_pins.remove(t)
                    v1_pins.append((r,v[1],v[2]))        
        
    
        signals, signals_names, io_pins, pw_pins = G.gen_route_nets(route_nets)
        G_R = G.gen_routing_graph(list(io_pins.values()),m2_pins)#generate routing graph, merge pre-connected nodes
        
        G.plot(pre_connect=True)
        # G_R.plot()
        

        if is_load:
            routed_edges, io_pins, pw_pins, m2_edges,v1_pins = load
            if savefig:
                G.plot(paths=list(routed_edges.values()),
                       m2_paths = list(m2_edges.values()),
                       savepath = savefig)
            self.routed_edges = routed_edges
            self.io_pins = io_pins
            self.pw_pins = pw_pins
            self.m2_edges = m2_edges
            self.v1_pins = v1_pins
            # G.plot(paths=list(routed_edges.values()),  m2_paths = list(m2_edges.values()))
        else:
            print('    Begin MIP Routing')
            router = MIPGraphRouter()
            result, paths = router.route(G_R, signals,
                                          node_cost_fn=None,
                                          edge_cost_fn=lambda e: 1)
    
    
            routed_edges = {}
            # if not(result):
            #     print('abc',route_nets,signals)
            #     G_R.plot()
               
            #     raise ValueError
            if result:
                for path, name in zip(paths,signals_names):
                    routed_edges[name] = list(path.edges())
                    
                    
                #process preconnect nodes
                pt_connected_nodes = {}
                for k,v in G.pt_connected.items():
                    pt_connected_nodes[k] = []
                    for e in v:
                        pt_connected_nodes[k].append(e[0])
                        pt_connected_nodes[k].append(e[1])
                
                routed_edges_t = {}       
                for net, nodes in routed_edges.items():
                    routed_edges_t[net] = []
                    for n0,n1 in nodes:
                        if n0 in pt_connected_nodes:
                            nearest_node, min_distance = find_nearst_nodes(pt_connected_nodes[n0], n1)
                            assert min_distance == 1                     
                            routed_edges_t[net].append((nearest_node,n1))
                        elif n1 in pt_connected_nodes:
                            nearest_node, min_distance = find_nearst_nodes(pt_connected_nodes[n1], n0)
                            assert min_distance == 1
                            routed_edges_t[net].append((nearest_node,n0))
                        else:
                            routed_edges_t[net].append((n0,n1))
                           
                # print(routed_edges_t)
                routed_edges = routed_edges_t
                
                
            
                for k,v in G.pt_connected.items():
                    net = G.nodes[k]['net']
                    if net in routed_edges:
                        routed_edges[net] += v
                    else:
                        routed_edges[net] = v

                if savefig:
                    G.plot(paths=list(routed_edges.values()),
                           m2_paths = list(m2_edges.values()),
                           savepath = savefig)
                
                self.routed_edges = routed_edges
                self.io_pins = io_pins
                self.pw_pins = pw_pins
                self.m2_edges = m2_edges
                self.v1_pins = v1_pins
                
                return True, routed_edges, io_pins, pw_pins, m2_edges, v1_pins

            return False, None, None, None, None, None
    
    


    def detail_process(self, graph, routed_edges, io_pins, pw_pins, m2_edges): 
        
        
        
        routed_edges = paths
        m2_edges = pattern.m2_edges
        
         
        
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
    
    
    
    
    def gen_graph(self):
        loc = {}
        for col in range(max([t.COL for t in self.ckt.devices])):
            loc[col+1] =[]
            for d in self.ckt.devices:
                if d.COL == col+1:
                    loc[d.COL].append(d)        
        
        self.pn = loc
        self.sub_patterns = []
        
        i = 1
        while( i<=max(self.pn.keys()) ):
            if i == max(self.pn.keys()):
                pn1 = self.pn[i]
                pn2 = None
            else:
                pn1 = self.pn[i]
                pn2 = self.pn[i+1]
            if len(pn1) == 0:
                self.sub_patterns.append(['none',[i]])
                i+=1
            elif len(pn1) == 1:
                self.sub_patterns.append(['single_%s'%(pn1[0].T),[i]])
                i+=1
            else:
                gt_nets = set([t.G for t in pn1])
                if len(gt_nets) == 1:
                    self.sub_patterns.append(['common_g',[i]])  
                    i+=1
                else:
                    cross = False
                    
                    if gt_nets == {'E_N', 'E'}:
                        if pn2:
                            next_gt_nets = set([t.G for t in pn2])
                            if  next_gt_nets  == {'E_N', 'E'}:
                                self.sub_patterns.append(['cross',[i,i+1]])  
                                i+=2
                                cross = True
                    if not(cross):
                        self.sub_patterns.append(['diff_g',[i]])  
                        i+=1
        # print(self.ckt)
        x = 1 #0 left for pattern gap       
        rts = []
        for i, sub_pattern in enumerate(self.sub_patterns): 
            if i != len(self.sub_patterns) - 1:
                right = False
                if self.sub_patterns[i+1][0] == 'none':
                    right = True
            else:
                right = True
            gt_type, pn_key = sub_pattern
            pn_pairs = [self.pn[t] for t in pn_key]    
            x, rt = gen_nodes_edges(x, gt_type, pn_pairs, self.track_num, 
                                    self.median, self.median_d, self.median_u, 
                                    right=right)         
            rts.append(rt)
    
        all_combinations = list(itertools.product(*rts))   

        self.graph = {}
        #create graph
        for i, rt_l in enumerate(all_combinations):
            nets_loc = {}
            gt_nodes = []
            m1_nodes = []
            gt_cts = []
            pre_connected = {}
            for rt in rt_l:
                #nets_loc,gt_nodes,m1_nodes,gt_cts,pre_connected = rt
                gt_nodes += rt[1]
                m1_nodes += rt[2]
                gt_cts   += rt[3]
                for k,v in rt[0].items():
                    if k in nets_loc:
                        # if k== 'OUT1':
                        #     print('xxx',v)
                        nets_loc[k] += v
                    else:
                        nets_loc[k] = v
                for k,v in rt[4].items():
                    if k in pre_connected:
                        pre_connected[k] += v
                    else:
                        pre_connected[k] = v                
            nets_loc_t = {}
            for k,v in nets_loc.items():
                v_t = []
                for t in v:
                    v_t.append(tuple(t))
                nets_loc_t[k] = list(set(v_t))

            self.net_loc = nets_loc
            # raise ValueError
            self.graph[i] = self.gen_pattern_graph(nets_loc_t,gt_nodes,m1_nodes,gt_cts,pre_connected)
            # self.graph[i].init(self.ckt, ) 
        

            
            # print(len(rts))
            # for rt in rts:
            #     nets_loc,gt_nodes,m1_nodes,gt_cts,pre_connected = rt
        
    def gen_pattern_graph(self,nets_loc,gt_nodes,m1_nodes,gt_cts,pre_connected):
        # print('1',nets_loc)
        # print('2',gt_nodes)
        # print('3',m1_nodes)
        # print('4',gt_cts)
        # print('5',pre_connected)
        gt_nodes = {tuple(t):{'net':'','loc':(t[0]+0.3, t[1]+0.3),'color':'blue'} for t in gt_nodes}
        m1_nodes = {tuple(t):{'net':'','loc':(t[0], t[1]),'color':'orange'} for t in m1_nodes}
        route_nets={}
        for k,v in nets_loc.items():
            new_v = []
            for t in v:
                new_v.append(tuple(t))
                if tuple(t) in gt_nodes:
                    gt_nodes[tuple(t)]['net'] = k
                elif tuple(t) in m1_nodes:
                    m1_nodes[tuple(t)]['net'] = k
                else:
                    raise ValueError
            
            route_nets[k] = new_v
        
        pre_connected_edges = {}
        for k,v in pre_connected.items():
            new_v = []
            for t in v:
                assert len(t)==2
                new_v.append( ( tuple(t[0]), tuple(t[1]) ) )
            pre_connected_edges[k] = new_v
        

        
        graph = PatternGraph()
        graph.init(self.ckt,pre_connected_edges)
        graph.add_nodes(m1_nodes, gt_nodes, gt_cts)
        graph.add_edges()
        # self.route_nets = route_nets
        # print(1,nets_loc)
        # print(2, route_nets)
        return graph,route_nets
    



            
            
def gen_nodes_edges(x, gt_type, pn_pairs, top, median, median_d, median_u, right=False):
    pre_connected = {}

    gt_nodes = []
    m1_nodes = []
    gt_cts = []
    nets_loc = {}
    return_types = []
    
    def update_dict(dictionary, key, value):
        if key not in dictionary:
            dictionary[key] = [value]
        else:
            dictionary[key].append(value)
            
    if gt_type == 'none':
        gt_nodes = [ [x, median_d, 0],[x, median_u, 0] ]
        m1_nodes = [ [x,t,1] for t in range(top) ]
        gt_cts =   [ [x,median_d],[x,median_u] ]
        return_types.append([nets_loc,gt_nodes,m1_nodes,gt_cts,pre_connected])
        next_x = x+1
    
    elif gt_type == 'single_P':
        pmos = pn_pairs[0][0]
        gt_nodes = [ [x,   median_d, 0], [x,   median_u, 0],
                     [x+1, median_d, 0], [x+1, median_u, 0]]
        m1_nodes = [ [t1, t2 , 1] for t2 in range(top) for t1 in [x,x+1]]
        gt_cts = [ [x+1, median_u], [x, median_d] ]

        update_dict(nets_loc,pmos.G,[x+1, median_u, 0])
        update_dict(nets_loc,pmos.S,[x,  top-2, 1] )

        next_x = x+2
        if right:
            gt_nodes.append( [x+2, median_d, 0] )
            gt_nodes.append( [x+2, median_u, 0] )
            m1_nodes = [ [t1, t2, 1] for t2 in range(top) for t1 in [x,x+1,x+2]]
            gt_cts = [ [x+1, median_u], [x, median_d], [x+2, median_d]]
            update_dict(nets_loc,pmos.D,[x+2, top-2, 1])
            next_x = x+3
        return_types.append([nets_loc,gt_nodes,m1_nodes,gt_cts,pre_connected])

    
    elif gt_type == 'single_N':
        nmos = pn_pairs[0][0]
        gt_nodes = [[x,  median_d,0],[x,  median_u,0],
                    [x+1,median_d,0],[x+1,median_u,0]]
        m1_nodes = [[t1,t2,1] for t2 in range(top) for t1 in [x,x+1]]
        gt_cts = [[x+1,median_d], [x,median_u]]
        update_dict(nets_loc,nmos.G,[x+1, median_d, 0])
        update_dict(nets_loc,nmos.S,[x,1,1] )

        next_x = x+2
        if right:
            gt_nodes.append([x+2,median_d,0])
            gt_nodes.append([x+2,median_u,0])
            m1_nodes = [[t1,t2,1] for t2 in range(top) for t1 in [x,x+1,x+2]]
            gt_cts = [[x+1,median_d], [x,median_u], [x+2,median_u]]
            update_dict(nets_loc,nmos.D,[x+2,1,1]  )
            next_x = x+3
        return_types.append([nets_loc,gt_nodes,m1_nodes,gt_cts,pre_connected])

    elif gt_type == 'common_g':
        for pn in pn_pairs[0]:
            if pn.T =='P':
                pmos = pn
            if pn.T =='N':
                nmos = pn
        
        pre_connected = {}
        nets_loc = {}
        gt_nodes = [[x,  median_d,0],[x,  median_u,0],
                    [x+1,median_d,0],[x+1,median_u,0]]
        m1_nodes = [[t1,t2,1] for t2 in range(top) for t1 in [x,x+1]]
        gt_cts = [ [x+1,median_d], [x+1,median_u], [x,median_u] ]          
             
        update_dict(nets_loc,pmos.G,[x+1, median_u, 0])
        update_dict(nets_loc,pmos.S,[x, top-2, 1] )
        update_dict(nets_loc,nmos.S,[x, 1    , 1])
        pre_connected[(x+1,median_u,0)] = [ [[x+1,median_d,0],[x+1,median_u,0]] ]
        next_x = x+2
        if right:
            gt_nodes.append([x+2,median_d,0])
            gt_nodes.append([x+2,median_u,0])
            m1_nodes = [[t1,t2,1] for t2 in range(top) for t1 in [x,x+1,x+2]]
            gt_cts = [ [x+1,median_d], [x+1,median_u], 
                       [x,  median_u], [x+2,median_u]]
            update_dict(nets_loc,pmos.D,[x+2, top-2, 1] )
            update_dict(nets_loc,nmos.D,[x+2, 1,     1] )
            next_x = x+3
        return_types.append([nets_loc,gt_nodes,m1_nodes,gt_cts,pre_connected])       

    elif gt_type == 'diff_g':
        #2 types now  
        for pn in pn_pairs[0]:
            if pn.T =='P':
                pmos = pn
            if pn.T =='N':
                nmos = pn
        #type 1
        pre_connected = {}
        nets_loc = {}
        
        gt_nodes = [[x,  median_d,0],[x,  median_u,0],
                    [x+1,median_d,0],[x+1,median_u,0]]
        m1_nodes = [[t1,t2,1] for t2 in range(top) for t1 in [x,x+1]]
        gt_cts = [ [x+1,median_u], [x,median_d] ]          
             
        update_dict(nets_loc,pmos.G,[x+1, median_u, 0] )
        update_dict(nets_loc,nmos.G,[x  , median_d, 0] )
        update_dict(nets_loc,pmos.S,[x, top-2, 1] )
        update_dict(nets_loc,nmos.S, [x, 1    , 1])
        pre_connected[(x,median_d,0)] = [ [[x,median_d,0],[x+1,median_d,0]] ]
        next_x = x+2
        if right:
            gt_nodes.append([x+2,median_d,0])
            gt_nodes.append([x+2,median_u,0])
            m1_nodes = [[t1,t2,1] for t2 in range(top) for t1 in [x,x+1,x+2]]
            gt_cts = [ [x+1,median_u],[x,median_d],[x+2,median_u] ]
                      
            update_dict(nets_loc,pmos.D,[x+2, top-2, 1] )
            update_dict(nets_loc,nmos.D,[x+2, 1,     1] )
            next_x = x+3
        return_types.append([nets_loc,gt_nodes,m1_nodes,gt_cts,pre_connected])  
        
        #type 2
        pre_connected = {}
        nets_loc = {}
        gt_nodes = [[x,  median_d,0],[x,  median_u,0],
                    [x+1,median_d,0],[x+1,median_u,0]]
        m1_nodes = [[t1,t2,1] for t2 in range(top) for t1 in [x,x+1]]
        gt_cts = [ [x+1,median_d], [x,median_u] ]          
             
        update_dict(nets_loc,pmos.G,[x  , median_u, 0] )
        update_dict(nets_loc,nmos.G,[x+1, median_d, 0] )
        update_dict(nets_loc,pmos.S,[x, top-2, 1] )
        update_dict(nets_loc,nmos.S,[x, 1    , 1])
        
        pre_connected[(x,median_u,0)] = [ [[x,median_u,0],[x+1,median_u,0]] ]
        next_x = x+2
        if right:
            next_x = x+3
            gt_nodes.append([x+2,median_d,0])
            gt_nodes.append([x+2,median_u,0])
            m1_nodes = [[t1,t2,1] for t2 in range(top) for t1 in [x,x+1,x+2]]
            gt_cts = [ [x+1,median_d],[x,median_u],[x+2,median_d] ]

            update_dict(nets_loc,pmos.D,[x+2, top-2, 1] )
            update_dict(nets_loc,nmos.D,[x+2, 1,     1] )
        return_types.append([nets_loc,gt_nodes,m1_nodes,gt_cts,pre_connected])          
        
    elif gt_type == 'cross':
        #4 types now
        for pn in pn_pairs[0]:
            if pn.T =='P':
                pmos1 = pn
            if pn.T =='N':
                nmos1 = pn
        for pn in pn_pairs[1]:
            if pn.T =='P':
                pmos2 = pn
            if pn.T =='N':
                nmos2 = pn        
        
        pre_connected = {}
        nets_loc = {}        
        
        gt_nodes = [[x,  median_d,0],[x,  median_u,0],
                    [x+1,median_d,0],[x+1,median_u,0],
                    [x+2,median_d,0],[x+2,median_u,0],
                    [x+3,median_d,0],[x+3,median_u,0] ]
        m1_nodes = [[t1,t2,1] for t2 in range(top) for t1 in [x,x+1,x+2,x+3]]
                
        update_dict(nets_loc,pmos1.S,[x,  top-2, 1] )
        update_dict(nets_loc,nmos1.S,[x,  1    , 1] )
        update_dict(nets_loc,pmos2.S,[x+2,top-2, 1] )
        update_dict(nets_loc,nmos2.S,[x+2,1    , 1] )
        next_x = x+4
        if right:
            gt_nodes.append([x+4,median_d,0])
            gt_nodes.append([x+4,median_u,0])
            m1_nodes = [[t1,t2,1] for t2 in range(top) for t1 in [x,x+1,x+2,x+3,x+4]]
        
            update_dict(nets_loc,pmos2.D,[x+4, top-2, 1] )
            update_dict(nets_loc,nmos2.D,[x+4, 1,     1])
            next_x = x+5
        #type 1
        pre_connected = {}
        nets_loc_t = {k:v for k,v in nets_loc.items()}
        
        gt_cts = [ [x,median_d], [x+1,median_u], [x+3,median_d] ]        
        update_dict(nets_loc_t,pmos1.G,[x, median_d, 0] )
        update_dict(nets_loc_t,pmos2.G,[x+1, median_u, 0])
        update_dict(nets_loc_t,pmos2.G,[x+3, median_d, 0])
        pre_connected[(x  ,median_d,0)] = [ [[x  ,median_d,0],[x+1,median_d,0]],
                                            [[x+1,median_d,0],[x+2,median_d,0]],
                                            [[x+2,median_d,0],[x+2,median_u,0]],
                                            [[x+2,median_u,0],[x+3,median_u,0]] ]
        
        return_types.append([nets_loc_t,gt_nodes,m1_nodes,gt_cts,pre_connected])  
        
        
        #type 2
        pre_connected = {}
        nets_loc_t = {k:v for k,v in nets_loc.items()}
        
        gt_cts = [ [x,median_u], [x+1,median_d], [x+3,median_u] ]        
        update_dict(nets_loc_t,pmos1.G,[x, median_u, 0] ) 
        update_dict(nets_loc_t,pmos2.G,[x+1, median_d, 0] )
        update_dict(nets_loc_t,pmos2.G,[x+3, median_u, 0] )        
        pre_connected[(x  ,median_u,0)] = [[[x  ,median_u,0],[x+1,median_u,0]],
                                           [[x+1,median_u,0],[x+2,median_u,0]],
                                           [[x+2,median_u,0],[x+2,median_d,0]],
                                           [[x+2,median_d,0],[x+3,median_d,0]] ]
        
        return_types.append([nets_loc_t,gt_nodes,m1_nodes,gt_cts,pre_connected])  
        
    else:
        raise ValueError
    return next_x, return_types
        
#for special side nodes locs
def gen_side_nodes(pattern_router):
    name = pattern_router.ckt.name
    tp = pattern_router.track_num-1
    mu = pattern_router.median_u
    md = pattern_router.median_d
    dn = 0
    
    side_nodes = []
    
    if 'INV' in name:
        if not('no' in name):
            side_nodes = []
            side_nodes.append( [ {'IN1': [mu , 0]}, {'OUT1': [mu , 1]},{} ] )
            
            side_nodes.append( [ {}, {'IN1': [tp , 1], 'OUT1': [dn , 1]}, {} ] )
            side_nodes.append( [ {}, {'IN1': [dn , 1], 'OUT1': [tp , 1]}, {} ] )       
            
            # side_nodes.append( [ {'IN1': [mu , 0]}, {'OUT1': [md , 1]} ] )
            # side_nodes.append( [ {'IN1': [md , 0]}, {'OUT1': [mu , 1]} ] )
            # side_nodes.append( [ {'IN1': [md , 0]}, {'OUT1': [md , 1]} ] )
            # side_nodes.append( [ {'IN1': [mu , 1]}, {'OUT1': [mu , 1]} ] )
            # side_nodes.append( [ {'IN1': [mu , 1]}, {'OUT1': [md , 1]} ] )
            # side_nodes.append( [ {'IN1': [md , 1]}, {'OUT1': [mu , 1]} ] )
            # side_nodes.append( [ {'IN1': [md , 1]}, {'OUT1': [md , 1]} ] )            
            # side_nodes.append( [ {'OUT1': [mu , 1]}, {'IN1': [mu , 0]} ] )   
            # side_nodes.append( [ {'OUT1': [md , 1]}, {'IN1': [mu , 0]} ] ) 
            # side_nodes.append( [ {'OUT1': [mu , 1]}, {'IN1': [md , 0]} ] ) 
            # side_nodes.append( [ {'OUT1': [md , 1]}, {'IN1': [md , 0]} ] ) 
            # t_side_nodes = [t for t in side_nodes]
            # for l_n,r_n in t_side_nodes:
            #     l = l_n.copy()
            #     r = r_n.copy()
            #     l['CR1'] = [tp,1]
            #     r['CR1'] = [tp,1]
            #     l['CR2'] = [dn,1]
            #     r['CR2'] = [dn,1]               
            #     side_nodes.append([l,r])
            #     l = l_n.copy()
            #     r = r_n.copy()
            #     l['CR1'] = [tp,1]
            #     r['CR1'] = [tp,1]
            #     l['CR2'] = [dn,1]
            #     r['CR2'] = [dn,1]    
            #     l['CR3'] = [tp-1,1]
            #     r['CR3'] = [tp-1,1]
            #     l['CR4'] = [dn+1,1]
            #     r['CR4'] = [dn+1,1]  
            #     side_nodes.append([l,r])                
            # print('aaa',len(side_nodes))
            return side_nodes
        elif 'noVDDVSS' in name:
            return side_nodes
        elif 'noVDD' in name:
            return side_nodes
        elif 'noVSS' in name:
            return side_nodes
        else:
            pass
        
    elif 'CLK' in name:
        return side_nodes
    elif 'LOGIC2' in name:
        return side_nodes
    elif 'FCROSS' in name:
        '''
        FCROSS_4,,"E_N,E,OUT1,D1",
        FCROSS_4,"E,E_N","OUT1,D1",
        FCROSS_4,"D1,E_N,E,D","D1,OUT1",
        FCROSS_4,"E_N,E,D","OUT1,D1",
        FCROSS_4,D,"E,E_N,OUT1,D1",
        FCROSS_4,"E,E_N",OUT1,
        FCROSS_4,D,"D1,E_N,E,OUT1",CR1
        FCROSS_4,"E_N,E","OUT1,D1",CR1
        '''
        side_nodes = []
        if not('no' in name):

            side_pins = [ [ [], ['E_N','E','OUT1','D1'], [] ],
                           [ ['E_N','E'], ['OUT1','D1'], [] ],
                           [ ['E_N','E','D','D1'], ['OUT1','D1'], [] ],
                           [ ['E_N','E','D'], ['OUT1','D1'], [] ],
                           [ ['D'], ['E_N','E','OUT1','D1'], [] ],
                           [ ['E_N','E'], ['OUT1'], [] ],
                           [ ['D'], ['E_N','E','OUT1','D1'], ['CR1'] ],
                           [ ['E_N','E'], ['OUT1','D1'], ['CR1'] ]
                         ]
    
            locs =[ [{'E_N':[tp,1],'E':[dn,1]},{'E_N':[dn,1],'E':[tp,1]}] , 
                    [{'D':[mu,1],'D1':[md,1],'OUT1':[mu,1], 'CR1':[tp-1,1],'CR2':[dn+1,1]} ] ]
            all_combinations = list(itertools.product(*locs))
            all_locs = []
            for locs in all_combinations:
                loc = {}
                for t in locs:
                    loc.update(t)
                all_locs.append(loc)
            
            for loc in all_locs:     
                for side_pin in side_pins:
                    l = {}
                    r = {}
                    m2 = {}
                    for t in side_pin[0]:
                        l[t] = loc[t]
                    for t in side_pin[1]:
                        r[t] = loc[t]   
                    for t in side_pin[2]:
                        m2[t] = loc[t]  
                    side_nodes.append([l,r,m2])
                
            return side_nodes
        else:
            return side_nodes

    elif 'PCROSS' in name:
        side_nodes.append( [ {}, 
                            {'IN1': [tp , 1], 'OUT1': [dn , 1]}, 
                            {} ] )
        
        
        
        
        return side_nodes        
    elif 'FRSCROSS' in name:
        return side_nodes        
    elif 'FRCROSS' in name:
        return side_nodes        
    elif 'FSCROSS' in name:
        return side_nodes        
    elif 'PRSCROSS' in name:
        return side_nodes        
    elif 'PRCROSS' in name:
        return side_nodes        
    elif 'PSCROSS' in name:
        return side_nodes    
    elif 'BACKTRACK3' in name:
        return side_nodes        
    elif 'BACKTRACK2' in name:
        return side_nodes  
    
    else:
        raise ValueError

def gen_pin_locs(pin,tp,dn,mu,md,pt_type=''):
    if pin == 'D':
        locs = [{},
            
            ]
        
        


class Vmodes:
    def __init__(self, track_num):
        self.track_num = track_num
    
    
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