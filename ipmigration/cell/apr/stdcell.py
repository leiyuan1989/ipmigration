#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: leiyuan
"""

from ipmigration.cell.apr.cir.decompose import DeCKT
from ipmigration.cell.apr.pr.pattern_placer import Placer


class StdCell:
    def __init__(self, ckt, tech, cfgs, patterns):
        self.ckt = ckt
        self.tech = tech
        self.cfgs = cfgs
        self.patterns= patterns
        
    def run(self):
        self.init_layout(x)
        self.global_place()
    
    def init_layout(self, x):
        pass
    
    def global_place(self):
        self.ckt.combine_parallel()
        self.de_ckt = DeCKT(self.ckt, 
                            self.patterns, 
                            self.tech.tech_name, 
                            self.cfgs.output_dir)
        result = self.de_ckt.run()

        if result:
            print('Success: ', self.ckt.name)
            pat_placer = Placer(self.de_ckt.sub_ckts)
            queue = pat_placer.find_opt_perm(self.ckt.ckt_type)
            
            #auto-folding
            
            
            
            # self.pat_placer = pat_placer
            self.queue = queue
        else:
            print('Fail: ', self.ckt.name)
        
        
        
    
    
    
    def global_route(self):
        pass
    

    def detail_place(self):
        pass
    
    def detail_route(self):
        pass    
    
    
    
    