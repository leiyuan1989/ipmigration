# -*- coding: utf-8 -*-
"""

@author: leiyuan
"""

from z3 import Optimize
from z3 import Int, Bool, Or, And, Not, Distinct, Implies,is_true,sat

from src.schema.basic import Transistor
from src.pr.basic_placer import Placer, Placement


from itertools import combinations, chain

import math
import time

import logging
logger = logging.getLogger(__name__)




class SMTPlacer(Placer):
    #satisfiability modulo theories 
    def __init__(self, load, folder):
        super().__init__(load, folder)
        self.facing_gates_must_have_same_net = True
        self.minimize_net_bounding_boxes = True
    
    def loss(self):
        pass
    
    
    
    def _place(self, pmos_list, nmos_list, cell_width, pairs, vertical_tracks_pmos = 1, vertical_tracks_nmos = 1):
        #TODO find relationship before run this and try decrease the running time
        
        # Wrapper arount solver.add

            
        assert len(nmos_list) <= cell_width 
        assert len(pmos_list) <= cell_width 
        #how to add some constraints to generate more 
        # transistors = []
        # transistors.extend(nmos_list)
        # transistors.extend(pmos_list)

        solver = Optimize()

        # Create symbols for transistor positions.
        pmos_loc = {t: (Int("pmos_{}_x".format(t.name)), Int("pmos_{}_y".format(t.name))) for t in pmos_list}
        nmos_loc = {t: (Int("nmos_{}_x".format(t.name)), Int("nmos_{}_y".format(t.name))) for t in nmos_list}
        # Create boolean symbols for transistor flips.
        pmos_flipped = {t: Bool("pmos_{}_flipped".format(t.name)) for t in pmos_list}     
        nmos_flipped = {t: Bool("nmos_{}_flipped".format(t.name)) for t in nmos_list}          
        
        # transistor_positions = {t: (Int("transistor_{}_x".format(i)), Int("transistor_{}_y".format(i)))
        #                         for i, t in enumerate(transistors)}
        # # Create boolean symbols for transistor flips.
        # # Each transistor can be flipped (source/drain swapped).
        # transistor_flipped = {t: Bool("transistor_{}_flipped".format(i))
        #                       for i, t in enumerate(transistors)}

        # Constraint 1: Positions are bounded.      
        for x, y in pmos_loc.values():
            # Add bounds on positions.
            solver.add(x > 0)# begin from 1
            solver.add(y > 0)
            # Add upper bounds on transistor positions.
            solver.add(x <= cell_width)
            solver.add(y <= vertical_tracks_pmos)
        for x, y in nmos_loc.values():
            # Add bounds on positions.
            solver.add(x > 0)
            solver.add(y > 0)
            # Add upper bounds on transistor positions.
            solver.add(x <= cell_width) # <=
            solver.add(y <= vertical_tracks_nmos)            
            
        # Constraint 2: No same x positions
        d_pmos = Distinct([x for x,y in pmos_loc.values()])
        d_nmos = Distinct([x for x,y in nmos_loc.values()])       
        solver.add(d_pmos)
        solver.add(d_nmos)        

        # Constraint 3: PN pair
        # for tn in nmos_list:
        #     for tp in pmos_list:
        #         if tn.gate_net == tp.gate_net:
        #             (xn, yn) = nmos_loc[tn]
        #             (xp, yp) = pmos_loc[tp]
        #             same_x = xn == xp
        #             solver.add_soft(same_x,weight=3)
        for p,n in pairs:
            (xn, yn) = nmos_loc[n]
            (xp, yp) = pmos_loc[p]
            # print(xn,xp,p,n)
            
            solver.add(xn == xp)
        # print(solver)                  
        # Constraint 4: Abutment, Diffusion sharing
        # If two transistors are placed side-by-side then the abutted sources/drain nets must match.

        # Loop through all potential (left, right) pairs.
        for a, b in combinations(pmos_list, 2):
            for t_left, t_right in [(a, b), (b, a)]:
                xl, yl = pmos_loc[t_left]
                xr, yr = pmos_loc[t_right]

                # Checks if t_left is left neighbor of t_right.
                are_neighbors = And(
                    yl == yr,
                    xl + 1 == xr
                )

                # Go through all combinations of flipped transistors
                # and check if they are allowed to be directly abutted if flipped
                # in a specific way.
                flip_combinations = [[False, False], [False, True], [True, False], [True, True]]
                for flip_l, flip_r in flip_combinations:
                    l = t_left.flipped() if flip_l else t_left
                    r = t_right.flipped() if flip_r else t_right

                    if l.drain_net != r.source_net:
                        # Drain/Source net mismatch.
                        # In case the transistors are flipped that way,
                        # they are not allowed to be direct neighbors.
                        solver.add(
                            Implies(
                                And(pmos_flipped[t_left] == flip_l,
                                    pmos_flipped[t_right] == flip_r),
                                Not(are_neighbors)
                            )
                        )
        for a, b in combinations(nmos_list, 2):
            for t_left, t_right in [(a, b), (b, a)]:
                xl, yl = nmos_loc[t_left]
                xr, yr = nmos_loc[t_right]

                # Checks if t_left is left neighbor of t_right.
                are_neighbors = And(
                    yl == yr,
                    xl + 1 == xr
                )

                # Go through all combinations of flipped transistors
                # and check if they are allowed to be directly abutted if flipped
                # in a specific way.
                flip_combinations = [[False, False], [False, True], [True, False], [True, True]]
                for flip_l, flip_r in flip_combinations:
                    l = t_left.flipped() if flip_l else t_left
                    r = t_right.flipped() if flip_r else t_right

                    if l.drain_net != r.source_net:
                        # Drain/Source net mismatch.
                        # In case the transistors are flipped that way,
                        # they are not allowed to be direct neighbors.
                        solver.add(
                            Implies(
                                And(nmos_flipped[t_left] == flip_l,
                                    nmos_flipped[t_right] == flip_r),
                                Not(are_neighbors)
                            )
                        )
        
        # Constraint 5: Route Congestion
        # Extract all net names.
        nets = set(chain(*(t.terminals() for t in pmos_list + nmos_list)))  #clear vdd vss

        # Create net bounds. This will be used to optimize
        # the bounding box perimeter of the nets (for wiring length optimization).
        net_max_x = {net: Int("net_max_x_{}".format(net))
                     for net in nets}

        net_min_x = {net: Int("net_min_x_{}".format(net))
                     for net in nets}

        net_max_y = {net: Int("net_max_y_{}".format(net))
                     for net in nets}

        net_min_y = {net: Int("net_min_y_{}".format(net))
                     for net in nets}

        for t in pmos_list:
            x, y = pmos_loc[t]

            # TODO: Net positions dependent on transistor terminal.
            #       Now, the net position equals the transistor position.
            #       Make it dependent on the actual terminal (drain, gate, source).
            #       Also depends on transistor flips.
            for net in t.terminals():
                solver.add(x <= net_max_x[net])
                solver.add(x >= net_min_x[net])
                # add_assertion(y <= net_max_y[net])
                # add_assertion(y >= net_min_y[net])

        for t in nmos_list:
            x, y = nmos_loc[t]

            # TODO: Net positions dependent on transistor terminal.
            #       Now, the net position equals the transistor position.
            #       Make it dependent on the actual terminal (drain, gate, source).
            #       Also depends on transistor flips.
            for net in t.terminals():
                solver.add(x <= net_max_x[net])
                solver.add(x >= net_min_x[net])
                # add_assertion(y <= net_max_y[net])
                # add_assertion(y >= net_min_y[net])

        # Optiimization goals
        # Note: z3 uses lexicographic priorities of objectives by default.
        # Here, the cell width is optimized first.
        # Could be interesting: z3 could also find pareto fronts.

        # # Optimization objective 1
        # # Minimize cell width.
        # solver.minimize(max_x)

        # Optimization objective 2
        # Minimize wiring length (net bounding boxes)
        # TODO: sort criteria by what? Number of terminals?

        for net in nets:
            # TODO: skip VDD/GND nets
            solver.minimize(net_max_x[net] - net_min_x[net])
            solver.minimize(net_max_y[net] - net_min_y[net])

        # TODO: optimization objective for pin nets.


        #
        logger.info("smt_placer-> Run SMT optimizer")
        is_sat = solver.check() == sat

        logger.info("smt_placer-> Is satisfiable: %s", is_sat)
        
        if is_sat:
            model = solver.model()
            # print(solver,model)
            assert len(model) > 0, "model is empty"
            #return model
        
            placements = Placement(cell_width)
            # cell = Cell(cell_width)
            # rows = [cell.lower, cell.upper]
            for p,n in pairs:
                (xn, yn) = nmos_loc[n]
                (xp, yp) = pmos_loc[p]
                # print('xx', model[xn],model[xp])
                
            for t in pmos_list:
                x, y = pmos_loc[t]
                x = model[x].as_long()
                # y = model[y].as_long()  
                flip = is_true(model[pmos_flipped[t]])
                transistor = t.flipped() if flip else t
                placements.upper[x - 1] = transistor
    
            for t in nmos_list:
                x, y = nmos_loc[t]
                x = model[x].as_long()
    
                # y = model[y].as_long()  
                flip = is_true(model[nmos_flipped[t]])
                transistor = t.flipped() if flip else t
                placements.lower[x - 1] = transistor        
            
            return [placements]
        else:
            return [] # No solution found

    def pn_relation(self,pmos,nmos):
        p_g = pmos.gate_net
        p_s = pmos.source_net
        p_d = pmos.drain_net
        n_g = nmos.gate_net
        n_s = nmos.source_net
        n_d = nmos.drain_net        
        
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
            


    def pn_pairs(self, pmos_list, nmos_list):
        pairs_score = {}
        mos_list = pmos_list +  nmos_list
        for p in pmos_list:
            for n in nmos_list:
                pairs_score[(p,n)] = self.pn_relation(p, n)
        
        pn_pairs = []
        # paired = []
        
        pairs_score = sorted(pairs_score.items(), key=lambda x: x[1],reverse=True)    
        for pair, score in pairs_score:
            if score >=2:
                p,n  = pair
                if (p in pmos_list) and (n in nmos_list):
                    pn_pairs.append(pair)
                    pmos_list.remove(p)
                    nmos_list.remove(n)

        return pn_pairs,pmos_list,nmos_list
        
    def place(self, devices, vertical_tracks_pmos = 1, vertical_tracks_nmos = 1):
        """
        Place transistors using an SMT solver (Z3).
        :param transistors list
        :return: Placement.
        """
        nmos_list = [t for t in devices if t.t == 'N']
        pmos_list = [t for t in devices if t.t == 'P']

        minimal_cell_width = math.ceil(max(len(nmos_list), len(pmos_list)))
        maximal_cell_width = max(len(nmos_list), len(pmos_list)) * 3 #?
        
        time_start = time.time()
        self.pairs,self.no_paires_p,self.no_paires_n  = self.pn_pairs(pmos_list, nmos_list)
        nmos_list = [t for t in devices if t.t == 'N']
        pmos_list = [t for t in devices if t.t == 'P']
        # print(self.pairs)
        for cell_width in range(minimal_cell_width, maximal_cell_width):
            logger.info("smt_placer-> Try cell width: %d"%(cell_width))
            print("smt_placer-> Try cell width: %d"%(cell_width))
            placements = self._place(pmos_list, nmos_list, cell_width, self.pairs, vertical_tracks_pmos = 1, vertical_tracks_nmos = 1)
            logger.info("smt_placer-> Placement of width %d cost %d seconds"%(cell_width, int(time.time() - time_start)))
            if len(placements) > 0:
                yield placements[0]
            else:
                logger.info("smt_placer-> Placement of width %d is impossible"%(cell_width))
        



def test():
    placer = SMTPlacer()
    from itertools import count
    c = count()
    transistors = [Transistor('P', 1, 1, 3, name=next(c)),
                   Transistor('N', 1, 2, 3, name=next(c)),
                   Transistor('P', 1, 1, 3, name=next(c)),
                   Transistor('N', 1, 2, 3, name=next(c)),
                   Transistor('P', 1, 1, 3, name=next(c)),
                   Transistor('N', 1, 2, 3, name=next(c))]
    placements = placer.place(transistors)
    placement = next(placements)
    assert placement is not None
