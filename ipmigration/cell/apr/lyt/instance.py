# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 10:10:51 2024

@author: leiyuan
"""


import logging
from ipmigration.cell.apr.lyt.shape import Range, Box, Shapes
# from src.basic.shape import Range, Box, Shapes
# import klayout.db as db

logger = logging.getLogger(__name__)

#
def half(value):
    return int(0.5*value)
 

class Instance:
    def __init__(self,tech):
        self.tech = tech
        self.data = {}
    
    def draw(self,ckt):
        for layer in self.data:    
            for box in self.data[layer]:
                ckt.db_shapes[layer].insert(box.to_dbBox())

class Rect(Instance):
    def __init__(self, tech, layer, value):
        super().__init__(tech)
        self.layer = layer
        self.box = Box(value)
        self.data[layer] = [self.box]

#
class M2_Tracks(Instance):
    def __init__(self,cells,left,right):
        super().__init__(cells.tech)
        self.data[self.tech.M2] = []
        for t in cells.tracks_m2: 
            box =  Box([left, t.p1, right, t.p2])
            self.data[self.tech.M2].append(box)
#      
class M1_Rails(Instance):
    def __init__(self,tech,left,right):
        super().__init__(tech)
        vdd_box   = Box([left, tech.rail_vdd.p1, right, tech.rail_vdd.p2] )
        vss_box   = Box([left, tech.rail_vss.p1, right, tech.rail_vss.p2] )
        border_box = Box([left, tech.rail_vss.c , right, tech.rail_vdd.c]  )
        self.data[tech.M1] =[vdd_box,vss_box]
        self.data[tech.BORDER] = [border_box]
        self.border_box = border_box

class NPWELL(Instance):
    def __init__(self,tech,cfgs,border):
        super().__init__(tech)
        
        SP_box = Box([border.l - cfgs.np_ext_border,
                      tech.middle,
                      border.r + cfgs.np_ext_border,
                      border.t + cfgs.np_ext_border])
        
        NW_box = Box([ SP_box.l - cfgs.nw_ext_np,
                      tech.middle,
                      SP_box.r + cfgs.nw_ext_np,
                      SP_box.t + cfgs.nw_ext_np])     
        
        SN_box = Box([border.l - cfgs.np_ext_border,
                            border.b - cfgs.np_ext_border,
                            border.r + cfgs.np_ext_border,
                            tech.middle])     
        self.data[tech.SP] = [SP_box]
        self.data[tech.NW] = [NW_box]
        self.data[tech.SN] = [SN_box]
class M1_Route(Instance):
    def __init__(self, tech, m1_edges, net_loc, w, eol_nodes):
        #end_type dict of end of line ct, with direction and end line type
        super().__init__(tech)
        #w1 min gt width; w2 cg ct width; w3 mos width
        self.data['M1'] = []
        # self.nodes = []
        
        h_w = int(0.5*w)    

        for i, net in enumerate(m1_edges):
            if len(m1_edges[net]) > 0: 
                for p1, p2 in m1_edges[net]:
                    # self.nodes.append(p1)
                    # self.nodes.append(p2)
                    di = edge_direction(p1,p2)
                    x1,y1 = net_loc[p1]
                    x2,y2 = net_loc[p2]
   
                    
                    box =  Box([min(x1,x2)-h_w, 
                                min(y1,y2)-h_w,  
                                max(x1,x2)+h_w, 
                                max(y1,y2)+h_w])
                    
                    t_eol = tech.CT_E_M1_END.v
                    self.data['M1'].append(box)
                    #TDDO left for end of line 
                    for eol_p in [p1,p2]:
                        if eol_p in eol_nodes:
                            di = eol_nodes[eol_p]
                            x1,y1  = net_loc[eol_p]
                            if di == 'ew':
                                eol_box = Box([x1-tech.CT_W.hv-t_eol, y1-tech.CT_W.hv,
                                               x1+tech.CT_W.hv+t_eol, y1+tech.CT_W.hv])
             
                            self.data['M1'].append(eol_box)
                        

class M2_Route(Instance):
    def __init__(self, tech, m2_edges, net_loc):
        #end_type dict of end of line ct, with direction and end line type
        super().__init__(tech)
        #w1 min gt width; w2 cg ct width; w3 mos width
        self.data['M2'] = []
        # self.nodes = []
        
        h_w = tech.M2_W.hv + tech.V1_E_M_END.v   
        ext= tech.V1_E_M_END.v +tech.M2_W.hv
        for i, net in enumerate(m2_edges):
            p1, p2 = m2_edges[net]
            p1 = (p1[0],p1[1])
            p2 = (p2[0],p2[1])
            x1,y1 = net_loc[p1]
            x2,y2 = net_loc[p2]
   
                
            box =  Box([min(x1,x2)-ext, 
                        min(y1,y2)-h_w,  
                        max(x1,x2)+ext, 
                        max(y1,y2)+h_w])
            self.data['M2'].append(box)       
 

class GT_Route(Instance):
    def __init__(self, tech, gt_edges, net_loc, w, draw_data):
        super().__init__(tech)
        self.data['GT'] = []
        h_w = int(0.5*w)
        for i, net in enumerate(gt_edges):
            if len(gt_edges[net]) > 0: 
                for p1, p2 in gt_edges[net]:
                    x1,y1 = net_loc[p1]
                    x2,y2 = net_loc[p2]
                    if p1[0] == p2[0]:
                        if draw_data[p1[0]]['is_gt']:
                            w_l = []
                            if draw_data[p1[0]]['P']:
                                w_l.append(draw_data[p1[0]]['P'].L)
                            if draw_data[p1[0]]['N']:
                                w_l.append(draw_data[p1[0]]['N'].L)
                            h_w2 = int(0.5*max(w_l))   
                            box =  Box([min(x1,x2)-h_w2, 
                                        min(y1,y2)-h_w,  
                                        max(x1,x2)+h_w2, 
                                        max(y1,y2)+h_w])
                            self.data['GT'].append(box) 
                        else:
                            box =  Box([min(x1,x2)-h_w, 
                                        min(y1,y2)-h_w,  
                                        max(x1,x2)+h_w, 
                                        max(y1,y2)+h_w])
                            self.data['GT'].append(box)  
                    else:
                            
                        box =  Box([min(x1,x2)-h_w, 
                                    min(y1,y2)-h_w,  
                                    max(x1,x2)+h_w, 
                                    max(y1,y2)+h_w])
                        
                        self.data['GT'].append(box) 

class Pin_Nodes(Instance):
    def __init__(self, tech, pins , node_loc):
        super().__init__(tech)
        self.data['GT'] = []
        self.data['CT'] = []
        self.data['M1'] = []
        h_w1 = tech.CT_W.hv
        v_w1 = tech.CT_W.hv
        
        h_w2 = tech.GT_CT_W.hv
        v_w2 = tech.GT_CT_W.hv
        
        for node in pins:
            x, y = node_loc[node]
            box1 =  Box([x-h_w1, y-v_w1, x+h_w1, y+v_w1])
            box2 =  Box([x-h_w2, y-v_w2, x+h_w2, y+v_w2])
            self.data['CT'].append(box1)
            self.data['GT'].append(box2)
            self.data['M1'].append(box2)
            
            
class CT_Nodes(Instance):
    def __init__(self, tech, gt_cts, aa_cts, node_loc):
        super().__init__(tech)
        self.data['GT'] = []
        self.data['CT'] = []
        h_w1 = tech.CT_W.hv
        v_w1 = tech.CT_W.hv
        
        h_w2 = tech.GT_CT_W.hv
        v_w2 = tech.GT_CT_W.hv
        
        for node in gt_cts:
            x, y = node_loc[node]
            box1 =  Box([x-h_w1, y-v_w1, x+h_w1, y+v_w1])
            box2 =  Box([x-h_w2, y-v_w2, x+h_w2, y+v_w2])
            self.data['CT'].append(box1)
            self.data['GT'].append(box2)

        for node in aa_cts:
            x, y = node_loc[node]
            box1 =  Box([x-h_w1, y-v_w1, x+h_w1, y+v_w1])
            self.data['CT'].append(box1)  


class V1_Nodes(Instance):
    #if 2 vias are needed
    def __init__(self, tech, v1_pins, node_loc):
        super().__init__(tech)
        self.data['V1'] = []
        w = tech.V1_W.hv

    
        for node in v1_pins:
            x, y = node_loc[(node[0],node[1])]
            box =  Box([x-w, y-w, x+w, y+w])

            self.data['V1'].append(box)
            # self.data['GT'].append(box2)




class GT_AA(Instance):
    #TODO: need revise for future more vmodes
    def __init__(self, tech, draw_data, gt_cts,aa_cts,pw_pins, node_loc, pattern_router):
        super().__init__(tech)
        tp = pattern_router.track_num-1
        mu = pattern_router.median_u
        md = pattern_router.median_d
        dn = 0
        dn = tech.gt_dn_rg.p1 + tech.GT_X_AA.v
        tp = tech.gt_up_rg.p2 - tech.GT_X_AA.v
        self.data['GT'] = []
        self.data['AA'] = []
        self.data['CT'] = []
        self.data['M1'] = []
        
        for col,attr in draw_data.items():
            if attr['is_gt']:
                if attr['P']:
                    L = attr['P'].L
                    W = attr['P'].W
                    h_l = int(0.5*L)
                    x,bottom = node_loc[(col,mu)]
                    box1 =  Box([x-h_l, 
                                bottom,  
                                x+h_l, 
                                tech.gt_up_rg.p2])
                    
                    box2 =  Box([x-h_l, 
                                tp-W,  
                                x+h_l, 
                                tp])
                    
                    self.data['GT'].append(box1) 
                    self.data['AA'].append(box2) 
                if attr['N']:
                    L = attr['N'].L
                    W = attr['N'].W
                    h_l = int(0.5*L)
                    x,top = node_loc[(col,md)]
                    box1 =  Box([x-h_l, 
                                tech.gt_dn_rg.p1,  
                                x+h_l, 
                                top])
                    box2 =  Box([x-h_l, 
                                dn,  
                                x+h_l, 
                                dn+W])
                        
                    self.data['GT'].append(box1) 
                    self.data['AA'].append(box2) 
            else:
                aa_ct_p = [tuple(t) for t in aa_cts if t[0]==col and t[1]>=mu]
                aa_ct_n = [tuple(t) for t in aa_cts if t[0]==col and t[1]<=md]
                pw_ct_p = [(t[0],t[1]) for t in pw_pins['VDD'][0] if t[0]==col]
                pw_ct_n = [(t[0],t[1]) for t in pw_pins['VSS'][0] if t[0]==col]
  
                sd_x,_ = node_loc[(col,0)]
                if attr['P']:
                    top_loc = tp
                    l_d = draw_data[col-1]['P']
                    r_d = draw_data[col+1]['P']

                    if l_d and r_d:
                        sd_x_l,_ = node_loc[(col-1,0)] 
                        sd_x_r,_ = node_loc[(col+1,0)] 
                        W1 = l_d.W
                        W2 = r_d.W 
                        box1 = Box([sd_x_l,top_loc-W1,sd_x,top_loc])  
                        box2 = Box([sd_x,top_loc-W2,sd_x_r,top_loc])   
                        self.data['AA'].append(box1)  
                        self.data['AA'].append(box2) 
                    elif l_d:
                        sd_x_l,_ = node_loc[(col-1,0)] 
                        sd_x_r = sd_x + tech.CT_E_AA.v + tech.CT_W.hv
                        W1 = l_d.W
                        box1 = Box([sd_x_l,top_loc-W1,sd_x_r,top_loc])   
                        self.data['AA'].append(box1)  
                    elif r_d:
                        sd_x_r,_ = node_loc[(col+1,0)] 
                        sd_x_l = sd_x - tech.CT_E_AA.v - tech.CT_W.hv
                        W1 = r_d.W
                        box1 = Box([sd_x_l,top_loc-W1,sd_x_r,top_loc])   
                        self.data['AA'].append(box1)  
                    
                    if aa_ct_p:
                        x,y = node_loc[aa_ct_p[0]]
                        w = tech.CT_E_AA.v + tech.CT_W.hv
                        box1 =  Box([x-w,y-w,x+w,tp])
                        self.data['AA'].append(box1)  
                    if pw_ct_p:
                        x,y = node_loc[pw_ct_p[0]]
                        w = tech.CT_W.hv
                        ext = tech.CT_E_AA.v
                        box1 = Box([x-w,tech.ct_up_rg.p1,x+w,tech.ct_up_rg.p2])
                        w = tech.CT_W.hv + tech.CT_E_AA.v 
                        ext = tech.CT_E_AA.v
                        box2 = Box([x-w,tp,x+w,tech.ct_up_rg.p2 + ext])
                        
                        
                        self.data['CT'].append(box1) 
                        self.data['M1'].append(box1)
                        self.data['AA'].append(box2)
                        
                        
                
                if attr['N']:
                    down_loc = dn
                    l_d = draw_data[col-1]['N']
                    r_d = draw_data[col+1]['N']

                    if l_d and r_d:
                        sd_x_l,_ = node_loc[(col-1,0)] 
                        sd_x_r,_ = node_loc[(col+1,0)] 
                        W1 = l_d.W
                        W2 = r_d.W 
                        box1 = Box([sd_x_l,down_loc,sd_x,down_loc+W1])  
                        box2 = Box([sd_x,down_loc,sd_x_r,down_loc+W2])   
                        self.data['AA'].append(box1)  
                        self.data['AA'].append(box2) 
                    elif l_d:
                        sd_x_l,_ = node_loc[(col-1,0)] 
                        sd_x_r = sd_x + tech.CT_E_AA.v + tech.CT_W.hv
                        W1 = l_d.W
                        box1 = Box([sd_x_l,down_loc,sd_x_r,down_loc+W1])   
                        self.data['AA'].append(box1)  
                    elif r_d:
                        sd_x_r,_ = node_loc[(col+1,0)] 
                        sd_x_l = sd_x - tech.CT_E_AA.v - tech.CT_W.hv
                        W1 = r_d.W
                        box1 = Box([sd_x_l,down_loc,sd_x_r,down_loc+W1])   
                        self.data['AA'].append(box1)                      
                    if aa_ct_n:
                        x,y = node_loc[aa_ct_n[0]]
                        w = tech.CT_E_AA.v + tech.CT_W.hv
                        box1 =  Box([x-w,dn,x+w,y+w])
                        self.data['AA'].append(box1)  
                        
                    if pw_ct_n:
                        x,y = node_loc[pw_ct_n[0]]
                        w = tech.CT_W.hv
                        ext = tech.CT_E_AA.v
                        box1 = Box([x-w,tech.ct_dn_rg.p1,x+w,tech.ct_dn_rg.p2])
                        w = tech.CT_W.hv + tech.CT_E_AA.v 
                        ext = tech.CT_E_AA.v
                        box2 = Box([x-w,tech.ct_dn_rg.p1 - ext,x+w,dn])
                        
                        self.data['CT'].append(box1) 
                        self.data['M1'].append(box1)
                        self.data['AA'].append(box2)                  
                        
                    
                    
                #     L = attr['P'].L
                #     W = attr['P'].W
                #     h_l = int(0.5*L)
                #     x,bottom = node_loc[(col,mu)]
                #     box1 =  Box([x-h_l, 
                #                 bottom,  
                #                 x+h_l, 
                #                 tech.gt_up_rg.p2])
                    
                #     box2 =  Box([x-h_l, 
                #                 tp-W,  
                #                 x+h_l, 
                #                 tp])
                    
                #     self.data['GT'].append(box1) 
                #     self.data['AA'].append(box2) 
                # if attr['N']:
                #     L = attr['N'].L
                #     W = attr['N'].W
                #     h_l = int(0.5*L)
                #     x,top = node_loc[(col,md)]
                #     box1 =  Box([x-h_l, 
                #                 tech.gt_dn_rg.p1,  
                #                 x+h_l, 
                #                 top])
                #     box2 =  Box([x-h_l, 
                #                 dn,  
                #                 x+h_l, 
                #                 dn+W])
                        
                #     self.data['GT'].append(box1) 
                #     self.data['AA'].append(box2) 
                
        
        
        
        # self.x = x
        # self.w = mos.W
        # self.l = mos.L
        # # self.net = net

        # self.data['GT'] = []
        # self.data['AA'] = []
        
        # gt_h_range = Range(x, self.l)

        # self.GT_box = Box([gt_h_range.p1, gt_v_range.p1, gt_h_range.p2, gt_v_range.p2 ])
        #    # b7 = Box([p1,w,h,'c'],name='b7') 
        # if mos.T == 'P':
        #     self.AA_box = Box([gt_h_range.p1, aa_range.p1, gt_h_range.p2, aa_range.p1 + self.w])
        # else:
        #     self.AA_box = Box([gt_h_range.p1, aa_range.p2 - self.w, gt_h_range.p2, aa_range.p2])
            
        # # self.AA_box = self.GT_box.copy()


        # self.data['GT'].append(self.GT_box)
        # self.data['AA'].append(self.AA_box)



class AA_SD(Instance):
    def __init__(self, tech, draw_data, aa_cts, pw_pins):        
        super().__init__(tech)
        self.data['AA'] = []

























#
class CT_GT(Instance):
    def __init__(self, tech, loc, mode = 'centre'):
        super().__init__(tech)
        self.loc = loc

        self.data['GT'] = []
        self.data['CT'] = []
        
        if mode == 'centre':
            p = loc
        elif mode == 'left':
            p = (loc[0]+self.tech.CT_W.hv + self.tech.CT_E_GT.v , loc[1])
        elif mode == 'right':
            p = (loc[0]-(self.tech.CT_W.hv + self.tech.CT_E_GT.v ) , loc[1])
        else:
            raise ValueError('mode type error!')
        
        self.CT_box = Box([p,self.tech.CT_W.hv,'c'])
        self.GT_box = Box([p,self.tech.CT_W.hv + self.tech.CT_E_GT.v ,'c'])   

        self.data['GT'].append(self.GT_box)
        self.data['CT'].append(self.CT_box)



        # self.data['AA'] = [self.AA_box]
        

#        



class EdgeRoute(Instance):
    def __init__(self, tech, gt_edges, m1_edges, node_loc, nodes_attr):
        super().__init__(tech)
        #w1 min gt width; w2 cg ct width; w3 mos width
        
        self.data['GT'] = []
        self.data['M1'] = []
        
        for edge in gt_edges:
            n1,n2 = edge
            h_w = tech.GT_W.hv# temp
            v_w = tech.GT_W.hv# temp
            
            if nodes_attr[n1]['is_gt'] and  nodes_attr[n2]['is_gt']:
                mos_l_list = []
                pn1 = nodes_attr[n1]['pn'] 
                pn2 = nodes_attr[n2]['pn'] 
                if len(pn1)>0:
                    if pn1['P']:
                       mos_l_list.append( pn1['P'].L) 
                    if pn1['N']:
                       mos_l_list.append( pn1['N'].L) 
                if len(pn2)>0:
                    if pn2['P']:
                       mos_l_list.append( pn2['P'].L) 
                    if pn2['N']:
                       mos_l_list.append( pn2['N'].L) 
                if len(mos_l_list)>0:
                    h_w = int(0.5*(min(mos_l_list)))
            x1, y1 = node_loc[n1]
            x2, y2 = node_loc[n2]
           
            box =  Box([x1-h_w, y1-v_w, x2+h_w, y2+v_w])
            self.data['GT'].append(box)
        
        for edge in m1_edges:
            n1,n2 = edge
            h_w = tech.M1_W.hv
            v_w = tech.M1_W.hv
            
            
            #TODO: EOL
            t1 = nodes_attr[n1]['eol'] 
            t2 = nodes_attr[n2]['eol'] 

            x1, y1 = node_loc[n1]
            x2, y2 = node_loc[n2]
           
            box =  Box([x1-h_w, y1-v_w, x2+h_w, y2+v_w])
            self.data['M1'].append(box)        



 

       
   
                    
                  
                    
        # self.nodes = list(set(self.nodes))


#
class AA_SD_bk(Instance):
    def __init__(self, tech, mos_type, x, left_gt, right_gt, matrix, ct_aa_nodes):
        #ct num: -1: all, 1.2.3... num of cts 
        #not enough
        
        super().__init__(tech)

        self.data['AA'] = []
        self.data['CT'] = []

        if left_gt:
            left_b = left_gt['AA'][0]
        if right_gt:
            right_b = right_gt['AA'][0]
   
   
        x = matrix[x][0][0]
                
        if left_gt and right_gt:
            bottom = min(left_gt['AA'][0].b, right_gt['AA'][0].b )
            top = max(left_gt['AA'][0].t, right_gt['AA'][0].t )
            if len(ct_aa_nodes) ==1:
                loc = matrix[ct_aa_nodes[0][0]][ct_aa_nodes[0][1]-1]      
                bottom = min(bottom, loc[1] - tech.CT_W.h_v - tech.CT_E_AA.v)
                top    = max(top,    loc[1] + tech.CT_W.h_v + tech.CT_E_AA.v)
            
            box_m = Box([ x - tech.CT_W.h_v - tech.CT_E_AA.v , bottom,
                          x + tech.CT_W.h_v + tech.CT_E_AA.v , top,
                         ])
            box_l = Box([left_b.r, left_b.b, box_m.l, left_b.t])
            box_r = Box([box_m.r, right_b.b, right_b.l, right_b.t])

            self.data['AA'].append(box_m)
            self.data['AA'].append(box_l)
            self.data['AA'].append(box_r)
            
        elif left_gt:
            bottom = left_gt['AA'][0].b
            top = left_gt['AA'][0].t
            if len(ct_aa_nodes) ==1:
                loc = matrix[ct_aa_nodes[0][0]][ct_aa_nodes[0][1]-1]      
                bottom = min(bottom, loc[1] - tech.CT_W.h_v - tech.CT_E_AA.v)
                top    = max(top,    loc[1] + tech.CT_W.h_v + tech.CT_E_AA.v)
            
            box_m = Box([ x - tech.CT_W.h_v - tech.CT_E_AA.v , bottom,
                          x + tech.CT_W.h_v + tech.CT_E_AA.v , top,
                         ])
            box_l = Box([left_b.r, left_b.b, box_m.l, left_b.t])
            # box_r = Box([box_m.r, right_b.b, right_b.l, right_b.t])

            self.data['AA'].append(box_m)
            self.data['AA'].append(box_l)
            # self.data['AA'].append(box_r)
        elif right_gt:
            bottom = right_gt['AA'][0].b 
            top =  right_gt['AA'][0].t 
            if len(ct_aa_nodes) ==1:
                loc = matrix[ct_aa_nodes[0][0]][ct_aa_nodes[0][1]-1]      
                bottom = min(bottom, loc[1] - tech.CT_W.h_v - tech.CT_E_AA.v)
                top    = max(top,    loc[1] + tech.CT_W.h_v + tech.CT_E_AA.v)
            
            box_m = Box([ x - tech.CT_W.h_v - tech.CT_E_AA.v , bottom,
                          x + tech.CT_W.h_v + tech.CT_E_AA.v , top,
                         ])
            # box_l = Box([left_b.r, left_b.b, box_m.l, left_b.t])
            box_r = Box([box_m.r, right_b.b, right_b.l, right_b.t])

            self.data['AA'].append(box_m)
            # self.data['AA'].append(box_l)
            self.data['AA'].append(box_r)
        else:
            pass


        #move to aa sd
        for x,y,z in ct_aa_nodes:
            loc = (matrix[x][y-1])
            ct_box = Box([loc,tech.CT_W.hv,'c'])
            self.data['CT'].append(ct_box)



class POWER(Instance):
    def __init__(self, tech, cells, power_nodes_prop, matrix, aa_range_p, aa_range_n):
        super().__init__(tech)
        self.data['AA'] = []
        self.data['CT'] = []
        self.data['M1'] = []
        
        top_ct = cells.rail_vdd_ct 
        bottom_ct = cells.rail_vss_ct  
       
        
        for node,v in power_nodes_prop.items():
            x,y = matrix[node[0]][node[1]-1]
            if  v['type'] == 'VDD':
               if v['m1_to_power']:
                   ct_box = Box([(x,y), tech.CT_W.h_v,'c'])
                   aa_box = Box([(x,y), tech.CT_W.h_v + tech.CT_E_AA.v,'c'])
                   t1 = tech.CT_E_M1_END.v
                   t2 = tech.CT_E_M1.v
                   m1_box = Box([ct_box.l-t1, ct_box.b-t2, ct_box.r+t1, cells.rail_vdd.p1 ])
               else:
                   ct_box = Box([(x,top_ct.c), tech.CT_W.h_v,'c'])
                   t1 = tech.CT_E_AA.v
                   aa_box = Box([ct_box.l-t1, aa_range_p.p1, ct_box.r+t1, ct_box.t+t1])
                   m1_box = Box([(x,top_ct.c), tech.CT_W.h_v + tech.CT_E_M1.v,'c'])
    
            if v['type'] == 'VSS':
               if v['m1_to_power']:
                   ct_box = Box([(x,y), tech.CT_W.h_v,'c'])
                   aa_box = Box([(x,y), tech.CT_W.h_v + tech.CT_E_AA.v,'c'])
                   t1 = tech.CT_E_M1_END.v
                   t2 = tech.CT_E_M1.v
                   m1_box = Box([ct_box.l-t1, cells.rail_vss.p2, ct_box.r+t1, ct_box.t+t2 ])
               else:
                   ct_box = Box([(x,bottom_ct.c), tech.CT_W.h_v,'c'])
                   t1 = tech.CT_E_AA.v
                   aa_box = Box([ct_box.l-t1, ct_box.b-t1, ct_box.r+t1, aa_range_n.p2])
                   m1_box = Box([(x,bottom_ct.c), tech.CT_W.h_v + tech.CT_E_M1.v,'c'])
                   
                   
            self.data['CT'].append(ct_box)
            self.data['AA'].append(aa_box)
            self.data['M1'].append(m1_box)
        

# class GT_EXT(Instance):
#     def __init__(self, tech, gt_aa ,mode = 'up'):
#         super().__init__(tech)
#         self.gt_aa = gt_aa
#         self.mode = mode

#         self.data['GT'] = []
        
#         gt_box = self.gt_aa.GT_box
        
#         if mode == 'up':
#             self.GT_box = Box([gt_box.l,gt_box.t,gt_box.r,gt_box.t + self.tech.GT_X_AA.v])
#         elif  mode == 'down':
#             self.GT_box = Box([gt_box.l,gt_box.b - self.tech.GT_X_AA.v,gt_box.r,gt_box.b ])
#         else:
#             raise ValueError('mos type error!')        
#         self.data['GT'].append(self.GT_box)





        
def edge_direction(p1,p2):
    if p1[0] == p2[0]:
        if p1[1] > p2[1]:
            direction = ('v','s')
        else:
            direction = ('v','n')
    elif p1[1] == p2[1]:
        if p1[0] > p2[0]:
            direction = ('h','w')
        else:
            direction = ('h','e')
    else:
        raise ValueError('not vertical or horizon line')
    return direction
        





class PATH(Instance):
    def __init__(self, tech, layer, points, width, bgn_ext=0, end_ext=0):
        super().__init__(tech)
        self.layer = layer
        self.points = points
        self.width = width
        self.bgn_ext = bgn_ext
        self.end_ext = end_ext
        self.box = []
      
        for i in range(len(points) - 1):
            p1 = points[i]
            p2 = points[i+1]
            if p1[0] == p2[0]:
                box = Box([p1[0]- half(width),
                           min(p1[1],p2[1]),
                           p1[0]+ half(width),
                           max(p1[1],p2[1]) ])
                self.box.append(box) 
                if p1[1] > p2[1]:
                    direction = 'vs'
                else:
                    direction = 'vn'
            elif p1[1] == p2[1]:
                box = Box([min(p1[0],p2[0]),
                           p1[1]- half(width),
                           max(p1[0],p2[0]), 
                           p1[1]+ half(width) ])
                self.box.append(box) 
                if p1[1] > p2[1]:
                    direction = 'hw'
                else:
                    direction = 'he'
            else:
                raise ValueError('not vertical or horizon line')
    
            if i == 0: #start
                if self.bgn_ext != 0:
                    if direction == 'vn':            
                        box = Box([p1[0] - half(width),
                                   p1[1] - self.bgn_ext,
                                   p1[0] + half(width),
                                   p1[1]] )
                        self.box.append(box) 
                    if direction == 'vs':
                        box = Box([p1[0] - half(width),
                                   p1[1] ,
                                   p1[0] + half(width),
                                   p1[1] + self.bgn_ext] )
                        self.box.append(box) 
                    if direction == 'hw':
                        box = Box([p1[0],
                                   p1[1]- half(width),
                                   p1[0]+self.bgn_ext, 
                                   p1[1]+ half(width) ])
                        self.box.append(box) 
                    if direction == 'he':
                        box = Box([p1[0]- self.bgn_ext,
                                   p1[1]- half(width),
                                   p1[0], 
                                   p1[1]+ half(width) ])
                        self.box.append(box)                
            if i + 1 == len(points) - 1: #end
                if self.end_ext != 0:
                    if direction == 'vn':
                        box = Box([p2[0] - half(width),
                                   p2[1] ,
                                   p2[0] + half(width),
                                   p2[1] + self.bgn_ext] )
                        self.box.append(box) 
                    if direction == 'vs':
                        box = Box([p2[0] - half(width),
                                   p2[1] - self.end_ext,
                                   p2[0] + half(width),
                                   p2[1]] )
                        self.box.append(box) 
                    if direction == 'hw':
                        box = Box([p2[0]- self.end_ext,
                                   p2[1]- half(width),
                                   p2[0], 
                                   p2[1]+ half(width) ])
                        self.box.append(box)   
                    if direction == 'he':
                        box = Box([p2[0],
                                   p2[1]- half(width),
                                   p2[0]+self.end_ext, 
                                   p2[1]+ half(width) ])
                        self.box.append(box) 
            else:
                box =  Box([p2[0]- half(width),
                            p2[1]- half(width),
                            p2[0]+ half(width), 
                            p2[1]+ half(width) ])  
                self.box.append(box)   
        self.data[layer] = self.box 























        
                
                
                
#        
class AA_ABUT(Instance):
    def __init__(self, tech, gt_left, gt_right, if_ct = False, mode = '1'):
        super().__init__(tech)
        self.gt_left = gt_left
        self.gt_right = gt_right        
        self.if_ct = if_ct
    
        self.data['AA'] = []
    
        
        
        box1 = self.gt_left.AA_box
        box2 = self.gt_right.AA_box
        
        if box1.b == box2.b and box1.t == box2.t:
            self.AA_box1 = Box([box1.r,box1.b,box2.l,box2.t])
            # assert self.AA_box1.w >= tech.
            self.data['AA'].append(self.AA_box1)
            
            self.CT_centerx =half(box2.l - box1.r) + box1.r
            self.AA_box = self.AA_box1   
            
        elif box1.b <= box2.b and box1.t >= box2.t:
            self.AA_box1 = Box([box1.r,
                                box1.b,
                                box1.r + tech.aa_width1,
                                box1.t])
            self.AA_box2 = Box([box1.r + tech.aa_width1,
                                box2.b,
                                box2.l,
                                box2.t])
            self.data['AA'].append(self.AA_box1)
            self.data['AA'].append(self.AA_box2)
            self.CT_centerx = box1.r + tech.CT_S_GT.v + tech.CT_W.hv
            self.AA_box = self.AA_box1 
        elif box1.b >= box2.b and box1.t <= box2.t:
            self.AA_box1 = Box([box1.r,box1.b,box1.r + tech.GT_S_LAA_GT.v, box1.t])
            self.AA_box2 = Box([box1.r + tech.GT_S_LAA_GT.v,box2.b,box2.l,box2.t])
            self.data['AA'].append(self.AA_box1)
            self.data['AA'].append(self.AA_box2)
            self.CT_centerx = half(box2.l - box1.r) + box1.r
            self.AA_box = self.AA_box2
        elif (box1.b < box2.b and box1.t < box2.t) or ( box1.b > box2.b and box1.t > box2.t):
            self.AA_box1 = Box([box1.r,
                                box1.b,
                                box1.r + tech.GT_S_LAA_GT.v, 
                                box1.t])
            self.AA_box2 = Box([box1.r + tech.GT_S_LAA_GT.v,
                                min(box1.b,box2.b),
                                box1.r + tech.GT_S_LAA_GT.v + tech.min_width,
                                max(box1.t,box2.t)])
            self.AA_box3 = Box([box1.r + tech.GT_S_LAA_GT.v + tech.min_width,
                                box2.b,
                                box2.l, 
                                box2.t])            
            self.data['AA'].append(self.AA_box1)
            self.data['AA'].append(self.AA_box2)
            self.data['AA'].append(self.AA_box3)
            self.CT_centerx = half(box2.l - box1.r) + box1.r
            self.AA_box = self.AA_box2 
        else:
            print(box1,box2)
            raise ValueError
        







class GT_middle(Instance):
    def __init__(self,tech,loc,w,l,net,mos_t = 'p'):
        super().__init__(tech)
        self.loc = loc
        self.w = w
        self.l = l
        self.net = net
        self.mos_t = mos_t
        
        
        self.left = None
        self.right = None
        self.ext =None
        self.int = None
        
    def create(self):
        self.data['GT'] = []
        self.data['AA'] = []
        if self.mos_t == 'p':
            GT_box = Box([(self.loc[0],self.loc[1] - self.w),self.l,self.w])
            self.data['GT'].append(GT_box)
            self.data['AA'].append(GT_box)
            
        elif self.mos_t == 'n':
            GT_box = Box([(self.loc[0],self.loc[1]),self.l,self.w])
            self.data['GT'].append(GT_box)
            self.data['AA'].append(GT_box)
        else:
            raise ValueError('mos type error!')

        self.GT_box = GT_box
        


class GT_ext(Instance):
    def __init__(self, tech, gt_middle ,mos_t = 'p'):
        super().__init__(tech)
        self.gt_middle = gt_middle
        self.mos_t = mos_t
    

    def create(self):
        self.data['GT'] = []
        
        gt_box = self.gt_middle.GT_box
        
        if self.mos_t == 'p':
            self.GT_box = Box([gt_box.l,gt_box.t,gt_box.r,gt_box.t + self.tech.GT_X_AA.v])
        elif self.mos_t == 'n':
            self.GT_box = Box([gt_box.l,gt_box.b - self.tech.GT_X_AA.v,gt_box.r,gt_box.b ])
        else:
            raise ValueError('mos type error!')        
        self.data['GT'].append(self.GT_box)
class GT_int:
    pass



def cal_gt_ct_space(tech,p1,n1, gt_metal=False):
    
    t1 = tech.CT_S_GT.v + max(half(p1.L),half(n1.L))+ tech.CT_W.hv
    t2 = tech.CT_W.hv + tech.CT_E_M1.v + half(tech.M1_S.v)
    t = max(t1,t2)
    if gt_metal:    
        t3 = 2*tech.CT_E_M1.v + tech.M1_S.v + tech.CT_W.v
        t = max(t,t3)
    if p1.W < tech.min_width or n1.W < tech.min_width:
        t4 = tech.CT_W.hv + tech.CT_E_AA.v + tech.GT_S_LAA_GT.v + max(half(p1.L),half(n1.L)) 
        t = max(t,t4)   
    
    return t

def cal_gt_gt_space(tech,p1,n1,p2,n2, gt_metal=True, aa_metal=True, aa_ct=True, diff_vddss=False):
   
    '''
        self.gt_space1 = self.CT_S_GT.v + self.CT_W.v + self.CT_S_GT.v
        self.gt_space2 = self.GT_S.v
        self.gt_space3 = self.GT_S_LAA_GT.v + self.aa_width1  #abut
        self.gt_space4 = 2*self.GT_S_LAA_GT.v + self.min_width  #abut
    '''    
    # space = 0
    channel1 = max(p1.L,n1.L)
    channel2 = max(p2.L,n2.L)
 
    s1 = half(channel1+channel2) + tech.gt_space2
    s2 = half(channel1+channel2) + tech.gt_space1
    s3 = half(channel1+channel2) + tech.gt_space3
    s4 = half(channel1+channel2) + tech.gt_space4
    s5 = tech.CT_W.v + tech.M1_S.v + tech.CT_E_M1.v*2
    s6 = tech.CT_W.v*2 + tech.M1_S.v*2 + tech.CT_E_M1.v*4
    # s2 = half(channel1+channel2) +   
    if not(aa_ct):
        if gt_metal:
            space = max(s1,s5)
        else:
            space = s1
    else:
        space = max(s1,s2)
        if (p1.W != p2.W) or (n1.W != n2.W):#abutment and align
            space = max(space,s3)
        
        if p2.W < tech.min_width or n2.W < tech.min_width or diff_vddss:
            space = max(space,s4)   
    
        if gt_metal:
            space = max(space,s5)
        if aa_metal and gt_metal:
            space = max(space,s6)


    return space



        







