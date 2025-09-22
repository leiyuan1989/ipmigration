# Copyright (c) ASTRI. All rights reserved.
import argparse
from ipmigration.cell.apr.io import cfg
from ipmigration.cell.apr.tech import Tech
# %%
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


cfgs  = cfg.Cfg(args.input, args.log_level)
cfgs.load_place = False#move to cfgs later
cfgs.load_place = 'demo\cell_apr\outputs\c153\queue.csv' #make placement can be revise by designer

# cfgs.gen_cells =  ['ff', 'latch', 'scanff','clockgate']
cfgs.gen_cells =  ['ff']

tech  = Tech(cfgs)

#Support pin align creation
# if EXTRACT_PIN:
#     nl=Netlist.extract_pins(cfgs.model_file, cfgs.netlist, cfgs.output_dir)

cells = ASCell(cfgs,tech)
cells.run()


# c1 = cells['OR02D0']
# c2 = cells['DENRQ0']
# c3 = cells['DFNFQ0']
c1 = cells['DFCFB1']
r1 = c1.apr.router
d1 = c1.cdr
e1 = c1.cdr.edges_op

import shutil
source_path = r"D:\projects\ipmigration\demo\cell_apr\outputs\c153\gds\top.gds"
# 目标文件路径
target_path = r"D:\ubuntu_share\top.gds"
shutil.copy2(source_path, target_path)