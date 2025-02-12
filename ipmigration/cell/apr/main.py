# Copyright (c) ASTRI. All rights reserved.
import logging
import argparse
from src.ascell import ASCell
from src.tech import Tech
from src.utils.utils import init_logger, init_check
from src.utils.gui import App



logger = logging.getLogger(__name__)
# Define commandline arguments.
parser = argparse.ArgumentParser(description='Generate GDS layout from SPICE netlist.')
parser.add_argument('--netlist',   default='',     type=str,   help='netlist file name') #
parser.add_argument('--tech-name', default='x180',     type=str,   help='technology name') #
parser.add_argument('--tech-dir' , default='data/dev', type=str,   help='technology dir') #
parser.add_argument('--save-dir' , default='output/test', type=str,   help='technology dir') #
parser.add_argument('--log_level', default='INFO',     type=str,   help='logging level: INFO, DEBUG or FATAL') #


# Parse arguments
args = parser.parse_args()
args.tech_align_file = 'data/tech_align.csv'
args.pin_align_file =  'data/pin_align.csv'
args.test_ckts = []
#for test 
tech_name_list = ['c153']


# args.test_ckts = ['LANHB1','LANHQ1','LANHN1','LANLB1','LANLQ1','LANLN1',             
#                   'DFNFB1','DFNRB1','DFNRN1','DFNRQ1',
#                   'DFFSR_X1','EDFFR_X1','CLKGTP_X1','LATSR_X1']


args.netlist = 'example/example_netlist.cdl'    
args.tech_name = 'c153'
args.tech_dir = 'example/ascell'

def ascell(args,app):
    file = open('log_tmp.txt','w')
    init_logger(args)
    init_check(args)
    #set tech file
    tech = Tech(args)
    cells = ASCell(args,tech)
    cells.run(file,app=app)
    file.close()


data = [
        ['Tech Name','c153'], 
        ['Netlist', 'example/example_netlist.cdl'],
        ['Cfg Dir','example/ascell'],
        ['Save Dir','output/test'],
        ['Tech Align','data/tech_align.csv'],
        ['Pin Align','data/pin_align.csv'],
       ]

app = App(ascell)
app.run(data,args)