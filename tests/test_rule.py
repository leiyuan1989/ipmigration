# -*- coding: utf-8 -*-
"""
@author: leiyuan
"""
import argparse
from ipmigration.rule.svrf_reader import RuleFile

# Define commandline arguments.
parser = argparse.ArgumentParser(description='Parsing Calibre Rule Deck')
args = parser.parse_args()

files = {
          'c153':'resources/drc_decks/c153.rul',
          's40' :'resources/drc_decks/s40.drc',
          's65' :'resources/drc_decks/s65.drc',
          's110':'resources/drc_decks/s110.drc',
          't40' :'resources/drc_decks/t40_calibre.drc',
          't65' :'resources/drc_decks/t65_calibre.drc',         
          'xx55':'resources/drc_decks/XXXX_CalDRC_55LLULPGE_0912182533_REV0_5.drc'
         }

args.dr_list     = 'ipmigration/rule/configs/dr_template.xlsx'
args.layer_align = 'ipmigration/rule/configs/tech_align.csv'
args.kws         = 'ipmigration/rule/configs/dr_kws.csv'
args.save_dir    = './output'
args.log_level   = 'DEBUG'

for tech_name,cal_file in files.items():
    args.tech_name = tech_name
    args.cal_file = cal_file

    print('*****%s*****'%(cal_file))
    
    rf = RuleFile(args.tech_name, args.cal_file, args.save_dir, 
                  args.layer_align, args.dr_list, args.kws, args.log_level)
    
    rf.extract_rules()
    
    
