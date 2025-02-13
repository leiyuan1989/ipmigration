# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 19:11:55 2024

@author: leiyuan
"""
import itertools as it
# from align.schema import constraint
# from .types import set_context
# from .subcircuit import SubCircuit, Circuit
# from .instance import Instance
# from .translator import ConstraintTranslator
import networkx as nx
import numpy as np
# from collections import Counter
import logging
# from flatdict import FlatDict
# import hashlib

# from src.schema.basic import Mos4
import matplotlib.pyplot as plt


logger = logging.getLogger(__name__)




#     def find_subgraph_matches(self, graph, skip=None, node_match=None, edge_match=None):
#         # if node_match is None:
#         #     node_match = self.default_node_match
#         # if edge_match is None:
#         #     edge_match = self.default_edge_match
#         matcher = nx.algorithms.isomorphism.GraphMatcher(
#             self, graph, node_match=node_match, edge_match=edge_match)
#         correct_matches = []
#         # matches = sorted(matcher.subgraph_isomorphisms_iter(), key=lambda k: [(x, y)for x, y in k.items()])
#         return matcher

#         # Three possible scenarios of non determinism (M1, M2, M3, M4, M5) (Ma, Mb, Mc)
#         # 1. Different keys [{M1:Ma, M2:Mb, M3:Mc}, {M4:Ma, M2:Mb, M3:Mc}]
#         # 2. keys in diff order: [{M1:Ma, M2:Mb, M3:Mc}, {M2:Mb, M1:Ma, M3:Mb}]
#         # 3. Different values: [{M1:Ma, M2:Mb, M3:Mc}, {M1:Ma, M2:Mc, M3:Mb}]
#         # Thus sorting based on key,value pair
#         # 
#         # for match in matches:
#         #     if skip and any(k in skip for k in match.keys()):
#         #         logger.debug(f"skipping skip nodes {skip} {match}")
#         #         continue
#         #     if not any(self._is_element(self.nodes[node]) and any(node in x for x in correct_matches) for node in match):
#         #         try:
#         #             self.check_constraint_satisfiability(graph, match)
#         #             correct_matches.append(match)
#         #         except BaseException:  # Make this more specific
#         #             # primitives with unsatisfied constraints will not be created
#         #             logger.debug(f"skipping match {graph.subckt.name} {match.keys()} due to unsatisfied constraints")
#         #             pass
#         # # revert any added const TODO: add checker here
#         # while len(self.subckt.constraints) > _temp:
#         #     self.subckt.constraints.pop()
#         # return correct_matches
    
    
    
class CellMultiGraph(nx.MultiGraph):
    '''
    
    '''
    def __init__(self, ckt):
        super().__init__()
        self.ckt = ckt
        self.pmos_l = []
        self.nmos_l = []
    
        self.nets_l = {}
        
        self.add_node('VDD', pos = (0,6), name = 'VDD')
        self.add_node('VSS', pos = (0,0), name = 'VSS')
        
        for device in ckt.devices:
            self._add_to_graph(device)

    def _add_to_graph(self, device):
        if device.T == 'N':
            pos = (len(self.nmos_l), 2)
            self.nmos_l.append(device)
        else:
            pos = (len(self.pmos_l), 4)
            self.pmos_l.append(device)
            
            
        self.add_node(device.name, pos = pos, device = device)
        for pin, net in device.pins_dict.items():
            if pin != 'B':
                if net == 'VDD':
                    self.add_edge(device.name, 'VDD', pin={device.name:pin},net=net)
                elif net == 'VSS':
                    self.add_edge(device.name, 'VSS', pin={device.name:pin},net=net)
                else:
                    if net in self.nets_l:
                        pins = self.nets_l[net]
                        for d_name,d_pin in pins:
                            self.add_edge(device.name, d_name, pin={device.name:pin,d_name:d_pin},net=net)
                        self.nets_l[net].append((device.name,pin))
                    else:
                        self.nets_l[net] = [(device.name,pin)]
                
    

    @staticmethod
    def _is_device(v):
        return 'device' in v

     
    @property
    def devices(self):
        return [v['device'] for v in self.nodes.values() if self._is_device(v)]
    def device(self, name):
        assert name in self.nodes and self._is_device(self.nodes[name]), name
        return self.nodes[name]['instance']
    
    @property
    def nets(self):
        return [x for x, v in self.nodes.items() if not self._is_device(v)]

    def remove(self, element):
        self.subckt.elements.remove(element)
        self.remove_nodes_from(
            [x for x in self.neighbors(element.name)
             if self.degree(x) == 1])
        self.remove_node(element.name)

    @staticmethod
    def default_node_match(x, y):
        #'name' is vdd or vss 
        if ('name' in x) and ('name' in y):
            return x['name'] == y['name']
        else:
            return type(x.get('device')) == type(y.get('device')) 
        

    @staticmethod
    def default_edge_match(x, y):
        x_ = dict(x)
        y_ = dict(y)
        
        if len(x_) != len(y_):
            return False
        else:
            return True
            


    def draw(self,cmap,label=''):
        fig, ax = plt.subplots(figsize=(len(self.pmos_l),8))
        ax.set(title=self.ckt.name + '-' + label)
        
        node_list = self.nodes
        node_pos = {t:node_list[t]['pos'] for t in node_list}
        node_color = [cmap[t] for t in node_list]
        nx.draw_networkx(self, 
                  pos=node_pos, 
                  nodelist= node_list,
                  ax =ax,
                  # labels = labels,
                  node_color=node_color, 
                  node_size=100, 
                  with_labels=True,
                  font_size = 10, 
                  edge_color='lightgray') 


    def if_match(self, graph):
        matcher =  nx.algorithms.isomorphism.GraphMatcher(self,graph,node_match=self.default_node_match, edge_match=self.default_edge_match)
        #node_match=self.default_node_match, edge_match=self.default_edge_match
        self.if_matcher = matcher
        if matcher.is_isomorphic():
            g1 = CellGraph(self.ckt)
            g2 = CellGraph(graph.ckt)
            # print('xxx1',g1.if_match(g2))
            if g1.if_match(g2):
                return True
            else:
                return False 
 
        else:
            return False


    def find_subgraph_matches(self, graph, skip=None, node_match=None, edge_match=None):
        # if node_match is None:
        #     node_match = self.default_node_match
        # if edge_match is None:
        #     edge_match = self.default_edge_match
        matcher = nx.algorithms.isomorphism.GraphMatcher(
            self, graph, node_match=node_match, edge_match=edge_match)
        correct_matches = []
        # matches = sorted(matcher.subgraph_isomorphisms_iter(), key=lambda k: [(x, y)for x, y in k.items()])
        return matcher

        # Three possible scenarios of non determinism (M1, M2, M3, M4, M5) (Ma, Mb, Mc)
        # 1. Different keys [{M1:Ma, M2:Mb, M3:Mc}, {M4:Ma, M2:Mb, M3:Mc}]
        # 2. keys in diff order: [{M1:Ma, M2:Mb, M3:Mc}, {M2:Mb, M1:Ma, M3:Mb}]
        # 3. Different values: [{M1:Ma, M2:Mb, M3:Mc}, {M1:Ma, M2:Mc, M3:Mb}]
        # Thus sorting based on key,value pair
        # 
        # for match in matches:
        #     if skip and any(k in skip for k in match.keys()):
        #         logger.debug(f"skipping skip nodes {skip} {match}")
        #         continue
        #     if not any(self._is_element(self.nodes[node]) and any(node in x for x in correct_matches) for node in match):
        #         try:
        #             self.check_constraint_satisfiability(graph, match)
        #             correct_matches.append(match)
        #         except BaseException:  # Make this more specific
        #             # primitives with unsatisfied constraints will not be created
        #             logger.debug(f"skipping match {graph.subckt.name} {match.keys()} due to unsatisfied constraints")
        #             pass
        # # revert any added const TODO: add checker here
        # while len(self.subckt.constraints) > _temp:
        #     self.subckt.constraints.pop()
        # return correct_matches    
    
    
    
    
 
class CellGraph(nx.Graph):
    '''
    
    '''
    def __init__(self, ckt):
        super().__init__()
        self.ckt = ckt
        for device in ckt.devices:
            self._add_to_graph(device)

    def _add_to_graph(self, device):
        # print(device,type(device))
        # assert isinstance(device, Mos4)
        for pin, net in device.pins_dict.items():
            if pin != 'B':
                if self.has_edge(device.name, net):
                    # Multiple device ports connected to same net
                    self[device.name][net]['pin'].add(pin)
                    #why there is no mutiple pins here
                else:
                    # New net / element
                    self.add_edge(device.name, net, pin={pin})
                    self.nodes[device.name]['device'] = device
                    if net == 'VDD' or net == 'VSS':
                        self.nodes[device.name]['net'] = net   

    @staticmethod
    def _is_device(v):
        return 'device' in v

    @property
    def devices(self):
        return [v['device'] for v in self.nodes.values() if self._is_device(v)]
    def device(self, name):
        assert name in self.nodes and self._is_device(self.nodes[name]), name
        return self.nodes[name]['instance']
    
    @property
    def nets(self):
        return [x for x, v in self.nodes.items() if not self._is_device(v)]

    def remove(self, element):
        self.subckt.elements.remove(element)
        self.remove_nodes_from(
            [x for x in self.neighbors(element.name)
              if self.degree(x) == 1])
        self.remove_node(element.name)

    @staticmethod
    def default_node_match(x, y):
        # return True
        if ('net' in x) and ('net' in y):
            return x['net'] == y['net']
        else:
            return type(x.get('device')) == type(y.get('device')) 

    @staticmethod
    def default_edge_match(x, y):
        pin1 = list(x.get('pin'))
        pin2 = list(y.get('pin'))
        if ('G' in pin1) or ('G' in pin2): 
            if pin1 == pin2:
                return True
            else:
                return False
        return True
        #TODO
        # return x.get('pin') == y.get('pin')
    
    def if_match(self, graph):
        matcher =  nx.algorithms.isomorphism.GraphMatcher(self,graph,node_match=self.default_node_match, edge_match=self.default_edge_match)
        #node_match=self.default_node_match, edge_match=self.default_edge_match
        self.if_matcher = matcher
        if matcher.is_isomorphic():
            return True
        else:
            return False
 
    
    
def replace_matching_subgraph(cellgraph, sub_nodes, plotting=False):
    """
    Split a graph into 2 subgraphs 
    """
    # assert nx.isomorphism.GraphMatcher(cellgraph, sub_cellgraph).subgraph_is_isomorphic(),'input is not a subgraph of graph'
    
    external_graph = nx.MultiGraph()

    main_graph = nx.MultiGraph()
    sub_graph = nx.MultiGraph()
    left_graph = nx.MultiGraph() 
    
    external_graph.add_node('graph1',color = 'orange',pos = (1,0),name = 'graph1')
    external_graph.add_node('graph2',color = 'green' ,pos = (5,0),name = 'graph2')
    
    for node in cellgraph.nodes:
        if node in sub_nodes:
            prop = cellgraph.nodes[node]
            prop['color'] = 'orange'
            sub_graph.add_node(node,**prop)

        else:
            prop = cellgraph.nodes[node]
            prop['color'] = 'green' 
            left_graph.add_node(node,**prop)  
            main_graph.add_node(node,**prop)

    sub_pos = np.mean([cellgraph.nodes[t]['pos'] for t in sub_nodes],axis=0)
    main_graph.add_node('subgraph',color = 'red',pos = sub_pos, name = 'subgraph') 
    cross_edges = [] 
    for edge in cellgraph.edges:
        prop =  cellgraph.edges[edge]
        node1,node2,note = edge
        
        if (node1 == 'VDD') or (node2 == 'VDD') or (node1 == 'VSS') or (node2 == 'VSS'): 
            if  (node1 == 'VDD') or (node1 == 'VSS'):
                if (node2 in sub_graph.nodes):
                    sub_graph.add_edge(node1,node2,note,**prop)
                    if not( [node1,prop] in cross_edges):#TODO may have problem
                        cross_edges.append([node1,prop,note])
                    
                elif (node2 in left_graph.nodes):
                    left_graph.add_edge(node1,node2,note,**prop)
                    main_graph.add_edge(node1,node2,note,**prop)
                    
            if  (node2 == 'VDD') or (node2 == 'VSS'):
                if (node1 in sub_graph.nodes):
                    sub_graph.add_edge(node1,node2,note,**prop)
                    if not( [node1,prop] in cross_edges):
                        cross_edges.append([node1,prop])
                        
                elif (node1 in left_graph.nodes):
                    left_graph.add_edge(node1,node2,note,**prop)          
                    main_graph.add_edge(node1,node2,note,**prop)
                    
        else:
            if  (node1 in sub_graph.nodes) and  (node2 in sub_graph.nodes):
                sub_graph.add_edge(node1,node2,note,**prop)

            elif (node1 in left_graph.nodes) and  (node2 in left_graph.nodes):
                left_graph.add_edge(node1,node2,note,**prop)
                main_graph.add_edge(node1,node2,note,**prop)
            elif ((node1 in sub_graph.nodes) and  (node2 in left_graph.nodes)) or ((node1 in left_graph.nodes) and  (node2 in sub_graph.nodes)):
                
                nets = [external_graph.edges[t]['net'] for t in external_graph.edges]
                if prop['net'] in nets:
                    pass
                else:
                    external_graph.add_edge('graph1','graph2',net = prop['net'])
                
                # main graph
                if node1 in sub_graph.nodes:
                    cross_edges.append([node2,prop,note])
                
                elif node2 in sub_graph.nodes:
                    cross_edges.append([node1,prop,note])
                
            else:
                raise ValueError(' ')
      
    
    
    for device_n, prop, note in cross_edges:
        pin = prop['pin'][device_n]
        net = prop['net']
        prop = {'pin':{device_n:pin},'net':net}
        main_graph.add_edge(device_n,'subgraph',**prop)

        
        
    #create subgraph ckt
    
    
    # Categorize nodes by their node_type attribute

    if plotting:
        #cellgraph
        for node in cellgraph.nodes:
            if node in sub_nodes:
                cellgraph.nodes[node]['color'] = 'orange'
            else:
                cellgraph.nodes[node]['color'] = 'green'
        
        cmap = {t:cellgraph.nodes[t]['color'] for t in cellgraph.nodes}
        cellgraph.draw(cmap,'cellgraph')
        
        cellname = cellgraph.ckt.name
        figsize = (len(cellgraph.pmos_l),8)
        
        #main and subgraph
        draw_graph(main_graph, figsize, label=cellname + '_main and sub graph')
        
        #subgraph     
        draw_graph(sub_graph, figsize, label=cellname + '_subgraph')
        
        #external graph
            
        draw_graph(external_graph, figsize, label=cellname + '_external graph')
    return main_graph, external_graph, sub_graph, left_graph  

    

def draw_graph(graph, figsize=(8,8), label='',ax = None):
    if ax:
        ax,fig = ax
    else:
        fig, ax = plt.subplots(figsize=figsize )
        ax.set(title=label)
    
    node_list = graph.nodes
    # print('aaa',{t:node_list[t] for t in node_list})
    node_pos = {t:node_list[t]['pos'] for t in node_list}
    cmap = {t:graph.nodes[t]['color'] for t in graph.nodes}
    node_color = [cmap[t] for t in node_list]
    
    # print(node_list,node_pos,node_color)
    
    
    
    
    nx.draw_networkx(graph, 
              pos=node_pos, 
              nodelist= node_list,
              ax =ax,
              # labels = labels,
              node_color=node_color, 
              node_size=100, 
              with_labels=True,
              font_size = 10, 
              edge_color='lightgray') 

    

