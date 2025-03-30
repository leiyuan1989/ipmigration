# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 11:53:21 2024

@author: leiyuan
"""


import logging, time, os, re
import json
import pandas as pd
import klayout.db as db
import matplotlib.pyplot as plt

from ipmigration.cell.apr.cir.netlist import Netlist
from ipmigration.cell.apr.cir.patterns import Patterns
from ipmigration.cell.apr.stdcell import StdCell


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
            
        
        #initial layout settings
        # self.init_layout()
        
        
        
        
        
        # self.tech_dir = args.tech_dir     
        # self.read_cell_para()
        # self.init_layout()
        # self.data_file = open(os.path.join(args.output_dir,'data_%s.txt'%(self.tech.tech_name)),'w')

        # #TODO
        # self.ready_structs = ready_structs()
        #init placer and router
        #set placer
        # self.placer = SMTPlacer(False, os.path.join(args.output_dir))
        # self.router = HybridRouter
        
        #load lego library here
        
    def run(self):
        # self.time_record = {}
        # time_s = time.time()

        #clear and create aux_file
        aux_file = os.path.join(self.cfgs.output_dir,'aux_netlist.txt')
        f=open(aux_file,'w')
        f.close()
        
        #route_data
        route_data_path = os.path.join(self.cfgs.output_dir,'route_data_%d.json'%(self.tech.M1_tracks_num))
        
        logger.info('ascell-> Begin processing tech%s @ %s'%(self.tech.tech_name, time.asctime())) 
        if self.cfgs.gen_cells == 'all':
            self.cfgs.gen_cells = list(self.netlist.ckt_types.keys())

        success = []
        for cell_type in self.cfgs.gen_cells:
            # print(cell_type)
            for count, ckt_name in enumerate(self.netlist.ckt_types[cell_type]):
                ckt = self.netlist[ckt_name]
                cell = StdCell(ckt,self.tech,self.cfgs,self.patterns,route_data_path)
                self.cells[ckt_name] = cell
                result = cell.run()
                if result:
                    success.append(cell)
                #     break
        self.success = success
        self.gen_gds()        

   





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
        
        
        
        
        

    