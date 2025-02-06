#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging

import math
import numpy as np
import pandas as pd
from ipmigration.analog.opt.edb import cirsim 


logger = logging.getLogger(__name__)

SIM_FUNC_DIC = {
    'opamp'              : cirsim.simulation_opamp,
    'levelshifter'       : cirsim.simulation_level_shifter,
    'schmitt_trigger'    : cirsim.simulation_schmitt_trigger,
    'comparator'         : cirsim.simulation_comparator,
    'dynamic_comparator' : cirsim.simulation_dynamic_comparator
    }



class Cfg:
    def __init__(self, gui_data_file):
        assert os.path.exists(gui_data_file)
        self.load_gui_data(gui_data_file)
 
    def load_cfgs(self):
        assert os.path.exists(self.setting_outputs), ""
        assert os.path.exists(self.setting_variables), ""
        
        logger.info("\nLoad Configuration: %s"%(self.gui_text))
        
        self.load_targets(self.setting_outputs)
        self.load_variables(self.setting_variables)
        
        self.hierarchy_sim_dict = cirsim.gen_hierarchy_sim_dict(self)
        
    def load_gui_data(self, file):
        '''example
            lib:[smic011]
            cell:[OpAmp]
            view:[schematic]
            log:[/data/icdesign/ams/ip_migration/users/leiyuan/cds/]
            model:[/data/icdesign/ams/ip_migration/users/leiyuan/ASMigration/ASOP/smic018/models/spectre/ms018_v1p7_spe.lib]
            outputs:[/data/icdesign/ams/ip_migration/users/leiyuan/ASMigration/ASOP/setting_outputs.csv]
            variables:[/data/icdesign/ams/ip_migration/users/leiyuan/ASMigration/ASOP/setting_variables.csv]
            testbench:[/data/icdesign/ams/ip_migration/users/leiyuan/ASMigration/ASOP/smic018/tb_template]
            result:[/data/icdesign/ams/ip_migration/users/leiyuan/ASMigration/ASOP/smic011/simResult]
            opt:[USGA3]
            generation:[2]
            population:[4]
            offspring:[4]
            corner_list:[tt]
            obj_index:[ ] 
            simulation_func:[simulation_opamp]
        '''
        assert os.path.exists(file)
        with open(file,'r') as f:
            lines = [t.strip() for t in f.readlines()]
        dic = {}
        for line in lines:
            line = line.split(']')[0]
            k, v = line.split('[')
            k = k.split(':')[0]
            k = k.strip()
            v = v.strip()
            dic[k] = v
            
        self.simulator = dic['simulator']
        self.lib_name = dic['lib']
        self.cell_name = dic['cell']  
        self.view_name = dic['view']
        
        self.log_folder = dic['log']
        self.tb_folder = dic['testbench']
        self.result_folder = dic['result']
        
        self.model_card = dic['model']
        
        self.setting_outputs = dic['outputs']
        self.setting_variables = dic['variables']

        self.optimizer_type= dic['opt']
        
        self.num_generation = int(dic['generation'])
        self.population_size = int(dic['population'])       
        self.num_offsprings = int(dic['offspring'])


        if dic['corner_list'].strip():
            self.corner_list = [t.strip() for t in dic['corner_list'].split(',')] 
        else:
            self.corner_list = ['tt']
            
        if dic['obj_index'].strip():
            self.objective_index = [int(t) for t in dic['obj_index'].split(',')]
        else:
            self.objective_index = []
        
        #set simulation function
        self.simulation_func_name = dic['simulation_func']
        assert self.simulation_func_name in SIM_FUNC_DIC, '%s not in SIM_FUNC_DIC'%(self.simulation_func_name)
        self.simulation_func = SIM_FUNC_DIC[self.simulation_func_name]
        
        self.seed = int(dic['seed'])
        self.output = int(dic['output'])

        #for log         
        self.gui_text =  '\n  lib:%s cell:%s view:%s'%(self.lib_name, self.cell_name, self.view_name ) 
        self.gui_text += '\n  log_folder:%s \n  tb_folder:%s \n  result_folder:%s'%(self.log_folder,self.tb_folder ,self.result_folder)
        self.gui_text += '\n  model_card:%s \n  setting_outputs:%s \n  setting_variables:%s'%(self.model_card,self.setting_outputs,self.setting_variables )
        self.gui_text += '\n  optimizer:%s, num_generation:%d population_size:%d num_offsprings:%d'%(self.optimizer_type,self.num_generation,self.population_size,self.num_offsprings)
        self.gui_text += '\n  corner_list:%s, objective_index:%s simulation_func:%s\n'%(str(self.corner_list ), str(self.objective_index ), self.simulation_func_name )

    
    
    def load_targets(self, file):
        assert os.path.exists(file)
        df = pd.read_csv(file)
        
        #log targets 
        logger.info('\nTargets:\n %s'%(str(df)))
        
        spec_dict = {'maximize':1.0,'minimize':-1.0}
        
        #all Type(cheap op expensive) must be equal?
        assert len(set(df.Type.tolist()))==1, 'all Type(cheap op expensive) must be equal?'
        _type = df.Type.tolist()[0]
        assert 'cheap' in _type or 'expensive' in _type or 'op' in _type, 'Type must be cheap op or expensive'
        
        names = df.Details.tolist()
        values = df.Value.tolist()
        
        if 'cheap' in _type:
            cheap_targets_name = names
            cheap_targets_value = values
        else:
            cheap_targets_name = []
            cheap_targets_value = []

        if 'expensive' in _type:
            expensive_targets_name = names
            expensive_targets_value = values
        else:
            expensive_targets_name = []
            expensive_targets_value = []
            
        if 'op' in _type:
            op_targets_name = names
            op_targets_value = values
        else:
            op_targets_name = []
            op_targets_value = []
        
        targets_min_max_type = [spec_dict[t.strip()] for t in df.Spec.tolist()]
        
        # print("op_targets_name: {0}, op_targets_value: {1}".format(op_targets_name, op_targets_value))
        # print("cheap_targets_name: {0}, cheap_targets_value: {1}".format(cheap_targets_name, cheap_targets_value))
        # print("expensive_targets_name: {0}, expensive_targets_value: {1}".format(expensive_targets_name, expensive_targets_value))
        # print("targets_min_max_type:", targets_min_max_type)


        targets={}
        targets["cheap"]=cheap_targets_value
        targets["cheap targets name"]=cheap_targets_name   
        targets["expensive"]=expensive_targets_value
        targets["expensive targets name"]=expensive_targets_name
        if op_targets_value: 
            targets["op"]=op_targets_value
            targets["op targets name"]=op_targets_name
        targets["all targets value"]=cheap_targets_value+expensive_targets_value
        targets["targets name"]=cheap_targets_name+expensive_targets_name
        if targets_min_max_type:
            targets["min_max_type"]=targets_min_max_type
        else:
            targets["min_max_type"]=list(np.ones(len(targets["all targets value"])))
        
        self.targets = targets

    
    def load_variables(self, file):
        df = pd.read_csv(file)
        #log targets 
        logger.info('\nVariables:\n %s'%(str(df)))
        
        self.capacitance_range, self.inductance_range, \
        self.resistance_range, self.current_source_range, \
        self.voltage_source_range, self.W_L_ratios_range, \
        self.lengths_values =get_design_space_setting(df)
        
        # define the bounds on the search
        self.bnds = {
                'capacitance': self.capacitance_range, 
                'inductance': self.inductance_range, 
                'resistance':self.resistance_range, 
                'current_source': self.current_source_range,
                'voltage_source': self.voltage_source_range,
                'W_L_ratios': self.W_L_ratios_range, 
                'lengths': self.lengths_values, #length fixed
                } 
   
        self.boundary = Boundary(self.bnds)
   

    
    def __repr__(self):
        text= '\n Data from GUI:%s\n'%(self.gui_text)
        
        return text



