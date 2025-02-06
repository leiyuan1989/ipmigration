# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 17:07:15 2024

@author: shunqidai


hide "op targets", "expensive target", "seed", "DNN_mode" in setting csv file
modifiy "cheap targets" as "targets" in setting csv file
Dec 10, 2024

"""


import pandas as pd
import math

from ipmigration.analog.opt.simulation_module import simulation_opamp, \
                                  simulation_level_shifter, simulation_schmitt_trigger, \
                                  simulation_dynamic_comparator, simulation_comparator

# #######get log setting###########
# def get_log_setting(log_setting_path):
# # 從 Excel 文件讀取資料
#     #df_excel = pd.read_excel(log_setting_path, sheet_name="Log_setting")
#     df_excel = pd.read_csv(log_setting_path)
#     df_excel=df_excel.T
#     #print(df_excel)
#     keys=list(df_excel.loc['item'])
#     values=list(df_excel.loc['value']) 
#     values = [str(item).strip() for item in values]
#     #print(values)
#     dictionary=dict(zip(keys, values))
#     log_flag=dictionary['log_flag']
#     log_flag=float(log_flag)
#     #print(log_flag)
#     if (not log_flag) or math.isnan(log_flag):
#         log_flag=1
#     else:
#         log_flag=float(log_flag)
#     logfilename_prefix=dictionary['logfilename_prefix']
#     if (logfilename_prefix == 'nan') or (not logfilename_prefix):
#         logfilename_prefix=r'log_temp_'
#     print("log_flag: {0}, logfilename_prefix: {1}".format(log_flag, logfilename_prefix))
#     return log_flag, logfilename_prefix


#######get target setting###########
def get_targets_setting(targets_setting_path):
# 從 Excel 文件讀取資料
    #df_excel = pd.read_excel(targets_setting_path, sheet_name="Targets_setting")
    df_excel = pd.read_csv(targets_setting_path)
    df_excel=df_excel.T
    #print(df_excel)
    keys=list(df_excel.loc['item'])
    values=list(df_excel.loc['value'])
    values = [str(item).strip() for item in values]
    dictionary=dict(zip(keys, values))
    
    # get op_targets_name
    if 'op_targets_name' in keys:
        print("Has op targets name")
        op_targets_name=dictionary['op_targets_name']
        if (op_targets_name == "nan") or (not op_targets_name):
            op_targets_name=[]
        else:
            op_targets_name=op_targets_name.split(",")
            op_targets_name=list(op_targets_name)
            op_targets_name=[str(item).strip() for item in op_targets_name]
        # print(op_targets_name)
    else:
       op_targets_name=[]
   
    # get op_targets_value
    if 'op_targets_value' in keys:
        print("Has op targets value")
        op_targets_value=dictionary['op_targets_value']
        if (op_targets_value == "nan") or (not op_targets_value):
            op_targets_value=[]
        else:
            op_targets_value=op_targets_value.split(",")
            op_targets_value=[float(item) for item in op_targets_value]
    else:
        op_targets_value=[]
        
        
    # get cheap_targets_name
    #cheap_targets_name=dictionary['cheap_targets_name']
    cheap_targets_name=dictionary['targets_name']
    if (cheap_targets_name == "nan") or (not cheap_targets_name):
        cheap_targets_name=[]
    else:
        cheap_targets_name=cheap_targets_name.split(",")
        cheap_targets_name=list(cheap_targets_name)
        cheap_targets_name=[str(item).strip() for item in cheap_targets_name]
   # print(cheap_targets_name)
    
    # get cheap_targets_value
    #cheap_targets_value=dictionary['cheap_targets_value']
    cheap_targets_value=dictionary['targets_value']
    if (cheap_targets_value == "nan") or (not cheap_targets_value):
        cheap_targets_value=[]
    else:
        cheap_targets_value=cheap_targets_value.split(",")
        cheap_targets_value=[float(item) for item in cheap_targets_value]
    
    # get expensive_targets_name
    if 'expensive_targets_name' in keys:
        print("Has expensive_targets_name")
        expensive_targets_name=dictionary['expensive_targets_name']
        if (expensive_targets_name == "nan") or (not expensive_targets_name):
            expensive_targets_name=[]
        else:
            expensive_targets_name=expensive_targets_name.split(",")
            expensive_targets_name=list(expensive_targets_name)
            expensive_targets_name=[str(item).strip() for item in expensive_targets_name]
        # print(expensive_targets_name)
    else:
        expensive_targets_name=[]
        
    # get expensive_targets_value
    if 'expensive_targets_value' in keys:
        print("Has expensive_targets_value")
        expensive_targets_value=dictionary['expensive_targets_value']
        if (expensive_targets_value == "nan") or (not expensive_targets_value):
            expensive_targets_value=[]
        else:
            expensive_targets_value=expensive_targets_value.split(",")
            expensive_targets_value=[float(item) for item in expensive_targets_value]
    else:
        expensive_targets_value=[]
        
    # get targets_min_max_type
    targets_min_max_type=dictionary['targets_min_max_type']
    if (targets_min_max_type == "nan") or (not targets_min_max_type):
        targets_min_max_type=[]
    else:
        targets_min_max_type=targets_min_max_type.split(",")
        targets_min_max_type=[float(item) for item in targets_min_max_type]
    
    
    print("op_targets_name: {0}, op_targets_value: {1}".format(op_targets_name, op_targets_value))
    print("cheap_targets_name: {0}, cheap_targets_value: {1}".format(cheap_targets_name, cheap_targets_value))
    print("expensive_targets_name: {0}, expensive_targets_value: {1}".format(expensive_targets_name, expensive_targets_value))
    print("targets_min_max_type:", targets_min_max_type)
    return op_targets_name, op_targets_value, \
            cheap_targets_name, cheap_targets_value, \
            expensive_targets_name, expensive_targets_value, \
            targets_min_max_type

#######get design space setting###########
def get_design_space_setting(setting_path):
# 從 Excel 文件讀取資料
    #df_excel = pd.read_excel(setting_path, sheet_name="Design_space_setting")
    df_excel = pd.read_csv(setting_path)
    df_excel=df_excel.T
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


#######get simulation function setting###########
def get_sim_func_setting(setting_path):
# 從 Excel 文件讀取資料
    #df_excel = pd.read_excel(setting_path, sheet_name="Sim_func_setting")
    df_excel = pd.read_csv(setting_path)
    df_excel=df_excel.T
    #print(df_excel)
    keys=list(df_excel.loc['item'])
    values=list(df_excel.loc['value']) 
    values = [str(item).strip() for item in values]
    #print(values)
    dictionary=dict(zip(keys, values))
    
    # get corner_list
    corner_list=dictionary['corner_list']
    if (corner_list == "nan") or (not corner_list):
        corner_list=['tt']
    else:
        corner_list=corner_list.split(",")
        corner_list=list(corner_list)
        corner_list=[str(item).strip() for item in corner_list]
   # print(corner_list)
    
    # get objective_index
    objective_index=dictionary['objective_index']
    if (objective_index == "nan") or (not objective_index):
        objective_index=[]
    else:
        objective_index=objective_index.split(",")
        objective_index=[int(item) for item in objective_index]

    # get simulation_circuit_func
    simulation_circuit_func=dictionary['simulation_circuit_func']
    if simulation_circuit_func=="simulation_opamp":
        simulation_circuit_func=simulation_opamp
    elif simulation_circuit_func=="simulation_level_shifter":
        simulation_circuit_func=simulation_level_shifter
    elif simulation_circuit_func=="simulation_schmitt_trigger":
        simulation_circuit_func=simulation_schmitt_trigger
    elif simulation_circuit_func=="simulation_dynamic_comparator":
        simulation_circuit_func=simulation_dynamic_comparator
    else:
        simulation_circuit_func=simulation_comparator
        
    print("corner_list: {0}, objective_index: {1}".format(corner_list, objective_index))
    print("simulation_circuit_func: {0}".format(simulation_circuit_func))
    return corner_list, objective_index,\
            simulation_circuit_func


#######get algorithmn setting###########
def get_algo_setting(algo_setting_path):
# 從 Excel 文件讀取資料
    #df_excel = pd.read_excel(algo_setting_path, sheet_name="Algo_setting")
    df_excel = pd.read_csv(algo_setting_path)
    df_excel=df_excel.T
    #print(df_excel)
    keys=list(df_excel.loc['item'])
    values=list(df_excel.loc['value']) 
    values = [str(item).strip() for item in values]
    #print(values)
    dictionary=dict(zip(keys, values))
    
    # get num_generation
    num_generation=dictionary['num_generation']
    if (num_generation == "nan") or (not num_generation):
        num_generation=20
    else:
        num_generation=int(float(num_generation))
    
    # get population_size
    population_size=dictionary['population_size']
    if (population_size == "nan") or (not population_size):
        population_size=40
    else:
        population_size=int(float(population_size))

    # get population_size
    num_offsprings=dictionary['num_offsprings']
    if (num_offsprings == "nan") or (not num_offsprings):
        num_offsprings=40
    else:
        num_offsprings=int(float(num_offsprings))
        
    # get seed
    if 'seed' in keys:
        print("Has seed")
        seed=dictionary['seed']
        if (seed == "nan") or (not seed):
            seed=66
        else:
            seed=int(float(seed))
    else:
        seed=66

    # get DNN_mode
    if 'DNN_mode' in keys:
        print("Has DNN_mode")
        DNN_mode=dictionary['DNN_mode']
        if (DNN_mode == "nan") or (not DNN_mode):
            DNN_mode=0
        else:
            DNN_mode=int(float(DNN_mode))
    else:
        DNN_mode=0
    
    # get Optimizer_type
    Optimizer_type=dictionary['Optimizer_type']
    if (Optimizer_type == "nan") or (not Optimizer_type):
        Optimizer_type="USGA3"
          
        
    print("num_generation: {0}, population_size: {1}".format(num_generation, population_size))
    print("num_offsprings: {0}, seed: {1}".format(num_offsprings, seed))
    print("DNN_mode: {0}".format(DNN_mode))
    print("Optimizer_type: {0}".format(Optimizer_type))
    return num_generation, population_size,\
            num_offsprings, seed, DNN_mode, Optimizer_type



###################test#####################
'''
log_setting_path='setting.csv' #'setting.xlsx'
get_log_setting(log_setting_path)
print("\n")
setting_path='setting_target.csv' #'setting.xlsx'
#setting_path='setting.xlsx' #'setting.xlsx'
get_targets_setting(setting_path)
print("\n")
setting_path='setting_design_space.csv' #'setting.xlsx'
get_design_space_setting(setting_path)
print("\n")
setting_path='setting_sim_func.csv' #'setting.xlsx'
get_sim_func_setting(setting_path)
print("\n")
setting_path='setting_algo.csv' #'setting.xlsx'
get_algo_setting(setting_path)
'''