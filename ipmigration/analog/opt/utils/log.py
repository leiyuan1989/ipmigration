import logging
import os
import time

logger = logging.getLogger(__name__)



def set_logger(save_dir,name,log_level):
    #set log file
    if log_level == 'INFO':
        log_level = logging.INFO
    elif log_level == 'DEBUG':
        log_level = logging.INFO
    elif log_level == 'FATAL':
        log_level = logging.INFO    
    else:
        raise ValueError('log_level is not INFO DEBUG or FATAL')
    
    log_file =  os.path.join(save_dir, '%s_opt_'%(name), time.strftime("%b_%d"),'.txt')  
    
    logging.basicConfig(format='%(asctime)s %(levelname)8s: %(message)s',
                        datefmt="%Y-%m-%d %H:%M:%S",
                        level=log_level,
                        filemode='w',
                        filename=log_file)
        

        
