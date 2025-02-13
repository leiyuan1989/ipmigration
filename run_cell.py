# Copyright (c) ASTRI. All rights reserved.
import logging
import argparse
from ipmigration.cell.apr.io import cfg
from ipmigration.cell.apr.tech import Tech
from ipmigration.cell.apr.ascell import ASCell






# from src.utils.gui import App



logger = logging.getLogger(__name__)
# Define commandline arguments.
parser = argparse.ArgumentParser(description='Generate GDS layout from SPICE netlist.')
parser.add_argument('--input', default='demo/cell_apr/setting_c110.csv', type=str, help='cell setting file') #
parser.add_argument('--log_level', default='INFO', type=str,  help='logging level') #

# Parse arguments
args = parser.parse_args()


'''
runfile('demo/cell_apr/rule/extract_rule.py',wdir='./')
'''

args.input = 'demo/cell_apr/setting_c110.csv'

cfgs  = cfg.Cfg(args.input, args.log_level)
tech  = Tech(cfgs)
cells = ASCell(cfgs,tech)






# def ascell(args,app):
#     file = open('log_tmp.txt','w')
#     init_logger(args)
#     init_check(args)
#     #set tech file
#     tech = Tech(args)
#     cells = ASCell(args,tech)
#     cells.run(file,app=app)
#     file.close()


# data = [
#         ['Tech Name','c153'], 
#         ['Netlist', 'example/example_netlist.cdl'],
#         ['Cfg Dir','example/ascell'],
#         ['Save Dir','output/test'],
#         ['Tech Align','data/tech_align.csv'],
#         ['Pin Align','data/pin_align.csv'],
#        ]

# app = App(ascell)
# app.run(data,args)