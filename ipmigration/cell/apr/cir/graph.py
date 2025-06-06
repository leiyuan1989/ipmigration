# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 09:50:42 2024

@author: leiyuan
"""
import copy
import itertools
import matplotlib.pyplot as plt

import networkx as nx
import numpy as np
from networkx.algorithms.isomorphism import GraphMatcher
#

color_theme = {'poly':'blue', 'diff':'red', 'net':'orange','net_io':'green'}
linestyle = {'net':'-','inter_net':'--'}

class MosGraph(nx.Graph):
    def __init__(self, ckt):
        super().__init__() 
        self.ckt = ckt
        self.pins = ckt.pins
        self.p_pointer = (5, 15, 5)
        self.n_pointer = (5, 5 , 5)
        self.net_pointer = (5, 10 , 5)
        self.vdd_pointer = (5, 20 , 5)
        self.vss_pointer = (5, 0 , 5) 
        
        self.vdd_net = ckt.vdd_net
        self.vss_net = ckt.vss_net     
        
        self.ckt_to_graph(ckt)
        
    def __repr__(self):
        return "%s graph: %d devices, %d nodes"%(self.ckt.name, len(self.ckt.devices), len(self.nodes))
        
    def ckt_to_graph(self, ckt):
        for device in ckt.devices:
            self._add_device(device)
        for net, terms in ckt.nets.items():
            self._add_nets(net,terms)
        

    def _add_device(self, device, pos = None):
        if pos:
            p = pos
        else:
            if device.T == 'P':
                p = self.p_pointer
            else:
                p = self.n_pointer
 
        #s
        attr = {'name' : device.name,
                'mostype' : device.T,
                'pintype' : 'SD',
                'pin'  : 'S',
                'net'  : device.S,
                'power': device.S==self.vdd_net or device.S==self.vss_net,
                'pos'  : (p[0]-1,p[1],p[2]),
                'color': color_theme['diff']}
        self.add_node(device.name+':S', **attr)
        #g
        attr = {'name' : device.name,
                'mostype' : device.T,
                'pintype' : 'G',
                'pin'  : 'G',
                'net'  : device.G,
                'power': device.G==self.vdd_net or device.G==self.vss_net,
                'pos'  : (p[0],p[1],p[2] + 1),
                'color': color_theme['poly']}
        self.add_node(device.name+':G', **attr)
        #d
        attr = {'name' : device.name,
                'mostype' : device.T,
                'pintype' : 'SD',
                'pin'  : 'D',
                'net'  : device.D,
                'power': device.D==self.vdd_net or device.D==self.vss_net,
                'pos'  : (p[0]+1,p[1],p[2]),
                'color': color_theme['diff']}
        self.add_node(device.name+':D', **attr)
        
        if pos:
            pass
        else:
            if device.T == 'P':
                self.p_pointer = (p[0]+5,p[1],p[2])
            else:
                self.n_pointer = (p[0]+5,p[1],p[2])
    
        #add internal edge
        attr = {'name': device.name+':DG','internal': True, 'linestyle' : linestyle['inter_net'] }
        self.add_edge(device.name+':D',device.name+':G',**attr)
        attr = {'name': device.name+':SG','internal': True, 'linestyle' : linestyle['inter_net'] }
        self.add_edge(device.name+':S',device.name+':G',**attr)  
    
    
    
    def _add_nets(self,net, terminsls, pos = None):
        if net in self.pins:
            color = color_theme['net_io']
        else:
            color = color_theme['net']
        
        if net == self.vdd_net:
            p = self.vdd_pointer
            power = True
        elif net == self.vss_net:
            p = self.vss_pointer
            power = True
        else:
            p = self.net_pointer
            power = False
        
        attr = {'name' : net,
                'mostype' : 'net',
                'pintype' : 'none',
                'pin'  : 'none',#to distinct with device node
                'net'  : net,
                'power': power,
                'pos'  : p,
                'color': color}
        self.add_node(net, **attr)
        
        if  net != 'VDD' and net != 'VSS':
            self.net_pointer = (p[0] + 5, p[1], p[2] + 0.1)
        #add edges
        
        for t in terminsls:
           attr = {'name': net,'internal': False, 'linestyle' : linestyle['net'] }
           self.add_edge(net,t[0].name+':'+t[1],**attr)  
                
        
    
    def search_nodes(self):
        pass
 
    @staticmethod
    def default_node_match(x, y):
        # return (x.get('power') == y.get('power')) and (x.get('mostype') == y.get('mostype')) and (x.get('pintype') == y.get('pintype')) 
        return (x.get('mostype') == y.get('mostype')) and (x.get('pintype') == y.get('pintype')) 
  
    @staticmethod #VDD and VSS are regarded as tasks that must be matched.
    def node_match_power(x, y):
        return  (x.get('mostype') == y.get('mostype')) and (x.get('pintype') == y.get('pintype')) and (x.get('power') == y.get('power'))

    @staticmethod
    def default_edge_match(x, y):        
        return (x.get('internal') == y.get('internal')) 
    
    @staticmethod #VDD and VSS are regarded as tasks that must be matched.
    def edge_match_power(x, y):        
        return (x.get('internal') == y.get('internal')) and (x.get('power') == y.get('power'))

        
    def find_subgraph_matches(self, graph, node_match=None, edge_match=None):
        if not(node_match):
            node_match=self.default_node_match
        if not(edge_match):
            edge_match=self.default_edge_match            
            
        matcher = GraphMatcher(self, graph, node_match=node_match, edge_match=node_match)
        matches = []
        for match in matcher.subgraph_isomorphisms_iter():
            matches.append( {v: k for k, v in  match.items()})    
        return matches        
   
    
    def is_isomorphic(self,graph):
        matcher = GraphMatcher(self, graph, node_match=self.default_node_match, edge_match=self.default_edge_match)
        return matcher.is_isomorphic()
    
    def match(self,graph):
        matcher = GraphMatcher(self, graph, node_match=self.default_node_match, edge_match=self.default_edge_match)
        return matcher.is_isomorphic(),  list(matcher.isomorphisms_iter())
    # @staticmethod
    # def graph_to_ckt(match_dict,devices_dict):
     
        
        
        
    #     return [devices_dict[t] for t in match_dict.values() if t in devices_dict]



class RouteGraph(nx.Graph):
    def __init__(self,):
        super().__init__() 

    def copy(self):
        return  copy.deepcopy(self)
        
    def init(self,pattern, pt_connected, pt_edges):
        self.pattern = pattern
        self.pt_connected = pt_connected
        self.pt_edges = pt_edges
        
    def add_nodes(self, m1_nodes, gt_nodes, ct_nodes):  
        self.m1_nodes = m1_nodes
        self.gt_nodes = gt_nodes
        self.ct_nodes = ct_nodes

        for node,attr in m1_nodes.items():
            self.add_node(node,**attr)        
        for node,attr in gt_nodes.items():
            self.add_node(node, **attr)  
        for node,attr in ct_nodes.items():
            self.add_node(node, **attr)  
        
        max_col = max([t[0] for t in self.nodes])
        self.max_col = max_col

    def add_edges(self):
        for node1 in self.m1_nodes:
            for node2 in self.m1_nodes:
                if node1 != node2:
                    if not(self.has_edge(node1,node2)):
                        distance = (node1[0] - node2[0]) ** 2 + (node1[1] - node2[1]) ** 2 
                        if distance == 1:
                            self.add_edge(node1, node2, cost=1)
        for node1 in self.gt_nodes:
            for node2 in self.gt_nodes:
                if node1 != node2:
                    if not(self.has_edge(node1,node2)):
                        distance = (node1[0] - node2[0]) ** 2 + (node1[1] - node2[1]) ** 2 
                        if distance == 1:
                            self.add_edge(node1, node2, cost=3)                    
        
        for node in self.ct_nodes:
            node1 = (node[0],node[1],0)
            node2 = (node[0],node[1],1)            
            self.add_edge(node, node1, cost=3)                    
            self.add_edge(node, node2, cost=3)   

    

    def add_right_nodes(self,median):
        max_col = self.max_col
        self.max_col = max_col+1
        right_nodes = [t for t in self.nodes if t[0] == max_col and t[2]==1]
        right_nodes_gt =  [t for t in self.nodes if t[0] == max_col and t[2]==0]
        for node in right_nodes:
            t1,t2,t3 = node
            attr =  {'net':'','loc':(t1+1,t2),'color':'orange'}
            self.add_node((t1+1,t2,t3),**attr)
            self.add_edge(node,(t1+1,t2,t3),cost=1)
        for i in [median-1,median,median+1] :
            attr1 = {'net':'', 'loc':(max_col+1+0.3, i+0.3),'color':'blue'}
            attr2 = {'net':'', 'loc':(max_col+1+0.15, i+0.15),'color':'cyan'}
            self.add_node((max_col+1,i,0),**attr1)
            self.add_node((max_col+1,i,0.5),**attr2)
            if (max_col,i,0) in right_nodes_gt:
                self.add_edge((max_col,i,0),(max_col+1,i,0),cost=3)
            
            #TODO: if need add ct edge?
    def add_left_nodes(self,median):
        right_nodes_gt =  [t for t in self.nodes if t[0] == 1 and t[2]==0]
        for i in [median-1,median,median+1] :
            attr1 = {'net':'', 'loc':(0+0.3, i+0.3),'color':'blue'}
            attr2 = {'net':'', 'loc':(0+0.15, i+0.15),'color':'cyan'}
            self.add_node((0,i,0),**attr1)
            self.add_node((0,i,0.5),**attr2)
            self.add_edge((0,i,0),(0,i,0.5),cost=3)   
            self.add_edge((0,i,0.5),(0,i,1),cost=3)   
            
            
            if (1,i,0) in right_nodes_gt:
                self.add_edge((0,i,0),(1,i,0),cost=3)            

        self.add_edge((0,median-1,0),(0,median,0),cost=3)   
        self.add_edge((0,median,0),(0,median+1,0),cost=3) 
    
    
    def gen_routing_graph(self):
        G_copy = copy.deepcopy(self)
        for k,v in self.pt_connected.items():
            nodes = []
            for t in v:
                nodes.append(t[0])
                nodes.append(t[1])
            nodes = list(set(nodes))
            # print(nodes,k)
            nodes.remove(k)
            
            adj_nodes= []
            for n1 in nodes:
                adjs = list(self.adj[n1])
                for adj in adjs:
                    if not(adj in nodes):
                        adj_nodes.append(adj)
            adj_nodes = list(set(adj_nodes))      
            adj_nodes.remove(k)
            G_copy.remove_nodes_from(nodes)
            for node in adj_nodes:    
                G_copy.add_edge(node,k,cost=1)

        return G_copy
            
    def gen_routing_signals(self, route_nets, routing_graph):
        signals = []
        pins = []
        for k,v in route_nets.items():
            if k !='VDD' and k !='VSS':
                if len(v)>1:
                    signals.append(set(v))
                else:
                    if len(v)==1:
                        if v[0][2] == 0: #pin
                            pins.append(v[0])        
        G_copy = copy.deepcopy(routing_graph)
        G_copy.remove_nodes_from(pins)
        
        # cost_dict = {}
        # for i,j,v in routing_graph.edges(data=True):
        #     cost_dict[(i,j)] = v['cost']
        #     cost_dict[(j,i)] = v['cost']
        # def cost_edge(t):
        #     return cost_dict[t]

        return signals, G_copy  

    def add_grid(self,loc,):
        # loc, 
        # net
        # is_merge?
        pass
    def add_connect(self,loc,):
        #cost
        
        pass

    def get_column(self, col):
        pass

    def plot(self,paths=[],m2_paths=[],savepath=None):
        pos = nx.get_node_attributes(self, 'loc')
        grid_columns = max([t[0] for t in self.nodes])
        
        colors = [self.nodes[node]['color'] for node in self.nodes()]

        plt.figure(figsize=(2*grid_columns, 12))
    
        nx.draw_networkx_nodes(self, pos, node_color=colors)
        nx.draw_networkx_edges(self, pos, edge_color='gray', style='dashed')
        
        labels = {node: str(self.nodes[node]['net']) for node in self.nodes()}
        nx.draw_networkx_labels(self, pos, labels=labels, font_size=16)
     

        colors = ['red', 'green', 'blue', 'yellow', 'purple', 'orange', 'cyan', 'magenta']
        for i,path in enumerate(paths):
           
            color = colors[i % len(colors)]
            if path is not None:
                # print(self.nodes,paths)
                nx.draw_networkx_edges(self, pos, edgelist=path, edge_color=color, width=2)

        # print(self.nodes)
        # print(m2_paths)
        m2_paths = [
            [
                tuple(item[:-1] + (1,) for item in sub_tuple)
                for sub_tuple in sub_list
            ]
            for sub_list in m2_paths
        ]
        
        for i,path in enumerate(m2_paths):
            color = colors[i % len(colors)]
            if path is not None:
                nx.draw_networkx_edges(self, pos, edgelist=path,style='dashed', edge_color='black', width=3)
                
        
        # 显示图形
        plt.title(self.pattern.pattern_name)
        plt.axis('on')
        
        if savepath:
            plt.savefig(savepath)
        plt.show()
        



class PatternGraph(nx.Graph):
    def __init__(self):
        super().__init__() 

    def copy(self):
        return  copy.deepcopy(self)
        
    def init(self,ckt, pt_connected):
        self.ckt = ckt
        self.pt_connected = pt_connected
        
    def add_nodes(self, m1_nodes, gt_nodes, ct_nodes):  
        self.m1_nodes = m1_nodes
        self.gt_nodes = gt_nodes
        self.ct_nodes = ct_nodes

        for node,attr in m1_nodes.items():
            self.add_node(node,**attr)        
        for node,attr in gt_nodes.items():
            self.add_node(node, **attr)  
        # for node,attr in ct_nodes.items():
        #     self.add_node(node, **attr)  
        
        max_col = max([t[0] for t in self.nodes])
        self.max_col = max_col

    def add_edges(self):
        for node1 in self.m1_nodes:
            for node2 in self.m1_nodes:
                if node1 != node2:
                    if not(self.has_edge(node1,node2)):
                        distance = (node1[0] - node2[0]) ** 2 + (node1[1] - node2[1]) ** 2 
                        if distance == 1:
                            self.add_edge(node1, node2, cost=1)
        for node1 in self.gt_nodes:
            for node2 in self.gt_nodes:
                if node1 != node2:
                    if not(self.has_edge(node1,node2)):
                        distance = (node1[0] - node2[0]) ** 2 + (node1[1] - node2[1]) ** 2 
                        if distance == 1:
                            self.add_edge(node1, node2, cost=3)                    
        
        for node in self.ct_nodes:
            node1 = (node[0],node[1],0)
            node2 = (node[0],node[1],1)      
            # print(node1,node2)
            assert node1 in self.nodes
            assert node2 in self.nodes
            self.add_edge(node1, node2, cost=3)                    
    
    def add_side_nodes(self, l_nodes, r_nodes):
        G = copy.deepcopy(self)
        l = 1
        r = G.max_col
        G.max_col = r+1
        
        l_m1 = [t for t in G.nodes if t[0] == l and t[2]==1]
        l_gt = [t for t in G.nodes if t[0] == l and t[2]==0]
        r_m1 = [t for t in G.nodes if t[0] == r and t[2]==1]
        r_gt = [t for t in G.nodes if t[0] == r and t[2]==0]
        
        m1_nodes = []
        for node in l_m1:
            t1,t2,t3 = node
            attr =  {'net':'','loc':(t1-1,t2),'color':'orange'}
            G.add_node((t1-1,t2,t3),**attr)
            G.add_edge(node,(t1-1,t2,t3),cost=1)
            m1_nodes.append((t1-1,t2,t3))
        for node1 in m1_nodes:
            for node2 in m1_nodes:
                if node1 != node2:
                    if not(self.has_edge(node1,node2)):
                        distance = (node1[0] - node2[0]) ** 2 + (node1[1] - node2[1]) ** 2 
                        if distance == 1:
                            G.add_edge(node1, node2, cost=1)
        m1_nodes = [] 
        for node in r_m1:
            t1,t2,t3 = node
            attr =  {'net':'','loc':(t1+1,t2),'color':'orange'}
            G.add_node((t1+1,t2,t3),**attr)
            G.add_edge(node,(t1+1,t2,t3),cost=1)
            m1_nodes.append((t1+1,t2,t3))
        
        #may have some potential problem for right nodes
        for node1 in m1_nodes:
            for node2 in m1_nodes:
                if node1 != node2:
                    if not(self.has_edge(node1,node2)):
                        distance = (node1[0] - node2[0]) ** 2 + (node1[1] - node2[1]) ** 2 
                        if distance == 1:
                            G.add_edge(node1, node2, cost=1)
        gt_nodes = []
        for node in l_gt:
            t1,t2,t3 = node
            attr =  {'net':'','loc':(t1-1+0.3,t2+0.3),'color':'blue'}
            G.add_node((t1-1,t2,t3),**attr)
            G.add_edge(node,(t1-1,t2,t3),cost=3)
            G.add_edge((t1-1,t2,1),(t1-1,t2,t3),cost=3)
            gt_nodes.append((t1-1,t2,t3))
            
        for node1 in gt_nodes:
            for node2 in gt_nodes:
                if node1 != node2:
                    if not(self.has_edge(node1,node2)):
                        distance = (node1[0] - node2[0]) ** 2 + (node1[1] - node2[1]) ** 2 
                        if distance == 1:
                            G.add_edge(node1, node2, cost=3)
        
        for node in r_gt:
            t1,t2,t3 = node
            attr =  {'net':'','loc':(t1+1+0.3,t2+0.3),'color':'blue'}
            G.add_node((t1+1,t2,t3),**attr)
            G.add_edge(node,(t1+1,t2,t3),cost=3)    
            G.add_edge((t1+1,t2,1),(t1+1,t2,t3),cost=3)    
        
        for net, (t1,t2) in l_nodes.items():
            G.nodes[(l-1,t1,t2)]['net'] = net
        for net, (t1,t2) in r_nodes.items():
            G.nodes[(r+1,t1,t2)]['net'] = net        
        return G

    # def add_right_nodes(self,median):
    #     max_col = self.max_col
    #     self.max_col = max_col+1
    #     right_nodes = [t for t in self.nodes if t[0] == max_col and t[2]==1]
    #     right_nodes_gt =  [t for t in self.nodes if t[0] == max_col and t[2]==0]
    #     for node in right_nodes:
    #         t1,t2,t3 = node
    #         attr =  {'net':'','loc':(t1+1,t2),'color':'orange'}
    #         self.add_node((t1+1,t2,t3),**attr)
    #         self.add_edge(node,(t1+1,t2,t3),cost=1)
    #     for i in [median-1,median,median+1] :
    #         attr1 = {'net':'', 'loc':(max_col+1+0.3, i+0.3),'color':'blue'}
    #         attr2 = {'net':'', 'loc':(max_col+1+0.15, i+0.15),'color':'cyan'}
    #         self.add_node((max_col+1,i,0),**attr1)
    #         self.add_node((max_col+1,i,0.5),**attr2)
    #         if (max_col,i,0) in right_nodes_gt:
    #             self.add_edge((max_col,i,0),(max_col+1,i,0),cost=3)
            
    #         #TODO: if need add ct edge?
    # def add_left_nodes(self,median):
    #     right_nodes_gt =  [t for t in self.nodes if t[0] == 1 and t[2]==0]
    #     for i in [median-1,median,median+1] :
    #         attr1 = {'net':'', 'loc':(0+0.3, i+0.3),'color':'blue'}
    #         attr2 = {'net':'', 'loc':(0+0.15, i+0.15),'color':'cyan'}
    #         self.add_node((0,i,0),**attr1)
    #         self.add_node((0,i,0.5),**attr2)
    #         self.add_edge((0,i,0),(0,i,0.5),cost=3)   
    #         self.add_edge((0,i,0.5),(0,i,1),cost=3)   
            
            
    #         if (1,i,0) in right_nodes_gt:
    #             self.add_edge((0,i,0),(1,i,0),cost=3)            

    #     self.add_edge((0,median-1,0),(0,median,0),cost=3)   
    #     self.add_edge((0,median,0),(0,median+1,0),cost=3) 
    
    
    def gen_routing_graph(self,io_pins,m2_pins):
        G_copy = copy.deepcopy(self)
    
        for k,v in self.pt_connected.items():
            nodes = []
            for t in v:
                nodes.append(t[0])
                nodes.append(t[1])
            nodes = list(set(nodes))
            # print(nodes,k)
            nodes.remove(k)
            
            adj_nodes= []
            for n1 in nodes:
                adjs = list(self.adj[n1])
                for adj in adjs:
                    if not(adj in nodes):
                        adj_nodes.append(adj)
            adj_nodes = list(set(adj_nodes))      
            
            adj_nodes.remove(k)
            G_copy.remove_nodes_from(nodes)
            for node in adj_nodes:    
                G_copy.add_edge(node,k,cost=1)
        G_copy.remove_pins(io_pins)
        G_copy.remove_pins(m2_pins)
        return G_copy
            
    def gen_route_nets(self,route_nets):
        signals = []
        signals_names = []
        io_pins = {}
        pw_pins = {'VDD':[], 'VSS':[]}
        for k,v in route_nets.items():
            if k == 'VDD':
                pw_pins['VDD'].append(v)
            elif k == 'VSS':
                pw_pins['VSS'].append(v)
            else:
                if len(v)>1:
                    signals.append(set(v))
                    signals_names.append(k)
                else:
                    if len(v)==1:
                        if v[0][2] == 0: #pin
                            io_pins[k] = v[0]  

        return signals, signals_names, io_pins, pw_pins
    
    def remove_pins(self, pins):
        self.remove_nodes_from(pins)
    

    def add_grid(self,loc,):
        # loc, 
        # net
        # is_merge?
        pass
    def add_connect(self,loc,):
        #cost
        
        pass

    def get_column(self, col):
        pass

    def plot(self,name='', paths=[], m2_paths=[], pre_connect=False, savepath=None):
        pos = nx.get_node_attributes(self, 'loc')
        grid_columns = max([t[0] for t in self.nodes])
        
        m2_modes = []
        for t in m2_paths:
            m2_modes.append(tuple(t[0]))
            m2_modes.append(tuple(t[1]))
        
        # colors = [self.nodes[node]['color'] for node in self.nodes()]
        colors = []
        for node in self.nodes():
            if node in m2_modes:
                colors.append('black')
            else:
                colors.append(self.nodes[node]['color'] )

        plt.figure(figsize=(2*grid_columns, 12))
    
        nx.draw_networkx_nodes(self, pos, node_color=colors)
        nx.draw_networkx_edges(self, pos, edge_color='gray', style='dashed')
        
        labels = {node: str(self.nodes[node]['net']) for node in self.nodes()}
        nx.draw_networkx_labels(self, pos, labels=labels, font_size=16)
     

        colors = ['red', 'green', 'blue', 'yellow', 'purple', 'orange', 'cyan', 'magenta']
        
        if pre_connect:
            for i,net in enumerate(self.pt_connected):
                color = colors[i % len(colors)]
                path = self.pt_connected[net]
                nx.draw_networkx_edges(self, pos, edgelist=path, edge_color=color, width=2)


        for i,path in enumerate(paths):
            color = colors[i % len(colors)]
            if path is not None:
                # print(self.nodes,paths)
                nx.draw_networkx_edges(self, pos, edgelist=path, edge_color=color, width=2)


        # m2_paths = [
        #     [
        #         tuple(item[:-1] + (1,) for item in sub_tuple)
        #         for sub_tuple in sub_list
        #     ]
        #     for sub_list in m2_paths
        # ]
        
        # for i,path in enumerate(m2_paths):
        #     color = colors[i % len(colors)]
        #     if path is not None:
        #         nx.draw_networkx_edges(self, pos, edgelist=path,style='dashed', edge_color='black', width=3)
                

        plt.title(self.ckt.name+'_'+name)
        plt.axis('on')

        if savepath:
            plt.savefig(savepath)
        plt.show()



# class PlaceGraph(nx.Graph):
#     def __init__(self, placement):
#         super().__init__()
#         for device in devices:
#             self._add_to_graph(device)    
    
#     def gen_graph(self):
        
        
    
    
#     def _add_to_graph(self, device):
#         self.add_edge(device.name+':D', device.name+':G') 
#         self.add_edge(device.name+':G', device.name+':S') 
        
#         self.add_edge(device.name+':D', device.D)
#         self.add_edge(device.name+':S', device.S)













class ChainGraph(nx.Graph):
    def __init__(self, devices):
        super().__init__()
        for device in devices:
            self._add_to_graph(device)    
    
    def _add_to_graph(self, device):
        self.add_edge(device.name+':D', device.name+':G') 
        self.add_edge(device.name+':G', device.name+':S') 
        
        self.add_edge(device.name+':D', device.D)
        self.add_edge(device.name+':S', device.S)
        
    
    

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
    
        

def graph_show(g, fig_save = None, fig_size = [20,20], view=(45,135), 
               axis_off=False, ticks_off=True):
    fig = plt.figure(figsize = fig_size)
    ax = fig.add_subplot(111, projection='3d')
    
    xs = []
    ys = []
    zs = []
    color = []
    for node in g.nodes:
        data = g.nodes[node]
        xs.append(data['pos'][0])
        ys.append(data['pos'][1])
        zs.append(-1*data['pos'][2])
        color.append(data['color'])
        
    ax.scatter(xs, ys, zs, marker='o', s= 150, alpha=0.5, edgecolors='none', color=color)    
    
    for edge in g.edges:
        data = g.edges[edge]
        p1 =  g.nodes[edge[0]]['pos']
        p2 =  g.nodes[edge[1]]['pos']
        x = [p1[0],p2[0]]
        y = [p1[1],p2[1]]
        z = [-1*p1[2],-1*p2[2]]
        
        ax.plot(x, y, z, linestyle = data['linestyle'],color='grey')
    
    # ax.legend()
    ax.set_zlim(-3,-10)
    
    if ticks_off:
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
    if axis_off:
        ax.set_axis_off()
    
    ax.view_init(view[0], view[1]) 
    plt.show() 
    if fig_save:
        fig.savefig(fig_save)


