# -*- coding: utf-8 -*-


import logging
import argparse

from ipmigration.analog.opt import aop 

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description='ASTRI Analog Optimization')
parser.add_argument('--data_file', default='./demo/analog_opt/opamp/simulation_setup.txt', type=str, help='data from skill gui') 
parser.add_argument('--simulator', default='spectre', type=str, help='simulator: spectre') 
parser.add_argument('--log_level', default='INFO', type=str, help='logging level: INFO DEBUG or WARNING')
parser.add_argument('--monitor', default=True, type=bool, help='animated results')
# Parse arguments
args = parser.parse_args()


if __name__ == '__main__':
    aop.analog_optimizer(args)