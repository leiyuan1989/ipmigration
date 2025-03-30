# -*- coding: utf-8 -*-
"""
@author: LEI Yuan
"""

from ipmigration.cell.apr.cir.netlist import Netlist
from ipmigration.cell.apr.cir.graph import MosGraph
from ipmigration.cell.apr.tech import VMode

class Patterns:
    def __init__(self):
        model = 'ipmigration/cell/apr/cir/pattern_cdl/model.cdl'
        netlist = 'ipmigration/cell/apr/cir/pattern_cdl/patterns.cdl'

        
        self.ckt_dict = {}
        self.ckt_place = {}
        self.ckt_graph = {}

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