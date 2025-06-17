#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: leiyuan
"""
import os
import copy
from ipmigration.cell.apr.cir.decompose import DeCKT
from ipmigration.cell.apr.pr.pattern_apr import PatternAPR
from ipmigration.cell.apr.utils.utils import concatenate_images
from ipmigration.cell.apr.cir.patterns import PatternRouter,PatternDrawer
from ipmigration.cell.apr.lyt.instance import M1_Rails,NPWELL

class StdCell:
    def __init__(self, ckt, tech, cfgs, patterns,route_db,aux_file,place_file):
        self.name = ckt.name
        self.ckt = ckt
        self.tech = tech
        self.cfgs = cfgs
        self.patterns= patterns
        self.route_path = []
        self.route_db = route_db
        self.aux_file = aux_file
        self.place_file = place_file
        self.load_place = cfgs.load_place
        
        
    def run(self,top_layout,db_layers):
        result,msg = self.global_pr()
        
        if result:
            self.init_layout(top_layout,db_layers)
            # save_fig_path = os.path.join(self.cfgs.output_dir,'route','%s.png'%(self.ckt.name))
            # concatenate_images(self.route_path, save_fig_path)
            # result = self.detail_pr()        
        else:
            pass
            
        
        return result,msg
    
    def init_layout(self,top_layout,db_layers):
        self.db_layout = top_layout.create_cell(self.ckt.name)
        self.db_shapes = {}
        for name in db_layers:
            self.db_shapes[name] = self.db_layout.shapes(db_layers[name]) 
    
    def global_pr(self):
        print(' %s Global_PR:'%(self.ckt.name))
        self.ckt.combine_parallel()
        self.de_ckt = DeCKT(self.ckt, 
                            self.patterns, 
                            self.tech.tech_name, 
                            self.cfgs.output_dir,
                            self.aux_file)
        #decompose
        result = self.de_ckt.run()
                
        if result:  
            
            self.apr = PatternAPR(self.ckt, self.de_ckt.sub_ckts, self.place_file, 6 , self.load_place)
            self.apr.place()
            self.apr.route()
            # queue = pat_placer.find_opt_perm(self.ckt.ckt_type)

            
            
            return 1, "Success"
        else:

            return 0, "Decompose Failed"      
        
        
        self.side_nodes_statistics = []
        if result:  
            #netlist decomposition sucessfully
            pat_placer = Placer(self.de_ckt.sub_ckts)
            queue = pat_placer.find_opt_perm(self.ckt.ckt_type)
            
            
            self.queue = [self.de_ckt.sub_ckts[t] for t in queue]
            #TODO: Visualization this part with multi-graph
            
            self.extract_ext_net(self.queue)
            
            l_nodes_ext = {}
            
            route_rst = True  
            
            for loc,p in enumerate(self.queue):
                name = p.pattern_name
                p.map_ext_nets()
 
                rst = self.global_net_locs(l_nodes_ext,
                                     p.left_nets_in,p.right_nets_in,p.cross_nets_in,
                                     p.left_nets,p.right_nets,p.cross_nets)
                l_nodes,r_nodes,m2_nodes,m2_cad_nodes,v1_nodes,r_nodes_ext = rst
                l_nodes_ext = r_nodes_ext
                self.side_nodes_statistics.append([self.ckt.name,name,
                                                   p.left_nets_in,p.right_nets_in,p.cross_nets_in,
                                                   p.left_nets,p.right_nets,p.cross_nets])
                
                save_fig_path = os.path.join(self.cfgs.output_dir,'route','temp_%s-%s_%d.png'%(self.ckt.name,p.pattern_name,loc))
                pt_router = PatternRouter(p.pattern_ckt, self.tech.M1_tracks_num, 
                                          self.route_db)
                pt_router.gen_graph()

                results= self.route_db.find(name,l_nodes,r_nodes,m2_nodes)
    
                result, graph_index, routed_edges, io_pins, pw_pins, m2_edges,v1_pins = results
                if result:
                    print('  %s found in RouteDB!'%(name))
                    graph,route_nets = pt_router.graph[graph_index]
                    pt_router.routing(graph,route_nets,
                                      l_nodes,r_nodes,m2_nodes,v1_nodes,
                                      is_load=True, 
                                      load=[routed_edges, io_pins, pw_pins, m2_edges,v1_pins],
                                      savefig = save_fig_path) 
                    self.route_path.append(save_fig_path)
                    p.pt_router = pt_router
                else:
                    print('  %s is not found in RouteDB! Route by Router'%(p.pattern_name))
                    route_rst = False
                    # print(l_nodes,r_nodes,m2_nodes)
                    for graph_index, (graph,route_nets) in pt_router.graph.items():      
                        results = pt_router.routing(graph,route_nets,
                                                    l_nodes,r_nodes,m2_nodes,v1_nodes,
                                                    savefig = save_fig_path) 
                        result, routed_edges, io_pins, pw_pins,m2_edges,v1_pins = results                         
                        if result:
                            self.route_db.update(name, l_nodes, r_nodes,m2_nodes, graph_index, 
                                   routed_edges, io_pins, pw_pins, m2_edges,v1_pins, save=True)
                            route_rst = True
                            self.route_path.append(save_fig_path)
                            p.pt_router = pt_router
                            break
                    if not(route_rst):
                        l_nodes_o = copy.deepcopy(l_nodes)
                        r_nodes_o = copy.deepcopy(r_nodes)
                        m2_nodes_o =  copy.deepcopy(m2_nodes)
                        route_rst = False
                        for k,v in m2_cad_nodes.items():
                            m2_nodes[k] = v
                            l_nodes.pop(k)
                            r_nodes.pop(k)
                            v1_nodes[k] = [(0,v[0],v[1]),(1,v[0],v[1])]
                            
                            for graph_index, (graph,route_nets) in pt_router.graph.items():      
                                results = pt_router.routing(graph,route_nets,
                                                            l_nodes,r_nodes,m2_nodes,v1_nodes,
                                                            savefig = save_fig_path) 
                                result, routed_edges, io_pins, pw_pins,m2_edges,v1_pins = results                         
                                if result:
                                    self.route_db.update(name, l_nodes_o, r_nodes_o,m2_nodes_o, graph_index, 
                                           routed_edges, io_pins, pw_pins, m2_edges, v1_pins, save=True)
                                    route_rst = True
                                    self.route_path.append(save_fig_path)
                                    p.pt_router = pt_router
                                    break
                            if route_rst:
                                break
                if not(route_rst):
                    print('  %s cannot be routed!'%(name))
                    break
            if route_rst:
                # print('$$$$ %s is successfully routed!'%(self.ckt.name))
                print('------------------All Success: %s------------------'%(self.ckt.name))
                return 1
            else:
                # print('**** %s is not routed!'%(self.ckt.name))
                print('------------------Fail: %s------------------'%(self.ckt.name))
                return 0

        else:
            print('------------------Decompose Failed: %s------------------'%(self.ckt.name))
            return 0
        

    
    def detail_pr(self):
        #init db layout and cell and shapes of cell, then we can use insert function.
        x = self.cfgs.cell_offset_x + self.tech.CT_E_AA.v + self.tech.CT_W.hv 
        x = self.cfgs.cell_offset_x #revise to up if is_start is used in future
        for i, pattern in enumerate(self.queue): 
            is_start = True if i == 0 else False 

            pt_drawer = PatternDrawer(pattern, self)
            x = pt_drawer.run(x,is_start)
            pt_drawer.draw()
      
            pattern.pt_drawer = pt_drawer
        self.post_process(right= x)
       

            # if i != len(structs_queue)-1:
            #     if not(struct.struct_ckt_name in merge_structs()):
            #         x1 = channels.detail_route(self.tech, self, i, x1)
            
            
            # struct.draw(ckt)
            # x = x1
            # channels.draw(ckt)   
            
        # self.post_process_layout(ckt,x1 + side_space)  
        

     

    def extract_ext_net(self,queue):
        for pattern in queue: 
            signal_nets = list(pattern.net_map.values())
            if 'VDD' in signal_nets:
                signal_nets.remove('VDD')
            if 'VSS' in signal_nets:
                signal_nets.remove('VSS')
            pattern.signal_nets  = signal_nets
        nets_loc = {}
        for net in self.ckt.nets:
            if net != 'VDD' and net != 'VSS':
                nets_loc[net] = []
                for i, pattern in enumerate(queue):
                    if net in pattern.signal_nets:
                        nets_loc[net].append(i)
        
        for i, pattern in enumerate(queue):
            for net, loc in nets_loc.items():
                if len(loc) ==1:
                    if loc[0] == i:
                        pattern.internal_nets.append(net)

                else: #len loc >1
                    if min(loc) == i:
                        pattern.right_nets.append(net)
                    elif max(loc) == i:
                        pattern.left_nets.append(net)
                    elif min(loc) < i and max(loc) > i:
                        if net in pattern.net_map_r:
                            pattern.right_nets.append(net)
                            pattern.left_nets.append(net)
                        else:
                            pattern.cross_nets.append(net)

    def global_net_locs(self, right_nodes_ext, 
                        left_nets_in, right_nets_in, cross_nets_in,
                        left_nets, right_nets, cross_nets):
        tp = self.tech.M1_tracks_num-1
        dn = 0
        mu = self.tech.median1
        md = self.tech.median2
        ckt_type = self.ckt.ckt_type
        
        net_locs = {'C':[tp,1], 'CN':[dn,1], 
                    'E':[tp,1],'E_N0': [dn,1],
                    'PM0':[mu,1],'M': [md,1],
                    'BM':[mu,1],'S': [md,1],
                    'SE':[tp,1],'SE_N0': [dn,1],
            }
        
        
        clk_locs = {'C':[tp,1], 'CN':[dn,1]}
        net_in_locs = {'OUT1':[mu,1] }

        
        if self.ckt.enable and ckt_type in ['ff']:
            m2_loc = {'S':  [tp-1,1] }
        else:
            m2_loc = {} #m2_loc is for cross
        
        # cross_locs = {'CR1':[dn+1,1]  }
        
        

        left_nodes = {}
        right_nodes = {}
        m2_nodes = {}
        v1_nodes = {}
        m2_cad_nodes = {}
        #1
        for node,node_in in zip(left_nets,left_nets_in):
            # if node in self.ckt.key_net_mapping:      
            #     node_map = self.ckt.key_net_mapping[node]
            #     if node_map in m2_loc:
            #         left_nodes[node_in] = m2_loc[node_map]
            #     else:
            #         left_nodes[node_in] = net_locs[node_map]
            
            if node in right_nodes_ext:
                #same with left
                left_nodes[node_in] = right_nodes_ext[node]
            elif node in right_nets:
                pass
                #node in left and right and not in right_nodes_ext 
                #means it is a m2 cross node and can left it for right nodes 
                                
            else:
                print(self.ckt.name, node,node_in)
                raise ValueError
                
            if node in self.ckt.key_net_mapping: 
                node_map = self.ckt.key_net_mapping[node]
                if (node_map in m2_loc) and (node in right_nets):
                    left_nodes.pop(node_in)
                    t = m2_loc[node_map]
                    m2_nodes[node_in] = t
                    v1_nodes[node_in] =[(1,t[0],t[1])]
                
        #2
        for node,node_in in zip(right_nets,right_nets_in):
            if node in self.ckt.key_net_mapping:
                node_map = self.ckt.key_net_mapping[node]
                if node_map in m2_loc:
                    t = m2_loc[node_map]
                    right_nodes[node_in] = t
                    right_nodes_ext[node] = t
                    v1_nodes[node_in] = [(1,t[0],t[1])]
                else:
                    right_nodes[node_in] = net_locs[node_map]
                    right_nodes_ext[node] = net_locs[node_map]
            elif node_in in net_in_locs:
                loc = net_in_locs[node_in]
                right_nodes[node_in] = loc
                right_nodes_ext[node] = loc
            else:
                print(self.ckt.name, node,node_in)
                raise ValueError       
           
        #TODO : we need add left_nets m2, right_nets_m2...    
        for node,node_in in zip(cross_nets,cross_nets_in):
            if node in self.ckt.key_net_mapping:
                node_map = self.ckt.key_net_mapping[node]
                if node_map in m2_loc:
                    m2_nodes[node_in] = m2_loc[node_map]
                else:
                    loc = right_nodes_ext[node]
                    left_nodes[node_in] = loc
                    right_nodes[node_in] = loc
                    right_nodes_ext[node] = loc                    
                    if not(node_map in clk_locs):
                        m2_cad_nodes[node_in] = loc
                        
                    
            else:
                loc = right_nodes_ext[node]
                left_nodes[node_in] = loc
                right_nodes[node_in] = loc
                right_nodes_ext[node] = loc                
                
                m2_cad_nodes[node_in] = loc

                
                # print(self.ckt.name, node,node_in)
                # raise ValueError         
                
        # print(left_nodes,right_nodes,m2_nodes,m2_cad_nodes,right_nodes_ext)
        return left_nodes,right_nodes,m2_nodes,m2_cad_nodes,v1_nodes,right_nodes_ext
        
        
        
        

   
    def post_process(self, right, left=0, m2_tracks=False):
        #TODO add merge shapes
        self.data = []
        
        #draw power ground rail
        m1_rails  = M1_Rails(self.tech, left, right)
        self.data.append(m1_rails.data)
      
        
        # if m2_tracks:
        #     m2_tracks = M2_Tracks(self, left, right)
        #     m2_tracks.draw(ckt)
        
        # #border and diffusion
        npwell = NPWELL(self.tech,self.cfgs,m1_rails.border_box)
        self.data.append(npwell.data)
        self.draw()

    
    def draw(self):
        for v in self.data:
            for layer in v:    
                for box in v[layer]:
                    self.db_shapes[layer].insert(box.to_dbBox())

    









                   
                   
