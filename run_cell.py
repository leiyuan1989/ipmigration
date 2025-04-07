# Copyright (c) ASTRI. All rights reserved.
import logging
import argparse
from ipmigration.cell.apr.io import cfg
from ipmigration.cell.apr.tech import Tech
from ipmigration.cell.apr.ascell import ASCell

EXTRACT_PIN = True #For Expertise Lib Design


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
# cfgs.io_offset
# if EXTRACT_PIN:
#     from ipmigration.cell.apr.cir.netlist import Netlist
#     Netlist.extract_pins(cfgs.model_file, cfgs.netlist, cfgs.output_dir  )


tech  = Tech(cfgs)
cells = ASCell(cfgs,tech)
cells.run()


c1 = cells['DFANRQ0']
c2 = cells['DENRQ0']
c3 = cells['DFNFQ0']
c4 = cells['DFNRB0']
c5 = cells['DFNRQ0']
c6 = cells['DFSCRQ0']
c7 = cells['SDANRQ0']
c8 = cells['SDNFB0']
c9 = cells['LANLB0']

pattern = c1.queue[3]
# app = App(ascell)
# app.run(data,args)