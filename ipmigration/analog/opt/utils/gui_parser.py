#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 22:02:24 2025

@author: leiyuan

will deprecated 
"""

import os

class GuiParser:
    #shared by gui parsers
    logFolder = ''
    modelCardFile = ''
    settingFile = ''
    netlistFolder = ''
    optNetlistFolder = ''
    optField = ''
    generationField = 0
    populationField = 0
    offspringField = 0
    def __init__(self, file):
        assert os.path.exists(file)
        with open(file,'r') as f:
            lines = [t.strip() for t in f.readlines()]
            
        GuiParser.logFolder = lines[0]
        GuiParser.modelCardFile = lines[1]
        GuiParser.settingFile = lines[2]
        GuiParser.netlistFolder = lines[3]
        GuiParser.optNetlistFolder = lines[4]
        GuiParser.optField = lines[5]
        GuiParser.generationField = int(lines[6])
        GuiParser.populationField = int(lines[7])
        GuiParser.offspringField = int(lines[8])
        
        self.num_generation  = GuiParser.generationField 
        self.population_size = GuiParser.populationField 
        self.num_offsprings  = GuiParser.offspringField 
        self.optimizer_type = GuiParser.optField 