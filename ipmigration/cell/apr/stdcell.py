#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: leiyuan
"""

from ipmigration.cell.apr.cir.decompose import DeCKT
from ipmigration.cell.apr.pr.pattern_apr import PatternAPR
from ipmigration.cell.apr.lyt.cell_drawer import CellDrawer
# from ipmigration.cell.apr.cir.patterns import PatternRouter,PatternDrawer

class StdCell:
    def __init__(self, ckt, tech, cfgs, patterns,route_db,aux_file,place_file):
        self.name = ckt.name
        self.ckt = ckt
        self.tech = tech
        self.cfgs = cfgs
        self.patterns= patterns
        self.route_path = []
        self.route_db = route_db
        self.aux_file = aux_file
        self.place_file = place_file
        self.load_place = cfgs.load_place
        
        
    def run(self,top_layout,db_layers):
        result,msg = self.global_pr()
        if result:
            result,msg  = self.detail_pr(top_layout,db_layers)

        return result,msg
    
    def init_layout(self,top_layout,db_layers):
        self.db_layout = top_layout.create_cell(self.ckt.name)
        self.db_shapes = {}
        for name in db_layers:
            self.db_shapes[name] = self.db_layout.shapes(db_layers[name]) 
    
    def global_pr(self):
        print(' %s Global_PR:'%(self.ckt.name))
        #1. decompose
        self.ckt.combine_parallel()
        self.de_ckt = DeCKT(self.ckt, 
                            self.patterns, 
                            self.tech.tech_name, 
                            self.cfgs.output_dir,
                            self.aux_file)
        dec_result = self.de_ckt.run()
        
        if not(dec_result):
            print('-----Decompose Failed----')
            return 0, "Decompose Failed"   
        
        
        #2. apr
        self.apr = PatternAPR(self.ckt, self.de_ckt.sub_ckts, self.place_file, 6 , self.load_place)
        apr_result = self.apr.run()         
            
        if not(apr_result):
            return 0, "Pattern APR Failed" 

        return 1, "Success"
    

    
    def detail_pr(self,top_layout,db_layers):
        #init db layout and cell and shapes of cell, then we can use insert function.        
        self.init_layout(top_layout,db_layers)
        #begin layout draw, if not success (width is too large), fold and re-grobal pr
        self.cdr = CellDrawer(self)
        result = self.cdr.run()

        if result:
            return 1,"Success"
        else:
            #process debug (widths too large)
            return 0, 'Detail APR Failed'
            


    









                   
                   
