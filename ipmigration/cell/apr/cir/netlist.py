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

CKT_TYPES  = ['arithmetic','complex','multiplex','ff'       ,'scanff'   ,'latch'     ,'clockgate']
CKT_CLOCKS = ['none'      ,'none'   ,'none'     ,'clock_pin','clock_pin','enable_pin','clock_pin']
DEBUG=False

class Netlist:
    def __init__(self, tech_name, pin_align_file, model_cdl, netlist_cdl):
        self.tech_name = tech_name
        #load pin maps
        self.pin_map = self._read_pin_align(pin_align_file)
        #load ckts
        self.pdk_lib, self.ckt_di = self.load_netlist(model_cdl, netlist_cdl)
        #classify ckts
        self.ckt_types = self._classify_ckts(self.ckt_di, self.pin_map)
        
        
        
        
        #gen pin map template
        
        

        #load pin maps
        # self.pin_maps = self.read_pin_align(pin_align_file) #netlist pinmap, which is one-way.
        # self.techs = list(self.pin_maps.keys())
        # assert tech_name in self.techs, 'tech %s, not found in pin align file!'%(tech_name) 
        # self.pin_map  = self.pin_maps[tech_name]
        # self.load(model_cdl, netlist_cdl)
    def __getitem__(self,key):
        return self.ckt_di[key]
    def _read_pin_align(self, file):
        #need have ability to help users to revise pin align file if there is some error
        df = pd.read_csv(file)
        di = {(r['type'],r['io']):[r['pins'],r['ascell']] for i,r in df.iterrows()}
        new_di = {}
        for k,v in di.items():
            new_di[k] = {x.strip():y.strip() for x,y in zip(v[0].split(),v[1].split())}
        di = new_di    
       
        def merge_dict(d1,d2):
            d3 = {}
            for k,v in d1.items():
                d3[k]=v
            for k,v in d2.items():
                d3[k]=v
            return d3
        
        for ckt_type, ckt_clock in zip(CKT_TYPES,CKT_CLOCKS):   
            di[(ckt_type,'inout')] = merge_dict( di[(ckt_type,'in')], di[(ckt_type,'out')])
            di[(ckt_type,'all')] =   merge_dict( di[(ckt_type,'inout')], di[('power_pin', 'all')])            
            if ckt_clock != 'none':
                if ckt_clock == 'clock_pin':
                    di[(ckt_type,'all')] =  merge_dict( di[(ckt_type,'all')], di[('clock_pin', 'all')])
                elif ckt_clock == 'enable_pin':
                    di[(ckt_type,'all')] =  merge_dict( di[(ckt_type,'all')], di[('enable_pin', 'all')])          
            
        return di
        

  
    def _classify_ckts(self,ckt_di,pin_map):
        ckt_types_di = {t:[] for t in CKT_TYPES}
        
        for name, ckt in ckt_di.items():
            predict_types = [] 
            pins = set(ckt.pins)
            for ckt_type, ckt_clock in zip(CKT_TYPES,CKT_CLOCKS):
                if pins <= set(pin_map[(ckt_type,'all')].keys()):
                
                    mapped_pins = [pin_map[(ckt_type,'all')][t] for t in pins]
                 
                    predict_type = self._classify_ckt(mapped_pins)
                    # print(mapped_pins,predict_type)
                    if predict_type == ckt_type:
                        predict_types.append([ckt_type, ckt_clock, mapped_pins])
                    
            if len(predict_types) == 1:
                ckt_type, ckt_clock, mapped_pins = predict_types[0]
 
                if ckt_type in ['ff', 'scanff', 'latch', 'clockgate']:#sl logic
                    input_type = self._analyze_sl_input_type(mapped_pins)

                else:
                    input_type= None #left for cl
                ckt_types_di[ckt_type].append(name)
                self._set_ckt(ckt, ckt_type, input_type, ckt_clock, pin_map)                
            else:#0 
                print('Warning: %s can not be processed!'%(name),pins,predict_types)
                if DEBUG:
                    for ckt_type, ckt_clock in zip(CKT_TYPES,CKT_CLOCKS):
                        print(pins,ckt_type,pin_map[(ckt_type,'all')].keys())
                        if pins <= set(pin_map[(ckt_type,'all')].keys()):
                            mapped_pins = [pin_map[(ckt_type,'all')][t] for t in pins]
                            predict_type = self._classify_ckt(mapped_pins,debug=True)
                            print(predict_type,ckt_type)

                # raise ValueError
                        
        return ckt_types_di
  
    def _classify_ckt(self, mapped_pins, debug=False):
        c0 = 'CK' in mapped_pins or 'CKN' in mapped_pins 
        c1 = 'G'  in mapped_pins or 'GN'  in mapped_pins 
        c2 = 'Y' in mapped_pins
        c3 = 'Q'  in mapped_pins or 'QN'  in mapped_pins 
        c4 = 'ECK' in mapped_pins
        c5 = 'S' in mapped_pins
        c6 = 'CO' in mapped_pins
        c7 = 'S0' in mapped_pins
        c8 = 'SE'  in mapped_pins and 'SI'  in mapped_pins 
        if debug:
            print(mapped_pins,c0,c1,c2,c3,c4,c5,c6,c7,c8)
        if c5 and c6:
            return 'arithmetic'
        elif c2 and not(c7):
            return 'complex'
        elif c2 and c7:
            return 'multiplex'
        elif c3 and c0 and not(c8):
            return 'ff'
        elif c3 and c0 and c8:
            return 'scanff'       
        elif c3 and c1:
            return 'latch'                 
        elif c0 and c4:
            return 'clockgate'  
        else:
            return 'none'
        # ckt_types  = ['arithmetic','complex','multiplex','ff'       ,'scanff'   ,'latch'     ,'clockgate']
  
    
    def _analyze_sl_input_type(self, mapped_pins):
        c0 = 'D'  in mapped_pins 
        c1 = 'E'  in mapped_pins 
        c2 = 'D0' in mapped_pins and 'D1' in mapped_pins 
        c3 = 'RN' in mapped_pins
        c4 = 'SN' in mapped_pins 
        din = False
        enable = False
        mulin = False
        sn = False
        rn = False
        if c0:
            din = True  
        if c1:
            enable = True
        if c2:
            mulin = True
        if c3:
            rn = True
        if c4:
            sn = True
        return [din,enable, mulin, rn, sn]
        
    
    
    def _set_ckt(self, ckt, ckt_type, input_type, ckt_clock, pin_map):                
        pins_in  = pin_map[(ckt_type, 'in')]  #From netlist names to standardized ascell names
        pins_out = pin_map[(ckt_type, 'out')] #From netlist names to standardized ascell names
        pins_power = pin_map[('power_pin', 'all')] #From netlist names to standardized ascell names
        
        if ckt_clock == 'clock_pin':
            pins_clk = pin_map[('clock_pin', 'all')]
        elif ckt_clock == 'enable_pin':
            pins_clk = pin_map[('enable_pin', 'all')]
        else:
            pins_clk = []
        #set circuit type and inputs 
        ckt.set_cir_type_and_in_nets(ckt_type,pins_in,pins_out,pins_power,pins_clk,input_type)  
        
  
    
    @staticmethod
    def extract_pins(model_cdl,netlist_cdl,output_dir):
        pdk_lib, ckts_dict = Netlist.load_netlist(model_cdl,netlist_cdl)
        pins = []
        with open(os.path.join(output_dir,'aux_pins_list.txt'),'w') as f:
            for k,v in ckts_dict.items():
                line = '%-15s: '%(k)
                for p in v.pins:
                    line += '%-4s ,'%(p)
                    if not(p in pins):
                        pins.append(p)
                        
                line += '\n'
                f.write(line)                
        
        with open(os.path.join(output_dir,'aux_pins_map_tp.csv'),'w') as f:     
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

    # def load(self, model_cdl, netlist_cdl):
    #     pdk_lib, ckt_dict = self.load_netlist(model_cdl, netlist_cdl)
    #     self.ckt_dict = ckt_dict


    def save_ckt_types(self, save_dir):
        data = {'ckt':[],'type':[],'en':[], 'mi':[], 'rn':[],'sn':[] }
        for k,vs in self.ckt_types.items():
            for v in vs:
                ckt = self[v]
                data['ckt'].append(v)
                data['type'].append(ckt.ckt_type)
                data['en'].append(ckt.enable)
                data['mi'].append(ckt.mul_in)
                data['rn'].append(ckt.rn)
                data['sn'].append(ckt.sn)
        df = pd.DataFrame(data)
        df.to_csv(os.path.join(save_dir,'ckt_types.csv'))
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