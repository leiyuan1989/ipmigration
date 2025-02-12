# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 10:32:44 2024

@author: leiyuan
"""

import itertools
import networkx as nx

from src.lego.layout.instance import CT_GT, M1_Route
from src.pr.smt_router import MIPGraphRouter

class Channels:
    def __init__(self, structs_queue, ckt, pin_locs):
        self.structs_queue = structs_queue
        self.ckt = ckt
        self.pin_locs = pin_locs
        self.data = {}
        
        
        for struct in structs_queue:
            signal_nets = list(struct.net_mapping.values())
            if 'VDD' in signal_nets:
                signal_nets.remove('VDD')
            if 'VSS' in signal_nets:
                signal_nets.remove('VSS')
            struct.signal_nets  = signal_nets
        nets_loc = {}
        for net in ckt.nets_cdl:
            if net != 'VDD' and net != 'VSS':
                nets_loc[net] = []
                for i, struct in enumerate(structs_queue):
                    if net in struct.signal_nets:
                        nets_loc[net].append(i)
        for i, struct in enumerate(structs_queue):
            for net, loc in nets_loc.items():
                if len(loc) ==1:
                    if loc[0] == i:
                        struct.internal_nets.append(net)
                    else:
                        pass
                else: #len loc >1
                    if min(loc) == i:
                        struct.right_nets.append(net)
                    elif max(loc) == i:
                        struct.left_nets.append(net)
                    elif min(loc) < i and max(loc) > i:
                        struct.cross_nets.append(net)
                        #add net 
                        #TODO maybe error
                        t = structs_queue[min(loc)].net_mapping_r[net] 
                        struct.net_mapping[t] = net
                        struct.net_mapping_r[net] = t
    
    def add_data(self,key,data):
        self.data[key] = data
        
    def draw(self, ckt):
        for k,v in self.data.items():
            for layer in v:    
                for box in v[layer]:
                    ckt.db_shapes[layer].insert(box.to_dbBox())                      
                        
    def graph_route(self):   
        values = []
        for s,v in self.pin_locs.items():
            t = []
            for i, pin_loc in enumerate(v):
                t.append((s,i))
            values.append(t)
        
        count = 1
        for value in itertools.product(*values):
            print("Begin %d try to route for channels!"%(count))
            pin_locs = {t[0]:self.pin_locs[t[0]][t[1]] for t in value}
           
            for i, struct in enumerate(self.structs_queue):
                # print('abc',struct.struct_ckt.name,pin_locs)
                for net in struct.left_nets:
                    struct.left_pins[net] = pin_locs[struct.struct_ckt.name][struct.net_mapping_r[net]]['l']
                for net in struct.right_nets:
                    struct.right_pins[net] = pin_locs[struct.struct_ckt.name][struct.net_mapping_r[net]]['r']
                
                for j,net in enumerate(struct.cross_nets):
                    left_struct = self.structs_queue[i-1]
                    if not(net in left_struct.right_pins):
                        raise ValueError
                    #TODO, align left cross nets, may be consider poly cross in the future
      
                    struct.left_pins[net]  = left_struct.right_pins[net]
                    struct.right_pins[net] = left_struct.right_pins[net]
                
            channel_route_result = []
            channel_nets_routed = []
            for i, s_right in enumerate(self.structs_queue[1:]):      
                s_left = self.structs_queue[i]         

                result, nets_routed = self.route_channel_graph(s_left, s_right)
                if result:
                    channel_route_result.append(0)
                    channel_nets_routed.append(nets_routed)
                else:
                    print('Channel route failed between %s and %s'%(s_left.struct_ckt.name, s_right.struct_ckt.name) )
                    channel_route_result.append(1)
                    break
            
            count += 1
            if sum(channel_route_result) == 0:
                print('Channel route succeed!' )
                self.channel_nets_routed = channel_nets_routed
                
                
                return True, channel_nets_routed, pin_locs
                break
            
        return False, [],[]
            #examine pin_locs
           
           
    def route_channel_graph(self,struct_left,struct_right):   
        left_pins = struct_left.right_pins 
        right_pins = struct_right.left_pins
        G = nx.Graph()
        #TODO 6 maybe change or parameterized
        num_tracks, gt_tracks = [6, [3,4]]
        
        #create graph
        for i in range(num_tracks):
            G.add_node((1,i+1,0), pos=(1,i+1), net='', ct='no', co='green')
            if i+1 in gt_tracks:
                G.add_node((1,i+1,1), pos =(1+0.3,i+1+0,3), net='', ct='no', co='blue')        
        for net,loc in left_pins.items():
            if loc[1] == 0:
                G.add_node((0,loc[0],loc[1]), pos=(0,loc[0]), net=net, ct='no', co='green')
            elif loc[1] == 1:
                G.add_node((0,loc[0],loc[1]), pos=(0+0.3,loc[0]+0.3), net=net, ct='no', co='blue')
        for net,loc in right_pins.items():
            if loc[1] == 0:
                G.add_node((2,loc[0],loc[1]), pos=(2,loc[0]), net=net, ct='no', co='green')
            elif loc[1] == 1:
                G.add_node((2,loc[0],loc[1]), pos=(2+0.3,loc[0]+0.3), net=net, ct='no', co='blue')
        
        #create edge
        for p1 in G.nodes:
            for p2 in G.nodes:
                if ((p1[0]-p2[0])== 1 and (p1[1]==p2[1])) or ((p1[1] - p2[1]) == 1 and (p1[0] == p2[0])):
                    if p1[2] == p2[2]:
                        G.add_edge(p1, p2)
                if (p1[0] == p2[0]) and (p1[1] == p2[1]) and (p1[2] != p2[2]):
                    G.add_edge(p1, p2)                

        #create net graph for channel
        graph_net = {}
        for node in G.nodes:
            net = G.nodes[node]['net']
            if  net != '':
                if net in graph_net:
                    graph_net[net].append(node)
                else:
                    graph_net[net] = [node]

        nets = list(graph_net.keys())
        signals = list(graph_net.values())
        #not load from json
        router = MIPGraphRouter()
        result, routing_trees = router.min_steiner_tree(G, signals,
                                         node_cost_fn=None,
                                         edge_cost_fn=lambda e: 1)
        if result:
            
            edges = [list(t.edges) for t in routing_trees]
            nets_routed = {k:v for k,v in zip(nets,edges)}    
              
            return True,nets_routed
        
        else:
            return False,[]
            
    def detail_route(self, tech, cells, index, start_x):  
        
        s_left = self.structs_queue[index]
        s_right = self.structs_queue[index+1]
       
        nets_routed = self.channel_nets_routed[index]
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
 
    
        if s_left.v_mode == s_right.v_mode:
            v_tracks = cells.v_mode[s_left.v_mode]['tracks']
            space = max(tech.M1_S.v+tech.M1_W.v, tech.GT_S.v+tech.GT_W.v)  
            space = max(space, tech.CT_S_AA.v + tech.CT_W.v + tech.CT_E_AA.v)
            #consider tech.CT_GT_W_half
            
            h_tracks = [start_x,start_x+space,start_x+space+space]
            
            matrix = []
            for x in h_tracks:
                col = []
                for y in v_tracks:
                    col.append((x,y.c))
                matrix.append(col)
            
            
            #1 GT
            for x,y,z in gt_ct_nodes:
                loc = (matrix[x][y-1])
                ct_gt = CT_GT( tech, loc, mode = 'centre')
                self.add_data((x,y),ct_gt.data)
            
            #2 route
            if len(gt_edges) >0:
                gt_nets = M1_Route(tech, gt_edges, matrix, 2*tech.CT_GT_W_half, {})
                gt_nets.data = {'GT':gt_nets.data['M1']}
           
                self.add_data((index,'gt_nets'), gt_nets.data)
            
            #3
            m1_nets = M1_Route(tech, m1_edges, matrix, tech.M1_W.v, {})
            self.add_data((index,'m1_nets'), m1_nets.data)     
            
            return h_tracks[-1]
            
        else:
            #TODO idea: add a new col to align
            pass
        