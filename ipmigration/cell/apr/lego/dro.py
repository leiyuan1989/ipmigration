# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 10:59:38 2024

@author: leiyuan
"""

#design rule orientation

class DRO:
    def __init__(self):
        pass
    
    
#TODO move to dro
class ColSpace:
    def __init__(self, tech, col_type, right_col_type, pn, pn_right):
        self.tech = tech
        self.space = {}
        self.col_type = col_type
        self.right_col_type = right_col_type

        
        
        mos_l = []
        if len(pn) >0:
            if pn['P']: 
                mos_l.append(pn['P'].L)
            if pn['N']:
                mos_l.append(pn['N'].L)
        if len(pn_right) >0:
            if pn_right['P']: 
                mos_l.append(pn_right['P'].L)
            if pn_right['N']:
                mos_l.append(pn_right['N'].L)                
        self.mos_l = mos_l
        
                    
        if col_type==1 and right_col_type==2:
            #TODO  now it is only 3AA box method, not the best
            self.space['GT_CT'] = tech.GT_S_LAA_GT.v + tech.CT_E_AA.v + int(0.5*(max(self.mos_l))) + tech.CT_W.h_v
        elif col_type==2 and right_col_type==1:
            self.space['GT_CT'] = tech.GT_S_LAA_GT.v + tech.CT_E_AA.v + int(0.5*(max(self.mos_l))) + tech.CT_W.h_v
        elif col_type==1 and right_col_type==0:
            self.space['GT_CT'] = tech.M1_S.v + tech.M1_W.v
        elif col_type==0 and right_col_type==1:
            self.space['GT_CT'] = tech.M1_S.v + tech.M1_W.v
        else:
            print(col_type,right_col_type)
            raise ValueError 
    
    def add_M1_S_rule(self,eol_num=0):
        self.space['M1_S'] = self.tech.M1_S.v + self.tech.M1_W.v + eol_num*self.tech.CT_E_M1_END.v
    def add_GT_S_rule(self):
                
        gt_w2 = self.tech.CT_GT_W_half
        
        if self.col_type == 2 or self.right_col_type == 2:
            gt_w3 = int(0.5*(max(self.mos_l)))
            self.space['GT_S'] = gt_w2  + gt_w3 + self.tech.GT_S.v
        else:
            self.space['GT_S'] = gt_w2  + gt_w2 + self.tech.GT_S.v
           
    
    def __repr__(self):
        return str(self.space)

    @property
    def max_space(self):
        return max(self.space.values())
        

        # return ctaa gtaa nodetolabeldict, edge_list with color lines for detail route    