# -*- coding: utf-8 -*-
"""
Created on Wed May 29 18:08:15 2024

@author: leiyuan
"""
import matplotlib.pyplot as plt
import networkx as nx
import klayout.db as db
import numpy as np
import logging
import os
import time

logger = logging.getLogger(__name__)


def init_logger(args):
    #set log file
    if args.log_level == 'INFO':
        log_level = logging.INFO
    elif args.log_level == 'DEBUG':
        log_level = logging.INFO
    elif args.log_level == 'FATAL':
        log_level = logging.INFO    
    else:
        raise ValueError('log_level is not INFO DEBUG or FATAL')
    log_file =  os.path.join(args.save_dir, time.strftime("%b_%d")+ '_log.txt')  
    logging.basicConfig(format='%(asctime)s %(levelname)8s: %(message)s',
                        datefmt="%Y-%m-%d %H:%M:%S",
                        level=log_level,
                        filemode='w',
                        filename=log_file)
    
    
    logger.info("="*50+"Begin ASCell: %s "%(args.tech_name) + "="*50)


def init_check(args): 
    #1
    assert os.path.exists(args.tech_align_file), str(args.tech_align_file)
    #2
    assert os.path.exists(args.pin_align_file), str(args.pin_align_file)
    #3
    args.cell_para_file = os.path.join(args.tech_dir,'cell_para.csv')
    assert os.path.exists(args.cell_para_file), str(args.cell_para_file)
    #4
    args.layer_mapping_file = os.path.join(args.tech_dir,'layer_mapping.txt')  
    assert os.path.exists(args.layer_mapping_file), str(args.layer_mapping_file)
    #5
    args.design_rule_file = os.path.join(args.tech_dir,'design_rule.xlsx')  
    assert os.path.exists(args.design_rule_file), str(args.design_rule_file)
    #6
    args.model_file = os.path.join(args.tech_dir,'model.cdl') 
    assert os.path.exists(args.model_file), str(args.model_file)
    #7
    assert os.path.exists(args.netlist), str(args.netlist_file)
    

    #set output dir

    # args.output_dir = os.path.join(args.save_dir, time.strftime("%b_%d") + '_' + args.tech_name)
    args.output_dir = os.path.join(args.save_dir, 'Jul_18' + '_' + args.tech_name)
    if not(os.path.exists(args.output_dir)):
        os.mkdir(args.output_dir)

    logger.info("Cfg initial check is sucessfull: %s "%(args.tech_name))



def timer(time_start, log):
    t = int(time.time() - time_start)
    logger.info('%s : %d s \n'%(log, t))
    return time.time(), t
    






#backup
def draw_pr(cell, graph, pos_m1, pos_gt, labels, width = 8, edges= None, file = None):
    # print(pos_m1,pos_gt)
    
    offset_x = 0.5
    offset_y = 0.2

    node_pos = {}
    node_pos.update(pos_m1)
    for key in pos_gt:
        x,y = pos_gt[key]
        node_pos[key] = (x+offset_x,y+offset_y )
    node_labels = {}
    nodes_list = list(pos_m1.keys()) + list(pos_gt.keys())
    color_list = ['green']*len(pos_m1) + ['blue']*len(pos_gt)
   
        # ax = pyplot.
    fig, ax = plt.subplots(figsize=(width,8))
    ax.set(title=cell.name)
    nx.draw_networkx(graph, 
                     pos=node_pos, 
                     nodelist= nodes_list,
                     ax =ax,
                     labels = labels,
                     node_color=color_list, 
                     node_size=30, 
                     with_labels=True,
                     font_size = 10, 
                     edge_color='lightgray')
    if edges:
        edges_m1 = []
        edges_gt = []
        edges_ct = []
        for t in edges:
            edge, label = t
            if label == 'gt':
                edges_gt.append(edge)
            elif label == 'm1':
                edges_m1.append(edge)
            elif label == 'ct':
                edges_ct.append(edge)
        nx.draw_networkx_edges(graph, node_pos, edgelist=edges_m1, width=4, edge_color='green')
        nx.draw_networkx_edges(graph, node_pos, edgelist=edges_gt, width=4, edge_color='blue')
        nx.draw_networkx_edges(graph, node_pos, edgelist=edges_ct, width=4, edge_color='orange')

    
    if file:
        fig.savefig(file)
            
 
    
def cal_m1_tracks_num(width,m_w,m_s):
    #calculate number of m1_tracks in different cases 
    num = int((width-m_s)/(m_s+m_w))
    off = int((width-m_s)%(m_s+m_w))    
    return num,off
 
# def half(value):
#     return int(0.5*value)
 
    
def output_cdl():
    pass
# cdl_file = open(os.path.join(args.output_dir,'scale_cdl.cdl'),'w')

# for i,cell in enumerate(self.cells):
#     line = '****Sub-Circuit for %s ****\n'%(cell.name) 
#     cdl_file.write(line)
#     line = '.SUBCKT %s'%(cell.name)
#     for p in cell.pins:
#         line = line + ' ' + p
#     cdl_file.write(line + '\n')  
#     for d in cell.devices:
#         line = d.name + ' ' + d.source_net + ' ' + d.gate_net + ' ' + d.drain_net + ' ' 
#         if d.t =='P':
#             line = line + args.scale_vpw + ' ' + args.scale_pmos + ' '
#         else:
#             line = line + args.scale_vnw + ' ' + args.scale_nmos + ' '
#         line = line + 'W=%.2fn L=%.2fn'%(d.w,d.l)
#         cdl_file.write(line + '\n')  
    
#     line = '.ENDS %s'%(cell.name)
            
 
        
##backup
def _merge_all_layers(shapes):
    """
    shapes: Dict[str, db.Shapes]
    Merge all polygons on all layers.
    """
    for layer_name, s in shapes.items():
        texts = [t.text for t in s.each() if t.is_text()]

        r = db.Region(s)
        r.merge()
        s.clear()
        s.insert(r)

        # Copy text labels.
        for t in texts:
            s.insert(t)


def _is_virtual_node_fn(n) -> bool:
    """
    Check if the node is virtual and has no direct physical representation.
    :param n:
    :return:
    """
    return n[0].startswith('virtual')


def _is_virtual_edge_fn(e) -> bool:
    """
    Check if the edge connects to at least one virtual node.
    :param n:
    :return:
    """
    a, b = e
    return _is_virtual_node_fn(a) or _is_virtual_node_fn(b)


def add_via_nodes(graph: nx.Graph, tech) -> nx.Graph:
    """
    Split all inter-layer edges by inserting a node which represents the via.
    This is used to define conflicts between vias and metal layers and allows
    to model the conflicts that are caused by the via-enclosure.
    :param graph:
    :param tech:
    :return:
    """
    new_graph = nx.Graph()

    for a, b, data in graph.edges(data=True):
        via_layer = data['layer']
        weight = data.get('weight', 0)
        _, location = a  # Via location.
        via_node = via_layer, location

        new_data = data.copy()
        new_data['weight'] = weight / 2

        new_graph.add_edge(a, via_node, **new_data)
        new_graph.add_edge(via_node, b, **new_data)

    return new_graph


