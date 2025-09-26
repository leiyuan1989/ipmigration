# -*- coding: utf-8 -*-

import shutil
from api_mip import ConfigLoader
from api_skill import extract_layout_data,extract_layout_mos_master
from mos_graph import gen_graph,get_chains
from tech import Tech
from modules import Canvas, Group, GuardRing, Res, MimCap
from modules import Rect, Mos, Box, Vias


'''
source layout and schematic
import data skill
layout routing 

'''

CONFIG='setting/settings.json'












if __name__ == "__main__" :
    
    pass
    cfg = ConfigLoader(config_file=CONFIG)
    para = ConfigLoader(config_file=cfg.PARA_FILE)
    tech = Tech(cfg.TECH, cfg.DR_FILE, cfg.LAYER_FILE)
    layout_data = extract_layout_data(cfg.LAYOUT_FILE)
    master_mos,inst_data = extract_layout_mos_master(layout_data,tech)

    #Extract Info if needed
    # G = gen_graph(layout_data)
    # groups = get_chains(G)
    canvas = Canvas(tech, cfg.INST_MAP)


     
    group_list = []
    ring_list = []

    #package these code?
    for ring in para.rings:
        l=10000
        r=-10000
        b=10000
        t=-10000 
        for i in ring:
            group = para.groups[i]
            groups_paras = para.groups_paras[i]
            g1 = Group(tech, groups_paras[2], master_mos, inst_data, group)
            g1.draw(groups_paras[0],groups_paras[1],'LR')
            g1.draw_SD_pin()
            g1.draw_GT_pin(groups_paras[3])
            group_list.append(g1)
            l = min(l,g1.box.l)
            r = max(r,g1.box.r)
            b = min(b,g1.box.b)
            t = max(t,g1.box.t)       
            canvas.add(g1)
        gr1 = GuardRing(tech, groups_paras[2], 1, Box([l,b,r,t]))
        ring_list.append(gr1)
        canvas.add(gr1)


    for data in para.res_setting:
        name,x,y = data
        res_para = inst_data[name]
        _,w,l,r,s = res_para
        r1 = Res(tech, name, x, y,  w, l, r, s)
        gr1 = GuardRing(tech, 'RES', 1, r1.box)
        canvas.add(r1)

    for data in para.cap_setting:
        name,x,y = data
        cap_para = inst_data[name]
        _,w,l,r = cap_para
        c1 = MimCap(tech, name, x, y,  w, l, r)
        canvas.add(c1)

    #routing
    #1. power
    box_vdd = Box([0,cfg.AREA[1]-cfg.POWER_WIDTH,cfg.AREA[0],cfg.AREA[1]])
    vdd = Rect(tech.layer[tech.M2][0],box_vdd)
    box_vss = Box([ring_list[-1].box_out.l,0,cfg.AREA[0],cfg.POWER_WIDTH])
    vss = Rect(tech.layer[tech.M2][0],box_vss)

    canvas.add(vdd)
    canvas.add(vss) 
    
    #2 group 
    #2.0 group0
    group = group_list[0]
    ring = ring_list[0]
    sd = group.SD_pin
    gt  = group.GT_pin 
    
    
    #sd to power
    sd_t = [sd[0]] + sd[1:-1:2] + [sd[-1]] 
    for rect in sd_t:
        box = Box([rect.l, vdd.b, rect.r, rect.t])
        rect2 = Rect(tech.layer[tech.M2][0],box)
        canvas.add(rect2) 
        vias = Vias(tech.layer[tech.V1][0], tech.V1_W, tech.V1_S, rect2, rect2, tech.V1_EN_M1_END)
        canvas.add(vias) 
    
    #sd to gate
    sd_t =[sd[t] for t in [0,1,10,12,-2,-1]]
    for rect in sd_t:
        box = Box([rect.l, gt[0][1].b, rect.r, rect.b])
        rect2 = Rect(tech.layer[tech.M1][0],box)
        canvas.add(rect2)
        
        
    #sd to net    
    TO_EDGE=2 
    WIDTH = 1.94
    
    sd_t =[sd[t] for t in [2,4,6,8]]
    g0_net1 = []
    for rect in sd_t:
        box = Box([rect.l, rect.b+TO_EDGE, rect.r, rect.b+TO_EDGE+WIDTH])
        g0_net1.append(box)
        rect2 = Rect(tech.layer[tech.M2][0],box)
        canvas.add(rect2)
        vias = Vias(tech.layer[tech.V1][0], tech.V1_W, tech.V1_S, rect2, rect2, tech.V1_EN_M1_END)
        canvas.add(vias) 
    box = Box([g0_net1[0].l, g0_net1[0].b, g0_net1[-1].r, g0_net1[0].t])
    rect2 = Rect(tech.layer[tech.M2][0],box)
    canvas.add(rect2)
    
    
    sd_t =[sd[t] for t in [14,16,18,20,22,24,26,28]]
    g0_net2 = []
    for rect in sd_t:
        box = Box([rect.l, rect.b+TO_EDGE, rect.r, rect.b+TO_EDGE+WIDTH])
        g0_net2.append(box)
        rect2 = Rect(tech.layer[tech.M2][0],box)
        canvas.add(rect2)
        vias = Vias(tech.layer[tech.V1][0], tech.V1_W, tech.V1_S, rect2, rect2, tech.V1_EN_M1_END)
        canvas.add(vias) 
    box = Box([g0_net2[0].l, g0_net2[0].b, g0_net2[-1].r, g0_net2[0].t])
    rect2 = Rect(tech.layer[tech.M2][0],box)
    canvas.add(rect2)
    
    
    
    
    #gt connect
    box = Box([sd[0].l, gt[0][1].b, sd[1].r, gt[0][1].t])
    rect = Rect(tech.layer[tech.M1][0],box)
    canvas.add(rect) 
    
    box = Box([sd[-2].l, gt[-1][1].b, sd[-1].r, gt[-1][1].t])
    rect = Rect(tech.layer[tech.M1][0],box)
    canvas.add(rect) 
    
    box = Box([gt[1][1].l, gt[1][1].b, gt[-2][1].r, gt[-2][1].t])
    rect = Rect(tech.layer[tech.M1][0],box)
    canvas.add(rect) 
    
    #ring
    
    
    
    
    
    #2.1 group1



    #2.2 group2


    #2.3 group3


    #2.4 group4


    #2.5 group5


    #2.6 group6


    #2.7 group7
    
    
    
    sd_vdd = [0] + list(range(1,31,2)) + [30]

    #TODO

    #




    # for i in net_to_sd_list:
    canvas.skill(cfg.SKILL_FILE)
    
    #if need copy to other place
    # target_path = r"D:\ubuntu_share\ota_demo.il"
    # shutil.copy2(cfg.SKILL_FILE, target_path)
    
    
    

    '''
    constraint

    left_alignment
    I0 I62 I64

    bottom alignment
    M15.8
    I53 I46 

    I14 I12 right align

    I14 I1 bottom align 

    I12 I1 top_aligh

    expertise_chain()
    '''