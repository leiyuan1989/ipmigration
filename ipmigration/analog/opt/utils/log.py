import logging
import os
import time

logger = logging.getLogger(__name__)



def set_logger(save_dir, cell_name, log_level):
    #set log file
    if log_level == 'INFO':
        log_level = logging.INFO
    elif log_level == 'DEBUG':
        log_level = logging.DEBUG
    elif log_level == 'WARNING':
        log_level = logging.WARNING    
    else:
        raise ValueError('log_level is not INFO DEBUG or WARNING')
    
    log_file =  os.path.join(save_dir, time.strftime("%b_%d")+ '_%s_opt_log.txt'%(cell_name))  
    logging.basicConfig(format='%(asctime)s %(levelname)8s: %(message)s',
                        datefmt="%Y-%m-%d %H:%M:%S",
                        level=log_level,
                        filemode='w',
                        filename=log_file)
        
    logger.info("************Create Cicuit %s Logger************"%(cell_name))
        
