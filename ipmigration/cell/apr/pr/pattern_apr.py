# -*- coding: utf-8 -*-
"""
@author: leiyuan
"""

from ipmigration.cell.apr.pr.placement import Placement
from ipmigration.cell.apr.pr.ip_router import IPRouter
from ipmigration.cell.apr.pr.sorter import CircuitSorter
import logging
logger = logging.getLogger(__name__)

PLOT = True

'''
Based on the design objectives, to better preserve the design intent, 
an enumeration method is employed here. 
In the case of new netlists, they need to be optimized according to the design.
'''

class PatternAPR:
    def __init__(self,ckt,sub_ckts,place_file, vertical_tracks=6, load=False):
        self.ckt = ckt
        self.vtracks = vertical_tracks
        self.sorter = CircuitSorter(ckt,sub_ckts,place_file,load) 
        

    def run(self):
        place_data = self.sorter.run()
        self.place_data = place_data
        sub_placement = [Placement(t) for t in place_data]
        self.placement = Placement.merge_placement_list(sub_placement,abutment=False)

        return self.route()  

    
    def route(self):
        self.router = IPRouter( self.ckt, self.place_data, vtracks=self.vtracks)
        return self.router.route()
       