#will be integrated into Cfg class load_variables
#----------------------------------------------------------------------
class Boundary:
    def __init__(self, bnds):
        self._bnds = bnds
        self._bnds['components'] = bnds['capacitance']+\
                                   bnds['inductance']+\
                                   bnds['resistance']+\
                                   bnds['current_source']+\
                                   bnds['voltage_source']
        self.components_num = len(self._bnds['components'])
        self.bounds = self._generate_bounds()
        #self.all_variables_index_dict = self._calculate_variables_index()
    def _generate_bounds(self):
        bounds = {}
        bounds['capacitance'] = self._bnds['capacitance']
        bounds['inductance'] = self._bnds['inductance']
        bounds['resistance'] = self._bnds['resistance']
        bounds['current_source'] = self._bnds['current_source']
        bounds['voltage_source'] = self._bnds['voltage_source']
        bounds['variables'] = self._bnds['components']+self._bnds['W_L_ratios']
        bounds['constants'] = self._bnds['lengths']
        bounds['components'] = self._bnds['components']
        bounds['W_L_ratios'] = self._bnds['W_L_ratios']
        return bounds
    def _calculate_variables_index(self):
        num_capacitance = len(self._bnds['capacitance'])
        num_inductance = len(self._bnds['inductance'])
        num_resistance = len(self._bnds['resistance'])
        num_current_source = len(self._bnds['current_source'])
        num_voltage_source = len(self._bnds['voltage_source'])
        variables_index_dict={}
        variables_index_dict['capacitance'] = list(range(len(self._bnds['capacitance'])))
        tmp1 = list(range(len(self._bnds['inductance'])))
        delta1 = num_capacitance
        variables_index_dict['inductance'] = [i + delta1 for i in tmp1]
        tmp2 = list(range(len(self._bnds['resistance'])))
        delta2 = num_capacitance + num_inductance
        variables_index_dict['resistance'] = [i + delta2 for i in tmp2]
        tmp3 = list(range(len(self._bnds['current_source'])))
        delta3 = num_capacitance + num_inductance + num_resistance
        variables_index_dict['current_source'] = [i + delta3 for i in tmp3]
        tmp4 = list(range(len(self._bnds['voltage_source'])))
        delta4 = num_capacitance + num_inductance + num_resistance + num_current_source
        variables_index_dict['voltage_source'] = [i + delta4 for i in tmp4]
        tmp5 = list(range(len(self._bnds['W_L_ratios'])))
        delta5 = num_capacitance + num_inductance + num_resistance + num_current_source + num_voltage_source
        variables_index_dict['W_L_ratios'] = [i + delta5 for i in tmp5]
        return variables_index_dict
    def get_variables_range(self):
        variables_range=[(item[0], item[1]) for item in self.bounds['variables']]
        return variables_range
    def get_variables_step(self):
        variables_step=[item[2] for item in self.bounds['variables']]
        return variables_step
    def get_variables_lower(self):
        variables_lower=[item[0] for item in self.bounds['variables']]
        return variables_lower
    def get_variables_upper(self):
        variables_upper=[item[1] for item in self.bounds['variables']]
        return variables_upper
    def get_normalized_variables_range(self):
        normalized_variables_range=[(0, math.floor((item[1]-item[0])/item[2])) for item in self.bounds['variables']]
        return normalized_variables_range
    def get_normalized_variables_lower(self):
        normalized_variables_lower=[0 for item in self.bounds['variables']]
        return normalized_variables_lower
    def get_normalized_variables_upper(self):
        normalized_variables_upper=[math.floor((item[1]-item[0])/item[2]) for item in self.bounds['variables']]
        return normalized_variables_upper
        


