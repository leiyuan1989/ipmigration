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

'''
TODO: Need a global analysis of poly arrangement

'''



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


        self.aux_file = os.path.join(cfgs.output_dir,'01_DEC_REPORT_%s.txt'%(time.strftime('%m_%d_%H')))
        self.place_file = os.path.join(cfgs.output_dir,'02_PLACE_REPORT_%s.csv'%(time.strftime('%m_%d_%H')))
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
        report_data = []
        
        for cell_type in self.cfgs.gen_cells:
            for count, ckt_name in enumerate(self.netlist.ckt_types[cell_type]):
                start_time = time.time() 
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

                run_time = time.time() - start_time
                if result:
                    out_msg = 'Success'
                else:
                    out_msg = 'Fail'
                if cell_type in  ['ff'       ,'scanff'   ,'latch'     ,'clockgate']:
                    ckt_t = 'Sequential Logic'
                else:
                    ckt_t = 'Combinational Logic'
                
                report_data.append([ckt_name,ckt_t, str(len(ckt.devices)), out_msg,msg,'%0.3f s'%run_time]) 
                # print('test1:',ckt_name,ckt_t,out_msg,msg,'%0.3f s'%run_time)
                
                # break
            # break
                        
        self.success = success
        self.fail = fail
        print('Pass Rate: %d/%d, %.2f%%'%(len(success),len(fail),len(success)*100/(len(fail)+len(success))))
        self.report(report_data)
        self.count_patterns(success)
        self.gen_gds()     

    def report(self,report_data):
        file = os.path.join(self.cfgs.output_dir,'final_report.csv')
        columns = ['cell', 'type', 'devices_num', 'result', 'message', 'time']
        df = pd.DataFrame(report_data, columns=columns)
        df.to_csv(file, index=True)

        

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
        
