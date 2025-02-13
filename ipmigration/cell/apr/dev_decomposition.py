# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 20:17:18 2024
"""

#develop decomposition


import time

from src.schematic.circuits import Circuits 
from src.schematic.deconstruction import Deconstruction
from src.schematic.patterns import Patterns
from src.schematic.graph import MosGraph,graph_show

from src.schematic.placement import Placement





# cell_data_list_file = 'data/dev/cell_pin.xlsx'
# df_cellpin = pd.read_excel(cell_data_list_file)

pin_align_file = 'data/pin_align.csv'
tech_list = ['c153','c110','s65','s110']
type_dict =  {'_latch':'latch','_dff':'flipflop','_sdff':'scan_flipflop'}    
type_list =  ['_latch','_dff','_sdff']    


# type_list =  ['_dff']   
# tech_list = ['s110']
data = {}


patterns = Patterns()
# chains = InputChain('src/schematic/pattern_cdl/input.chain')
# log = {}

# ml  = 'src/lego/schematic/components/model.cdl'
# nl1 = 'src/lego/schematic/components/structures.cdl'
# nl2 = 'src/lego/schematic/components/input.cdl'
# # nl3 = 'src/lego/schematic/components/output.cdl'
# struct_dict = {}
# struct_g_dict = {}
# pdk_lib, ckt_dict = Circuits.load_netlist(ml, nl1)
# struct_dict.update(ckt_dict)
# pdk_lib, ckt_dict = Circuits.load_netlist(ml, nl2)
# struct_dict.update(ckt_dict)
# # pdk_lib, ckt_dict = Circuits.load_netlist(ml, nl3)
# # struct_dict.update(ckt_dict)

# for k,v in struct_dict.items():
#     struct_g_dict[k] =  MosGraph(v)


log = open('log.txt','w')



total = 0 
found =  0 
nofound = 0 
partfound = 0
fail_list = []

ckt_type_list = []


for tp in type_list:
    data[tp] = {}
    print(time.asctime(),'\n##### Cell Type: %s #####  \n'%(tp))
    for tech in tech_list:     
        print('-----------------',tech,'-----------------')
        model_cdl = 'data/dev/%s/ascell/model.cdl'%(tech)
        file = '/%s%s.cdl'%(tech,tp) 
        netlist_cdl = 'data/cdl' + file     
        print(netlist_cdl)
        ckts = Circuits(tech, pin_align_file, model_cdl, netlist_cdl)
        
        for ckt_name,ckt in ckts.ckt_dict.items():
            g = MosGraph(ckt)
            p1 = Placement(ckt,  ckts,  tech, log)
            t1 = p1.place_sl(patterns)
# 
            # raise ValueError            

            ckt_type_list.append(p1.ckt_dc.ckt_type['input_type'])
            total += 1
            if t1:
                found += 1 
            else:
                fail_list.append([tech,ckt_name ])
                nofound += 1
                
            if ckt_name == 'DFBFB1':
                k1 = p1
            
            # line = tech + ' ' + ckt_name + ' : '
            # for struct,struct_g in struct_g_dict.items():
            #     matches = g.find_subgraph_matches(struct_g)
            #     t1 = len(matches)
            #     if t1>0:
            #         line += ' %s : %d, '%(struct,t1)
            # line += '\n'
            # file_.write(line)
            
            # print(ckt_name)
            # graph_show(g)
            
            
            
        data[tp][tech] = [ckts]

log.close()
        
print('Total %d, success %d, fail %d'%(total,found,nofound))    

type_set =  list(set(ckt_type_list))
type_set.sort()
for t in type_set:
    print('Type %s: %d'%(str(t), ckt_type_list.count(t)))



# from src.schematic.chain import Chain

# ch = Chain()
# ch.load_from_pattern(c1.sub_ckts['cross1'])






# file_.close()

# cs1 = data['_latch']['c110'][0]
        
# le.pass_rate()
 

# model_cdl = 'data/cdl/test/s110_model.cdl'
# netlist_cdl = 'data/cdl/test/s110_netlist.cdl'

# le_dev = lego.LEGO(pin_align_file)
# le_dev.run('s110', model_cdl, netlist_cdl)
# print(time.asctime(),'\n##### Cell Type: s110 #####  \n')
# le_dev.pass_rate()


# from src.lego.graph import StructGraph 
# name = 'DFFNSRHX1MTR'
# c1 = le_dev.ckt_dict[name] 
# g1 = StructGraph(c1.devices)

# for i,r in le_dev.structs_db.df.iterrows():
#     s = le_dev.structs_db.ckt_dict[i]
#     g2 = StructGraph(s.devices)
#     matches = g1.find_subgraph_matches(g2)
    
#     print(s,matches)


# test
# model_cdl = 'data/cdl/test/x180_model.cdl'
# netlist_cdl = 'data/cdl/test/x180_netlist.cdl'

# le_test = lego.LEGO(pin_align_file)
# le_test.run('x180', model_cdl, netlist_cdl)
# print(time.asctime(),'\n##### Cell Type: x180 #####  \n')
# le_test.pass_rate()




    

