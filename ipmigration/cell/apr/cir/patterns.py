# -*- coding: utf-8 -*-
"""
@author: LEI Yuan
"""
import os
import json
import itertools
from datetime import datetime

from ipmigration.cell.apr.cir.netlist import Netlist
from ipmigration.cell.apr.cir.graph import MosGraph,PatternGraph

from ipmigration.cell.apr.tech import VMode
from ipmigration.cell.apr.pr.smt_router import MIPGraphRouter


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

    
    def load_route_data(self, track_num):
        self.route_data_dir = 'ipmigration/cell/apr/cir/pattern_route'
        self.track_num = track_num
        self.route_data_path = os.path.join(self.route_data_dir,'pattern_route_%d.json'%(self.track_num))

        with open(self.route_data_path, 'r', encoding='utf-8') as file:
            self.route_data = json.load(file)
            print("Load Pattern Routing Data (%s) Successfully!"%(self.route_data_path))
    

    
    def pattern_routing(self, json_out=None):
        copy_json_file(self.route_data_path)
        for name, ckt in self.ckt_dict.items():
            # print(name,ckt)
            pt_router = PatternRouter(ckt, self.track_num)
            pt_router.gen_graph()
            side_nodes = gen_side_nodes(pt_router)
            for l_nodes,r_nodes in side_nodes:
                #TODO 
                for i, (graph,route_nets) in pt_router.graph.items():      
                    pt_router.routing(graph,route_nets,l_nodes,r_nodes)
                    pt_router.G.plot()
            
            self.pattern_route_dict[name] = pt_router


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
        self.left_pins  = {}
        self.right_pins = {}




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
    
    def set_vmode(self,tech):
        for pn_pair in self.place:
            vmode = VMode.get_vmode(pn_pair,self.master_ckt.pin_map)
            self.vmode.append(tech.vmode[vmode])

    def gen_left_nodes_in(self,left_nodes_ex):
        left_node_in = {}
        net_map = {}
        count=0
        for net,v in left_nodes_ex.items():
            if net in self.net_map_r:
                net_r = self.net_map_r[net]
                net_map[net_r] = net
                left_node_in[net_r]=v
            
            else:
                # cross net 
                left_node_in['cross_%d'%(count)] = left_nodes_ex[net]
                net_map['cross_%d'%(count)] = net
                count+=1  

        return left_node_in,net_map

    def gen_right_nodes_ex(self,right_nodes_in,net_map):
        right_nodes_ex = {}
        for net,v in right_nodes_in.items():
            right_nodes_ex[net_map[net]] = v
        return right_nodes_ex    




    def gen_right_nodes(self, tech, left_nodes_ex,net_map,clk_loc):
        median = tech.median
        # possible_locs = [median-1,median+1,median+2]
        right_nodes_ex = {}
        right_nodes_in = {}
        
        
        
        net_map_r = {v:k for k,v in net_map.items()}
        for net in self.right_nets + self.cross_nets:   
            if net in self.net_map_r: #C/CN also in pattern
                net_r = self.net_map_r[net]
                net_map[net_r] = net
                if net in clk_loc:
                    if net in left_nodes_ex:
                        right_nodes_ex[net] = left_nodes_ex[net]
                        right_nodes_in[net_r] = left_nodes_ex[net]
                    else:
                        right_nodes_ex[net] = [clk_loc[net],1]
                        right_nodes_in[net_r] = [clk_loc[net],1]
                elif net_r == 'OUT1':
                    right_nodes_ex[net] = [median,1]
                    right_nodes_in[net_r] = [median,1]
                elif net_r == 'D1':
                    right_nodes_ex[net] = [median+1,0]
                    right_nodes_in[net_r] = [median+1,0]
                elif net_r == 'IN1':
                    right_nodes_ex[net] = [median+1,0]
                    right_nodes_in[net_r] = [median+1,0]
                else:
                    t = set([v[0] for k,v in right_nodes_in.items()])
                    possible_locs = list(set(range(tech.M1_tracks_num)) - t)
                    possible_locs.sort()
                    loc = possible_locs.pop()
                    # print(self.right_nets + self.cross_nets)
                    right_nodes_ex[net] = [loc,1]
                    right_nodes_in[net_r] = [loc,1]
            else:
                # cross net 
                t = [v[0] for k,v in right_nodes_in.items()]
                if left_nodes_ex[net][0] in t:
                    possible_locs = list(set(range(tech.M1_tracks_num)) - set(t))
                    possible_locs.sort()
                    loc = possible_locs.pop()
                    right_nodes_ex[net] = [loc,1]
                    right_nodes_in[net_map_r[net]] = [loc,1]
                else:
                    right_nodes_ex[net] = left_nodes_ex[net]
                    right_nodes_in[net_map_r[net]] = left_nodes_ex[net]
   
        #TODO: future can use generate a list of possible right nodes.      
        return right_nodes_ex,right_nodes_in
    
    
    
    
    
