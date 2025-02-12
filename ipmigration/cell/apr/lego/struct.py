# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 18:21:47 2024

@author: leiyuan
"""
import os
import itertools
import json
import pandas as pd
import networkx as nx
import numpy as np


from src.pr.router import Router
from src.lego.graph import GraphNets
from src.lego.dro import ColSpace
from src.lego.layout.instance import GT_AA, CT_GT, GT_Route, M1_Route,AA_SD,POWER

'''
add struct merge input d and dff make sure that device name are not same

'''

class Struct:

    def __init__(self, struct_type, struct_ckt, devices, match_table):
        self.struct_type = struct_type
        self.struct_ckt  = struct_ckt
        self.struct_ckt_name = self.struct_ckt.name
        self.data = {}
        
        self.v_tracks_num = 6 #TODO revise future
        
        self.devices     = devices
        self.match_table = match_table
        self.match_devices()
        self.struct_ckt.extract_nets()
        self.nets_cdl = self.struct_ckt.nets_cdl
        # if self.struct_ckt.name == 'CLK1':
        #     print([t.W for t in self.devices])
        #     print([t.W for t in self.struct_ckt.devices]  )  
        #
        self.signal_nets = []
        self.left_nets = []
        self.right_nets = []
        self.cross_nets = []
        self.internal_nets = []
        #
        self.left_pins  = {}
        self.right_pins = {}
        
        # self.pin_locs = []
        
        #layout
        self.v_mode = 0
        
        self.route_folder = 'src/lego/layout/route/'
        self.load_from_saved = True
        
    def __repr__(self):
        return "( {}->{} )".format(self.struct_type, self.struct_ckt_name)        
        
    def match_devices(self):
        self.device_mapping = {}
        self.net_mapping = {}
        self.net_mapping_r = {}
        
        for k,v in self.match_table.items():
            if self.struct_ckt.find_device(k):
                device_struct = self.struct_ckt.get_device(k)
                devices = self.devices
                device = [t for t in devices if t.name == v][0]
                device_struct.W = device.W 
                device_struct.L = device.L 
                device_struct.NF = device.NF       
                self.device_mapping[k] = device
            else:
                #net                                                                                                                                                                                                                                                
                self.net_mapping[k] = v
                self.net_mapping_r[v] = k
                
    def merge_struct(self, struct):
        pass

    def add_data(self,key,data):
        self.data[key] = data

    def save_apr(self):
        pass
        #tuple to list
    def load_apr(self):
        pass
        #list to tuple


    def draw(self, ckt):
        for k,v in self.data.items():
            for layer in v:    
                for box in v[layer]:
                    ckt.db_shapes[layer].insert(box.to_dbBox())

    def global_pr_7T(self, ckt, start_x = 0, ):
        print('Begin process struct %s'%(self.struct_ckt.name))
        #first search inv, cross, common gate 
        
    
        #create devices array
        self.cols =max([t.COL for t in self.struct_ckt.devices])
        self.devices_array = []
        for col in range(self.cols):
            pn = {'P':None,'N':None,'G_COL':0,'P_ROW':0,'N_ROW':0}
            for device in self.struct_ckt.devices:
                if device.COL == (col + 1):
                    pn[device.T] = device
                    pn[device.T+'_ROW'] = device.ROW
            self.devices_array.append(pn)     
  
        #TODO     
        graph = self.create_graph_v1(self.devices_array, start_x, edge_cost={})

        route_result = False
        #save load apr here
        if self.load_from_saved:
            pass
            # graph_net, ct_aa_nodes, nets_routed
           
        graph_nets = GraphNets(self, ckt, graph)

        for graph_net,block_nodes,ct_aa_nodes,one_node_net in graph_nets.canditate():
            
            #TODO load canditate here       
            #TODO save graph_net,block_nodes,ct_aa_nodes,one_node_net here
            # print('graph_net', graph_net)    
            # print('block_nodes', block_nodes)      
            # print('ct_aa_nodes', ct_aa_nodes)   
            # print('routed_nets', graph_nets.routed_nets)   
            # print('one_node_net', one_node_net)
            #route here           
            route_graph = graph.copy()         

            for t in block_nodes:
                route_graph.remove_node(t)

            #TODO one node net # prerouted   problem:maybe prerouted or abumentment 
            for t in one_node_net.values():
                for t1 in t:
                    route_graph.remove_node(t1)
            
            nets = list(graph_net.keys())
            signals = list(graph_net.values())
            
            
            node_cost_fn = None
            edge_cost_fn = lambda e:1 #
            #router here
            router = Router(self.struct_ckt_name, route_graph, nets, signals, node_cost_fn, edge_cost_fn)
            result, nets_routed = router.smt_route()
            # nodes_label = graph_nets.postprocess_nets(graph_net, ct_aa_nodes)
            # self.draw_graph(graph, nodes_label, ckt.name + '->' + self.struct_ckt.name ,figsize=(cols*2,8))


            if result:
                route_result = True
                # self.unrouted_nets = graph_net
                break

        if route_result:
            post_result= graph_nets.postprocess_nets(graph_net, ct_aa_nodes, nets_routed=nets_routed)
            nodes_label,nets_routed,m1_edges,gt_edges,gt_ct_nodes,ct_aa_nodes = post_result            
            
            router.draw_graph(graph, nodes_label, ckt.name + ': ' + self.struct_ckt.name, routed=nets_routed )
            
            self.m1_edges = m1_edges
            self.gt_edges = gt_edges
            self.gt_ct_nodes = gt_ct_nodes
            self.ct_aa_nodes = ct_aa_nodes
            self.power_nets = graph_nets.power_nets
            self.one_node_net = one_node_net
            self.graph_net = graph_net
            
            self.router = router
            
            return True

        else:
            raise ValueError
            
        #test
        self.graph = graph
        self.graph_nets = graph_nets
        self.start_x = start_x
              


    
    def create_graph_v1(self, devices_array, start_x, edge_cost):   
        #TODO need optimize
        v_num = 6
        offset = 0.3

        self.col_type = []
        self.mos_loc = []
        #create nx.graph 
        G = nx.Graph()
        x = start_x
        
        for col,pn in enumerate(devices_array):
            if pn['P'] == None and pn['N'] == None:
                self.col_type.append(0)
                self.mos_loc.append({})
                for i in range(v_num):
                    G.add_node((x,i+1,0), pos=(x,i+1), net='', ct='no', co='green')
                    if i == 2 or i ==3:
                        G.add_node((x,i+1,1), pos =(x+offset,i+1+offset), net='', ct='no', co='blue')    
                    #add GT CT edge
                x = x + 1
            else:
                self.col_type.append(1)
                self.col_type.append(2)
                self.mos_loc.append({})
                self.mos_loc.append(pn)
                for i in range(v_num):
                    G.add_node((x,  i+1,0), pos=(x,i+1),   net='', ct='no', co='green')
                    G.add_node((x+1,i+1,0), pos=(x+1,i+1), net='', ct='no', co='green')
                    if i == 2 or i ==3:
                        G.add_node((x,  i+1,1), pos =(x+offset,  i+1+offset), net='', ct='no', co='blue')  
                        G.add_node((x+1,i+1,1), pos =(x+1+offset,i+1+offset), net='', ct='no', co='blue')                 
                
                if pn['P'] or pn['N']:
                    pn['G_COL'] = x+1                
                x = x + 2 
        self.col_type.append(1) 
        self.mos_loc.append({})
        for i in range(v_num):
            G.add_node((x,  i+1,0), pos=(x,i+1),   net='', ct='no', co='green')
            if i == 2 or i ==3:
                G.add_node((x,  i+1,1), pos =(x+offset,i+1+offset), net='', ct='no', co='blue')  
        
        self.max_col = x
        #add edges
        #TODO: edge_cost
        for p1 in G.nodes:
            for p2 in G.nodes:
                if ((p1[0]-p2[0])== 1 and (p1[1]==p2[1])) or ((p1[1] - p2[1]) == 1 and (p1[0] == p2[0])):
                    if p1[2] == p2[2]:
                        G.add_edge(p1, p2, weight =1)
                if (p1[0] == p2[0]) and (p1[1] == p2[1]) and (p1[2] != p2[2]):
                    G.add_edge(p1, p2, weight =1)
        return G
                
        
        
    def detail_pr_7T(self, ckt, tech, cells, start_x=0):
        '''
        self.rail_vdd_ct = Range(self.cell_height-half_ct_s-tech.CT_W.v, self.cell_height-half_ct_s, set_t = 'pp')
        self.rail_vss_ct = Range(0+half_ct_s, 0+half_ct_s + tech.CT_W.v, set_t = 'pp')        

        self.v_mode['1'] = {'tracks': [self.net_m1_down, mos_ct_down, gt_ct_down,gt_ct_up,mos_ct_up, self.net_m1_up]}
        self.v_mode['1']['AA_pmos'] = Range(AA_p_up, AA_p_down,set_t='pp')
        self.v_mode['1']['AA_nmos'] = Range(AA_n_up, AA_n_down,set_t='pp')
        
        first calculate each col axis, take account global routing result
        
        '''
        #TODO, set v mode type, num of v tracks same with self.v_tracks_num
        v_mode = cells.v_mode[self.v_mode]
        v_tracks = v_mode['tracks']
        gt_range_p =  v_mode['GT_pmos']
        gt_range_n =  v_mode['GT_nmos']
        aa_range_p =  v_mode['AA_pmos']
        aa_range_n =  v_mode['AA_nmos']
        
        #TODO if not add , strcut ckt is shared  but struct is not shared
        self.match_devices() 
   
        self.end_of_line_examine()
        self.tech_process(start_x,tech,cells)
        
        #TODO cal here space
        #TODO condider end of line detect and pass to m1_route

        matrix = []
        for c in range(self.max_col+1):
            col = []
            for r in range(self.v_tracks_num):
                col.append((self.h_tracks[c],v_tracks[r].c))
            matrix.append(col)
        
        
        #1 CT because of vdd vss this may move to last
        for x,y,z in self.gt_ct_nodes:
            loc = (matrix[x][y-1])
            ct_gt = CT_GT( tech, loc, mode = 'centre')
            self.add_data((x,y),ct_gt.data)
        
        #2 route
        gt_nets = GT_Route(tech, self.gt_edges, matrix, self.col_type, 
                           col_w1 = tech.GT_W.v, 
                           col_w2 = tech.CT_GT_W_half*2, 
                           col_w3 = min(cells.mos_length_P,cells.mos_length_N))
        
        # gt_nets.draw(ckt)
        self.add_data('gt_nets',gt_nets.data)
        
        
        m1_nets = M1_Route(tech, self.m1_edges, matrix, tech.M1_W.v, self.eol_nodes)
        self.add_data('m1_nets',m1_nets.data)
        
        
        #3 MOS
        for i,pn in enumerate(self.mos_loc):
            if len(pn) >0:
                pmos = pn['P']
                nmos = pn['N']
                x = matrix[i][0][0]
                if pmos:
                    gt_aa = GT_AA(tech, x, gt_range_p, aa_range_p, pmos)
                    self.add_data(pmos.name,gt_aa.data)
                if nmos:
                    gt_aa = GT_AA(tech, x, gt_range_n, aa_range_n, nmos)
                    self.add_data(nmos.name,gt_aa.data)
        
        #4 AA SD
        for i,pn in enumerate(self.mos_loc):
            ct_nodes_p = [t for t in self.ct_aa_nodes if t[1]>(self.v_tracks_num/2) and t[0] == i]
            ct_nodes_n = [t for t in self.ct_aa_nodes if t[1]<=(self.v_tracks_num/2) and t[0] == i]
            ##????
            
            if i == 0:
                mos_l_p = None
                mos_l_n = None
                pn = self.mos_loc[i+1]
                if len(pn)>0:
                    if pn['P']:
                        mos_r_p = self.data[pn['P'].name]
                    else:
                        mos_r_p = None
                    if pn['N']:
                        mos_r_n = self.data[pn['N'].name]
                    else:
                        mos_r_n = None
                else:
                    mos_r_p = None
                    mos_r_n = None
            elif i >0 and i != len(self.mos_loc) - 1:
                pn = self.mos_loc[i-1]

                if len(pn)>0:
                    if pn['P']:
                        mos_l_p = self.data[pn['P'].name]
                    else:
                        mos_l_p = None
                    if pn['N']:
                        mos_l_n = self.data[pn['N'].name]               
                    else:
                        mos_l_n = None
                else:
                    mos_l_p = None
                    mos_l_n = None
                pn = self.mos_loc[i+1]

                if len(pn)>0:
                    if pn['P']:
                        mos_r_p = self.data[pn['P'].name]
                    else:
                        mos_r_p = None
                    if pn['N']:
                        mos_r_n = self.data[pn['N'].name]               
                    else:
                        mos_r_n = None
                else:
                    mos_r_p = None
                    mos_r_n = None                
            else: 
                mos_r_p = None
                mos_r_n = None
                pn = self.mos_loc[i-1]
                if len(pn)>0:
                    if pn['P']:
                        mos_l_p = self.data[pn['P'].name]
                    else:
                        mos_l_p = None
                    if pn['N']:
                        mos_l_n = self.data[pn['N'].name]
                    else:
                        mos_l_n = None
                else:
                    mos_l_p = None
                    mos_l_n = None          
                
            if mos_l_p or mos_r_p:
                
                aa_sd = AA_SD(tech, 'P', i , mos_l_p, mos_r_p, matrix, ct_nodes_p)
                
                self.add_data(('P',i),aa_sd.data)
            
            if mos_l_n or mos_r_n:
                aa_sd = AA_SD(tech, 'N', i , mos_l_n, mos_r_n, matrix, ct_nodes_n)
                self.add_data(('N',i),aa_sd.data)        
        
        #5 power   
        power = POWER(tech, cells, self.power_nodes_prop, matrix, aa_range_p, aa_range_n)
        self.add_data('power',power.data)    
        

        #may move to ascell for merge
        
        return self.h_tracks[-1]
            


    #TODO move to dro
    def tech_process(self,start_x,tech,cells):
  
        
        
        self.power_nodes_prop = {}
        self.ct_nodes_prop = {}
        self.m1_edges_nodes = []
        self.gt_edges_nodes = []


        graph = self.create_graph_v1(self.devices_array, 0, 1)
        graph.remove_edges_from(graph.edges)
        cols = max([t[0] for t in graph.nodes])
        rows = max([t[1] for t in graph.nodes])
        
        #add edge
        for net, nodes in self.m1_edges.items():
            for n0,n1 in nodes:
                graph.nodes[n0]['net'] = net
                graph.nodes[n1]['net'] = net
                graph.add_edge(n0,n1)
                self.m1_edges_nodes.append(n0)
                self.m1_edges_nodes.append(n1)

        for net, nodes in self.gt_edges.items():
            for n0,n1 in nodes:
                graph.nodes[n0]['net'] = net
                graph.nodes[n1]['net'] = net
                graph.add_edge(n0,n1)
            
                self.gt_edges_nodes.append(n0)
                self.gt_edges_nodes.append(n1)

        self.m1_edges_nodes = list(set(self.m1_edges_nodes))
        self.gt_edges_nodes = list(set(self.gt_edges_nodes))
        
        #process power
        for node in self.power_nets['VDD']:
            m1_to_power = True
            graph.nodes[node]['net'] = 'VDD'            
            for i in range(node[1], rows+1):
                if (node[0],i,0) in self.m1_edges_nodes:
                    m1_to_power = False
            self.power_nodes_prop[node] = {'m1_to_power':m1_to_power,'type':'VDD'}
            
        for node in self.power_nets['VSS']:
            m1_to_power = True
            graph.nodes[node]['net'] = 'VSS'       
            for i in range(1, node[1]+1):
                if (node[0],i,0) in self.m1_edges_nodes:
                    m1_to_power = False   
            self.power_nodes_prop[node] = {'m1_to_power':m1_to_power,'type':'VSS'}
         

         
        #process space
        self.spaces = []
        for i in range(cols+1):
            #begin 
            if i != cols:
                col_type = self.col_type[i]
                right_col_type = self.col_type[i+1]
                pn = self.mos_loc[i]
                pn_right = self.mos_loc[i+1]
                
                space = ColSpace(tech, col_type, right_col_type, pn, pn_right)
                
                for j in range(rows):
                    #m1 
                    node_l = (i,j+1,0)
                    node_r = (i+1,j+1,0)
                    
                    net_l = graph.nodes[node_l]['net']
                    net_r = graph.nodes[node_r]['net']
                    if net_l != '' and net_r != '':
                        if net_l != net_r: 
                            eol_num = 0
                            if node_l in self.eol_nodes:
                                eol_num += 1
                            if node_r in self.eol_nodes:
                                eol_num += 1                            
                            space.add_M1_S_rule(eol_num)
                        else:
                            if not(graph.has_edge(node_l,node_r)):
                                eol_num = 0
                                if node_l in self.eol_nodes:
                                    eol_num += 1
                                if node_r in self.eol_nodes:
                                    eol_num += 1                            
                                space.add_M1_S_rule(eol_num)
                    
                    
                    #GT
                    node_l = (i,j+1,1)
                    node_r = (i+1,j+1,1)
                    
                    if node_l in graph.nodes and node_r in graph.nodes:
                        net_l = graph.nodes[node_l]['net']
                        net_r = graph.nodes[node_r]['net']
                        if net_l != '' and net_r != '':
                            if net_l != net_r:
                                space.add_GT_S_rule()
                            else:
                                if not(graph.has_edge(node_l,node_r)):
                                    space.add_GT_S_rule()
                self.spaces.append(space)          

        self.h_tracks = [start_x]
        for t in self.spaces:
            start_x = start_x+t.max_space
            self.h_tracks.append(start_x)
            
              
        #  ct_aa_nodes  
        connect_ct = []
        
        for node in self.ct_aa_nodes:
            if node in self.m1_edges_nodes:
                connect_ct.append(node)
            else:
                #TODO add for left and right nodes
                pass
        self.ct_aa_nodes = connect_ct
                

        
    def end_of_line_examine(self):
        #TODO L shape on ct
        self.eol_nodes = {}
        for net, values in self.m1_edges.items():
            nodes = []
            for t1,t2 in values:
                nodes.append(t1)
                nodes.append(t2)
            nodes = list(set(nodes))
            
            for node in nodes:
                t = []
                t2 = []
                
                x,y,z = node
                if (x+1,y,z) in nodes:
                    t.append((x+1,y,z))
                    t2.append('e')
                if (x-1,y,z) in nodes:
                    t.append((x-1,y,z)) 
                    t2.append('w')
                if (x,y+1,z) in nodes:
                     t.append((x,y+1,z))     
                     t2.append('n')
                if (x,y-1,z) in nodes:
                    t.append((x,y-1,z)) 
                    t2.append('s')
                if len(t) == 1:
                    if node in self.ct_aa_nodes or  node in self.gt_ct_nodes:
                       self.eol_nodes[node] = t2[0]


    




      


