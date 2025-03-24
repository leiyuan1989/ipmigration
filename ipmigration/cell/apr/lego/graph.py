# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 09:50:42 2024

@author: leiyuan
"""
import itertools
import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher
#
class StructGraph(nx.Graph):
    '''
    
    '''
    def __init__(self, devices):
        super().__init__()
        for device in devices:
            self._add_to_graph(device)

    def _add_to_graph(self, device):
        for pin, net in device.pins_dict.items():
            if pin != 'B':
                if self.has_edge(device.name, net):
                    # Multiple device ports connected to same net
                    self[device.name][net]['pin'].add(pin)
                    #why there is no mutiple pins here
                else:
                    # New net / element
                    self.add_edge(device.name, net, pin={pin}) #set
                    
                    self.nodes[device.name]['type'] = device.T
                    self.nodes[net]['type'] = 'net'
                    self.nodes[device.name]['power'] = ''
                    self.nodes[net]['power'] = ''
                    
                    
                    if net == 'VDD' or net == 'VSS':
                        self.nodes[net]['power'] = net
                        self[device.name][net]['power'] = net   
   

    @property
    def devices(self):
        return [t for t in self.nodes if self.nodes[t]['type'] != 'net' ]
    
    @property
    def nets(self):
        return  [t for t in self.nodes if self.nodes[t]['type'] == 'net' ]

    @staticmethod
    def default_node_match(x, y):
        # return True
        return (x['power'] == y['power']) and (x.get('type') == y.get('type')) 


    @staticmethod
    def default_edge_match(x, y):
        pin1 = list(x.get('pin'))
        pin2 = list(y.get('pin'))
        if len(pin1) == 1 and len(pin2) == 1:
            if (pin1[0] == 'G') or (pin2[0] == 'G'): 
                if pin1[0] != pin2[0]:
                    return False
        if ('power' in x) and ('power' in y):
            if x['power'] != y['power']:
                return False
        
        return True
    
    def is_isomorphic(self,graph):
        matcher = GraphMatcher(self, graph, node_match=self.default_node_match, edge_match=self.default_edge_match)
        return matcher.is_isomorphic()
    
    def find_subgraph_matches(self, graph):
        matcher = GraphMatcher(self, graph, node_match=self.default_node_match, edge_match=self.default_edge_match)
        matches = []
        for match in matcher.subgraph_isomorphisms_iter():
            matches.append( {v: k for k, v in  match.items()})    
        return matches
    
    


class RouteGraph:
    def __init__(self, net_dict):
        self.net_dict = net_dict













  

class GraphNets:
    def __init__(self,struct,ckt,graph):
        
        self.struct = struct
        self.ckt    = ckt
        
        self.routed_nets = {}
        self.unrouted_nets = {}
        # self.one_node_net = {}
        
        self.power_nets = {'VDD':[],'VSS':[]}
        # self.diff_ct = {}
        #TODO how about different kinds of 7 vertical tracks
        for col,pn in enumerate(struct.devices_array):        
            if pn['P'] and pn['N']:
                x = pn['G_COL']
                if pn['P'].G == pn['N'].G:
                    # self.add_common_gt(pn['P'].G,[(x,3,1),(x,4,1)])
                    if self.struct.net_mapping[pn['P'].G] in self.ckt.nets_cdl_io:
                        #TODO add pin loc
                        # self.add_pin_loc(pn['P'].G, (x,3))
                        
                        #P and N gates
                        # self.add_routed_nodes(pn['P'].G, ((x,4,0),(x,3,0)) )
                        self.add_routed_nodes(pn['P'].G, ((x,4,1),(x,3,1)) )
                        self.add_routed_nodes(pn['P'].G, ((x,4,1),(x,4,0)) )                       
                        # self.add_routed_nodes(pn['P'].G, ((x,3,1),(x,3,0)) )
                        
                        self.add_unrouted_nodes(pn['P'].G, [(x,4,0),(x,4,1),(x,3,1)], 1)
                    else:
                        #not pin
                        self.add_routed_nodes(pn['P'].G, ((x,4,1),(x,3,1)) )
                        self.add_unrouted_nodes(pn['P'].G,  [(x,4,1),(x,3,1)], 1)
                else:
                    self.add_unrouted_nodes(pn['P'].G, [(x,4,1)], 0)
                    self.add_unrouted_nodes(pn['N'].G, [(x,3,1)], 0)
        
                #P and N source? 4 and 5
                self.add_unrouted_nodes(pn['P'].S, [(x-1,5,0),(x-1,4,0)], 2)
                self.add_unrouted_nodes(pn['N'].S, [(x-1,2,0),(x-1,3,0)], 2)   
        
            elif pn['P']: #only pmos
                x = pn['G_COL']
                self.add_unrouted_nodes(pn['P'].G, [(x,4,1)], 0)
                self.add_unrouted_nodes(pn['P'].S, [(x-1,5,0),(x-1,4,0)], 2)
            elif pn['N']: #only nmos
                x = pn['G_COL']
                self.add_unrouted_nodes(pn['N'].G, [(x,3,1)], 0)
                self.add_unrouted_nodes(pn['N'].S, [(x-1,2,0),(x-1,3,0)], 2)  
            else:
                pass
            
            #drain 
            if col == len(struct.devices_array) - 1:
                x = pn['G_COL']
                if pn['P']:
                    self.add_unrouted_nodes(pn['P'].D, [(x+1,5,0),(x+1,4,0)], 2)
                if pn['N']:
                    self.add_unrouted_nodes(pn['N'].D, [(x+1,2,0),(x+1,3,0)], 2)  


        #load from pin_loc
        # pins_dict = self.struct.pin_loc[self.struct.struct_ckt.name]
        
        #add pre set pin here    
        # for k, v in self.unrouted_nets.items():
        for net, t in  self.struct.left_pins.items():
            if net in self.struct.net_mapping_r:
                s_net = self.struct.net_mapping_r[net]
            else:
                s_net = 'cross_' + net
            self.add_unrouted_nodes(s_net, [(0, t[0], t[1])], 0) 

        for net, t in  self.struct.right_pins.items():
            if net in self.struct.net_mapping_r:
                s_net = self.struct.net_mapping_r[net]
            else:
                s_net = 'cross_' + net
            self.add_unrouted_nodes(s_net, [(self.struct.max_col, t[0], t[1])], 0)             
            
        if 'VDD' in self.unrouted_nets:
            self.power_nets['VDD'] = [t[0][0] for t in self.unrouted_nets.pop('VDD')]
        if 'VSS' in self.unrouted_nets:
            self.power_nets['VSS'] = [t[0][0] for t in self.unrouted_nets.pop('VSS')]
 

    def add_unrouted_nodes(self, net, nodes_c, node_type):
        # node_type: 0 common, 1 gt 2 aa ct
        if net in self.unrouted_nets:
            self.unrouted_nets[net].append([nodes_c,node_type]) 
        else:
            self.unrouted_nets[net] = [[nodes_c,node_type]] 

    def add_routed_nodes(self,net,nodes):
        if net in self.routed_nets:
            self.routed_nets[net].append(nodes) 
        else:
            self.routed_nets[net] = [nodes] 

            
    def canditate(self):
        optional_nodes = {}
        for net,v in self.unrouted_nets.items():
            for i, node in enumerate(v):
                t1 = len(node[0])
                if t1 > 1 and node[1] == 2:
                    optional_nodes[(net,i)]=list(range(t1))
        
        for net,v in self.unrouted_nets.items():
            for i, node in enumerate(v):
                t1 = len(node[0])
                if t1 > 1 and node[1] == 1:
                    optional_nodes[(net,i)]=list(range(t1))
        keys = optional_nodes.keys()
        values = list(optional_nodes.values())
        cartesian_values = list(itertools.product(*values))
        # print('aa',keys,values,cartesian_values)
        # dict_keys([('CN', 0), ('CN', 1), ('C', 0), ('C', 1), ('CN', 2)]) 
        # [[0, 1], [0, 1], [0, 1], [0, 1], [0, 1]] 
        # [(0, 0, 0, 0, 0), (0, 0, 0, 0, 1), (0, 0, 0, 1, 0), ......
        
        for value in cartesian_values:
            unrouted_nets = {}
            ct_aa_nodes = {}
            block_nodes = []
            one_node_net = {}
            optional_node = {k:v for k,v in zip(keys,value)}
            for net,v in self.unrouted_nets.items(): 
                unrouted_net = []
                for i, node in enumerate(v):
                    if len(node[0]) > 1:
                        index = optional_node[(net,i)]
                        t_node = node[0][index]
                        if node[1] == 1:# muti- node because of routed
                            for j, t_node2 in enumerate(node[0]):
                                if j != index:
                                    block_nodes.append(node[0][j])
                                    
                    else:
                        t_node = node[0][0]
                    unrouted_net.append(t_node) 
                    if node[1] == 2:
                        ct_aa_nodes[t_node] = net
                        
                unrouted_nets[net] = list(set(unrouted_net))
            #same points in
            pop_nets = []
            for net, value in unrouted_nets.items():
                if len(value) == 1:
                    if net in one_node_net:
                        one_node_net[net].append(value[0])
                    else:
                        one_node_net[net] = [value[0]]
                    pop_nets.append(net)
            for net in pop_nets:
                unrouted_nets.pop(net)
            
            yield unrouted_nets,block_nodes,ct_aa_nodes,one_node_net
        #cartesian product, equivalent to a nested for-loop
        # list(itertools.product(*d))

    def postprocess_nets(self, graph_net, ct_aa_nodes, only_nodes = False, nets_routed=None):
        
        #TODO add one node edge
        nodes_label = {}
        for net, nodes in graph_net.items():
            for node in nodes:
                if node in nodes_label:
                    pass
                else:
                    label = net
                    if node in ct_aa_nodes:
                        label = label + '_CT'
                    nodes_label[node] = label
        
        for net, edges in self.routed_nets.items():
            for n1,n2 in edges:
                if n1 in nodes_label:
                    pass
                else:
                    nodes_label[n1] = net
                if n2 in nodes_label:
                    pass
                else:
                    nodes_label[n2] = net 
        
        if not(only_nodes):
            for net, edges in self.routed_nets.items():
                if net in nets_routed:
                    nets_routed[net] = nets_routed[net] + edges
                else:
                    nets_routed[net] = edges
            
            gt_ct_nodes = []
            m1_edges = {}
            gt_edges = {}
            for net, edges in nets_routed.items():
                m1_edges[net] = []
                gt_edges[net] = []
                for e1,e2 in edges:
                    if e1[2] == 1 and e2[2] == 1:
                        gt_edges[net].append((e1,e2))
                    elif (e1[2] == 0 and e2[2] == 1) or (e1[2] == 1 and e2[2] == 0):
                        gt_ct_nodes.append((e1[0],e1[1],0))
                    elif e1[2] == 0 and e2[2] == 0:
                        m1_edges[net].append((e1,e2))
            
            self.routed_nets = nets_routed     
            self.m1_edges = m1_edges
            self.gt_edges = gt_edges
            self.gt_ct_nodes = gt_ct_nodes
            self.ct_aa_nodes = ct_aa_nodes
        
            return nodes_label,nets_routed,m1_edges,gt_edges,gt_ct_nodes,ct_aa_nodes
        else:
            return nodes_label