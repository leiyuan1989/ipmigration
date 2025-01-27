#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 16:07:33 2024

@author: shunqidai

setup modelcard path, testbench template folder and simulation result folder
"""



###############define SPICE simulator##########################
r'''
#CFG = r'..\..\\ngspice-41_64\Spice64\bin\ngspice_con' #SPICE simulator path, not use in linux version
#CFG = r'ngspice' # linux version
'''
circuit_simulator_path = r'' # linux spectre version

##############setting csv file path####################
setting_file_path=r'./setting.csv' 


#############SMIC 180nm Technology  smic018#################
########define work folder##########################
netlist_template_folder_dir = r'./smic018/tb_template' #netlist template folder
defined_netlist_folder_dir = r'./smic018/simResult' #defined netlist folder

######### define model card ################
model_card_path=r"/home/shunqidai/Sizing/SizingDemoLinuxSpectre_integer_stdcell/smic018/models/spectre/ms018_v1p7_spe.lib"


#############SMIC 110nm Technology    smic011#################
########define work folder##########################
#netlist_template_folder_dir = r'./smic011/tb_template' #netlist template folder
#defined_netlist_folder_dir = r'./smic011/simResult' #defined netlist folder

######### define model card ################
#model_card_path=r"/home/shunqidai/Sizing/SizingDemoLinuxSpectre_integer_stdcell/smic011/models/spectre/ms011_ms013s_io33_v1p24_spe.lib"



#############SMIC 40nm Technology    smic40#################
########define work folder##########################
#netlist_template_folder_dir = r'./smic40/tb_template' #netlist template folder
#defined_netlist_folder_dir = r'./smic40/simResult' #defined netlist folder

######### define model card ################
#model_card_path=r"/home/shunqidai/Sizing/SizingDemoLinuxSpectre_integer_stdcell/smic40/models/spectre/l0040ll_v1p4_1r_spe.lib"


