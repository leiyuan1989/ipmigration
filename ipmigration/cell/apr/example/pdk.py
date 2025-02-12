# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 17:57:54 2024

@author: leiyuan
"""

from basic import PMos4, NMos4, Pin

# import json

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
        
        
    

# class PDK_Lib():
#     def __init__(self, model_file):
#         models = None
#         if pdk_models:
#             models = pdk_models()
        
#         elif loadbuiltins:
#             models = self.default_models()
        
#         if models:
#             with set_context(self):
#                 for m in models:
#                     self.append(m)

#     def find(self, name):
#         return next((x for x in self if x.name == name.upper()), None)

#     def append(self, item):
#         assert not self.find(item.name), f'Duplicate model/subcircuit name {item.name} New: {item}, Existing: {self.find(item.name)}'
#         self.__root__.append(item)

#     def preview(self):
#         return [x.name for x in self]



#     def default_models(self):
#         models = list()
#         models.append(
#             Model(
#                 name='NMOS',
#                 pins=['D', 'G', 'S', 'B'],
#                 parameters={
#                     'W': 0,
#                     'L': 0,
#                     'NFIN': 1,
#                     'NF': 2,
#                     'M': 1,
#                     'PARALLEL': 1,  # Internal attribute used for parallel and stacked devices
#                     'STACK': 1},
#                 prefix=''
#             )
#         )
#         models.append(
#             Model(
#                 name='PMOS',
#                 pins=['D', 'G', 'S', 'B'],
#                 parameters={
#                     'W': 0,
#                     'L': 0,
#                     'NFIN': 1,
#                     'NF': 2,
#                     'M': 1,
#                     'PARALLEL': 1,  # Internal attribute used for parallel and stacked devices
#                     'STACK': 1},
#                 prefix=''
#             )
#         )
#         models.append(
#             Model(
#                 name='CAP',
#                 pins=['PLUS', 'MINUS'],
#                 parameters={
#                     'VALUE': 0,
#                     'PARALLEL': 1,
#                     'STACK': 1
#                 },
#                 prefix='C'
#             )
#         )
#         models.append(
#             Model(
#                 name='RES',
#                 pins=['PLUS', 'MINUS'],
#                 parameters={
#                     'VALUE': 0,
#                     'PARALLEL': 1,
#                     'STACK': 1
#                 },
#                 prefix='R'
#             )
#         )
#         models.append(
#             Model(
#                 name='IND',
#                 pins=['PLUS', 'MINUS'],
#                 parameters={
#                     'VALUE': 0,
#                     'PARALLEL': 1,
#                     'STACK': 1
#                 },
#                 prefix='L'
#             )
#         )
#         return models


# def read_lib_json(json_file_path):
#     with open(json_file_path, "r") as f:
#         data = json.load(f)
#     library = Library(loadbuiltins=False)
#     with set_context(library):
#         for x in data:
#             if 'generator' in x:
#                 library.append(SubCircuit(**{k: v for k, v in x.items() if v}))
#             else:
#                 library.append(Model(**{k: v for k, v in x.items() if v and not k=='base'}))
#     return library
