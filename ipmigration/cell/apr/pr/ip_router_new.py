# -*- coding: utf-8 -*-
"""
@author: leiyuan
"""
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from collections import OrderedDict
from itertools import combinations

import z3
from z3 import Optimize,Solver
from z3 import Int, Bool, Or, And, Not, Distinct, If, is_true,sat,Abs

from ipmigration.cell.apr.pr.placement import Pin

DEBUG=False
PLOT =False

pin_locs = {
            6:{'gtc':[[2,3],  [0,5]],'gtp':[[3],  [5]],'gtn':[[2],  [0]],'aap':[[5,4,3],[]],'aan':[[0,1],[]]},
            7:{'gtc':[[2,3,4],[0,6]],'gtp':[[3,4],[6]],'gtn':[[2],  [0]],'aap':[[6,5,4],[]],'aan':[[0,1,2],[]]},
            8:{'gtc':[[3,4],  [0,7]],'gtp':[[4,5],[7]],'gtn':[[2,3],[0]],'aap':[[7,6,5],[]],'aan':[[0,1,2],[]]}
            }

class PinLoc:
    def __init__(self,v_tracks):
        self.pin_loc = pin_locs[v_tracks]
        # self.gt_c =  pin_loc['gt_c']
        # self.gtp =  pin_loc['gt_p']
        # self.gtn =  pin_loc['gt_n']
        # self.gtm =  pin_loc['gt_m']
        # self.aap =  pin_loc['aap_range']
        # self.aan =  pin_loc['aan_range']
        
    def get(self,name,level=0):
        assert name in self.pin_loc
        loc = self.pin_loc[name]
        possible_loc = []
        for i,t in enumerate(loc):
            possible_loc += t
            if i >= level:
                break
        return possible_loc
            
            
        
        
        
        
        
#Integer Programming, IP0
class IPRouter:
    #satisfiability modulo theories 
    def __init__(self,ckt, placement, vtracks):
        self.ckt = ckt
        self.vtracks = vtracks
        self.pl = PinLoc(vtracks)
        self.placement = placement
        #process placement
        self.placement.process(ckt)        
        # self.grid_size = (len(self.placement.pins) + 1,self.vtracks)#?
        

        
    def create_graph(self, level=0):
        #level 0, 1, maybe 2, if larger, routability is good but layout is ugly.
        ckt=self.ckt
        
        col_attr = {} #Pin #block nodes availables nodes
    
        num=len(self.placement.pins)
        idx = 0
        # for idx, (p,n) in range(num):
        while(idx<num):
            p,n = self.placement.pins[idx]
            if idx < num-1:
                next_p,next_n = self.placement.pins[idx+1]         
            else:
                next_p=None
                next_n=None
            if idx < num-2:
                next2_p,next2_n = self.placement.pins[idx+2]         
            else:
                next2_p=None
                next2_n=None
            
            if p and n:
                if p.is_gate and n.is_gate:
                    if p.net == n.net:
                        pin = Pin.merge(p, n)
                        pin.set_locs(self.pl.get('gtc',level))
                        col_attr[idx] = {'pin':pin,'block':[]}
                        idx += 1
                    else:       
                        #cross gate
                        if (p.net == next2_n.net and n.net == next2_p.net) and (p.net != n.net):
                            #idx ,idx+1, idx+2,idx+3
                
                
                
                else:
                    #p and n are aa
                    if p in self.placement.abut_pins:
                        pass
                    if p in self.placement.vdd_pins:
                        pass
                    if p in self.placement.o_pins:
                        pass
                      
            elif p:
                #only p
                pass
            
            elif n:
                #only n
            
            else:
                pass                


        

    
        G = nx.grid_2d_graph(4, 4)
        node_attributes = {
            (1, 1): {'a': '1', 'b': 2},
            (0, 0): {'a': '0', 'b': 0},
            (2, 3): {'a': '3', 'b': 5},
            # 可以继续添加更多节点的属性
        }
        
        # 为节点添加属性
        nx.set_node_attributes(G, node_attributes)
        '''            
            self.pins = pins
            self.nets = nets
            self.vdd_pins = vdd_pins
            self.vss_pins = vss_pins
            self.nets_route = nets_route
            self.abut_pins = abut_pins
            self.cgg_pins = cgg_pins
            self.caa_pins = caa_pins
            self.i_pins = i_pins
            self.o_pins = o_pins        
        '''
                


        
    def route(self):
         
        return True
        
        
def find_subgraph_with_nodes(self):
     
    return True        
    
    
def visualize_pins(self):
     
    return True       
        
        
        
        
        
        
        
        
        
        
        
        