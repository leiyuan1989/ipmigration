# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 17:57:54 2024

@author: leiyuan
"""

from src.basic.basic import PMos4, NMos4, Pin


support_model_types = ['PMOS4','NMOS4','PIN']

class PDK_Model:
    def __init__(self, name, parameters={}):
        self.name = name
        self.parameters= parameters
        assert name in support_model_types
        
        if name == 'PMOS4':
            self.model = PMos4
            # self.pins = PMos4.pins()
        elif name == 'NMOS4':
            self.model = NMos4
            # self.pins = NMos4.pins()
        elif name == 'PIN':
            self.model = Pin  
        
        else:
            raise ValueError('Model type not supported')
        
        
    