class PatternRouter:
    def __init__(self, ckt, track_num):
        self.ckt = ckt
        self.track_num = track_num
        
        self.median_u = track_num // 2
        self.median_d = self.median_u - 1
        if track_num % 2 == 0:
            self.median = self.median_d
        else:
            self.median = self.median_u
        
        
        
    def load(self):
        pass
    
    def routing(self,graph,route_nets,l_nodes,r_nodes):
        G = graph.add_side_nodes(l_nodes,r_nodes)
        self.G = G
        
        # signals,pins = graph.gen_route_nets(route_nets)
        # self.pins = pins

        # graph_route = graph.gen_routing_graph()
        # graph_route.remove_pins(pins)
        
        # return graph, graph_route, signals,pins 
        
    
    
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
        print(self.ckt)
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
                        if k== 'OUT1':
                            print('xxx',v)
                        nets_loc[k] += v
                    else:
                        nets_loc[k] = v
                for k,v in rt[4].items():
                    if k in pre_connected:
                        pre_connected[k] += v
                    else:
                        pre_connected[k] = v                
            print('yyy',nets_loc)
            self.net_loc = nets_loc
            # raise ValueError
            self.graph[i] = self.gen_pattern_graph(nets_loc,gt_nodes,m1_nodes,gt_cts,pre_connected)
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
            side_nodes.append( [ {'IN1': [mu , 0]}, {'OUT1': [mu , 1]} ] )
            side_nodes.append( [ {'IN1': [mu , 0]}, {'OUT1': [md , 1]} ] )
            side_nodes.append( [ {'IN1': [md , 0]}, {'OUT1': [mu , 1]} ] )
            side_nodes.append( [ {'IN1': [md , 0]}, {'OUT1': [md , 1]} ] )
            side_nodes.append( [ {'IN1': [mu , 1]}, {'OUT1': [mu , 1]} ] )
            side_nodes.append( [ {'IN1': [mu , 1]}, {'OUT1': [md , 1]} ] )
            side_nodes.append( [ {'IN1': [md , 1]}, {'OUT1': [mu , 1]} ] )
            side_nodes.append( [ {'IN1': [md , 1]}, {'OUT1': [md , 1]} ] )            
            side_nodes.append( [ {'OUT1': [mu , 1]}, {'IN1': [mu , 0]} ] )   
            side_nodes.append( [ {'OUT1': [md , 1]}, {'IN1': [mu , 0]} ] ) 
            side_nodes.append( [ {'OUT1': [mu , 1]}, {'IN1': [md , 0]} ] ) 
            side_nodes.append( [ {'OUT1': [md , 1]}, {'IN1': [md , 0]} ] ) 
            t_side_nodes = [t for t in side_nodes]
            for l_n,r_n in t_side_nodes:
                l = l_n.copy()
                r = r_n.copy()
                l['CR1'] = [tp,1]
                r['CR1'] = [tp,1]
                l['CR2'] = [dn,1]
                r['CR2'] = [dn,1]               
                side_nodes.append([l,r])
                l = l_n.copy()
                r = r_n.copy()
                l['CR1'] = [tp,1]
                r['CR1'] = [tp,1]
                l['CR2'] = [dn,1]
                r['CR2'] = [dn,1]    
                l['CR3'] = [tp-1,1]
                r['CR3'] = [tp-1,1]
                l['CR4'] = [dn+1,1]
                r['CR4'] = [dn+1,1]  
                side_nodes.append([l,r])                
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
        return side_nodes
    elif 'PCROSS' in name:
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




class Vmodes:
    def __init__(self, track_num):
        self.track_num = track_num
    
    




def copy_json_file(file_path):
    try:
        if not os.path.exists(file_path):
            print(f"Error: File {file_path} does not exist.")
            return
        now = datetime.now()
        month_day = now.strftime("%m%d")
        file_name, file_ext = os.path.splitext(file_path)
        new_file_name = f"{file_name}_{month_day}{file_ext}"
        with open(file_path, 'rb') as src, open(new_file_name, 'wb') as dst:
            dst.write(src.read())
        print(f"File successfully copied to {new_file_name}")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    
    