#will be integrated into Cfg class load_variables
#######get design space setting###########
def get_design_space_setting(df):

    df_excel=df.T
    #print(df_excel)
    keys=list(df_excel.loc['item'])
    values=list(df_excel.loc['value'])
    values = [str(item).strip() for item in values]
    dictionary=dict(zip(keys, values))
    
    # get capacitance_range
    capacitance_range=dictionary['capacitance_range']
    if (capacitance_range == "nan") or (not capacitance_range):
        capacitance_range=[]
    else:
        capacitance_range=capacitance_range.split(",")
        capacitance_range_new=[]
        for idx in range(len(capacitance_range)):
            item=capacitance_range[idx]
            item_new=item.split(":")  
            item_new=[float(i) for i in item_new]
            capacitance_range_new.append(tuple(item_new))
        capacitance_range=capacitance_range_new
   
    # get inductance_range
    inductance_range=dictionary['inductance_range']
    if (inductance_range == "nan") or (not inductance_range):
        inductance_range=[]
    else:
        inductance_range=inductance_range.split(",")
        inductance_range_new=[]
        for idx in range(len(inductance_range)):
            item=inductance_range[idx]
            item_new=item.split(":")  
            item_new=[float(i) for i in item_new]
            inductance_range_new.append(tuple(item_new))
        inductance_range=inductance_range_new    

    # get resistance_range
    resistance_range=dictionary['resistance_range']
    if (resistance_range == "nan") or (not resistance_range):
        resistance_range=[]
    else:
        resistance_range=resistance_range.split(",")
        resistance_range_new=[]
        for idx in range(len(resistance_range)):
            item=resistance_range[idx]
            item_new=item.split(":")  
            item_new=[float(i) for i in item_new]
            resistance_range_new.append(tuple(item_new))
        resistance_range=resistance_range_new    

    # get current_source_range
    current_source_range=dictionary['current_source_range']
    if (current_source_range == "nan") or (not current_source_range):
        current_source_range=[]
    else:
        current_source_range=current_source_range.split(",")
        current_source_range_new=[]
        for idx in range(len(current_source_range)):
            item=current_source_range[idx]
            item_new=item.split(":")  
            item_new=[float(i) for i in item_new]
            current_source_range_new.append(tuple(item_new))
        current_source_range=current_source_range_new    
    
    # get voltage_source_range
    voltage_source_range=dictionary['voltage_source_range']
    if (voltage_source_range == "nan") or (not voltage_source_range):
        voltage_source_range=[]
    else:
        voltage_source_range=voltage_source_range.split(",")
        voltage_source_range_new=[]
        for idx in range(len(voltage_source_range)):
            item=voltage_source_range[idx]
            item_new=item.split(":")  
            item_new=[float(i) for i in item_new]
            voltage_source_range_new.append(tuple(item_new))
        voltage_source_range=voltage_source_range_new   
    
    # get W_L_ratios_range
    W_L_ratios_range=dictionary['W_L_ratios_range']
    if (W_L_ratios_range == "nan") or (not W_L_ratios_range):
        W_L_ratios_range=[]
    else:
        W_L_ratios_range=W_L_ratios_range.split(",")
        W_L_ratios_range_new=[]
        for idx in range(len(W_L_ratios_range)):
            item=W_L_ratios_range[idx]
            item_new=item.split(":")  
            item_new=[float(i) for i in item_new]
            W_L_ratios_range_new.append(tuple(item_new))
        W_L_ratios_range=W_L_ratios_range_new   
    
    # get lengths_values
    lengths_values=dictionary['lengths_values']
    if (lengths_values == "nan") or (not lengths_values):
        lengths_values=[]
    else:
        lengths_values=lengths_values.split(",")
        lengths_values=[float(item) for item in lengths_values]
    
    print("capacitance_range: {0}, inductance_range: {1}".format(capacitance_range, inductance_range))
    print("resistance_range:",resistance_range)
    print("current_source_range:",current_source_range)
    print("voltage_source_range:",voltage_source_range)
    print("W_L_ratios_range:",W_L_ratios_range)
    print("lengths_values: {0}".format(lengths_values))
    return capacitance_range, inductance_range, \
        resistance_range, current_source_range, \
        voltage_source_range, W_L_ratios_range, lengths_values


