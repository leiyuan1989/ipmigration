#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: leiyuan
"""

from ipmigration.cell.apr.cir.decompose import DeCKT

class StdCell:
    def __init__(self, ckt, tech, cfgs, patterns):
        self.ckt = ckt
        self.tech = tech
        self.cfgs = cfgs
        self.patterns= patterns
        
    def run(self):
        self.global_place()
    
    
    def global_place(self):
        self.de_ckt = DeCKT(self.ckt, 
                            self.patterns, 
                            self.tech.tech_name, 
                            self.cfgs.output_dir)
        self.de_ckt.run()
    
    def global_route(self):
        pass
    

    def detail_place(self):
        pass
    
    def detail_route(self):
        pass    
    
    
    
    