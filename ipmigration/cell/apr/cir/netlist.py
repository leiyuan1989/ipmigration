# -*- coding: utf-8 -*-
"""
@author: LEI Yuan
"""

#decompose

#deconstruction match

import os
import pandas as pd
import re
import logging
from ipmigration.cell.apr.io.netlist_reader import SpiceParser

logger = logging.getLogger(__name__)


class Netlist:
    def __init__(self, tech_name, pin_align_file, model_cdl, netlist_cdl):
        self.tech_name = tech_name
        #load pin maps
        self._read_pin_align(pin_align_file)
        
        
        
        self.load(model_cdl, netlist_cdl)
        
        #gen pin map template
        
        

        #load pin maps
        # self.pin_maps = self.read_pin_align(pin_align_file) #netlist pinmap, which is one-way.
        # self.techs = list(self.pin_maps.keys())
        # assert tech_name in self.techs, 'tech %s, not found in pin align file!'%(tech_name) 
        # self.pin_map  = self.pin_maps[tech_name]
        # self.load(model_cdl, netlist_cdl)


    def _read_pin_align(self, file):
        #need have ability to help users to revise pin align file if there is some error
        df = pd.read_csv(file)
        
        # for i,r in df.iterrows():
            
        
        
        pin_map = {}
        for i,r in df_pin_align.iterrows():
            pin_map[i] = {}
            for c in df_pin_align.columns:
                names = r[c]
                for name in names.split():     
                    pin_map[i][name] = c        
                    
        return pin_map
  
    def _classify_ckt(self):
        pass
  
    
  
    
    @staticmethod
    def extract_pins(model_cdl,netlist_cdl,output_dir):
        pdk_lib, ckts_dict = Netlist.load_netlist(model_cdl,netlist_cdl)
        pins = []
        with open(os.path.join(output_dir,'pins_list.txt'),'w') as f:
            for k,v in ckts_dict.items():
                line = '%-15s: '%(k)
                for p in v.pins:
                    line += '%-4s ,'%(p)
                    if not(p in pins):
                        pins.append(p)
                        
                line += '\n'
                f.write(line)                
        
        with open(os.path.join(output_dir,'pins_map_tp.csv'),'w') as f:     
            f.write('netlist_pin,ascell_pin\n')
            for p in pins:
                f.write('%s,%s\n'%(p,p))
        
        
        
  
    
    @staticmethod
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

    def load(self, model_cdl, netlist_cdl):
        pdk_lib, ckt_dict = self.load_netlist(model_cdl, netlist_cdl)
        self.ckt_dict = ckt_dict



        

        '''
        very bad process
        '''

        #TODO not process V8 V12 ... 
        #no high v cells here
        # new_ckt_dict = {}
        # for k,v in ckt_dict.items():
        #     digit = re.findall(r'\d+', k)
        #     if len(digit)>0:        
        #         if int(digit[0]) <=1:
        #             new_ckt_dict[k] = v


        # self.ckt_dict = new_ckt_dict
        # for name,ckt in self.ckt_dict.items():
        #     ckt.inspect_parallel()


        

        # self.run_deconstruction(tech_name, ckt_dict)