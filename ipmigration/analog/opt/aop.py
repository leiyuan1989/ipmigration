#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import logging

from ipmigration.analog.opt.apis import config 
from ipmigration.analog.opt.utils import log
from ipmigration.analog.opt.optimizer.moo import Optimizer

logger = logging.getLogger(__name__)


def analog_optimizer(args):
    log_level = args.log_level    
    cfg = config.Cfg(args.data_file)
    log.set_logger(cfg.log_folder, cfg.cell_name, log_level)
    
    cfg.load_cfgs()
    
    optimizer = Optimizer(cfg)


    pareto_set, obj_loss, const_loss = optimizer.optimize_run(cfg.num_generation, DNN_mode=0)
    run_time = optimizer.run_time
    
    ############### Plot result ###################
    all_pareto_set_result=[]
    all_pareto_set_corner_list=[]
    for best_solution in pareto_set:
        for corner in cfg.corner_list:
            result=cfg.simulation_func(best_solution, cfg, mode="all", output=1, plot=1, corner=corner)
        
            all_pareto_set_result.append(result)
            all_pareto_set_corner_list.append(corner)
    
    time.sleep(1)
    print("\npareto set:")
    for j in pareto_set:
        print(j)
    
    print("Specification:\n", cfg.targets['all targets value'])
    print("pareto set simulation result:")
    for j in range(len(all_pareto_set_result)):
        print(all_pareto_set_corner_list[j], all_pareto_set_result[j])
    
    print("run_time:", run_time)

