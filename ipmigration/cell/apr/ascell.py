# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 11:53:21 2024

@author: leiyuan
"""


import logging, time, os, re
import json
import pandas as pd
import klayout.db as db
import matplotlib.pyplot as plt

from ipmigration.cell.apr.cir.netlist import Netlist
from ipmigration.cell.apr.cir.patterns import Patterns


from ipmigration.cell.apr.stdcell import StdCell


# from ipmigration.cell.apr.cir.shape import Range, Box
# from ipmigration.cell.apr.lego import lego
# from ipmigration.cell.apr.lego.channel import Channels
# from ipmigration.cell.apr.lego.layout.instance import M2_Tracks,M1_Rails
# from ipmigration.cell.apr.utils.utils import timer
# import tkinter as tk

#ascell
logger = logging.getLogger(__name__)


class ASCell:
    def __init__(self, cfgs, tech):
        '''
        Parameters
        ----------
        tech : TYPE
            DESCRIPTION.
        Returns
        -------
        None.
        '''
        
        self.cells = {}
        self.cfgs = cfgs
        self.tech = tech
        self.tech.pre_cal()
        print('01 Design Rule Loaded and Preprocessed!')
        #load .cdl file and process
        self.netlist = Netlist(cfgs.tech_name, cfgs.pins_align, cfgs.model_file, cfgs.netlist)
        #save ckt types 
        self.netlist.save_ckt_types(cfgs.output_dir)
        print('02 Netlist Loaded and Classified!')
        self.patterns = Patterns()
        print('03 Expertise-Library Loaded!')
        
        #load patterns
        
        
            
        
        #initial layout settings
        # self.init_layout()
        
        
        
        
        
        # self.tech_dir = args.tech_dir     
        # self.read_cell_para()
        # self.init_layout()
        # self.data_file = open(os.path.join(args.output_dir,'data_%s.txt'%(self.tech.tech_name)),'w')

        # #TODO
        # self.ready_structs = ready_structs()
        #init placer and router
        #set placer
        # self.placer = SMTPlacer(False, os.path.join(args.output_dir))
        # self.router = HybridRouter
        
        #load lego library here
        
    def run(self):
        # self.time_record = {}
        # time_s = time.time()
        
        
        #clear and create aux_file
        aux_file = os.path.join(self.cfgs.output_dir,'aux_netlist.txt')
        f=open(aux_file,'w')
        f.close()
        
        logger.info('ascell-> Begin processing tech%s @ %s'%(self.tech.tech_name, time.asctime())) 
        if self.cfgs.gen_cells == 'all':
            self.cfgs.gen_cells = list(self.netlist.ckt_types.keys())
        
        for cell_type in self.cfgs.gen_cells:
            # print(cell_type)
            for ckt_name in self.netlist.ckt_types[cell_type]:
                ckt = self.netlist[ckt_name]
                cell = StdCell(ckt,self.tech,self.cfgs,self.patterns)
                self.cells[ckt_name] = cell
                result = cell.run()
                
    def __getitem__(self,key):
        return self.cells[key]     
        
        
    # def read_cell_para(self):
    #     df = pd.read_csv(self.args.cell_para_file)
    #     for i,r in df.iterrows():
    #         para = r['parameter'].strip()
    #         my_re = re.compile(r'[A-Za-z]',re.S)
    #         res = re.findall(my_re,str(r['value']))
    #         if len(res):
    #             value = str(r['value'])  
    #         else:
    #             value = int(r['value'])
    #         self.__setattr__(para,value)
        
    #     logger.info('ascell-> Read cell para file successfully')
  
    
  
    
  
    def output_data(self,file, ckt_name, structs_sequence=None):
        file.write('\n**------------%s--------------**\n'%(ckt_name))
        if structs_sequence:
            for struct in structs_sequence:
                file.write('----%s----\n'%(struct.struct_ckt.name))
                for device in struct.struct_ckt.devices:
                    line = '%s->%s: %s->%s %s->%s %s->%s\n'%(struct.device_mapping[device.name].name,
                                                          device.name,
                                                          struct.net_mapping[device.S],
                                                          device.S,
                                                          struct.net_mapping[device.G],
                                                          device.G,
                                                          struct.net_mapping[device.D],
                                                          device.D)
                    file.write(line)
        
        #out put cdl at utils
        pass

    def init_layout(self):
        #init klayout 
        self.layout = db.Layout()
        self.db_unit = 1e-9
        self.layout_layers = {}
        for name, (num, purpose) in self.tech.output_map.items():
            self.layout_layers[name] = self.layout.layer(num, purpose, name)      

        #init layout tracks
        tech = self.tech
        #vdd and vss rails        
        self.rail_vdd = Range(self.cell_height, self.power_rail_width) 
        self.rail_vss = Range(0, self.power_rail_width) 
       
        #calculate m2_tracks which is stdcell tracks 
        self.tracks_num = int(self.cell_height / self.v_pin_grid)
        assert self.cell_height % self.v_pin_grid == 0, 'cell height cannot be divided by pin grid v!'
        self.tracks_m2 = [Range(t, tech.M1_W.v) for t in list(range(0, self.cell_height + self.v_pin_grid,  self.v_pin_grid)) ] 
        #TODO change to M2.W
               
        #up and down poly tracks
        half_gt_s = int(0.5*tech.GT_S.v)
        self.net_gt_up   = Range(self.cell_height-half_gt_s-tech.GT_W.v, self.cell_height-half_gt_s, set_t='pp')
        self.net_gt_down = Range(0+half_gt_s, 0+half_gt_s+tech.GT_W.v, set_t='pp')        
       
        #AA up and down
        AA_p_up   = self.net_gt_up.p2   - tech.GT_X_AA.v
        AA_n_down = self.net_gt_down.p1 + tech.GT_X_AA.v
       
        #power rail diffusion contact
        #TODO consider AA space? Add AA space to dr
        half_ct_s = int(0.5*tech.CT_S.v)
        self.rail_vdd_ct = Range(self.cell_height-half_ct_s-tech.CT_W.v, self.cell_height-half_ct_s, set_t = 'pp')
        self.rail_vss_ct = Range(0+half_ct_s, 0+half_ct_s + tech.CT_W.v, set_t = 'pp')        
       
        # m1 tracks on top and bottom
        top    = self.rail_vdd_ct.p1 - tech.CT_E_M1.v  
        bottom = self.rail_vss_ct.p2 + tech.CT_E_M1.v
        self.net_m1_up   = Range(top - tech.M1_S.v - tech.M1_W.v, top - tech.M1_S.v, set_t='pp')
        self.net_m1_down = Range(bottom + tech.M1_S.v ,bottom + tech.M1_S.v + tech.M1_W.v, set_t='pp')
        
        self.middle =  int(0.5*((self.cell_height) + self.io_offset ))
        self.v_mode = {}     

        #1 2 gt-ct in middle, gt are connected. e.x. clk and output, dff cn c c cn 
        #2 1 gt-ct in middle,  e.x. inv  
        #output 6 tracks, track2 and 5 may not exist
        #output AA range 
        
        #1e3
        t1 = int(0.5*(tech.GT_S.v + tech.CT_W.v + 2*tech.CT_E_GT.v))
        t2 = int(0.5*(tech.M1_S.v + tech.CT_W.v + 2*tech.CT_E_M1.v))
        t = max(t1,t2)
        
        gt_ct_up   = Range(self.middle + t,  tech.CT_W.v)  
        gt_ct_down = Range(self.middle - t,  tech.CT_W.v)  
        
        # gt_ct_up center to next ct center
        t = max(tech.GT_S_LGT_AA.v + tech.CT_E_GT.v, tech.CT_S_AA.v) + tech.CT_E_AA.v + tech.CT_W.v
        
        mos_ct_up  = Range( gt_ct_up.c   + t,  tech.CT_W.v)  
        mos_ct_down = Range( gt_ct_down.c - t,  tech.CT_W.v) 
        
        AA_p_down = mos_ct_up.p1   - tech.CT_E_AA.v
        AA_n_up   = mos_ct_down.p2 + tech.CT_E_AA.v
        
        #drc check
        assert self.net_m1_up.p1 - mos_ct_up.p2 - tech.CT_E_M1.v >= tech.M1_S.v  
        assert mos_ct_down.p1 - self.net_m1_down.p2 - tech.CT_E_M1.v >= tech.M1_S.v
        
        self.v_mode[0] = {'tracks': [self.net_m1_down, mos_ct_down, gt_ct_down,gt_ct_up,mos_ct_up, self.net_m1_up]}
        self.v_mode[0]['AA_pmos'] = Range(AA_p_up, AA_p_down,set_t='pp')
        self.v_mode[0]['AA_nmos'] = Range(AA_n_up, AA_n_down,set_t='pp')
        self.v_mode[0]['GT_pmos'] = Range(self.net_gt_up.p2, gt_ct_up.p1 - tech.CT_E_GT.v,set_t='pp')
        self.v_mode[0]['GT_nmos'] = Range(gt_ct_down.p2 + tech.CT_E_GT.v, self.net_gt_down.p1,set_t='pp')        
        #2

    def run_bk(self,file, app = None):
        self.time_record = {}
        time_s = time.time()
        
        logger.info('ascell-> Begin processing tech%s @ %s'%(self.tech.tech_name, time.asctime()))
        
        self.le = lego.LEGO(self.args.pin_align_file)
        self.le.run(self.tech.tech_name, self.args.model_file, self.args.netlist)
        self.le.pass_rate()
        self.ckt_dict = self.le.ckt_dict
        # print('Fail cells:', self.le.fail_l[self.tech.tech_name])  some error here
        time_s,_ = timer(time_s, 'Circuits deconstruction use')
        
        #le.ckt_dict
        
        count = 0
        ckts_collection = {}    
        
        #for test
        if len(self.args.test_ckts) >0:
            for ckt_name,ckt in self.le.ckts_collection.items():  
                if ckt_name in self.args.test_ckts:
                    ckts_collection[ckt_name] = ckt        
        else:
            ckts_collection = self.le.ckts_collection
        
        
        for ckt_name,ckt in ckts_collection.items():
            if ckt.de:
                #TODO add process time
                logger.info('@'*60)
                logger.info('Begin processing circuit %s'%(ckt_name))
                
                if app:
                    text = 'Begin processing circuit %s \n'%(ckt_name)
                    app.text_box.insert(tk.END,  time.asctime() +'\n') 
                    app.text_box.insert(tk.END, text)   
                    app.root.update_idletasks()
                
                time_s = time.time()
                result, msg = self.apr(ckt, file)
                
                if not(result):
                    #TODO log
                    logger.info('Error 02! Circuit %s netlist cannot be APR: %s!'%(ckt_name,msg))
                else:
                    logger.info('Success! Circuit %s'%(ckt_name))
                    
                    if app:
                        text = 'Success! Circuit %s \n'%(ckt_name)
                        app.text_box.insert(tk.END,  time.asctime() +'\n') 
                        app.text_box.insert(tk.END, text)
                        
                        app.progress['value'] += 10
                        app.root.update_idletasks()
                    
                
                time_s, time_used = timer(time_s, 'Time used: ')
                self.time_record[self.tech.tech_name +'->' + ckt_name] = time_used   
            else: 
                logger.info('Error 01! Circuit %s netlist cannot be processed!'%(ckt_name))
            

        self.output_gds()
        self.data_file.close()  
   
        
      
    def apr(self, ckt, file):
        #init ckt layout
        ckt.preprocess(self.layout,self.layout_layers)
        
        #TODO maybe more complicated here
        structs_queue = [ckt.de.struct_clk]   + \
                        [ckt.de.struct_input] + \
                         ckt.de.struct_queue  + \
                        [ckt.de.struct_out]
        

        line = self.tech.tech_name +  ' '  + ckt.name + ': '
        for s in structs_queue:
            line = line + s.struct_ckt_name + ' '
        print(line)
        file.write(line + '\n')

        #examine struct
        for struct in structs_queue:
            if not(struct.struct_ckt.name in self.ready_structs):
                logger.info('%s not in ready struct'%(struct.struct_ckt.name))
                return False, struct.struct_ckt.name        
        
        #TODO delete these
        pin_locs = json.load(open('src/lego/layout/pin_loc.json','r'))
        struct_names = [t.struct_ckt.name for t in structs_queue]
        pin_locs = {k:v for k,v in pin_locs.items() if k in struct_names}
                
        channels = Channels(structs_queue, ckt, pin_locs)
        result, channel_nets_routed,pin_locs = channels.graph_route()

        if not(result):
            logger.info('%s can not be channel routed '%(ckt.name))
            return False, ckt.name
        
        for i, struct in enumerate(structs_queue):
            # if i == 0:        
            struct.global_pr_7T(ckt,start_x=0)
        

        side_space =  self.cell_offset_x + self.tech.CT_E_AA.v + self.tech.CT_W_half 
        x = side_space
        
        for i, struct in enumerate(structs_queue):   
            x1 = struct.detail_pr_7T(ckt, self.tech, self, start_x=x)       
            
            if i != len(structs_queue)-1:
                if not(struct.struct_ckt_name in merge_structs()):
                    x1 = channels.detail_route(self.tech, self, i, x1)
            struct.draw(ckt)
            x = x1
        channels.draw(ckt)   
            
        self.post_process_layout(ckt,x1 + side_space)  
        
        return True, ''


    def post_process_layout(self, ckt, right, left=0, m2_tracks=False):
        
        #draw power ground rail
        m1_rails  = M1_Rails(self, left, right)
        m1_rails.draw(ckt)
        ckt.border = m1_rails.border_box
        
        if m2_tracks:
            m2_tracks = M2_Tracks(self, left, right)
            m2_tracks.draw(ckt)
        
        #border and diffusion
        border = ckt.border
        ckt.SP_box = Box([border.l - self.np_ext_border,
                           self.middle,
                           border.r + self.np_ext_border,
                           border.t + self.np_ext_border])
        
        ckt.NW_box = Box([ ckt.SP_box.l - self.nw_ext_np,
                           self.middle,
                           ckt.SP_box.r + self.nw_ext_np,
                           ckt.SP_box.t + self.nw_ext_np])     
        
        ckt.SN_box = Box([border.l - self.np_ext_border,
                           border.b - self.np_ext_border,
                           border.r + self.np_ext_border,
                           self.middle])      
        
        ckt.db_shapes[self.tech.NW].insert( ckt.NW_box.to_dbBox())
        ckt.db_shapes[self.tech.SP].insert( ckt.SP_box.to_dbBox())
        ckt.db_shapes[self.tech.SN].insert( ckt.SN_box.to_dbBox())    
    


    def output_gds(self):
        self.layout.dbu = self.db_unit * 1e6 # 0.001 micro 
        # Write GDS.
        gds_file_name = 'top.gds'
        gds_out_path = os.path.join(self.args.output_dir, gds_file_name)
        logger.info("Write GDS: %s", gds_out_path)
        self.layout.write(gds_out_path)        
        
        
        
        
        

    