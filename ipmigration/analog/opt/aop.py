#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import logging

from ipmigration.analog.opt.apis import config 
from ipmigration.analog.opt.utils import log,figureplot,monitor
from ipmigration.analog.opt.optimizer.moo import Optimizer
from ipmigration.analog.opt.simulator import spectre 


logger = logging.getLogger(__name__)


def analog_optimizer(args):
    log_level = args.log_level    
    cfg = config.Cfg(args.data_file)
    log.set_logger(cfg.log_folder, cfg.cell_name, log_level)
    
    cfg.load_cfgs()

    #test simulator 
    if cfg.simulator == 'spectre':    
        version = spectre.Circuit.check_cmd()
        logger.info(version)
    else:
        raise ValueError("Simulator %s is not support now"%(cfg.simulator ))


    optimizer = Optimizer(cfg)

    if args.monitor:
        mon = monitor.Monitor(cfg.log_folder, cfg.targets_df)
    pareto_set, obj_loss, const_loss = optimizer.optimize_run(cfg.num_generation, DNN_mode=0, monitor=mon)
    
    mon.save()
    figureplot.plot_result(cfg, optimizer,pareto_set)

