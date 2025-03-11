# -*- coding: utf-8 -*-
"""
@author: LEI Yuan
"""

from ipmigration.cell.apr.cir.netlist import Netlist
from ipmigration.cell.apr.cir.graph import MosGraph

class Patterns:
    def __init__(self):
        model = 'ipmigration/cell/apr/cir/pattern_cdl/model.cdl'
        netlist = 'ipmigration/cell/apr/cir/pattern_cdl/patterns.cdl'

        
        self.ckt_dict = {}
        self.ckt_place = {}
        self.ckt_graph = {}

        self.clk_dict = {}
        self.logic_dict = {}
        self.mux_dict = {}
        
        self.fcross_dict = {}
        
        
        
        # self.out_dict = {}
        self.cross_dict = {}

        self.backtrack_dict  = {}
        self.pull_dict  = {}



        pdk_lib, ckt_dict = Netlist.load_netlist(model, netlist)
        
        self.ckt_dict = self.sort_dict(ckt_dict)
        
        for k,v in self.ckt_dict.items():
            if 'CLK' in k:
                self.clk_dict[k] = v
            # if 'OUT_' in k:
            #     self.clk_dict[k] = v                
                
            if 'LOGIC' in k:
                self.logic_dict[k] = v 
            if 'MUX' in k:
                self.mux_dict[k] = v           
            
            if 'FCROSS' in k:
                self.fcross_dict[k] = v
                
                
            if 'CROSS' in k:
                self.cross_dict[k] = v            
         
            

            
            if 'BACKTRACK' in k:
                self.backtrack_dict[k] = v  
            if 'PULL' in k:
                self.pull_dict[k] = v                 

            self.ckt_graph[k] = MosGraph(v)
            # print(chain)
        
        self.examine_structs(self.cross_dict)

    def sort_dict(self, di):
        return  dict(sorted(di.items(), key=lambda item: len(item[1]),reverse=True))


    def examine_structs(self,ckt_dict):
        for name1,ckt1 in ckt_dict.items():
            for name2,ckt2 in ckt_dict.items():
                if name1 != name2:
                    graph1 = MosGraph(ckt1)
                    graph2 = MosGraph(ckt2)
                    if graph1.is_isomorphic(graph2):
                        print('Two struct with same graph: %s, %s !!'%(name1,name2))



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
        # self.match_table = match_table
        #
        self.map_ckt(match_table) #map and flipped
 
        #for global routing
        self.pins = []
        # self.place = {}
        
        
        self.signal_nets = []
        self.left_nets = []
        self.right_nets = []
        self.cross_nets = []
        self.internal_nets = []
        #load from saved
        self.load_from_saved = True
        
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
        
        self.place = []
        for i in range(max(loc.values())):
             self.place.append({'P':None,'N':None})
        for device,loc in loc.items():
            self.place[loc-1][device.T] = device

        
        
        # for device in self.ckt.devices:
            
                    
        # chain = Chain()
        # chain.load_from_netlist(v)                
        # self.ckt_place[k] = chain
        # def add_device(self, device):
            
                # device_struct.W = device.W 
                # device_struct.L = device.L 
                # device_struct.NF = device.NF     
                
                # #flip devices
                # if 'S:D' in v and 'D:S' in v:
                #     device = self.master_ckt.get_device(t2)
                #     # print('a',device)
                #     device.flipped()    
                    # print('b',self.master_ckt.get_device(t2))