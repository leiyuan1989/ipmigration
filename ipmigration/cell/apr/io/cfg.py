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
        self.log_level = log_level
        self.input_file = input_file
        self.load_input(input_file)
        self.set_logger()
        # logger.info('cfgs: ' +str(self.__dict__))
    def load_input(self,file):
        df = pd.read_csv(file)
        cfg_dict = {r['setting']:r['value'] for i,r in df.iterrows()}
        
        settings = ['tech_name', 'netlist','output_dir','model_file','mapping_file',
                    'rule_file','layer_align','pins_align','cell_height',
                    'gate_length','v_pin_grid','h_pin_grid','power_rail_width',
                    'cell_offset_x','np_ext_border','nw_ext_np','gen_cells','cost_funcs']
        for setting in settings:
            assert setting in cfg_dict, '%s not in input file'%(setting)
        
        #string
        self.tech_name = cfg_dict['tech_name']     
        self.netlist = cfg_dict['netlist']       
        self.output_dir = cfg_dict['output_dir']       
        self.model_file = cfg_dict['model_file']       
        self.mapping_file = cfg_dict['mapping_file']  
        self.rule_file = cfg_dict['rule_file']   
        self.rule_align = cfg_dict['rule_align']  
        self.layer_align = cfg_dict['layer_align']  
        self.pins_align = cfg_dict['pins_align']  
        self.gen_cells =  [t.strip() for t in cfg_dict['gen_cells'].split()]
        
        if self.gen_cells == ['all']:
            self.gen_cells = ['arithmetic','complex','multiplex','ff'       ,'scanff'   ,'latch'     ,'clockgate']
        
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
        # self.metal_layers = int(cfg_dict['metal_layers'])   
      
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
        
    def set_logger(self):
        #set log file
        log_level = self.log_level
        output_dir = self.output_dir
        tech_name = self.tech_name
        
        # output_dir = "./demo/cell_apr/outputs/c153"
        # log_level = "INFO"  # 可选: DEBUG, INFO, WARNING, ERROR, CRITICAL
        # tech_name = "C153"
        
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        # 生成日志文件名
        log_file = os.path.join(output_dir, f"00_LOG_{time.strftime('%m_%d_%H')}.txt")
        
        # 获取根日志记录器
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, log_level))
        
        # 创建文件处理器
        file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
        
        # 设置日志格式
        formatter = logging.Formatter(
            fmt='%(asctime)s %(levelname)5s: %(message)s',
            datefmt="%d-%H:%M:%S"
        )
        file_handler.setFormatter(formatter)
        
        # 清空所有已存在的处理器（避免重复）
        root_logger.handlers = []
        
        # 添加文件处理器到根日志记录器
        root_logger.addHandler(file_handler)
        
        # 获取命名日志记录器（继承根日志记录器的配置）
        logger = logging.getLogger(__name__)
        
        # 记录初始化信息
        root_logger.info(f"logging file is: {log_file}")
        root_logger.info(f"************Create Cell Apr: {tech_name} Logger************")
        
        # # 验证日志配置
        # print(f"日志文件路径: {log_file}")
        # print(f"根日志级别: {logging.getLevelName(root_logger.getEffectiveLevel())}")
        # print(f"根日志处理器: {root_logger.handlers}")
        # print(f"当前日志级别: {logging.getLevelName(logger.getEffectiveLevel())}")
        # print(f"当前日志处理器: {logger.handlers}")
        
        # 测试日志记录
        # logger.debug("这是一条DEBUG级别的日志")
        # logger.info("这是一条INFO级别的日志")
        # logger.warning("这是一条WARNING级别的日志")
        # logger.error("这是一条ERROR级别的日志")    
        