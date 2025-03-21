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

    def apr(self):
        pass
    
