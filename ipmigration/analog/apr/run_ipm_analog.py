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
if __name__ == "__main__" :
    
    pass
    cfg = ConfigLoader(config_file="settings.json")
    para = ConfigLoader(config_file="paras.json")
    tech = Tech(cfg.TECH, cfg.DR_FILE, cfg.LAYER_FILE)
    layout_data = extract_layout_data(cfg.LAYOUT_FILE)
    master_mos,inst_data = extract_layout_mos_master(layout_data,tech)


    # G = gen_graph(layout_data)
    # groups = get_chains(G)


    canvas = Canvas(tech, cfg.LIB, cfg.CELL, cfg.INST_MAP)


    #power
    box_vdd = Box([0,cfg.AREA[1]-cfg.POWER_WIDTH,cfg.AREA[0],cfg.AREA[1]])
    vdd = Rect(tech.layer[tech.M2][0],box_vdd)
    box_vss = Box([0,0,cfg.AREA[0],cfg.POWER_WIDTH])
    # vss = Rect

    canvas.add(vdd)
    # canvas.add(vss) 
     

    group_list = []
    ring_list = []

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

    sd_vdd = [0] + list(range(1,31,2)) + [30]

    #TODO

    #


    group = group_list[0]
    ring = ring_list[0]
    net_to_sd_to_sd_b = 2.0
    net_to_sd_w = 1.94
    net_to_sd_list = [2,4,6,8]

    box1 = group.SD_pin[2]    
    box2 = group.SD_pin[8]   

    box_t = Box([box1.l, box1.b+net_to_sd_to_sd_b, 
                 box2.r, box1.b+net_to_sd_to_sd_b + net_to_sd_w])
    net2 = Rect(tech.layer[tech.M2][0],box_t)
    canvas.add(net2)

    # for i in net_to_sd_list:
    canvas.skill(cfg.SKILL_FILE)
    target_path = r"D:\ubuntu_share\ota_demo.il"
    shutil.copy2(cfg.SKILL_FILE, target_path)
    
    
    

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