#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: leiyuan
"""

from ipmigration.cell.apr.cir.decompose import DeCKT
from ipmigration.cell.apr.pr.pattern_placer import Placer


class StdCell:
    def __init__(self, ckt, tech, cfgs, patterns):
        self.ckt = ckt
        self.tech = tech
        self.cfgs = cfgs
        self.patterns= patterns
        
    def run(self):
        self.init_layout()
        self.global_place()
    
    def init_layout(self):
        pass
    
    def global_place(self):
        self.ckt.combine_parallel()
        self.de_ckt = DeCKT(self.ckt, 
                            self.patterns, 
                            self.tech.tech_name, 
                            self.cfgs.output_dir)
        result = self.de_ckt.run()

        if result:
            print('Success: ', self.ckt.name)
            pat_placer = Placer(self.de_ckt.sub_ckts)
            queue = pat_placer.find_opt_perm(self.ckt.ckt_type)
            
            #auto-folding
            
            
            
            self.pat_placer = pat_placer
            self.queue = queue
        else:
            print('Fail: ', self.ckt.name)
        
        
        
    
    
    
    def global_route(self):
        pass
    

    def detail_place(self):
        pass
    
    def detail_route(self):
        pass    
    
    
    def pre_process(self, ckt, right, left=0, m2_tracks=False):
        pass

       
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
   
    def post_process(self, ckt, right, left=0, m2_tracks=False):
        #TODO add merge shapes
        
        
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
    