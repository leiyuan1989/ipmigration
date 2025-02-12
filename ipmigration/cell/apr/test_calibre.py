# Copyright (c) ASTRI. All rights reserved.
import logging
import argparse
import os
from src.tech import Tech
from src.utils.utils import init_logger, init_check




logger = logging.getLogger(__name__)
# Define commandline arguments.
parser = argparse.ArgumentParser(description='Generate GDS layout from SPICE netlist.')
parser.add_argument('--netlist',   default='example/s1/c153_sl.cdl',     type=str,   help='netlist file name') #
parser.add_argument('--tech-name', default='c153',     type=str,   help='technology name') #
parser.add_argument('--tech-dir' , default='example/s1/ascell', type=str,   help='technology dir') #
parser.add_argument('--save-dir' , default='output/test', type=str,   help='technology dir') #
parser.add_argument('--log_level', default='INFO',     type=str,   help='logging level: INFO, DEBUG or FATAL') #


# Parse arguments
args = parser.parse_args()
args.tech_align_file = 'data/tech_align.csv'
args.pin_align_file =  'data/pin_align.csv'


init_logger(args)
init_check(args)
tech = Tech(args,  from_calibre = True)


