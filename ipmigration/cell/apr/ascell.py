# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 11:53:21 2024

@author: leiyuan
"""

import logging, time, os
import pandas as pd
from collections import defaultdict
import klayout.db as db
import matplotlib.pyplot as plt

from ipmigration.cell.apr.cir.netlist import Netlist
from ipmigration.cell.apr.cir.patterns import Patterns
from ipmigration.cell.apr.stdcell import StdCell
from ipmigration.cell.apr.io.route_loader import RouteDB

logger = logging.getLogger(__name__)
DEBUG = True

class ASCell:
    def __init__(self, cfgs, tech):
        self.cells = {}
        self.cfgs = cfgs
        self.tech = tech
        self.tech.preprocess(cfgs)
        print('----01 Design Rule Loaded and Preprocessed!')
        #load .cdl file and process
        self.netlist = Netlist(cfgs.tech_name, cfgs.pins_align, cfgs.model_file, cfgs.netlist)
        #save ckt types 
        self.netlist.save_ckt_types(cfgs.output_dir)
        print('----02 Netlist Loaded and Classified!')
        self.patterns = Patterns()
        print('----03 Expertise-Library Loaded!')
        self.initialize_layout()
        print('----04 Layout Initialized!')


        self.aux_file = os.path.join(cfgs.output_dir,'DEC_REPORT_%s.txt'%(time.strftime('%m_%d_%H')))
        self.place_file = os.path.join(cfgs.output_dir,'PLACE_REPORT_%s.csv'%(time.strftime('%m_%d_%H')))
        #clear previous data
        f = open(self.aux_file,'w')
        f.close()
        
        if cfgs.load_place:
            df = pd.read_csv(cfgs.load_place)
            self.place_file = {}
            for i,r in df.iterrows():
                l1 = [t.strip() for t in r.tolist()]
                l2= []
                for e in l1:
                    if e =='NA':
                        break
                    l2.append(e)
                self.place_file[l2[0]] = l2[1:]
            
        else:
            f = open(self.place_file,'w')
            line = '%-10s,'%('name')
            for i in range(10):
                line += '%-30s,'%('cb%d'%(i+1))
            f.write(line[:-1]+'\n')
            f.close()
        
        

    def __getitem__(self,key):
        return self.cells[key]       

    def initialize_layout(self):
        self.layout = db.Layout()
        self.db_unit = 1e-9
        self.layout_layers = {}
        for name, (num, purpose) in self.tech.output_map.items():
            self.layout_layers[name] = self.layout.layer(num, purpose, name)   




    def run(self):
        logger.info('ascell-> Begin processing tech%s @ %s'%(self.tech.tech_name, time.asctime())) 
        if self.cfgs.gen_cells == 'all':
            self.cfgs.gen_cells = list(self.netlist.ckt_types.keys())
        
        self.route_db = RouteDB(self.tech.M1_tracks_num)
        success = []
        fail = []
        # side_nodes_statistics = []
        
        for cell_type in self.cfgs.gen_cells:
            for count, ckt_name in enumerate(self.netlist.ckt_types[cell_type]):
                
                ckt = self.netlist[ckt_name]
                cell = StdCell(ckt,self.tech,self.cfgs,self.patterns, self.route_db, self.aux_file, self.place_file)
                self.cells[ckt_name] = cell
                if DEBUG:
                    result,msg = cell.run(self.layout,self.layout_layers)
                    if result:          
                        success.append(cell)
                    else:
                        fail.append([cell,msg])                    

                else:
                    try:
                        result,msg = cell.run(self.layout,self.layout_layers)
                        if result:          
                            success.append(cell)
                        else:
                            fail.append([cell,msg])
                    except:
                        print(cell.name,'run failed')
                        fail.append([cell,'run failed'])
                # break
            break
                        
        self.success = success
        self.fail = fail
        print('Pass Rate: %d/%d, %.2f%%'%(len(success),len(fail),len(success)*100/(len(fail)+len(success))))
        self.count_patterns(success)
        
        
        
        self.gen_gds()     


    def count_patterns(self,success):
        counter = defaultdict(int)
        nested_list = [[v.ckt.name for k,v in t.de_ckt.sub_ckts.items() ] for t in success]
        for sub_list in nested_list:
            for element in sub_list:
                counter[element] += 1
        print("Element occurrence counts:")
        for element, count in dict(counter).items():
            print(f"{element}: {count} times") 


    def gen_gds(self):
        #merge
        layout = self.layout
        work_layer = layout.layer()
        for li in layout.layer_indexes():
          for ci in layout.each_top_cell():
             c=layout.cell(ci)
             mergeReg = db.Region(c.begin_shapes_rec(li))
             mergeReg.merge()
             c.shapes(work_layer).insert(mergeReg)
          layout.clear_layer(li)   # clears all cells
          layout.swap_layers(li, work_layer)     # move work_layer in place of the layer li
        #end merge
        
        self.layout.dbu = self.db_unit * 1e6 # 0.001 micro 
        # Write GDS.
        gds_file_name = 'top.gds'
        gds_out_path = os.path.join(self.cfgs.output_dir, gds_file_name)
        logger.info("Write GDS: %s", gds_out_path)
        self.layout.write(gds_out_path)        
        

        
# def save_side_nodes_statistics(path, side_nodes_statistics):
#     with open(path, 'w', encoding='utf-8') as file:
#         for d in  side_nodes_statistics:
#             line = '%10s->%10s\n'%(d[0],d[1])
#             file.write(line)
#             line = 'L: %-40s || %-40s\n'%(str(d[2]),str(d[5]))
#             file.write(line)
#             line = 'R: %-40s || %-40s\n'%(str(d[3]),str(d[6]))
#             file.write(line)
#             line = 'C: %-40s || %-40s\n'%(str(d[4]),str(d[7]))
#             file.write(line)
