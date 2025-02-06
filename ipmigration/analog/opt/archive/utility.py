# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 21:33:43 2024

@author: dsqfr
modified generate_targets: 
        add targets_min_max_type,
        if min: -1, max: 1
        targets['min_max_type']=[-1,1,1]
modified configuration:
    add modelCardPath, conerNameList
28/08/2024
"""
#This is a linux version


#move to analog database
class configuration:
    def __init__(self, CFG,\
                 undefinedNetlist_dir,\
                 definedNetlist_dir):
        self.cfg = {}
        self.cfg['ngspice'] = CFG
        self.undefinedNetlistPath = {}
        self.definedNetlistPath = {}
        self.outputFilePath ={}
        self.modelCardParth = {}
        self.cornerNameList = {}
        self.undefinedNetlistPath["undefinedNetlist_dir"] = undefinedNetlist_dir
        self.definedNetlistPath["definedNetlist_dir"] = definedNetlist_dir
    
    def setup_cfg(self, simulation_cfg, model_cfg=None):
        #simulation_cfg: list 
        #simulation_cfg=[undefinedNetlist_file, definedNetlist_file, data_filename]
        #model_cfg: list
        #model_cfg=[model_card_path, corner_name_list]
        #corner_name_list=['tt', 'ff', 'ss', 'fnsp', 'spfn']
        undefinedNetlist_file, definedNetlist_file, data_filename = simulation_cfg 
        self._generate_outputFilePath(data_filename)
        self._generate_undefinedNetlistPath(undefinedNetlist_file)
        self._generate_definedNetlistPath(definedNetlist_file)
        if model_cfg:
            model_card_path, corner_name_list=model_cfg
            self._generate_modelCardPath_and_cornerNameList(model_card_path, corner_name_list)
    def _generate_outputFilePath(self, data_filename):
        self.outputFilePath["old_data_output_filename"] = r"old_data_output_filename"
        self.outputFilePath["data_filename"] = data_filename
        self.outputFilePath["data_file_dir"] = self.definedNetlistPath["definedNetlist_dir"]
        self.outputFilePath["data_file_relatively_dir"]=r'psf'
        self.outputFilePath["data_file_path"] = self.outputFilePath["data_file_dir"]+r'/' \
                                                +self.outputFilePath["data_file_relatively_dir"]+r'/' \
                                                +self.outputFilePath["data_filename"]
    def _generate_undefinedNetlistPath(self, undefinedNetlist_file):
        self.undefinedNetlistPath["undefinedNetlist_file"] = undefinedNetlist_file
    def _generate_definedNetlistPath(self, definedNetlist_file):
        self.definedNetlistPath["definedNetlist_file"] = definedNetlist_file
    def _generate_modelCardPath_and_cornerNameList(self, model_card_path, corner_name_list):
        self.modelCardParth["model_card_path"]=model_card_path
        self.modelCardParth["dummy_model_card_path"]=r"dummy_model_card_path"
        corner_key_list=corner_name_list
        for idx in range(len(corner_key_list)):
            self.cornerNameList[corner_key_list[idx]]=corner_name_list[idx]
        self.cornerNameList["dummy_corner_name"]=r"dummy_corner_name"
        

#####################test#######
'''
import os
CFG = r'' # linux spectre version
undefinedNetlist_dir = r'./smic018/tb_template' #netlist template folder
definedNetlist_dir = r'./smic018/simResult' #defined netlist folder, namely the simulation result folder

undefinedNetlist_file=r'/template_diffamp1_ac1.sp'
definedNetlist_file=r'/test_diffamp1_ac1.sp'
data_filename=r"outac1.ac.ac"
simulation_cfg=[undefinedNetlist_file, definedNetlist_file, data_filename]
ac1_cfg=configuration(CFG, undefinedNetlist_dir, definedNetlist_dir)
ac1_cfg.setup_cfg(simulation_cfg)
print(ac1_cfg.cfg)
print(ac1_cfg.undefinedNetlistPath)
print(ac1_cfg.definedNetlistPath)
print(ac1_cfg.outputFilePath)
print(os.path.splitext(data_filename)[0])
'''
###########test boundary class ###########
'''
old_type_bounds= {'capacitance': [(0.1, 10.0)], 
         'inductance': [], 
         'resistance': [], 
         'current_source': [(5.0, 5.0)], 
         'voltage_source': [], 
         'variables': [(0.1, 10.0), (5.0, 5.0), (1, 200), (1, 200), (1, 200), (1, 200), (1, 200), (1, 200), (1, 200), (1, 200), (1, 200), (1, 200), (1, 200)], 
         'constants': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0], 
         'components': [(0.1, 10.0), (5.0, 5.0)], 
         'W_L_ratios': [(1, 200), (1, 200), (1, 200), (1, 200), (1, 200), (1, 200), (1, 200), (1, 200), (1, 200), (1, 200), (1, 200)]}

# define range for input
c_min, c_max, c_step = 0.1, 10.0, 0.1 #pF 0.1, 3.0 
r_min, r_max, r_step = 0.1, 100, 0.1 #kohm   0.1kohm, 100kohm typical range of zero resistor
ib_min, ib_max, ib_step = 5.0, 5.0, 0.1 #uA 10uA 60u 5uA

w_l_min = 1
w_l_max = 200 #1-100
w_l_step = 0.1

# define the bounds on the search
bnds = {'capacitance': [(c_min, c_max, c_step)], \
        'inductance': [], \
        'resistance': [], \
        'current_source': [(ib_min, ib_max, ib_step)],\
        'voltage_source': [],\
        'W_L_ratios': [(w_l_min, w_l_max, w_l_step), (w_l_min, w_l_max, w_l_step), (w_l_min, w_l_max, w_l_step), \
                       (w_l_min, w_l_max, w_l_step), (w_l_min, w_l_max, w_l_step), (w_l_min, w_l_max, w_l_step), \
                       (w_l_min, w_l_max, w_l_step), (w_l_min, w_l_max, w_l_step), (w_l_min, w_l_max, w_l_step), \
                       (w_l_min, w_l_max, w_l_step), (w_l_min, w_l_max, w_l_step),], \
         'lengths': [1.0, 1.0, 1.0, 1.0, 1.0, \
                     1.0, 1.0, 1.0, 1.0, 1.0, 1.0], #length
              } # class ab two stage,, #L:10, W:10, fixed w3=3.0

boundary = boundary(bnds)
bounds = boundary.bounds
print("bounds:", bounds) 
print(boundary.get_variables_range())
print(boundary.get_variables_step())
print(boundary.get_variables_upper())
print(boundary.get_normalized_variables_range())
print(boundary.get_normalized_variables_upper())
'''