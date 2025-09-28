# -*- coding: utf-8 -*-

import shutil
from api_mip import ConfigLoader
from api_skill import extract_layout_data,extract_layout_mos_master
from mos_graph import gen_graph,get_chains
from tech import Tech
from modules import Canvas, Group, GuardRing, Res, MimCap
from modules import Rect,Polygon, Mos, Box, Vias


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
    
    #ring rect
    vias = Vias(tech.layer[tech.V1][0], tech.V1_W, tech.V1_S, ring.box_t, ring.box_t, tech.V1_EN_M1_END)
    canvas.add(vias) 

    
    #2.1 group1&2
    # Group 1 and 2 not have ring to vdd
    group1 = group_list[1]
    group2 = group_list[2]
    ring1 = ring_list[1]
    sd1 = group1.SD_pin
    gt1  = group1.GT_pin 
    sd2 = group2.SD_pin
    gt2  = group2.GT_pin   
    
    SIDE  = 1.00 
    WIDTH = 1.94
    SPACE = 2.00
    RRBOX = ring1.box_r
    
    
    sd_ll = [[0,2,4,6],[1,5],[3]]
    
    ring1_net = []
    
    top1 = sd1[0].t - SIDE
    bottom1 = top1 - WIDTH
    bottom2 = sd2[0].b + SIDE
    top2 = bottom2 + WIDTH
    for sd_l in sd_ll:
        box = Box([sd1[sd_l[0]].l, bottom1, RRBOX.r, top1])
        rect_t = Rect(tech.layer[tech.M2][0],box)
        ring1_net.append(rect_t)
        canvas.add(rect_t)
        
        box = Box([sd2[sd_l[0]].l, bottom2, RRBOX.r, top2])
        rect_b = Rect(tech.layer[tech.M2][0],box)
        ring1_net.append(rect_b)
        canvas.add(rect_b)
        
        for t in sd_l:
            box = Box([sd1[t].l, bottom1, sd1[t].r, top1])
            vias = Vias(tech.layer[tech.V1][0], tech.V1_W, tech.V1_S, box, box, tech.V1_EN_M1_END)
            canvas.add(vias) 
            box = Box([sd2[t].l, bottom2, sd2[t].r, top2])
            vias = Vias(tech.layer[tech.V1][0], tech.V1_W, tech.V1_S, box, box, tech.V1_EN_M1_END)
            canvas.add(vias)        
        
        top1 = bottom1 - SPACE
        bottom1 = top1 - WIDTH
        bottom2 = top2 + SPACE
        top2 = bottom2 + WIDTH
        
    #inside 
    box1 = sd1[0]
    box2 = gt1[0][1]
    points = [box1.ll,box1.lr,(box1.r,box2.t),box2.ur,box2.lr, (box1.l,box2.b), box1.ll]
    p1 = Polygon(tech.layer[tech.M1][0],points)
    canvas.add(p1)        
    
    box1 = sd2[0]
    box2 = gt2[0][1]
    points = [box1.ul,box1.ur,(box1.r,box2.b),box2.lr,box2.ur, (box1.l,box2.t), box1.ul]
    p1 = Polygon(tech.layer[tech.M1][0],points)
    canvas.add(p1)  
    
    box1 = sd1[-1]
    box2 = gt1[-1][1]
    points = [box1.lr,box1.ll,(box1.l,box2.t),box2.ul,box2.ll, (box1.r,box2.b), box1.lr]
    p1 = Polygon(tech.layer[tech.M1][0],points)
    canvas.add(p1)          
    
    box1 = sd2[-1]
    box2 = gt2[-1][1]
    points = [box1.ur,box1.ul,(box1.l,box2.b),box2.ll,box2.ul, (box1.r,box2.t), box1.ur]
    p1 = Polygon(tech.layer[tech.M1][0],points)
    canvas.add(p1)         
    
    #add contact
    for i in [1,2,3,4]:
        rect1 = gt1[i][1]
        rect2 = gt2[i][1]
        vias = Vias(tech.layer[tech.V1][0], tech.V1_W, tech.V1_S, rect1, rect1, tech.V1_EN_M1_END)
        canvas.add(vias)    
        vias = Vias(tech.layer[tech.V1][0], tech.V1_W, tech.V1_S, rect2, rect2, tech.V1_EN_M1_END)
        canvas.add(vias)     
    
    
    box = Box.merge(gt1[0][1], gt1[1][1])  
    rect = Rect(tech.layer[tech.M2][0],box) 
    canvas.add(rect)       

    box = Box.merge(gt1[2][1], gt1[3][1])  
    rect = Rect(tech.layer[tech.M2][0],box) 
    canvas.add(rect)  

    box = Box.merge(gt2[0][1], gt2[1][1])  
    rect = Rect(tech.layer[tech.M2][0],box) 
    canvas.add(rect)  

    box = Box.merge(gt2[2][1], gt2[3][1])  
    rect = Rect(tech.layer[tech.M2][0],box) 
    canvas.add(rect)  
    
    rect = Rect(tech.layer[tech.M2][0],gt1[4][1]) 
    canvas.add(rect)  
    rect = Rect(tech.layer[tech.M2][0],gt2[4][1]) 
    canvas.add(rect)  
    
    HWIDTH=0.45
    r12 = gt1[1][1]
    r11 = gt2[1][1]
    r22 = gt1[2][1]
    r21 = gt2[2][1]
    
    box = Box.merge(r11, r22)
    c_x1 = box.c[0] - box.h_h
    c_x2 = box.c[0] + box.h_h 
    points1 = [(c_x1-HWIDTH,box.t),(c_x1+HWIDTH,box.t),(c_x2+HWIDTH,box.b),(c_x2-HWIDTH,box.b),(c_x1-HWIDTH,box.t)]
    points2 = [(c_x2-HWIDTH,box.t),(c_x2+HWIDTH,box.t),(c_x1+HWIDTH,box.b),(c_x1-HWIDTH,box.b),(c_x2-HWIDTH,box.t)]
    p1 = Polygon(tech.layer[tech.M2][0],points1)
    canvas.add(p1)   
    p1 = Polygon(tech.layer[tech.M1][0],points2)
    canvas.add(p1)   
    
    r12 = gt1[3][1]
    r11 = gt2[3][1]
    r22 = gt1[4][1]
    r21 = gt2[4][1]
    
    box = Box.merge(r11, r22)
    c_x1 = box.c[0] - box.h_h
    c_x2 = box.c[0] + box.h_h
    points1 = [(c_x1-HWIDTH,box.t),(c_x1+HWIDTH,box.t),(c_x2+HWIDTH,box.b),(c_x2-HWIDTH,box.b),(c_x1-HWIDTH,box.t)]
    points2 = [(c_x2-HWIDTH,box.t),(c_x2+HWIDTH,box.t),(c_x1+HWIDTH,box.b),(c_x1-HWIDTH,box.b),(c_x2-HWIDTH,box.t)]
    p1 = Polygon(tech.layer[tech.M2][0],points1)
    canvas.add(p1)   
    p1 = Polygon(tech.layer[tech.M1][0],points2)
    canvas.add(p1)  
    
    #left for ring
    

    #2.2 group3&4
    group1 = group_list[3]
    group2 = group_list[4]
    ring1 = ring_list[2]
    sd1 = group1.SD_pin
    gt1  = group1.GT_pin 
    sd2 = group2.SD_pin
    gt2  = group2.GT_pin   

    #ring rect
    vias = Vias(tech.layer[tech.V1][0], tech.V1_W, tech.V1_S, ring1.box_t, ring1.box_t, tech.V1_EN_M1_END)
    canvas.add(vias) 
    
    #sd to power
    sd_t = [sd1[0]] + sd1[1:-1:2] + [sd1[-1]] 
    for rect in sd_t:
        box = Box([rect.l, vdd.b, rect.r, rect.t])
        rect2 = Rect(tech.layer[tech.M2][0],box)
        canvas.add(rect2) 
        vias = Vias(tech.layer[tech.V1][0], tech.V1_W, tech.V1_S, rect2, rect2, tech.V1_EN_M1_END)
        canvas.add(vias)    
    
    #
    for i in [0,1,4,5,6]:
        rsdu = sd1[i]
        rsdd = sd2[i]
        box = Box([rsdu.l,rsdd.t,rsdu.r,rsdu.b])
        rect_t = Rect(tech.layer[tech.M1][0],box)
        ring1_net.append(rect_t)
        canvas.add(rect_t)
    for i1,i2 in [[0,1],[5,6]]:
        rgtu = gt1[i1][1]
        rgtd = gt2[i1][1]
        rsd1 = sd1[i1]
        rsd2 = sd1[i2]
        
        box = Box([rsd1.l,rgtu.b,rsd2.r,rgtu.t])
        rect_t = Rect(tech.layer[tech.M1][0],box)
        ring1_net.append(rect_t)
        canvas.add(rect_t)
        
        box = Box([rsd1.l,rgtd.b,rsd2.r,rgtd.t])
        rect_t = Rect(tech.layer[tech.M1][0],box)
        ring1_net.append(rect_t)
        canvas.add(rect_t)

    left = gt1[1][1].l 
    right = gt1[4][1].r 
    box = Box([left,rgtu.b,right,rgtu.t])
    rect_t = Rect(tech.layer[tech.M1][0],box)
    ring1_net.append(rect_t)
    canvas.add(rect_t)

    box = Box([left,rgtd.b,right,rgtd.t])
    rect_t = Rect(tech.layer[tech.M1][0],box)
    ring1_net.append(rect_t)
    canvas.add(rect_t)
    
    EDGE=1.5 
    for i in [2,3]:
        rsdu = sd1[i]
        rsdd = sd2[i]
        
        box1 = Box([rsdu.l,rsdu.b,rsdu.r,rsdu.b + EDGE])
        vias = Vias(tech.layer[tech.V1][0], tech.V1_W, tech.V1_S, box1, box1, tech.V1_EN_M1_END)
        canvas.add(vias)   
        
        box2 = Box([rsdd.l,rsdd.t - EDGE,rsdd.r,rsdd.t])
        vias = Vias(tech.layer[tech.V1][0], tech.V1_W, tech.V1_S, box2, box2, tech.V1_EN_M1_END)
        canvas.add(vias)   
        
        rect_t = Rect(tech.layer[tech.M2][0],Box.merge(box1, box2))
        ring1_net.append(rect_t)
        canvas.add(rect_t)
        
        
    ring2_net = [] 
    for i in [2,4]:
        rsdd = sd2[i] 
        box1 = Box([rsdd.l,rsdd.b,rsdd.r,rsdd.b+EDGE])
        rect_t = Rect(tech.layer[tech.M2][0],box1)
        canvas.add(rect_t)
        
        vias = Vias(tech.layer[tech.V1][0], tech.V1_W, tech.V1_S, box1, box1, tech.V1_EN_M1_END)
        canvas.add(vias)   
        vias = Vias(tech.layer[tech.V2][0], tech.V2_W, tech.V2_S, box1, box1, tech.V2_EN_M2_END)
        canvas.add(vias) 
        
        box2 = Box([rsdd.l,ring1.box_b.b,rsdd.r,rsdd.b+EDGE])
        rect_t = Rect(tech.layer[tech.M3][0],box2)
        ring2_net.append(rect_t)
        canvas.add(rect_t)
    
    
    
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
    
    # if need copy to other place
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