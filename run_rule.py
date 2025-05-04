# -*- coding: utf-8 -*-
# Copyright (c) ASTRI. All rights reserved.
import json
import logging
import argparse
from ipmigration.rule.svrf_reader import RuleFile

logger = logging.getLogger(__name__)
# Define commandline arguments.
parser = argparse.ArgumentParser(description='Parsing Calibre Rule Deck')
parser.add_argument('--tech-name',   type=str, help='technology name') 
parser.add_argument('--drc-deck' ,   type=str, help='rule deck file') #
parser.add_argument('--layer-def',   type=str, help='layer defination') #will extract all rules of layers in defined in this file
parser.add_argument('--client-host', default= 'http://10.6.126.115:11434', type=str, help='ollama host ip')
parser.add_argument('--save-dir' ,   default='./demo/rule/output',         type=str, help='save dir') #
parser.add_argument('--log-level',   default='INFO',                       type=str, help='logging level') 
#not necessary, for oriented rule extracted
parser.add_argument('--drs' ,    default='', type=str, help='list of design rules want to extract') 

# Parse arguments
args = parser.parse_args()



'''
test llm
https://platform.deepseek.com/usage
https://platform.moonshot.cn/docs/guide

test rule
python run_rule.py --tech-name s40   --drc-deck ./demo/rule/decks/s40.drc
python run_rule.py --tech-name c153  --drc-deck ./demo/rule/decks/c153.rul
python run_rule.py --tech-name s65   --drc-deck ./demo/rule/decks/s65.drc
python run_rule.py --tech-name s110  --drc-deck ./demo/rule/decks/s110.drc
python run_rule.py --tech-name t40   --drc-deck ./demo/rule/decks/t40_calibre.drc
python run_rule.py --tech-name t65   --drc-deck ./demo/rule/decks/t65_calibre.drc
python run_rule.py --tech-name xx55 --drc-deck ./demo/rule/decks/XXXX_CalDRC_55LLULPGE_0912182533_REV0_5.drc

'''
if __name__ == '__main__':

    
    #for test
    tbs = [
            ['c153','./demo/rule/decks/c153.rul'      ,'./demo/rule/decks/c153_ldef.csv'],
            # ['s40','./demo/rule/decks/s40.drc'        ,'./demo/rule/decks/s40_ldef.csv'],
            # ['s65','./demo/rule/decks/s65.drc'        ,'./demo/rule/decks/s65_ldef.csv'],
            # ['s110','./demo/rule/decks/s110.drc'      ,'./demo/rule/decks/s110_ldef.csv'],
            # ['t40','./demo/rule/decks/t40_calibre.drc','./demo/rule/decks/t40_ldef.csv'],
            # ['t65','./demo/rule/decks/t65_calibre.drc','./demo/rule/decks/t65_ldef.csv'],
            
        ]
            
    for tb in tbs:
        tech_name,drc_deck,layer_def = tb
        rf = RuleFile(tech_name, 
                      drc_deck, 
                      layer_def, 
                      args.client_host,
                      args.save_dir, 
                      args.drs, 
                      args.log_level)
        rf.extract_rules()

# def deck_reader(args):
#     print('Begin processing %s'%(args.drc_deck))
#     #You can uncomment this if you want to search a llm, but deepseek is not stable now
#     # llm_apis = API.search_available_llm(json.load(open(args.llm_apis,'r')))
#     llm_apis=['moonshot']
#     # llm_apis=['deepseek']
#     if len(llm_apis)>0:
#         name = llm_apis[0]
#         api=json.load(open(args.llm_apis,'r'))[name]['api']
#         llm_api = API(name, api)
        
        
#         rf = RuleFile(args.tech_name, args.drc_deck, args.save_dir, 
#                        args.layer_align, args.dr_list, args.kws, args.log_level,llm_api)
        
#         #if dr_template or not
        
#         rf.extract_rules()
#         # print('Finish processing %s, extracted design rule file is %s'%(args.drc_deck, rf.extracted_file))
#     else:
#         raise ValueError('No llm is available')


# if __name__ == '__main__':
#     deck_reader(args)
