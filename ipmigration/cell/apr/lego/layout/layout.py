# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 15:41:40 2024

@author: leiyuan
"""

import itertools
import  pandas as pd
from src.lego.layout.instance import CT_GT,CT_AA,GT_AA,AA_ABUT,AA_SD,GT_EXT,RECT,PATH
# from src.layout import pcell 
from src.schema.shape import Box, Shapes
from src.utils.utils import half

import networkx as nx
import matplotlib.pyplot as plt


def ready_structs():
    return ['CLK1']




class BaseStructure(object):
    def __init__(self,tech,ckt,devices):
        self.tech = tech
        self.ckt = ckt
        self.devices = devices
        self.data = {}
        
        self.left = None
        self.right = None
    
        self.width = 0    
    
        self.pins = None
        self.cross_nets = []
        self.left_nets = []
        self.right_nets = []
        self.internal_nets = []
        
    def new(self,devices):
        cls_ = type(self)
        new_obj = cls_(self.cells,self.pdk_lib)
        new_obj.add_devices(devices)
        return new_obj
      
    def add_devices(self, devices):
        self.devices = devices
        self.devices_flatten = list(itertools.chain.from_iterable(devices))
        self.nets = {}
        for d in self.devices_flatten:
            for p, net in d.pins_dict.items():
                if p != 'B':
                    if net in self.nets:
                        self.nets[net].append((d,p))
                    else:
                        self.nets[net] = [(d,p)]

    def draw(self,cell, loc, struct_name, offset):
        #redraw with loc
        self.data={}
        self.layout(cell, loc, struct_name, offset)
        
        for layer in self.data:    
            for box in self.data[layer]:
                cell.db_shapes[layer].insert(box.to_dbBox())

    def add_shapes(self,shapes):
        for layer, shapes in shapes.items():
            if layer in self.data:
                self.data[layer] = self.data[layer] + shapes
            else:
                self.data[layer] = shapes




class SWITCH_V1(BaseStructure):
    
    def __init__(self,cells,pdk_lib):
        super().__init__(cells,pdk_lib)
        self.name = 'SWITCH_V1'
        self.devices_num = 4

        self.p1 = None
        self.n1 = None
        self.p2 = None
        self.n2 = None
    
    def match(self, devices, ckt):
        assert len(devices) == 2
        p1,n1 = devices[0]
        p2,n2 = devices[1]
        
        cond1 = (p1.D == n1.D) and (p2.S == n2.S) and (p1.D == p2.S)
        cond2 = (p1.G == n2.G) and (p2.G == n1.G)
        
        cond3 = (p1.S in ckt.nets_abutment) and \
                (p2.D in ckt.nets_abutment) and \
                (n1.S in ckt.nets_abutment) and \
                (n2.D in ckt.nets_abutment)
        # print('a', devices)
        # print('b', cond1 , cond2 , cond3)
       
        # #TODO add abutment cond
        # print('c', cond1 & cond2 & cond3)
        return cond1 & cond2 & cond3

    def layout(self, cell, loc, struct_num, offset):
        tech = self.tech
        cells = self.cells
        mode = cells.v_mode['2']
        x,y = loc
        
        p1,n1 = self.devices[0]
        p2,n2 = self.devices[1]
        
        self.left.abutment_p 
        
        p1,n1 = self.devices[0]
        p_next,n_next = self.left.devices[-1]
         
        in1 = p1.G 
        out1 = p1.D
        out2 = n1.D
        #mode
        mode = cells.v_mode['2']
        # self.abutment_p
        #start point, left ct 
        if self.left:
            pass
            #TODO 
        else:
            aa_p_bottom = mode['p'].p1
            aa_n_top= mode['n'].p2
        
        
        net_clkn = p1.S
        net_clk  = p2.D        
        #make sure 2 tracks in the p region
        assert mode['p_m1'].p1 + tech.CT_W_half + tech.CT_E_M1.v + tech.CT_E_M1_END.v + tech.M1_S.v < cells.top_track.p1
        track_p1 = mode['p_m1'].p1 + tech.CT_W_half + tech.CT_E_M1.v 
        track_n1 = mode['n_m1'].p2 - tech.CT_W_half - tech.CT_E_M1.v 
        #TODO according to this one method is advise mos w; another is select different types of layouts       
        # t0 = x + tech.CT_E_AA.v + tech.CT_W_half
        t1 = pcell.cal_gt_ct_space(tech,p1,n1,gt_metal=True)
        centerx = x + t1
        print('abc',x,t1,centerx)
        
        self.ct_gt1 = CT_GT(tech, (centerx, mode['gt_ct1_track'].c), mode='centre')
        
        self.p1_gt = GT_AA(tech, (centerx -  half(p1.L) , mode['p'].p1), p1.W, p1.L, mode='down')
        self.n1_gt = GT_AA(tech, (centerx -  half(n1.L) , mode['n'].p2), n1.W, n1.L, mode='up')   
        
        self.ct_p1_s0 = CT_AA(tech, (x , track_p1 ))
        self.ct_n1_s0 = CT_AA(tech, (x , track_n1 ))
        
        self.p1_aa_left = AA_SD(tech, self.p1_gt, self.ct_p1_s0,  pin = 'S')
        self.n1_aa_left = AA_SD(tech, self.n1_gt, self.ct_n1_s0,  pin = 'S')
        
        t1 = pcell.cal_gt_gt_space(tech,p1,n1,p2,n2, gt_metal=True, aa_metal=False,diff_vddss = True)
        centerx = self.p1_gt.GT_box.c[0] + t1
        
        self.ct_gt2 = CT_GT(tech, (centerx, mode['gt_ct2_track'].c), mode='centre')
        self.p2_gt = GT_AA(tech, (centerx -  half(p2.L) , mode['p'].p1), p2.W, p2.L, mode='down')
        self.n2_gt = GT_AA(tech, (centerx -  half(n2.L) , mode['n'].p2), n2.W, n2.L, mode='up')       
        
        self.p1_gt_ext = GT_EXT(tech, self.p1_gt ,mode = 'up')
        self.n1_gt_ext = GT_EXT(tech, self.n1_gt ,mode = 'down')
        self.p2_gt_ext = GT_EXT(tech, self.p2_gt ,mode = 'up')
        self.n2_gt_ext = GT_EXT(tech, self.n2_gt ,mode = 'down')
        
        self.p_aa_middle = AA_ABUT(tech, self.p1_gt, self.p2_gt)
        self.n_aa_middle = AA_ABUT(tech, self.n1_gt, self.n2_gt)
        
        self.ct_p_m = CT_AA(tech, (self.p_aa_middle.CT_centerx, cells.rail_vdd_ct.c ))
        self.ct_n_m = CT_AA(tech, (self.n_aa_middle.CT_centerx, cells.rail_vss_ct.c  ))   
        
        self.aa_vdd = RECT(tech, tech.AA,[self.ct_p_m.AA_box.l, self.p_aa_middle.AA_box.t,
                                          self.ct_p_m.AA_box.r, self.ct_p_m.AA_box.b ] )
        self.aa_vss = RECT(tech, tech.AA,[self.ct_n_m.AA_box.l, self.ct_n_m.AA_box.t,
                                          self.ct_n_m.AA_box.r, self.n_aa_middle.AA_box.b ] )
        
        t1 = pcell.cal_gt_ct_space(tech,p2,n2,gt_metal=True)
        centerx = self.p2_gt.GT_box.c[0] + t1
        
        self.ct_p2_d0 = CT_AA(tech, (centerx, track_p1))
        self.ct_n2_d0 = CT_AA(tech, (centerx, track_n1))
        
        self.p2_aa_right = AA_SD(tech, self.p2_gt, self.ct_p2_d0,  pin = 'D')
        self.n2_aa_right = AA_SD(tech, self.n2_gt, self.ct_n2_d0,  pin = 'D')
        
        
        self.gt_connect1 = RECT(tech, tech.GT,[max(self.p1_gt.GT_box.l,self.n1_gt.GT_box.l), 
                                                self.n1_gt.GT_box.t, 
                                                min(self.p1_gt.GT_box.r,self.n1_gt.GT_box.r), 
                                                self.p1_gt.GT_box.b ])
        self.gt_connect2 = RECT(tech, tech.GT,[max(self.p2_gt.GT_box.l,self.n2_gt.GT_box.l), 
                                                self.n2_gt.GT_box.t, 
                                                min(self.p2_gt.GT_box.r,self.n2_gt.GT_box.r), 
                                                self.p2_gt.GT_box.b ])
        
        
        
        points = [(self.ct_p2_d0.CT_box.c[0], self.ct_p2_d0.CT_box.t),
                  (self.ct_p2_d0.CT_box.c[0], cells.bottom_track.p1)]
        
        self.clk = PATH(tech, tech.M1, points, tech.M1_W.v, bgn_ext=tech.CT_E_M1_END.v)
        
        
        points = [self.ct_n1_s0.CT_box.c,
                  self.ct_p1_s0.CT_box.c,
                 (self.ct_gt2.CT_box.c[0], self.ct_p1_s0.CT_box.c[1]),
                  self.ct_gt2.CT_box.c ]
        self.clkn1 = PATH(tech, tech.M1, points, tech.M1_W.v, bgn_ext=tech.CT_E_M1_END.v+tech.CT_W_half, end_ext=tech.CT_E_M1_END.v+tech.CT_W_half)
        
        points = [self.ct_gt2.CT_box.c, 
                  (self.ct_gt2.CT_box.c[0], cells.top_track.c), 
                  (self.ct_p2_d0.CT_box.r,  cells.top_track.c)]
        self.clkn2 = PATH(tech, tech.M1, points, tech.M1_W.v)
        

        self.pin_clk = RECT(tech, tech.M1,[self.ct_gt1.CT_box.l, self.ct_gt1.CT_box.b - tech.M1_S.v ,
                                           self.ct_gt2.CT_box.l - tech.CT_E_M1.v - tech.M1_S.v,
                                           self.ct_gt2.CT_box.b  , ])
    
        #finish
        self.width = self.p2_aa_right.AA_box2.r - self.p1_aa_left.AA_box2.l
        #set grid
        self.grid = LayoutGrid(struct_num, 4,1, offset)
        self.grid.remove_nodes([(struct_num, 0,2,0),(struct_num, 0,0,0)])
        nets_mapping = {(struct_num, 0,3,1):net_clkn,
                        (struct_num, 0,2,1):net_clk,
                        (struct_num, 0,1,1):net_clk,
                        (struct_num, 0,0,1):net_clk,
                        (struct_num, 0,1,0):net_clkn}
        self.grid.set_nets( nets_mapping)
        # LayoutGrid.draw(self.grid.graph)
    
        self.add_shapes(self.ct_p1_s0.data)
        self.add_shapes(self.ct_n1_s0.data)
        self.add_shapes(self.ct_gt1.data)
        self.add_shapes(self.p1_gt.data)
        self.add_shapes(self.n1_gt.data)
        self.add_shapes(self.p1_aa_left.data)
        self.add_shapes(self.n1_aa_left.data)
        self.add_shapes(self.p2_gt.data)
        self.add_shapes(self.n2_gt.data)        
        self.add_shapes(self.ct_gt2.data)
        self.add_shapes(self.p_aa_middle.data)
        self.add_shapes(self.n_aa_middle.data)
        self.add_shapes(self.p1_gt_ext.data)
        self.add_shapes(self.n1_gt_ext.data)
        self.add_shapes(self.p2_gt_ext.data)
        self.add_shapes(self.n2_gt_ext.data)
        self.add_shapes(self.ct_p_m.data)
        self.add_shapes(self.ct_n_m.data)
        self.add_shapes(self.aa_vdd.data)
        self.add_shapes(self.aa_vss.data)        
        self.add_shapes(self.gt_connect1.data)
        self.add_shapes(self.gt_connect2.data)
        self.add_shapes(self.ct_p2_d0.data)
        self.add_shapes(self.ct_n2_d0.data)
        self.add_shapes(self.p2_aa_right.data)
        self.add_shapes(self.n2_aa_right.data)
        self.add_shapes(self.clk.data)
        self.add_shapes(self.clkn1.data)
        self.add_shapes(self.clkn2.data)
        self.add_shapes(self.pin_clk.data) #TODO process pins together, why you know there is a pin??
        
        

# class COMMONG_V1(BaseStructure):
    
#     def __init__(self,cells,pdk_lib):
#         super().__init__(cells,pdk_lib)
#         self.name = 'COMMONG_V1'
#         self.devices_num = 2

    
#     def match(self, devices, ckt):
#         assert len(devices) == 1
#         p1,n1 = devices[0]
#         cond1 = (p1.S == 'VDD') and (n1.S == 'VSS') 
#         cond3 = (p1.D in ckt.nets_abutment) and (n1.D in ckt.nets_abutment) 
#         cond5 = p1.G == n1.G
#         return cond1 and cond3 and cond5


#     def layout(self, cell, loc, struct_num, offset):
#         tech = self.tech
#         cells = self.cells
#         #TODO how to set this, maybe according to group!
#         mode = cells.v_mode['1']
        
#         x,y = loc
         
#         p1,n1 = self.devices[0]
#         p_next,n_next = self.right.devices[0]
         
#         in1 = p1.G 
#         out1 = p1.D
#         out2 = n1.D
#         #mode
#         mode = cells.v_mode['2']
        
#         #start point, left ct 
#         if self.left:
#             pass
#             #TODO 
#         else:
#             aa_p_bottom = mode['p'].p1
#             aa_n_top= mode['n'].p2

#         t1 = pcell.cal_gt_ct_space(tech,p1,n1,gt_metal=True)
#         centerx = x + t1    
#         self.p1_gt = GT_AA(tech, (centerx -  half(p1.L) , aa_p_bottom), p1.W, p1.L, mode='down')
#         self.n1_gt = GT_AA(tech, (centerx -  half(n1.L) , aa_n_top), n1.W, n1.L, mode='up') 
                
#         ct_p1_s0 = CT_AA(tech, (x, cells.rail_vdd_ct.c  ))
#         ct_n1_s0 = CT_AA(tech, (x, cells.rail_vss_ct.c  ))

#         ct_p1_s1 = CT_AA(tech, (x, mode['p_m1'].p1 + tech.CT_W_half + tech.CT_E_M1.v  ))
#         ct_n1_s1 = CT_AA(tech, (x, mode['n_m1'].p2 - tech.CT_W_half - tech.CT_E_M1.v  ))
        

#         self.p1_aa_left = AA_SD(tech, self.p1_gt, ct_p1_s1,  pin = 'S')
#         self.n1_aa_left = AA_SD(tech, self.n1_gt, ct_n1_s1,  pin = 'S')
        
#         if len(self.cross_nets) >=2:
#             self.ct_p1_s0 = ct_p1_s0
#             self.ct_n1_s0 = ct_n1_s0  
#             self.aa_vdd = RECT(tech, tech.AA,[self.ct_p1_s0.AA_box.l, self.p1_aa_left.AA_box.t,
#                                               self.ct_p1_s0.AA_box.r, self.ct_p1_s0.AA_box.b ] )
#             self.aa_vss = RECT(tech, tech.AA,[self.ct_n1_s0.AA_box.l, self.ct_n1_s0.AA_box.t,
#                                               self.ct_n1_s0.AA_box.r, self.n1_aa_left.AA_box.b ] )
#         else:
#             #TODO
#             print('xxxxxxxx')
        
#         t1 = pcell.cal_gt_gt_space(tech,p1,n1,p_next,n_next, gt_metal=True, aa_metal=False, aa_ct=False, diff_vddss=False)
#         centerx = self.p1_gt.GT_box.c[0] + t1
        
#         # self.ct_gt2 = CT_GT(tech, (centerx, mode['gt_ct2_track'].c), mode='centre')
#         self.p2_gt = GT_AA(tech, (centerx -  half(p_next.L) , aa_p_bottom), p_next.W, p_next.L, mode='down')
#         self.n2_gt = GT_AA(tech, (centerx -  half(n_next.L) , aa_n_top), n_next.W, n_next.L, mode='up')       
        
#         self.p1_gt_ext = GT_EXT(tech, self.p1_gt ,mode = 'up')
#         self.n1_gt_ext = GT_EXT(tech, self.n1_gt ,mode = 'down')

#         self.p1_aa_right = AA_ABUT(tech, self.p1_gt, self.p2_gt)
#         self.n1_aa_right = AA_ABUT(tech, self.n1_gt, self.n2_gt)
        
#         #take account cross line num; 
#         self.ct_gt1 = CT_GT(tech, (self.p1_gt.GT_box.r, mode['gt_ct1_track'].c), mode='right')
#         self.gt_connect1 = RECT(tech, tech.GT,[max(self.p1_gt.GT_box.l,self.n1_gt.GT_box.l), 
#                                                 self.n1_gt.GT_box.t, 
#                                                 min(self.p1_gt.GT_box.r,self.n1_gt.GT_box.r), 
#                                                 self.p1_gt.GT_box.b ])
#         if in1 in cell.pins:
#             self.in1 = RECT(tech, tech.M1,[self.ct_p1_s0.CT_box.l , self.ct_gt1.CT_box.b -tech.M1_S.v  ,
#                                            self.ct_gt1.CT_box.r,    self.ct_gt1.CT_box.t + tech.M1_S.v ])            
        
#         #set abutment pins
#         self.abutment_p = self.p1_aa_right
#         self.abutment_n = self.n1_aa_right
        
        
#         #finish
#         self.width = self.p2_gt.GT_box.c[0] - x
#         #set grid
#         self.grid = LayoutGrid(struct_num, 4,2, offset)

#         self.grid.remove_nodes([(struct_num, 0,2,0),(struct_num, 0,0,0)]) #gt
#         self.grid.remove_nodes([(struct_num, 0,2,1),(struct_num, 1,2,1)]) #m1
        
#         nets_mapping = {(struct_num, 0,1,1):in1,
#                         (struct_num, 1,1,1):in1,
#                         (struct_num, 0,1,0):in1}
#         self.grid.set_nets( nets_mapping)
#         # LayoutGrid.draw(self.grid.graph)              
         
#         self.add_shapes(self.p1_gt.data)
#         self.add_shapes(self.n1_gt.data)
#         self.add_shapes(self.p1_aa_left.data)
#         self.add_shapes(self.n1_aa_left.data)
#         self.add_shapes(self.ct_p1_s0.data)
#         self.add_shapes(self.ct_n1_s0.data)    
#         if len(self.cross_nets) >=2:
#             self.add_shapes(self.aa_vdd.data)
#             self.add_shapes(self.aa_vss.data)

#         self.add_shapes(self.p1_aa_right.data)
#         self.add_shapes(self.n1_aa_right.data)
#         self.add_shapes(self.p1_gt_ext.data)
#         self.add_shapes(self.n1_gt_ext.data)
#         self.add_shapes(self.ct_gt1.data)
#         self.add_shapes(self.gt_connect1.data)
#         if in1 in cell.pins:
#             self.add_shapes(self.in1.data)
        
# class COMMONG_V2(BaseStructure):
    
#     def __init__(self,cells,pdk_lib):
#         super().__init__(cells,pdk_lib)
#         self.name = 'COMMONG_V1'
#         self.devices_num = 2

    
#     def match(self, devices, ckt):
#         assert len(devices) == 1
#         p1,n1 = devices[0]
        
#         cond2 = (p1.D == 'VDD') and (n1.D == 'VSS')  
#         cond4 = (p1.S in ckt.nets_abutment) and (n1.S in ckt.nets_abutment)
#         cond5 = p1.G == n1.G

#         return cond2 and cond4 and cond5


#     def layout(self, cell, loc, struct_name, offset):
#          tech = self.tech
#          cells = self.cells
#          mode = cells.v_mode['1']
#          x,y = loc
         
#          p1,n1 = self.devices[0]
         
#          #mode
         
         
#          #one net vdd/vss one net is 




# class INV_V1(BaseStructure):
    
#     def __init__(self,cells,pdk_lib):
#         super().__init__(cells,pdk_lib)
#         self.name = 'INV_V1'
#         self.devices_num = 2

    
#     def match(self, devices, ckt):
#         assert len(devices) == 1
#         p1,n1 = devices[0]
        
#         cond1 = (p1.S == 'VDD') and (n1.S == 'VSS') 
#         cond2 = (p1.D == 'VDD') and (n1.D == 'VSS') 
#         cond3 = p1.D == n1.D 
#         cond4 = p1.S == n1.S 
#         cond5 = p1.G == n1.G
       
#         #TODO add abutment cond
#         # print('a',devices)
#         # print('b',cond1 , cond2 , cond3, cond4,cond5)
#         return ((cond1 and cond3) or (cond2 and cond4)) and cond5


#     def layout(self, cell, loc, struct_name, offset):
#         t = self.tech



# class CLK_V1(BaseStructure):
    
#     def __init__(self,cells,pdk_lib):
#         super().__init__(cells,pdk_lib)
#         self.name = 'CLK_V1'
#         self.devices_num = 4

#         netlist = [
#         ".SUBCKT CLK_V1 VDD VSS G cn c",
#         "mp_1_0  cn    G    VDD  VNW pmos l=1.3e-07 w=2.8e-07",
#         "mn_1_0  cn    G    VSS  VPW nmos l=1.3e-07 w=2.3e-07",
#         "mp_2_0  VDD   cn   c    VNW pmos l=1.3e-07 w=2.3e-07",
#         "mn_2_0  VSS   cn   c    VPW nmos l=1.3e-07 w=1.8e-07",
#         ".ends CLK_V1"]
#         self.read_netlist(netlist)
#         #TODO leave for 
   
#     def match(self, devices, ckt):
        
#         assert len(devices) == 2
#         p1,n1 = devices[0]
#         p2,n2 = devices[1]
        
#         cond1 = (p1.S == n1.S) and (p2.D == n2.D)
#         cond2 = (p1.G == n1.G) and (p2.G == n2.G)
#         cond3 = (p1.S == p2.G)
#         cond4 = (p1.D == 'VDD') and (p2.S == 'VDD') and (n1.D == 'VSS') and (n2.S == 'VSS')
        
#         # print(cond1 , cond2 , cond3, cond4)
#         return cond1 & cond2 & cond3 & cond4

#     def layout(self, cell, loc, struct_num, offset):
#         tech = self.tech
#         cells = self.cells
#         mode = cells.v_mode['1']
#         x,y = loc
        
#         p1,n1 = self.devices[0]
#         p2,n2 = self.devices[1]
        
#         net_clkn = p1.S
#         net_clk  = p2.D        
#         #make sure 2 tracks in the p region
#         assert mode['p_m1'].p1 + tech.CT_W_half + tech.CT_E_M1.v + tech.CT_E_M1_END.v + tech.M1_S.v < cells.top_track.p1
#         track_p1 = mode['p_m1'].p1 + tech.CT_W_half + tech.CT_E_M1.v 
#         track_n1 = mode['n_m1'].p2 - tech.CT_W_half - tech.CT_E_M1.v 
#         #TODO according to this one method is advise mos w; another is select different types of layouts       
#         # t0 = x + tech.CT_E_AA.v + tech.CT_W_half
#         t1 = pcell.cal_gt_ct_space(tech,p1,n1,gt_metal=True)
#         centerx = x + t1
#         print('abc',x,t1,centerx)
        
#         self.ct_gt1 = CT_GT(tech, (centerx, mode['gt_ct1_track'].c), mode='centre')
        
#         self.p1_gt = GT_AA(tech, (centerx -  half(p1.L) , mode['p'].p1), p1.W, p1.L, mode='down')
#         self.n1_gt = GT_AA(tech, (centerx -  half(n1.L) , mode['n'].p2), n1.W, n1.L, mode='up')   
        
#         self.ct_p1_s0 = CT_AA(tech, (x , track_p1 ))
#         self.ct_n1_s0 = CT_AA(tech, (x , track_n1 ))
        
#         self.p1_aa_left = AA_SD(tech, self.p1_gt, self.ct_p1_s0,  pin = 'S')
#         self.n1_aa_left = AA_SD(tech, self.n1_gt, self.ct_n1_s0,  pin = 'S')
        
#         t1 = pcell.cal_gt_gt_space(tech,p1,n1,p2,n2, gt_metal=True, aa_metal=False,diff_vddss = True)
#         centerx = self.p1_gt.GT_box.c[0] + t1
        
#         self.ct_gt2 = CT_GT(tech, (centerx, mode['gt_ct2_track'].c), mode='centre')
#         self.p2_gt = GT_AA(tech, (centerx -  half(p2.L) , mode['p'].p1), p2.W, p2.L, mode='down')
#         self.n2_gt = GT_AA(tech, (centerx -  half(n2.L) , mode['n'].p2), n2.W, n2.L, mode='up')       
        
#         self.p1_gt_ext = GT_EXT(tech, self.p1_gt ,mode = 'up')
#         self.n1_gt_ext = GT_EXT(tech, self.n1_gt ,mode = 'down')
#         self.p2_gt_ext = GT_EXT(tech, self.p2_gt ,mode = 'up')
#         self.n2_gt_ext = GT_EXT(tech, self.n2_gt ,mode = 'down')
        
#         self.p_aa_middle = AA_ABUT(tech, self.p1_gt, self.p2_gt)
#         self.n_aa_middle = AA_ABUT(tech, self.n1_gt, self.n2_gt)
        
#         self.ct_p_m = CT_AA(tech, (self.p_aa_middle.CT_centerx, cells.rail_vdd_ct.c ))
#         self.ct_n_m = CT_AA(tech, (self.n_aa_middle.CT_centerx, cells.rail_vss_ct.c  ))   
        
#         self.aa_vdd = RECT(tech, tech.AA,[self.ct_p_m.AA_box.l, self.p_aa_middle.AA_box.t,
#                                           self.ct_p_m.AA_box.r, self.ct_p_m.AA_box.b ] )
#         self.aa_vss = RECT(tech, tech.AA,[self.ct_n_m.AA_box.l, self.ct_n_m.AA_box.t,
#                                           self.ct_n_m.AA_box.r, self.n_aa_middle.AA_box.b ] )
        
#         t1 = pcell.cal_gt_ct_space(tech,p2,n2,gt_metal=True)
#         centerx = self.p2_gt.GT_box.c[0] + t1
        
#         self.ct_p2_d0 = CT_AA(tech, (centerx, track_p1))
#         self.ct_n2_d0 = CT_AA(tech, (centerx, track_n1))
        
#         self.p2_aa_right = AA_SD(tech, self.p2_gt, self.ct_p2_d0,  pin = 'D')
#         self.n2_aa_right = AA_SD(tech, self.n2_gt, self.ct_n2_d0,  pin = 'D')
        
        
#         self.gt_connect1 = RECT(tech, tech.GT,[max(self.p1_gt.GT_box.l,self.n1_gt.GT_box.l), 
#                                                 self.n1_gt.GT_box.t, 
#                                                 min(self.p1_gt.GT_box.r,self.n1_gt.GT_box.r), 
#                                                 self.p1_gt.GT_box.b ])
#         self.gt_connect2 = RECT(tech, tech.GT,[max(self.p2_gt.GT_box.l,self.n2_gt.GT_box.l), 
#                                                 self.n2_gt.GT_box.t, 
#                                                 min(self.p2_gt.GT_box.r,self.n2_gt.GT_box.r), 
#                                                 self.p2_gt.GT_box.b ])
        
        
        
#         points = [(self.ct_p2_d0.CT_box.c[0], self.ct_p2_d0.CT_box.t),
#                   (self.ct_p2_d0.CT_box.c[0], cells.bottom_track.p1)]
        
#         self.clk = PATH(tech, tech.M1, points, tech.M1_W.v, bgn_ext=tech.CT_E_M1_END.v)
        
        
#         points = [self.ct_n1_s0.CT_box.c,
#                   self.ct_p1_s0.CT_box.c,
#                  (self.ct_gt2.CT_box.c[0], self.ct_p1_s0.CT_box.c[1]),
#                   self.ct_gt2.CT_box.c ]
#         self.clkn1 = PATH(tech, tech.M1, points, tech.M1_W.v, bgn_ext=tech.CT_E_M1_END.v+tech.CT_W_half, end_ext=tech.CT_E_M1_END.v+tech.CT_W_half)
        
#         points = [self.ct_gt2.CT_box.c, 
#                   (self.ct_gt2.CT_box.c[0], cells.top_track.c), 
#                   (self.ct_p2_d0.CT_box.r,  cells.top_track.c)]
#         self.clkn2 = PATH(tech, tech.M1, points, tech.M1_W.v)
        

#         self.pin_clk = RECT(tech, tech.M1,[self.ct_gt1.CT_box.l, self.ct_gt1.CT_box.b - tech.M1_S.v ,
#                                            self.ct_gt2.CT_box.l - tech.CT_E_M1.v - tech.M1_S.v,
#                                            self.ct_gt2.CT_box.b  , ])
    
#         #finish
#         self.width = self.p2_aa_right.AA_box2.r - self.p1_aa_left.AA_box2.l
#         #set grid
#         self.grid = LayoutGrid(struct_num, 4,1, offset)
#         self.grid.remove_nodes([(struct_num, 0,2,0),(struct_num, 0,0,0)])
#         nets_mapping = {(struct_num, 0,3,1):net_clkn,
#                         (struct_num, 0,2,1):net_clk,
#                         (struct_num, 0,1,1):net_clk,
#                         (struct_num, 0,0,1):net_clk,
#                         (struct_num, 0,1,0):net_clkn}
#         self.grid.set_nets( nets_mapping)
#         # LayoutGrid.draw(self.grid.graph)
    
#         self.add_shapes(self.ct_p1_s0.data)
#         self.add_shapes(self.ct_n1_s0.data)
#         self.add_shapes(self.ct_gt1.data)
#         self.add_shapes(self.p1_gt.data)
#         self.add_shapes(self.n1_gt.data)
#         self.add_shapes(self.p1_aa_left.data)
#         self.add_shapes(self.n1_aa_left.data)
#         self.add_shapes(self.p2_gt.data)
#         self.add_shapes(self.n2_gt.data)        
#         self.add_shapes(self.ct_gt2.data)
#         self.add_shapes(self.p_aa_middle.data)
#         self.add_shapes(self.n_aa_middle.data)
#         self.add_shapes(self.p1_gt_ext.data)
#         self.add_shapes(self.n1_gt_ext.data)
#         self.add_shapes(self.p2_gt_ext.data)
#         self.add_shapes(self.n2_gt_ext.data)
#         self.add_shapes(self.ct_p_m.data)
#         self.add_shapes(self.ct_n_m.data)
#         self.add_shapes(self.aa_vdd.data)
#         self.add_shapes(self.aa_vss.data)        
#         self.add_shapes(self.gt_connect1.data)
#         self.add_shapes(self.gt_connect2.data)
#         self.add_shapes(self.ct_p2_d0.data)
#         self.add_shapes(self.ct_n2_d0.data)
#         self.add_shapes(self.p2_aa_right.data)
#         self.add_shapes(self.n2_aa_right.data)
#         self.add_shapes(self.clk.data)
#         self.add_shapes(self.clkn1.data)
#         self.add_shapes(self.clkn2.data)
#         self.add_shapes(self.pin_clk.data) #TODO process pins together, why you know there is a pin??
        

# class OUT_V1(BaseStructure):
    
#     def __init__(self,cells,pdk_lib):
#         super().__init__(cells,pdk_lib)
#         self.name = 'OUT_V1'
#         self.devices_num = 4
    
#     def match(self, devices, ckt):
#         assert len(devices) == 2
#         p1,n1 = devices[0]
#         p2,n2 = devices[1]
        
#         cond1 = (p1.S == n1.S) and (p2.D == n2.D)
#         cond2 = (p1.G == n1.G) and (p2.G == n2.G)
#         cond3 =  (p1.S != p2.G)
#         cond4 = (p1.D == 'VDD') and (p2.S == 'VDD') and (n1.D == 'VSS') and (n2.S == 'VSS')
#         # print(cond1 , cond2 , cond3, cond4)
#         return cond1 & cond2 & cond3 & cond4


#     def layout(self, cell, loc, struct_name, offset):
#         pass




    
    
    
    
    
    
# def if_abutment(device, pin, nets):
#     net = device.__getattribute__(pin) 
#     pins = nets[net]
    