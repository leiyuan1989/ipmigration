# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 17:18:11 2024

@author: shunqidai

automatic extract setting from csv file
"""

r'''
from SimulationModule2_test import simulation_opamp, \
        simulation_level_shifter, simulation_schmitt_trigger, \
        simulation_dynamic_comparator, simulation_comparator


####################################################
#-----------------------Log setup-----------------#
#######################DEFINE LOG#############################
log_flag=True #log flag
logfilename_prefix="Two_stage_OTA_"

######################DEFINE TARGETS########################################
# Target index = [0, 1, 2, 3]
op_targets_name = ['num_saturation_device']
op_targets_value = [27] # this is num_saturation_device, VDSAT define in simulation module
cheap_targets_name = ['DC Gain', 'GBW[MHz]', \
                      'Phase margin [deg]', 'CMRR', 'PSRR', 'Output swing'] #DC gain=70dB, CMRR=80dB
cheap_targets_value = [ 3162, 10.0, 60.0, 3162, 3162, 2.7] #[10000, 30, 60.0, 10000, 10000, 2.0]
expensive_targets_name = ['Slew rate +[MV/s]', 'Slew rate -[MV/s]']
expensive_targets_value = [10, 10] #[10, 10]

targets_min_max_type = [ 1, 1, 1, 1, \
                        1, 1, 1, 1] # maximize:1.0, minimize: -1.0

###################DEFINE BOUUNDS OF DESIGN SPACE############################## 
# define range for input
c_min, c_max, c_step = 0.1, 3.0, 0.01 #pF 0.1, 3.0 #pF
cl_min, cl_max, cl_step = 0.1, 3.0, 0.1 #nH
r_min, r_max, r_step = 0.1, 100, 0.1 #kohm   0.1kohm, 100kohm typical range of zero resistor
ib_min, ib_max, ib_step = 10.0, 10.0, 0.1 #uA 10uA 60u 5uA
w_l_min, w_l_max, w_l_step = 1, 100, 0.1 #w_l_max 1-100

# define the bounds on the search
bnds = {'capacitance': [(c_min, c_max, c_step)], \
        'inductance': [], \
        'resistance': [(r_min, r_max, r_step)], \
        'current_source': [(ib_min, ib_max, ib_step)],\
        'voltage_source': [],\
        'W_L_ratios': [(w_l_min, w_l_max, w_l_step), (w_l_min, w_l_max, w_l_step), (w_l_min, w_l_max, w_l_step), \
                       (w_l_min, w_l_max, w_l_step), (w_l_min, w_l_max, w_l_step),], \
         'lengths': [0.35, 1.4, 1.4, 1.4, \
                      1.4], #length fixed
              } 


########################DEFINE SIMULATION FUNCTION############################
# simulation function dict
#corner_list=["tt", "ff", "ss", "fnsp", "snfp"]
corner_list=["tt"]
objective_index=[] #[2]
simulation_circuit_func=simulation_opamp
#########################DEFINE Algorithmn Parameter###########################
num_generation=100
population_size=40
num_offsprings=40
seed=66
DNN_mode=0
'''


from src.get_setting_for_release import get_log_setting, get_targets_setting, \
        get_algo_setting, get_design_space_setting, \
        get_sim_func_setting


class OptSetting:
    def __init__(self, setting_file_path):
    
        ############SETTING PATH#################
        # from simulation_setup import setting_file_path
        # setting_file_path=setting_file_path
        # log_setting_path=setting_file_path  #'setting.csv' #'setting_log.xlsx'
        # targets_setting_path=setting_file_path   #'setting.csv' #'setting_target.csv'
        # design_space_setting_path=setting_file_path   #"setting.csv" #"setting_design_space.csv"
        # sim_func_setting_path=setting_file_path    #"setting.csv" #"setting_sim_func.csv"
        # algo_setting_path=setting_file_path       #'setting.csv' #'setting_algo.csv'
        
        #-----------------------Log setup-----------------#
        #######################DEFINE LOG#############################
        self.log_flag, self.logfilename_prefix = get_log_setting(setting_file_path)
        
        ######################DEFINE TARGETS########################################
        # Target index = [0, 1, 2, 3]
        self.op_targets_name, self.op_targets_value, \
        self.cheap_targets_name, self.cheap_targets_value, \
        self.expensive_targets_name, self.expensive_targets_value, \
        self.targets_min_max_type = get_targets_setting(setting_file_path)
        
        ###################DEFINE BOUUNDS OF DESIGN SPACE############################## 
        # define range for input
        self.capacitance_range, self.inductance_range, \
        self.resistance_range, self.current_source_range, \
        self.voltage_source_range, self.W_L_ratios_range, \
        self.lengths_values =get_design_space_setting(setting_file_path)
        
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
        
        
        ########################DEFINE SIMULATION FUNCTION############################
        # simulation function dict
        #corner_list=["tt", "ff", "ss", "fnsp", "snfp"]
        #objective_index=[] #[2]
        self.corner_list, self.objective_index, self.simulation_circuit_func=get_sim_func_setting(setting_file_path)
        #########################DEFINE Algorithmn Parameter###########################
        '''
        move to gui
        '''
        
        # num_generation, population_size,\
        # num_offsprings, seed,\
        # DNN_mode, Optimizer_type=get_algo_setting(setting_file_path)

