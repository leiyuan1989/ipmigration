# Copyright (c) ASTRI. All rights reserved.
import argparse
from ipmigration.cell.apr.io import cfg
from ipmigration.cell.apr.tech import Tech
from ipmigration.cell.apr.ascell import ASCell
from ipmigration.cell.apr.cir.netlist import Netlist

EXTRACT_PIN = True #For Expertise Lib Design


# logger = logging.getLogger(__name__)
# Define commandline arguments.
parser = argparse.ArgumentParser(description='Generate GDS layout from SPICE netlist.')
parser.add_argument('--input', default='demo/cell_apr/setting_c153.csv', type=str, help='cell setting file') #
parser.add_argument('--log_level', default='INFO', type=str,  help='logging level') #

# Parse arguments
args = parser.parse_args()



#TODO
'''
1. db with fast index
2. text add
3. pin align
'''

cfgs  = cfg.Cfg(args.input, args.log_level)
tech  = Tech(cfgs)

#Support pin align creation
if EXTRACT_PIN:
    nl=Netlist.extract_pins(cfgs.model_file, cfgs.netlist, cfgs.output_dir)

cells = ASCell(cfgs,tech)
cells.run()


#test 



# c1 = cells['DFANRQ0']
# c2 = cells['DENRQ0']
# c3 = cells['DFNFQ0']
# c4 = cells['DFNRB0']
# c5 = cells['DFNRQ0']
# c6 = cells['DFSCRQ0']
# c7 = cells['SDANRQ0']
# c8 = cells['SDNFB0']
# c9 = cells['LANLB0']
# p0 = c2.queue[0]
# p1 = c2.queue[1]
# app = App(ascell)
# app.run(data,args)