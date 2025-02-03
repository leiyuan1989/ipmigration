# Copyright (c) ASTRI. All rights reserved.
import logging
import argparse
from svrf_reader import RuleFile



logger = logging.getLogger(__name__)
# Define commandline arguments.
parser = argparse.ArgumentParser(description='Parsing Calibre Rule Deck')
parser.add_argument('--tech-name', default='s40',     type=str,   help='technology name') #
parser.add_argument('--drc-deck' , default='example/rule/s40.drc', type=str,   help='technology dir') #
parser.add_argument('--layer_align', default='tech_align.csv',   type=str, help='layer alignment') #
parser.add_argument('--save-dir' ,   default='./output',              type=str, help='save dir') #
parser.add_argument('--log_level',   default='DEBUG',                 type=str, help='logging level: INFO, DEBUG or FATAL') #

#not necessary
parser.add_argument('--kws',        default='data/dr_kws.csv',       type=str,   help='key words') 
parser.add_argument('--dr_list' ,    default='data/dr_template.xlsx', type=str, help='list of design rules') 




# Parse arguments
args = parser.parse_args()



def deck_reader():
    print('Begin processing %s'%(args.drc_deck))
    rf = RuleFile(args.tech_name, args.drc_deck, args.save_dir, 
                   args.layer_align, args.dr_list, args.kws, args.log_level)
    rf.extract_rules()
    print('Finish processing %s, extracted design rule file is %s'%(args.drc_deck, rf.extracted_file))

if __name__ == '__main__':
    deck_reader()

        