#desprated 
#######get target setting###########
# def get_targets_setting(targets_setting_path):
# # 從 Excel 文件讀取資料
#     #df_excel = pd.read_excel(targets_setting_path, sheet_name="Targets_setting")
#     df_excel = pd.read_csv(targets_setting_path)
#     df_excel=df_excel.T
#     #print(df_excel)
#     keys=list(df_excel.loc['item'])
#     values=list(df_excel.loc['value'])
#     values = [str(item).strip() for item in values]
#     dictionary=dict(zip(keys, values))
    
#     # get op_targets_name
#     if 'op_targets_name' in keys:
#         print("Has op targets name")
#         op_targets_name=dictionary['op_targets_name']
#         if (op_targets_name == "nan") or (not op_targets_name):
#             op_targets_name=[]
#         else:
#             op_targets_name=op_targets_name.split(",")
#             op_targets_name=list(op_targets_name)
#             op_targets_name=[str(item).strip() for item in op_targets_name]
#         # print(op_targets_name)
#     else:
#        op_targets_name=[]
   
#     # get op_targets_value
#     if 'op_targets_value' in keys:
#         print("Has op targets value")
#         op_targets_value=dictionary['op_targets_value']
#         if (op_targets_value == "nan") or (not op_targets_value):
#             op_targets_value=[]
#         else:
#             op_targets_value=op_targets_value.split(",")
#             op_targets_value=[float(item) for item in op_targets_value]
#     else:
#         op_targets_value=[]
        
        
#     # get cheap_targets_name
#     #cheap_targets_name=dictionary['cheap_targets_name']
#     cheap_targets_name=dictionary['targets_name']
#     if (cheap_targets_name == "nan") or (not cheap_targets_name):
#         cheap_targets_name=[]
#     else:
#         cheap_targets_name=cheap_targets_name.split(",")
#         cheap_targets_name=list(cheap_targets_name)
#         cheap_targets_name=[str(item).strip() for item in cheap_targets_name]
#    # print(cheap_targets_name)
    
