# -*- coding: utf-8 -*-
"""
@author: LEI Yuan
"""

#decompose

#deconstruction match


import pandas as pd
import re
import logging
from ipmigration.cell.apr.io.netlist_reader import SpiceParser

logger = logging.getLogger(__name__)


class Netlist:
    def __init__(self, tech_name, pin_align_file, model_cdl, netlist_cdl):
        self.tech_name = tech_name
        
        self.log = []

        #load pin maps
        self.pin_maps = self.read_pin_align(pin_align_file)
        self.techs = list(self.pin_maps.keys())
        assert tech_name in self.techs, 'tech %s, not found in pin align file!'%(tech_name) 
        self.pin_map  = self.pin_maps[tech_name]
        self.load(model_cdl, netlist_cdl)


    def read_pin_align(self, file):
        df_pin_align = pd.read_csv(file,index_col='pin')
        pin_map = {}
        for i,r in df_pin_align.iterrows():
            pin_map[i] = {}
            for c in df_pin_align.columns:
                names = r[c]
                for name in names.split():     
                    pin_map[i][name] = c        
        return pin_map
    
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