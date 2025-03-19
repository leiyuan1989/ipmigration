# -*- coding: utf-8 -*-
"""

@author: leiyuan
"""

from z3 import Optimize
from z3 import Int, Bool, Or, And, Not, Distinct, Implies,is_true,sat

from itertools import combinations, chain
import itertools

import math
import time

import logging
logger = logging.getLogger(__name__)



class Placer:
    def __init__(self,sub_ckts):
        self.sub_ckts = sub_ckts
        self.sub_ckts_num = {k:i for i,k in enumerate(sub_ckts)}
        self.sub_ckts_num_r = {i:k for i,k in enumerate(sub_ckts)}
        self.cal_ext_net_mat()
        
    def cal_ext_net_mat(self):
        ext_net_mat = [[0 for _ in range(len(self.sub_ckts))] for _ in range(len(self.sub_ckts))]
        ext_net_mat_dict = {}
        for k1,v1 in self.sub_ckts.items():
            for k2,v2 in self.sub_ckts.items():
                if k1 != k2:
                    ext_net_mat_dict[(k1,k2)] = self.extract_ext_nets(v1.net_map, v2.net_map)
    
        self.ext_net_mat_dict = ext_net_mat_dict
        for k,v in ext_net_mat_dict.items():
            n1 = self.sub_ckts_num[k[0]]
            n2 = self.sub_ckts_num[k[1]]
            ext_net_mat[n1][n2] = len(v)
        self.ext_net_mat = ext_net_mat

        
    def extract_ext_nets(self,net_map1,net_map2):
        ext_nets = []
        for k1,v1 in net_map1.items():
            for k2,v2 in net_map2.items():
                if k1 != 'VDD' and k1 != 'VSS':
                    if v1 == v2:
                        if not(v1 in ext_nets):
                            ext_nets.append(v1)
        return ext_nets

    def find_opt_perm(self,ckt_type):        
        init_queue1 = [['clk'],['inputs','sync'],
                      ['cross1'],['backtrack1'],
                      ['out_ECK','out_Q'],['out_QN']]
        init_queue2 = [['inputs','sync'],['sesi'],
                      ['cross1'],['backtrack1'],['clk'],
                      ['cross2'],['backtrack2'],
                      ['out_Q'],['out_QN']]
        
        # ['ff', 'scanff', 'latch', 'clockgate']
        if ckt_type in ['latch','clockgate']:
            init_queue = init_queue1
        else:
            init_queue = init_queue2
            
        queue = {}
        inv_l = []
        for ckt_name in self.sub_ckts:
            is_search = False
            for i, ckt_l in enumerate(init_queue):
                if ckt_name in ckt_l:
                    queue[ckt_name] = i
                    is_search = True
            if not(is_search):
                assert 'ininv' in ckt_name
                inv_l.append(ckt_name)
        queue = dict(sorted(queue.items(), key=lambda item: item[1]))
        queue = list(queue.keys())
        #TODO, insert inverter by name is another solution?
        for inv in inv_l:
            for ckt_name in queue:
                if len(self.ext_net_mat_dict[(inv,ckt_name)])>0:
                    index = queue.index(ckt_name)
                    queue.insert(index, inv)
                    break                    
        return queue



        

