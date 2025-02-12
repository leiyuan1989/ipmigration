# -*- coding: utf-8 -*-
"""
@author: leiyuan
"""
import os
import re
import networkx as nx
import matplotlib.pyplot as plt

from src.pr.smt_router import MIPGraphRouter


class Router:
    def __init__(self, struct_name, route_graph, nets, signals, node_cost_fn, edge_cost_fn):
        self.struct_name = struct_name
        self.graph = route_graph
        self.nets = nets
        self.signals = signals
        self.node_cost_fn = node_cost_fn
        self.edge_cost_fn = edge_cost_fn
        
        self.saved_folder = 'src/lego/struct_route/'
        self.load_saved_structs()

        self.signal_dict = {}
        for t in self.signals:
            t.sort()
            self.signal_dict[t[0]] = t
            
            
    def load_saved_structs(self):
        self.saved_structs = {}
        saved_structs_files = [t for t in os.listdir(self.saved_folder) if '.txt' in t]
        for file in saved_structs_files:
            file = file.strip()[:-4]
            s_n, ver = file.split('@')
            self.saved_structs[(s_n,int(ver))] = file
    
       
    def find_saved_structs(self):
        match = []
        for key,file in self.saved_structs.items():
            s_n, ver = key
            if s_n ==  self.struct_name:
                match.append(file + '.txt')
        
        return match
        
    def read_saved_route(self,file):
        with open(self.saved_folder + file, 'r') as f:
            lines = f.readlines()
        
        save_signal = False
        save_routed = False
        signals = []
        routes = []
        
        for line in lines:
            line = line.strip()
            if line == 'Signals':
                save_signal = True
            if line == 'End Signals':
                save_signal = False
            if line == 'Routed':
                save_routed = True            
            if line == 'End Routed':
                save_routed = False       
            if save_signal:
                points = re.findall(r"[(](.*?)[)]",line)
                signal = []
                for p in points:
                    t1,t2,t3 = p.split(',')
                    signal.append( (int(t1), int(t2), int(t3)) )
                signals.append(signal)
            if save_routed:
                points = re.findall(r"[(](.*?)[)]",line)
                route = []
                for i, p2 in enumerate(points):
                    if i!=0 and i%2==1:
                        p1 = points[i-1]
                        t11,t12,t13 = p1.split(',')
                        t21,t22,t23 = p2.split(',')
                        route.append( ( (int(t11), int(t12), int(t13)),(int(t21), int(t22), int(t23) ) ))
                routes.append(route)  
        return signals[1:], routes[1:]
    
    def signal_match(self,signals):
        for signal in signals:
            signal.sort()
            if set(signal) != set(self.signal_dict[signal[0]]):
                return False
        return True
        
    
    
    def save_struct_route(self, nets_routed):
        ver = len(self.find_saved_structs()) + 1
        self.file =  self.struct_name + '@%d'%(ver)  
        file =  self.file + '.txt'  
        
        with open(self.saved_folder + file, 'w') as f:
            f.write('Signals\n')
            for signal in self.signals:
                for p in signal:
                    f.write('(%d, %d, %d) '%(p[0],p[1],p[2]))
                f.write('\n')
            f.write('End Signals\n')
            
            f.write('Routed\n')
            for net in nets_routed.values():
                for edge in net:
                    print(net,edge)
                    p1,p2 = edge
                    f.write('[(%d, %d, %d),(%d, %d, %d)] '%(p1[0],p1[1],p1[2],p2[0],p2[1],p2[2]))
                f.write('\n')
            f.write('End Routed\n')           
            f.close()
    
    
    def smt_route(self,save=True,load=True):
        
        #TODO add preroute function here
        if load:
            matches = self.find_saved_structs()
            if matches:
                for match in matches:
                    signals, edges = self.read_saved_route(match)
                    signal_match = self.signal_match(signals)
                    if signal_match:
                        print("Find routed struct %s : %s"%(self.struct_name, match))
                        nets_routed = {k:v for k,v in zip(self.nets,edges)}
                        self.file = match[:-4]
                        return True, nets_routed
                    
            else:
                print("Cannot find routed struct: %s, use STM router"%(self.struct_name))
        
        router = MIPGraphRouter()
        result, routing_trees = router.min_steiner_tree(
                                         self.graph, self.signals,
                                         node_cost_fn=self.node_cost_fn,
                                         edge_cost_fn=self.edge_cost_fn)
        edges = [list(t.edges) for t in routing_trees]
        nets_routed = {k:v for k,v in zip(self.nets,edges)}
        
        
        if load and save:
            self.save_struct_route(nets_routed)
        
        return result, nets_routed
 
    def draw_graph(self,graph, labels, label, figsize=(8,8),ax = None, routed=None):
        if ax:
            ax,fig = ax
        else:
            fig, ax = plt.subplots(figsize=figsize )
            ax.set(title=label)

        node_pos =  {t:graph.nodes[t]['pos'] for t in graph.nodes}
        cmap= {t:graph.nodes[t]['co']  for t in graph.nodes}
        node_color = [cmap[t] for t in graph.nodes]
        # labels = {t:graph.nodes[t]['net'] for t in graph.nodes}

        nx.draw_networkx(graph, pos=node_pos, nodelist= graph.nodes, ax =ax, labels = labels,
                 node_color=node_color, node_size=100, with_labels=True, font_size = 10, edge_color='lightgray') 

        if routed:
            colors = ['red', 'blue', 'green', 'orange', 'violet','cyan','yellow']
            for i, net in  enumerate(routed):
                edges = routed[net]
                nx.draw_networkx_edges(graph, node_pos, edgelist=edges, width=4, edge_color=colors[i%7])

        fig.savefig(self.saved_folder + self.file + '.jpg')



    #draw noted graph and save
    # save routed to a easy look and save foramt
    














