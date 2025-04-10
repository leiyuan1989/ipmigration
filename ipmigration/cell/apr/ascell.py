# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 11:53:21 2024

@author: leiyuan
"""


import logging, time, os, re
import json,csv
import pandas as pd
import klayout.db as db
import matplotlib.pyplot as plt

from ipmigration.cell.apr.cir.netlist import Netlist
from ipmigration.cell.apr.cir.patterns import Patterns
from ipmigration.cell.apr.stdcell import StdCell
from ipmigration.cell.apr.io.route_loader import RouteDB

# from ipmigration.cell.apr.cir.shape import Range, Box
# from ipmigration.cell.apr.lego import lego
# from ipmigration.cell.apr.lego.channel import Channels
# from ipmigration.cell.apr.lego.layout.instance import M2_Tracks,M1_Rails
# from ipmigration.cell.apr.utils.utils import timer
# import tkinter as tk

logger = logging.getLogger(__name__)

class ASCell:
    def __init__(self, cfgs, tech):
        self.cells = {}
        self.cfgs = cfgs
        self.tech = tech
        self.tech.preprocess(cfgs)
        print('----01 Design Rule Loaded and Preprocessed!')
        #load .cdl file and process
        self.netlist = Netlist(cfgs.tech_name, cfgs.pins_align, cfgs.model_file, cfgs.netlist)
        #save ckt types 
        self.netlist.save_ckt_types(cfgs.output_dir)
        print('----02 Netlist Loaded and Classified!')
        
        self.patterns = Patterns()
        print('----03 Expertise-Library Loaded!')

        self.layout = db.Layout()
        self.db_unit = 1e-9
        self.layout_layers = {}
        for name, (num, purpose) in self.tech.output_map.items():
            self.layout_layers[name] = self.layout.layer(num, purpose, name)   
        print('----04 Layout Initialized!')


        
    def __getitem__(self,key):
        return self.cells[key]       

    

    def run(self):
        # self.time_record = {}
        # time_s = time.time()

        #clear and create aux_file
        aux_file = os.path.join(self.cfgs.output_dir,'aux_netlist.txt')
        f=open(aux_file,'w')
        f.close()
        

        
        logger.info('ascell-> Begin processing tech%s @ %s'%(self.tech.tech_name, time.asctime())) 
        if self.cfgs.gen_cells == 'all':
            self.cfgs.gen_cells = list(self.netlist.ckt_types.keys())
        
        self.route_db = RouteDB(self.tech.M1_tracks_num)
        success = []
        side_nodes_statistics = []
        
        for cell_type in self.cfgs.gen_cells:
            # print(cell_type)
            for count, ckt_name in enumerate(self.netlist.ckt_types[cell_type]):
                ckt = self.netlist[ckt_name]
                cell = StdCell(ckt,self.tech,self.cfgs,self.patterns, self.route_db)
                self.cells[ckt_name] = cell
                result = cell.run(self.layout,self.layout_layers)
                if result:
                    side_nodes_statistics+=cell.side_nodes_statistics
                    
                    success.append(cell)
                #     break
        self.success = success
        self.gen_gds()     
        statis_path = os.path.join(self.cfgs.output_dir, 'side_nodes_statistics.txt')
        save_side_nodes_statistics(statis_path, side_nodes_statistics)
   





    def run_bk(self,file, app = None):
        self.time_record = {}
        time_s = time.time()
        
        logger.info('ascell-> Begin processing tech%s @ %s'%(self.tech.tech_name, time.asctime()))
        
        self.le = lego.LEGO(self.args.pin_align_file)
        self.le.run(self.tech.tech_name, self.args.model_file, self.args.netlist)
        self.le.pass_rate()
        self.ckt_dict = self.le.ckt_dict
        # print('Fail cells:', self.le.fail_l[self.tech.tech_name])  some error here
        time_s,_ = timer(time_s, 'Circuits deconstruction use')
        
        #le.ckt_dict
        
        count = 0
        ckts_collection = {}    
        
        #for test
        if len(self.args.test_ckts) >0:
            for ckt_name,ckt in self.le.ckts_collection.items():  
                if ckt_name in self.args.test_ckts:
                    ckts_collection[ckt_name] = ckt        
        else:
            ckts_collection = self.le.ckts_collection
        
        
        for ckt_name,ckt in ckts_collection.items():
            if ckt.de:
                #TODO add process time
                logger.info('@'*60)
                logger.info('Begin processing circuit %s'%(ckt_name))
                
                if app:
                    text = 'Begin processing circuit %s \n'%(ckt_name)
                    app.text_box.insert(tk.END,  time.asctime() +'\n') 
                    app.text_box.insert(tk.END, text)   
                    app.root.update_idletasks()
                
                time_s = time.time()
                result, msg = self.apr(ckt, file)
                
                if not(result):
                    #TODO log
                    logger.info('Error 02! Circuit %s netlist cannot be APR: %s!'%(ckt_name,msg))
                else:
                    logger.info('Success! Circuit %s'%(ckt_name))
                    
                    if app:
                        text = 'Success! Circuit %s \n'%(ckt_name)
                        app.text_box.insert(tk.END,  time.asctime() +'\n') 
                        app.text_box.insert(tk.END, text)
                        
                        app.progress['value'] += 10
                        app.root.update_idletasks()
                    
                
                time_s, time_used = timer(time_s, 'Time used: ')
                self.time_record[self.tech.tech_name +'->' + ckt_name] = time_used   
            else: 
                logger.info('Error 01! Circuit %s netlist cannot be processed!'%(ckt_name))
            

        self.output_gds()
        self.data_file.close()  
   
        





    def gen_gds(self):
        self.layout.dbu = self.db_unit * 1e6 # 0.001 micro 
        # Write GDS.
        gds_file_name = 'top.gds'
        gds_out_path = os.path.join(self.cfgs.output_dir, gds_file_name)
        logger.info("Write GDS: %s", gds_out_path)
        self.layout.write(gds_out_path)        
        
        
        
def save_side_nodes_statistics(path, side_nodes_statistics):
    with open(path, 'w', encoding='utf-8') as file:
        for d in  side_nodes_statistics:
            line = '%10s->%10s\n'%(d[0],d[1])
            file.write(line)
            line = 'L: %-40s || %-40s\n'%(str(d[2]),str(d[5]))
            file.write(line)
            line = 'R: %-40s || %-40s\n'%(str(d[3]),str(d[6]))
            file.write(line)
            line = 'C: %-40s || %-40s\n'%(str(d[4]),str(d[7]))
            file.write(line)
    
# def json_to_csv(json_file_path, csv_file_path):
#     try:
#         with open(json_file_path, 'r', encoding='utf-8') as json_file:
#             data = json.load(json_file)

#         with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
#             fieldnames = ['name', 'left', 'right', 'cross']
#             writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
#             writer.writeheader()

#             for name, elements in data.items():
#                 for element in elements:
#                     left_str = ','.join(map(str, element.get('left', [])))
#                     right_str = ','.join(map(str, element.get('right', [])))
#                     cross_str = ','.join(map(str, element.get('cross', [])))
                    
#                     writer.writerow({
#                         'name': name,
#                         'left': left_str,
#                         'right': right_str,
#                         'cross': cross_str
#                     })
                    
#         print(f"Successfully converted {len(data)} modules to {csv_file_path}")
        
#     except FileNotFoundError:
#         print("Error: Specified JSON file not found")
#     except json.JSONDecodeError:
#         print("Error: Failed to parse JSON file")
#     except Exception as e:
#         print(f"An unexpected error occurred: {str(e)}")


# json_to_csv('demo\cell_apr\outputs\c110\side_nodes_statistics.json', 'demo\cell_apr\outputs\c110\side_nodes_statistics.csv')
