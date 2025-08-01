# -*- coding: utf-8 -*-
# Copyright (c) ASTRI. All rights reserved.
import argparse
from ipmigration.rule.svrf_reader import RuleFile


# Define commandline arguments.
parser = argparse.ArgumentParser(description='Parsing Calibre Rule Deck')
parser.add_argument('--tech-name',   type=str, help='technology name') 
parser.add_argument('--drc-deck' ,   type=str, help='rule deck file') #
parser.add_argument('--layer-def',   type=str, help='layer defination') 
parser.add_argument('--client-host', default= 'http://10.6.126.115:11434', type=str, help='ollama host ip')
parser.add_argument('--client-model', default= 'deepseek-r1:32b', type=str, help='ollama client mode')
parser.add_argument('--save-dir' ,   default='./demo/rule/output',         type=str, help='save dir') #
parser.add_argument('--output-mode', choices=['single', 'split'], default='single',
                    help='output mode: single=all layers in one csv, split=one layer one csv')
parser.add_argument('--debug', choices=['True', 'False'], default='True',
                    help='output debug md file')
#not necessary, for oriented rule extracted
parser.add_argument('--drs' ,    default='', type=str, help='list of design rules want to extract') 

# Parse arguments
args = parser.parse_args()

#test
drc_dir = "./demo/rule/decks/"
args.tech_name = 'c153'
args.drc_deck = drc_dir + 'c153.rul'
args.layer_def = drc_dir + 'c153_ldef.csv'


if __name__ == '__main__':
    rf = RuleFile(args)
    rf.extract_rules()
   
