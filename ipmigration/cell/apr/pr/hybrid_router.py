# -*- coding: utf-8 -*-
"""

@author: leiyuan
#hybrid router

"""

from typing import Dict, Iterable, Mapping, TypeVar, AbstractSet, Any, List
from itertools import product, tee, count
from heapq import heappush, heappop
import networkx as nx

from src.pr.basic_router import SignalRouter,all_min,all_max

class HybridRouter(SignalRouter):
    def __init__(self):
        pass


