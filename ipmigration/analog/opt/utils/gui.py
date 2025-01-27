#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 22:02:24 2025

@author: leiyuan

will deprecated 
"""

import os

def gui_parser(file):

    #default value
    logFolder = ''
    modelCardFile = ''
    settingFile = ''
    netlistFolder = ''
    optNetlistFolder = ''
    optField = ''
    generationField = 0
    populationField = 0
    offspringField = 0
    
    assert os.path.exists(file)
    with open(file,'r') as f:
        lines = [t.strip() for t in f.readlines()]
        
    log_folder = lines[0]
    modelcard_file = lines[1]
    setting_file = lines[2]
    netlistFolder = lines[3]
    optNetlistFolder = lines[4]
    optField = lines[5]
    generationField = int(lines[6])
    populationField = int(lines[7])
    offspringField = int(lines[8])
    
    return log_folder, modelcard_file