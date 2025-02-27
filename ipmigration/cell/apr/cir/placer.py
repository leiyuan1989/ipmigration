# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 12:03:26 2024

@author: leiyuan
"""


# -*- coding: utf-8 -*-
"""

@author: leiyuan
"""

from z3 import Optimize
from z3 import Int, Bool, Or, And, Not, Distinct, Implies,is_true,sat, Sum

from src.pr.basic_placer import Placer, Placement


from itertools import combinations, chain

import math
import time

import logging

from src.basic.circuit import Ckt

from ortools.sat.python import cp_model

logger = logging.getLogger(__name__)



class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, variables: list[cp_model.IntVar]):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0

    def on_solution_callback(self) -> None:
        self.__solution_count += 1
        for v in self.__variables:
            print(f"{v}={self.value(v)}", end=" ")
        print()

    @property
    def solution_count(self) -> int:
        return self.__solution_count


def pn_relation(pmos,nmos):
    p_g = pmos.G
    p_s = pmos.S
    p_d = pmos.D
    n_g = nmos.G
    n_s = nmos.S
    n_d = nmos.D   
    common_g = int(p_g == n_g)
    
    if (p_s == n_s) and (p_d == n_d):
        common_ds1 = 2
    elif(p_s == n_s) or (p_d == n_d):
        common_ds1 = 1
    else:
        common_ds1 = 0
    
    if (p_s == n_d) and (p_d == n_s):
        common_ds2 = 2
    elif(p_s == n_d) or (p_d == n_s):
        common_ds2 = 1
    else:
        common_ds2 = 0        
    
    #6 = 4 + 2 5 = 4 + 1 4 = 4 + 0  2 = 0 + 2 1 = 0 + 1 0 = 0 + 0
    return 4*common_g + max(common_ds1,common_ds2)
        


def pn_pairs(pmos_list, nmos_list):
    pairs_score = {}
    mos_list = pmos_list +  nmos_list
    for p in pmos_list:
        for n in nmos_list:
            pairs_score[(p,n)] = pn_relation(p, n)
    
    pn_pairs = []
    # paired = []
    
    pairs_score = sorted(pairs_score.items(), key=lambda x: x[1],reverse=True)    
    for pair, score in pairs_score:
        if score >=2:
            p,n  = pair
            if (p in pmos_list) and (n in nmos_list):
                pn_pairs.append(pair)
                # pmos_list.remove(p)
                # nmos_list.remove(n)

    return pn_pairs



def smt_place(pmos_list, nmos_list, ports):
    solver = Optimize()
    pairs = pn_pairs(pmos_list, nmos_list)
    
    
    
    
    # create matrix 
    pmos_loc_x = {t: Int(t.name + '_x') for t in pmos_list}
    nmos_loc_x = {t: Int(t.name + '_x') for t in nmos_list}
    pmos_loc_y = {t: Int(t.name + '_y') for t in pmos_list}
    nmos_loc_y = {t: Int(t.name + '_y') for t in nmos_list}   
    
    pmos_loc = {t: (pmos_loc_x[t],pmos_loc_y[t]) for t in pmos_list}
    nmos_loc = {t: (nmos_loc_x[t],nmos_loc_y[t]) for t in nmos_list}
    
    
    
    # Constraint 1: Positions are bounded.       
    for x in pmos_loc_x.values():
        solver.add(x >= 1)
    for y in pmos_loc_y.values():
        solver.add(y >= 1)       
        solver.add(y <= 4)
    for x in nmos_loc_x.values():
        solver.add(x >= 1)
    for y in nmos_loc_y.values():
        solver.add(y >= 5)       
        solver.add(y <= 8)        
        
    # Constraint 2: No same positions
    for a, b in combinations(pmos_loc.values(), 2):
        print('xx',a,b)
        solver.add(Implies(a[0] == b[0], a[1] != b[1]))
        solver.add(Implies(a[1] == b[1], a[0] != b[0]))
    
    # Constraint 3: Not neighbor if not abutment 
    for d1 in pmos_list:
        for d2 in pmos_list:
            if d1 != d2:
                if not(d1.if_abutment(d2)):
                    a = pmos_loc[d1]
                    b = pmos_loc[d2]
                    solver.add(Implies(a[1] == b[1], a[0] != b[0] + 1))
                    solver.add(Implies(a[1] == b[1], a[0] != b[0] - 1))

    for d1 in nmos_list:
        for d2 in nmos_list:
            if d1 != d2:
                if not(d1.if_abutment(d2)):
                    a = pmos_loc[d1]
                    b = pmos_loc[d2]
                    solver.add(Implies(a[1] == b[1], a[0] != b[0] + 1))
                    solver.add(Implies(a[1] == b[1], a[0] != b[0] - 1))
 
    
    # Constraint 4: Port abutment
    #{'P': ['N_13', 'N_14'], 'N': ['N_21', 'N_23']}
    
    
    
    
    # Constraint : PN pair, not a must 
    solver.push() #backtrack point
    for p,n in pairs:
        xn,yn = nmos_loc[n]
        xp,yp = pmos_loc[p]
        solver.add(xn == xp )
        solver.add(yn == yp+4 ) #

    
    print(solver)
        
    #if unsat pop, elif sat pass 
        
    # for x in nmos_loc.values():
    #     solver.add(x >= 0)
    #     solver.add(x < max_pos)
    #     for x1 in block_pos:
    #         solver.add(x != x1)
    
    
    
    
    # block_pos = []
    # max_pos = len(placement) 
    # for i,t in enumerate(placement):
    #     if t != [None,None]:
    #         block_pos.append(i)
    
    # pmos_side = {}
    # nmos_side = {}
    
    # not_abut_net = ['VDD','VSS']
    
    # for pos in block_pos:
    #     if placement[pos - 1] == [None,None] :
    #         pmos_side[placement[pos][0]] = pos
    #         nmos_side[placement[pos][1]] = pos
    #         # if placement[pos][0].S == placement[pos][1].S:
    #         #     not_abut_net.append(placement[pos][0].S)
 
    #     if placement[pos + 1] == [None,None]:
    #         pmos_side[placement[pos][0]] = pos
    #         nmos_side[placement[pos][1]] = pos           
    #         # if placement[pos][0].D == placement[pos][1].D:
    #         #     not_abut_net.append(placement[pos][0].D)

    

    # # Create symbols for transistor positions.
    # pmos_loc = {t: Int(t.name) for t in pmos_list}
    # nmos_loc = {t: Int(t.name) for t in nmos_list}
    # # # Create boolean symbols for transistor flips.
    # pmos_flipped = {t: Bool(t.name+'_flip') for t in pmos_list}     
    # nmos_flipped = {t: Bool(t.name+'_flip') for t in nmos_list}    


    # # Constraint 1: No same x positions
    # d_pmos = Distinct(list(pmos_loc.values()))
    # d_nmos = Distinct(list(nmos_loc.values()))      
    # solver.add(d_pmos)
    # solver.add(d_nmos)  
    

    # # Constraint 2: Positions are bounded.       
    # for x in pmos_loc.values():
    #     solver.add(x >= 0)
    #     solver.add(x < max_pos)
    #     for x1 in block_pos:
    #         solver.add(x != x1)
     
    # for x in nmos_loc.values():
    #     solver.add(x >= 0)
    #     solver.add(x < max_pos)
    #     for x1 in block_pos:
    #         solver.add(x != x1)
    
    
    
    # # Constraint 3: Abutment, Diffusion sharing
    
    # ckt_pos = Ckt(name = 'pmos_list',devices= pmos_list + list(pmos_side.keys()))
    # ckt_pos.extract_nets()
    # ckt_nos = Ckt(name = 'nmos_list',devices= nmos_list + list(nmos_side.keys()))
    # ckt_nos.extract_nets()
    # nets_abutment_p = {}
    # nets_abutment_n = {}
    # for net, ds in  ckt_pos.nets_cdl.items():
    #     if len(ds) == 2 and not(net in not_abut_net):
    #         t1 = ds[0][1]
    #         t2 = ds[1][1]

    #         if ((t1 == 'D') or (t1 == 'S')) and ((t2 == 'D') or (t2 == 'S')):
    #             nets_abutment_p[net] = [ds[0][0],ds[1][0]]    
    # for net, ds in  ckt_nos.nets_cdl.items():
    #     if len(ds) == 2  and not(net in not_abut_net):
    #         t1 = ds[0][1]
    #         t2 = ds[1][1]

    #         if ((t1 == 'D') or (t1 == 'S')) and ((t2 == 'D') or (t2 == 'S')):
    #             nets_abutment_n[net] = [ds[0][0],ds[1][0]]      
    

    # #3.1 device must neighbor of cross
    
    # for  net, d in nets_abutment_p.items():


    #     if d[0] in pmos_loc and d[1] in pmos_side:
    #         solver.add(Or(pmos_loc[d[0]] == pmos_side[d[1]] + 1,  pmos_loc[d[0]] == pmos_side[d[1]] - 1  ))
    #     elif d[0] in pmos_side and d[1] in pmos_loc:
    #         solver.add(Or(pmos_loc[d[1]] == pmos_side[d[0]] + 1,  pmos_loc[d[1]] == pmos_side[d[0]] - 1  ))
    #     elif d[0] in pmos_loc and d[1] in pmos_loc:
    #         solver.add(Or(pmos_loc[d[0]] == pmos_loc[d[1]] + 1,  pmos_loc[d[0]] == pmos_loc[d[1]] - 1  ))
  
    # for  net, d in nets_abutment_n.items():
    #     if d[0] in nmos_loc and d[1] in nmos_side:
    #         solver.add(Or(nmos_loc[d[0]] == nmos_side[d[1]] + 1,  nmos_loc[d[0]] == nmos_side[d[1]] - 1  ))
    #     elif d[0] in nmos_side and d[1] in nmos_loc:
    #         solver.add(Or(nmos_loc[d[1]] == nmos_side[d[0]] + 1,  nmos_loc[d[1]] == nmos_side[d[0]] - 1  ))
    #     elif d[0] in nmos_loc and d[1] in nmos_loc:
    #         solver.add(Or(nmos_loc[d[0]] == nmos_loc[d[1]] + 1,  nmos_loc[d[0]] == nmos_loc[d[1]] - 1  ))
    
    
    # #3.2 not abutment devices cannot be neighbor
    # for d1 in pmos_list:
    #     for d2 in pmos_list:
    #         if d1 != d2:
    #             if not(d1.if_abutment(d2)):
    #                 solver.add(pmos_loc[d1] != pmos_loc[d2] + 1)
    #                 solver.add(pmos_loc[d1] != pmos_loc[d2] - 1)
    # for d1 in nmos_list:
    #     for d2 in nmos_list:
    #         if d1 != d2:
    #             if not(d1.if_abutment(d2)):
    #                 solver.add(nmos_loc[d1] != nmos_loc[d2] + 1)
    #                 solver.add(nmos_loc[d1] != nmos_loc[d2] - 1)
 
    # if pn_constraint:
    #     for p,n in pairs:
    #         xn = nmos_loc[n]
    #         xp = pmos_loc[p]
    #         solver.add(xn == xp)


    # if solver.check() == sat:
    #     model = solver.model()
  
    #     return [True, model]
    
    
    # else:
    #     if pn_constraint:
    #         return smt_place(pmos_list, nmos_list, placement, pn_constraint = False)
    #     else:   
    #         return [False, None]

