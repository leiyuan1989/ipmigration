#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: leiyuan
"""
import pandas as pd
import logging
import os
import time



class Cfg:
    def __init__(self,input_file,log_level='INFO'):
        self.input_file = input_file
        self.load_input(input_file)
        set_logger(self.output_dir, self.tech_name, log_level)
        # logger.info('cfgs: ' +str(self.__dict__))
    def load_input(self,file):
        df = pd.read_csv(file)
        cfg_dict = {r['setting']:r['value'] for i,r in df.iterrows()}
        
        settings = ['tech_name', 'netlist','output_dir','model_file','mapping_file',
                    'rule_file','layer_align','pins_align','cell_height',
                    'gate_length','v_pin_grid','h_pin_grid','power_rail_width',
                    'cell_offset_x','np_ext_border','nw_ext_np','gen_cells',
                    'metal_layers','cost_funcs']
        for setting in settings:
            assert setting in cfg_dict, '%s not in input file'%(setting)
        
        #string
        self.tech_name = cfg_dict['tech_name']     
        self.netlist = cfg_dict['netlist']       
        self.output_dir = cfg_dict['output_dir']       
        self.model_file = cfg_dict['model_file']       
        self.mapping_file = cfg_dict['mapping_file']  
        self.rule_file = cfg_dict['rule_file']   
        self.layer_align = cfg_dict['layer_align']  
        self.pins_align = cfg_dict['pins_align']  
        self.gen_cells =  [t.strip() for t in cfg_dict['gen_cells'].split()]
        self.cost_funcs = cfg_dict['cost_funcs'] 
        #list
        self.gate_length = self.load_gate_length(cfg_dict['gate_length']) 
        #int
        self.cell_height = int(cfg_dict['cell_height'])
        self.v_pin_grid = int(cfg_dict['v_pin_grid'])         
        self.h_pin_grid = int(cfg_dict['h_pin_grid'])          
        self.power_rail_width = int(cfg_dict['power_rail_width'])
        self.cell_offset_x = int(cfg_dict['cell_offset_x'])         
        self.np_ext_border = int(cfg_dict['np_ext_border'])  
        self.nw_ext_np = int(cfg_dict['nw_ext_np'])       
        self.metal_layers = int(cfg_dict['metal_layers'])   
      
        #create output dir if not exist
        if not(os.path.exists(self.output_dir)):
            os.mkdir(self.output_dir)
      
        
    def load_gate_length(self,gate_length):
        #drawn gate length(nm) example 300 ; 420/500; 
        #all gate legnth in netlist must same with this;
        if '/' in gate_length:
            return [int(t) for t in gate_length.split('/')]
        else:
            return [int(gate_length)]
        





def set_logger(save_dir, tech_name, log_level):
    #set log file
    if log_level == 'INFO':
        log_level = logging.INFO
    elif log_level == 'DEBUG':
        log_level = logging.DEBUG
    elif log_level == 'WARNING':
        log_level = logging.WARNING    
    else:
        raise ValueError('log_level is not INFO DEBUG or WARNING')
    
    log_file =  os.path.join(save_dir, time.strftime("%b_%d")+ '_%s_cellapr_log.txt'%(tech_name))  
    logging.basicConfig(format='%(asctime)s %(levelname)5s: %(message)s',
                        datefmt="%d-%H:%M:%S",
                        level=log_level,
                        filemode='w',
                        filename=log_file)
    print('logging file is:',log_file) 
    logger = logging.getLogger(__name__)
    logger.info("************Create Cell Apr: %s Logger************"%(tech_name))
        