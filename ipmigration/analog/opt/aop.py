#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: leiyuan
"""

#analog optimizer



import time
import logging
import argparse



from ipmigration.analog.opt.utils.gui import GuiParser
from ipmigration.analog.opt.utils.log import set_logger




logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description='')
parser.add_argument('--gui_data',  default='resources/simulation_setup.txt',  type=str, help='data from skill gui') 
parser.add_argument('--log_level', default='DEBUG', type=str, help='logging level: INFO, DEBUG or FATAL')

# Parse arguments
args = parser.parse_args()



args.seed = 66


def analog_optimizer(gui_data,log_level):
    
    gui = GuiParser(gui_data) #load all data according to gui txt.
    
    
    
    
    set_logger(save_dir,name,log_level)
    
    opts = OptSetting(gui.settingFile)

# def main(args):


    
    
    from src.logger import record_log
    from src.utility import boundary, generate_targets
    from src.simulation_module import generate_hierarchy_simulationFun_dict
    from src.moo_optimizer_hierarchy import USGA3Optimizer, NSGA2Optimizer, RVEAOptimizer
    from src.opt_setting import OptSetting
    
    
    opts = OptSetting(gui.settingFile)
    #-----------------------Log setup-----------------#
    #######################DEFINE LOG#############################
    record_log(opts.log_flag, opts.logfilename_prefix)
    # ------------------------------------------------------------------
    ######################DEFINE TARGETS########################################
    # Target index = [0, 1, 2, 3]
    targets = generate_targets(opts.op_targets_name, opts.op_targets_value,
                               opts.cheap_targets_name,
                               opts.cheap_targets_value, 
                               opts.expensive_targets_name,
                               opts.expensive_targets_value,
                               opts.targets_min_max_type)
    print("targets:", targets)
    ###################DEFINE BOUUNDS OF DESIGN SPACE############################## 
    boundary_class = boundary(opts.bnds)
    print("bounds_dict:", boundary_class.bounds) #print bounds_dict
    ########################DEFINE SIMULATION FUNCTION############################
    # simulation function dict
    hierarchy_simulationFun_dict = generate_hierarchy_simulationFun_dict(boundary_class, targets, \
                                                 opts.simulation_circuit_func, 
                                                 opts.corner_list)
    
    #########################DEFINE Algorithmn Parameter###########################
    
    print("num_generation: {:0}, population_size: {:1}, num_offsprings: {:2}, seed: {:3}"\
          .format(gui.num_generation, gui.population_size, gui.num_offsprings, args.seed))
    print("DNN_mode:", 0)
    ##################### Optimization loop  ###########
    
    if gui.optimizer_type=="NSGA2":
        optimizer = NSGA2Optimizer(hierarchy_simulationFun_dict, targets, 
                               boundary_class, gui.population_size, gui.num_offsprings, 
                               args.seed, opts.objective_index)
    elif gui.optimizer_type=="RVEA":
        optimizer = RVEAOptimizer(hierarchy_simulationFun_dict, targets, 
                               boundary_class, gui.population_size, gui.num_offsprings, 
                               args.seed, opts.objective_index)
    # elif Optimizer_type=="DEHome":
    #     optimizer = DEHomemadeOptimizer(hierarchy_simulationFun_dict, targets, \
    #                            boundary_class, population_size, num_offsprings, \
    #                            seed, objective_index)
    else:
        optimizer = USGA3Optimizer(hierarchy_simulationFun_dict, targets, 
                               boundary_class, gui.population_size, gui.num_offsprings, 
                               args.seed, opts.objective_index)
    
    
    
    
    pareto_set, obj_loss, const_loss = optimizer.optimize_run(gui.num_generation, DNN_mode=0)
    run_time = optimizer.run_time
    
    
    ############### Plot result ###################
    all_pareto_set_result=[]
    all_pareto_set_corner_list=[]
    for best_solution in pareto_set:
        for corner in opts.corner_list:
            result=opts.simulation_circuit_func(best_solution, boundary_class, targets,\
                                           mode="all", output=1, plot=1, corner=corner)
            all_pareto_set_result.append(result)
            all_pareto_set_corner_list.append(corner)
    
    time.sleep(1)
    print("\npareto set:")
    for j in pareto_set:
        print(j)
    
    print("Specification:\n", targets['all targets value'])
    print("pareto set simulation result:")
    for j in range(len(all_pareto_set_result)):
        print(all_pareto_set_corner_list[j], all_pareto_set_result[j])
    
    print("run_time:", run_time)
    #print(optimizer.all_sim_result)
    
if __name__ == '__main__':
    analog_optimizer(args.gui_data, args.log_level)







#from simulation_setup import model_card_path, setting_file_path


# #################DEFINE LOG SETTING######################
# from setting_up_function import log_flag, logfilename_prefix 


# #################DEFINE TARGET######################
# from setting_up_function import op_targets_name, op_targets_value,\
# cheap_targets_name, cheap_targets_value,\
# expensive_targets_name, expensive_targets_value, \
# targets_min_max_type

# ####DEFINE BOUUNDS OF DESIGN SPACE and SIMULATION FUNCTION####
# '''
# from gui
# '''
# from setting_up_function import bnds,\
# corner_list, objective_index, \
# simulation_circuit_func

# ####DEFINE Algorithmn Parameter####
# '''
# from gui
# '''
# from setting_up_function import num_generation, \
# population_size, \
# num_offsprings, \
# seed, DNN_mode, \
# Optimizer_type