#     # get cheap_targets_value
#     #cheap_targets_value=dictionary['cheap_targets_value']
#     cheap_targets_value=dictionary['targets_value']
#     if (cheap_targets_value == "nan") or (not cheap_targets_value):
#         cheap_targets_value=[]
#     else:
#         cheap_targets_value=cheap_targets_value.split(",")
#         cheap_targets_value=[float(item) for item in cheap_targets_value]
    
#     # get expensive_targets_name
#     if 'expensive_targets_name' in keys:
#         print("Has expensive_targets_name")
#         expensive_targets_name=dictionary['expensive_targets_name']
#         if (expensive_targets_name == "nan") or (not expensive_targets_name):
#             expensive_targets_name=[]
#         else:
#             expensive_targets_name=expensive_targets_name.split(",")
#             expensive_targets_name=list(expensive_targets_name)
#             expensive_targets_name=[str(item).strip() for item in expensive_targets_name]
#         # print(expensive_targets_name)
#     else:
#         expensive_targets_name=[]
        
#     # get expensive_targets_value
#     if 'expensive_targets_value' in keys:
#         print("Has expensive_targets_value")
#         expensive_targets_value=dictionary['expensive_targets_value']
#         if (expensive_targets_value == "nan") or (not expensive_targets_value):
#             expensive_targets_value=[]
#         else:
#             expensive_targets_value=expensive_targets_value.split(",")
#             expensive_targets_value=[float(item) for item in expensive_targets_value]
#     else:
#         expensive_targets_value=[]
        
#     # get targets_min_max_type
#     targets_min_max_type=dictionary['targets_min_max_type']
#     if (targets_min_max_type == "nan") or (not targets_min_max_type):
#         targets_min_max_type=[]
#     else:
#         targets_min_max_type=targets_min_max_type.split(",")
#         targets_min_max_type=[float(item) for item in targets_min_max_type]
    
    
#     print("op_targets_name: {0}, op_targets_value: {1}".format(op_targets_name, op_targets_value))
#     print("cheap_targets_name: {0}, cheap_targets_value: {1}".format(cheap_targets_name, cheap_targets_value))
#     print("expensive_targets_name: {0}, expensive_targets_value: {1}".format(expensive_targets_name, expensive_targets_value))
#     print("targets_min_max_type:", targets_min_max_type)
#     return op_targets_name, op_targets_value, \
#             cheap_targets_name, cheap_targets_value, \
#             expensive_targets_name, expensive_targets_value, \
#             targets_min_max_type



#desprated 
# def generate_targets(op_targets_name, op_targets_value, cheap_targets_name, cheap_targets_value, \
#                       expensive_targets_name, expensive_targets_value, targets_min_max_type=None):
#     """
#     return: targets_dict
#     targets_dict = {"cheap": [3163, 30, 60.0],\
#                 "expensive": [10, 10],\
#                 "targets name": ['DC Gain[dB]', 'GBW[MHz]', \
#                                 'Phase margin [deg]', 'Slew rate[MV/s]',\
#                                 'Slew rate [MV/s]']}#70dB
#     """
#     targets={}
#     targets["cheap"]=cheap_targets_value
#     targets["cheap targets name"]=cheap_targets_name   
#     targets["expensive"]=expensive_targets_value
#     targets["expensive targets name"]=expensive_targets_name
#     if op_targets_value: 
#         targets["op"]=op_targets_value
#         targets["op targets name"]=op_targets_name
#     targets["all targets value"]=cheap_targets_value+expensive_targets_value
#     targets["targets name"]=cheap_targets_name+expensive_targets_name
#     if targets_min_max_type:
#         targets["min_max_type"]=targets_min_max_type
#     else:
#         targets["min_max_type"]=list(np.ones(len(targets["all targets value"])))
#     return targets



