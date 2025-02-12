# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 11:43:20 2024

@author: leiyuan
"""

#lego


# import numpy as np
import pandas as pd
import re
import logging
from src.io.netlist_reader import SpiceParser
from src.lego.graph import StructGraph
from src.lego.schematic import deconstruction 

# from src.schema.graph import CellMultiGraph, CellGraph
# from networkx.algorithms.isomorphism import GraphMatcher

logger = logging.getLogger(__name__)


def load_netlist(base_model,base_netlist):
    with open(base_model, 'r') as f:
        lines = f.read() 
    s = SpiceParser( mode='model')
    s.parse(lines)  
    pdk_lib = s.pdk_lib
    # print(pdk_lib)
    
    with open(base_netlist, 'r') as f:
        lines = f.read()           
    s = SpiceParser(pdk_lib = pdk_lib)  
    s.parse(lines) 
    return pdk_lib, s.data    



#netlist match
def gen_lego_db1(base_model = 'src/lego/schematic/components/model.cdl', base_netlist = 'src/lego/schematic/components/components.cdl'):
    pdk_lib, ckt_dict = load_netlist(base_model, base_netlist)
    graph_dict = {}
    match_dict = {}
    df_cells = pd.DataFrame(columns=['devices','name'])
    for name,ckt in ckt_dict.items():
        ckt.process_parallel()
        ckt.gen_cellgraph()
        graph_dict[name] = ckt.cellgraph
        match_dict[name] = {}
        df_cells.loc[name] = [len(ckt.devices),name]
    df_cells = df_cells.sort_values(['devices','name'], ascending=[True, True])
  
    return graph_dict,df_cells,match_dict


#deconstruction match
def read_pin_align(file):
    df_pin_align = pd.read_csv(file,index_col='pin')
    pin_map = {}
    for i,r in df_pin_align.iterrows():
        pin_map[i] = {}
        for c in df_pin_align.columns:
            names = r[c]
            for name in names.split():     
                pin_map[i][name] = c        
    return pin_map


'''
#TODO
def _scale_netlist(self,args):
    if args.scale_l != 0: 
        scale_ratio = float(args.scale_ratio)
        scale_l = int(args.scale_l)
        for i,cell in enumerate(self.cells):
            for device in cell.devices:
                device.scale(scale_ratio,scale_l)
        self._output_cdl(args)
'''



class LEGO:

    def __init__(self,pin_align_file):
        self.log = []
        self.debug = False
        self.pass_l = {}
        self.fail_l = {}
        
        #load pin maps
        self.pin_maps = read_pin_align(pin_align_file)
        self.techs = list(self.pin_maps.keys())
        
        
        #load
        self.ckts_collection = {}
        # self.fail_collection = []
        
        for tech_name in self.techs:
            self.pass_l[tech_name] = []
            self.fail_l[tech_name] = [] 

            
    def pass_rate(self):
        total_pass = 0
        total_fail = 0
        for tech_name in self.techs:  
            t1 = len(self.pass_l[tech_name])    
            t2 = len(self.fail_l[tech_name]) 
            total_pass += t1
            total_fail += t2
            if (t1+t2)>0: 
                pr = t1/(t1+t2)
                logger.info('Tech:%s ->Pass: %d; Fail: %d; rate: %.2f%% \n'%(tech_name, t1,t2,pr*100))
                logger.info('Fail list: %s \n'%(str(self.fail_l[tech_name])))
                # raise ValueError
            
            
        if (total_pass+total_fail)>0: 
            pr = total_pass/(total_fail+total_pass)
            logger.info('Total ->Pass: %d; Fail: %d; rate: %.2f%% \n'%(total_pass,total_fail,pr*100))



    
   
    def run(self, tech_name, model_cdl, netlist_cdl):
        assert tech_name in self.techs
        pdk_lib, ckt_dict = load_netlist(model_cdl, netlist_cdl)
        self.ckt_dict = ckt_dict
        #no high v cells here
        new_ckt_dict = {}

        #TODO not process V8 V12 ... 
        for k,v in ckt_dict.items():
            digit = re.findall(r'\d+', k)
            if len(digit)>0:        
                if int(digit[0]) <=1:
                    new_ckt_dict[k] = v
        ckt_dict = new_ckt_dict


        self.run_deconstruction(tech_name, ckt_dict)
        

    
    def run_deconstruction(self, tech_name, ckt_dict):    
        self.structs_db = StructDatabase()
        pin_map =  self.pin_maps[tech_name]

        for name,ckt in ckt_dict.items():
            ckt.process_parallel()

            ckt_d = deconstruction.CktDeconstruction(tech_name, ckt, pin_map, self.structs_db, self.log, self.debug)
            # self.ckt_d = ckt_d  
            deconstruction_result = ckt_d.run()
            
            # print('Result: ',deconstruction_result, name, ckt_d, len(ckt_d.devices))
            # print(deconstruction_result)
              
            if deconstruction_result:
                # print(ckt_d.devices)
                self.pass_l[tech_name].append((name,ckt_d.ckt_type['type']))
                ckt.de = ckt_d                
            else:
                ckt.de = None
                self.fail_l[tech_name].append((name,ckt_d.ckt_type['type']))
            self.ckts_collection[name] = ckt




class StructDatabase:
    def __init__(self):
        model_netlist = 'src/lego/schematic/components/model.cdl'
        strut_netlist = 'src/lego/schematic/components/structures.cdl'
        clk_netlist = 'src/lego/schematic/components/clk.cdl'
        input_netlist = 'src/lego/schematic/components/input.cdl'
        output_netlist = 'src/lego/schematic/components/output.cdl'
        
        pdk_lib, self.ckt_dict = load_netlist(model_netlist, strut_netlist)
        pdk_lib, self.clk_dict = load_netlist(model_netlist, clk_netlist)
        pdk_lib, self.input_dict = load_netlist(model_netlist, input_netlist)
        pdk_lib, self.output_dict = load_netlist(model_netlist, output_netlist)
        
        #TODO add struct examine here to make sure not 2 struct are same
        self.examine_structs(self.ckt_dict)
        # self.examine_structs(self.input_dict)
        
        #sort input

        df_input = pd.DataFrame(columns=['devices'])
        for name,ckt in self.input_dict.items():
            ckt.process_parallel()
            df_input.loc[name] = len(ckt.devices)
            df_input = df_input.sort_values(['devices'],ascending=False)
        new_dict = {}
        for i,r in df_input.iterrows():
            new_dict[i] = self.input_dict[i] 
        self.input_dict = new_dict
        
        
        self.df = pd.DataFrame(columns=['devices'])
        for name,ckt in self.ckt_dict.items():
            ckt.process_parallel()
            self.df.loc[name] = len(ckt.devices)
            self.df = self.df.sort_values(['devices'],ascending=False)
    
    
    
    def __getitem__(self,name):
        return self.ckt_dict[name]


    
    def examine_structs(self,ckt_dict):
        for name1,ckt1 in ckt_dict.items():
            for name2,ckt2 in ckt_dict.items():
                if name1 != name2:
                    graph1 = StructGraph(ckt1.devices)
                    graph2 = StructGraph(ckt2.devices)
                    if graph1.is_isomorphic(graph2):
                        raise ValueError('Two struct with same graph: %s, %s'%(name1,name2))
        print('Struct examine passed!') #TODO to log
    @staticmethod
    def graph_to_devices(match_dict,devices_dict):
        return [devices_dict[t] for t in match_dict.values() if t in devices_dict]

    @staticmethod
    def remove_match(devices,match_devices):
        # print(devices,'aa') 
        # print(match_devices,'bb')
        for d1 in match_devices:
            for d2 in d1:
                devices.remove(d2)       
        return devices
    
    
  
    def find_substruct_matches(self,devices):
        struct_l = []
        for index,row in self.df.iterrows():
           struct = self.ckt_dict[index]
           if len(devices) >= len(struct) and len(struct) > 2 :
               devices_graph = StructGraph(devices)
               struct_graph  = StructGraph(struct.devices)
               matches = devices_graph.find_subgraph_matches(struct_graph)
               if  len(matches) >= 1:
                   struct_l.append((index, len(matches), len(devices) - len(struct)  ))
        return struct_l
    
    def assemble(self,ckt,devices,log):#p1:p2.p1 is pin in struct, p2 is pin in columns of pin align 
        devices_dict = {t.name:t for t in devices}      
        t_devices = devices.copy()    
        
        matches_l = []
        match_devices_l = []
        struct_l = []
        
        all_found = False
        for index,row in self.df.iterrows():
            struct = self.ckt_dict[index]
            if len(t_devices) >= len(struct) and not(all_found):
                devices_graph = StructGraph(t_devices)
                struct_graph  = StructGraph(struct.devices)
                matches = devices_graph.find_subgraph_matches(struct_graph)
                if  len(matches) >= 1:
                    for match in matches:
                        #need to explore every match here; but not inverter here
                        match_devices = self.graph_to_devices(match,devices_dict)
                        t1_devices = t_devices.copy()  
                        self.remove_match(t1_devices,[match_devices])
                        if  len(t1_devices) == 0:
                            all_found = True
                            matches_l = [match]
                            match_devices_l = [match_devices]
                            struct_l = [struct]
                            break
                        else:                            
                            result, match_dict = self.assemble(ckt,t1_devices,log)
                            match_dict['match'].append(match)
                            match_dict['devices'].append(match_devices)
                            match_dict['struct'].append(struct)
                            if result:
                                matches_l = match_dict['match']
                                match_devices_l = match_dict['devices']
                                struct_l =  match_dict['struct']                         
                                all_found = True
                                break
                            else:
                                matches_l = match_dict['match']
                                match_devices_l = match_dict['devices']
                                struct_l =  match_dict['struct'] 
                            
                    

        if all_found:
            return True, {'match':matches_l, 'devices':match_devices_l, 'struct': struct_l  }
        else:
            # log.append("No structs found for left devices!")
            return False, {'match':matches_l, 'devices':match_devices_l, 'struct': struct_l  }


    
    