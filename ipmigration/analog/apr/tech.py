# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 14:45:48 2024

@author: leiyuan
"""

#tech 
import os
import logging
import pandas as pd

class Tech(object):
    def __init__(self, tech_name, dr_csv, layer_csv):
        self.tech_name = tech_name
        self._init_layer_name()
        self._read_layer(layer_csv)           
        self._read_drc(dr_csv)


    def _init_layer_name(self):
        self.NW = 'NW' 
        self.AA = 'AA'
        self.GT = 'GT'
        self.SP = 'SP'
        self.SN = 'SN'
        self.CT = 'CT'
        self.M1 = 'M1'
        self.V1 = 'V1'
        self.M2 = 'M2'
        self.V2 = 'V2'
        self.M3 = 'M3'
        self.V3 = 'V3'
        self.M4 = 'M4'
        self.V4 = 'V4'
        self.M5 = 'M5'
        self.V5 = 'V5'
        self.M6 = 'M6'
        self.M1_Pin = 'M1Pin'
        self.M2_Pin = 'M2Pin'
        self.M3_Pin = 'M3Pin'
        self.M4_Pin = 'M4Pin'
        self.M5_Pin = 'M5Pin'
        self.M6_Pin = 'M6Pin'        
        self.TXT ='TXT'

        self.layer_list = [self.NW, self.AA, self.GT, self.SP, self.SN, self.CT, 
                           self.M1, self.V1, self.M2, self.V2, self.M3, self.V3,
                           self.M4, self.V4, self.M5, self.V5, self.M6, self.TXT,
                           self.M1_Pin, self.M2_Pin, self.M3_Pin,
                           self.M4_Pin, self.M5_Pin, self.M6_Pin]

       
        
       
        
       
    def _read_layer(self, layer_file):
        assert os.path.exists(layer_file), "layer file is not exist"
        df = pd.read_csv(layer_file)
        df.columns = df.columns.str.strip()
        for col in ['layer', 'layer_name', 'layer_purpose']:
            df[col] = df[col].str.strip()
        self.layer={}
        for _, row in df.iterrows():
            self.layer[row['layer']] = [row['layer_name'],row['layer_purpose']]



    def _read_drc(self,dr_file):
        df = pd.read_csv(dr_file)
        df.columns = df.columns.str.strip()
        for col in ['name', 'type', 'note']:
            df[col] = df[col].str.strip().fillna('')
        self.drs=df
        for _, row in df.iterrows():
            setattr(self, row['name'], row['value'])

    def _read_setting(self, set_file):
        assert os.path.exists(set_file), "setting file is not exist"
        df = pd.read_csv(set_file)
        df.columns = df.columns.str.strip()
        for col in ['name', 'value', 'note']:
            df[col] = df[col].str.strip()
        self.layer={}
        for _, row in df.iterrows():
            self.layer[row['layer']] = [row['layer_name'],row['layer_purpose']]

    
    
    

#test
if __name__ == "__main__" :
    dr_file = 'data/dr.csv'
    layer_file = 'data/layer.csv'    
    tech = Tech('t180', dr_file, layer_file)