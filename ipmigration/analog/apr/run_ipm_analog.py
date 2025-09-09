# -*- coding: utf-8 -*-


from api_skill import extract_layout_data,extract_layout_mos_master
from mos_graph import gen_graph,get_chains
from tech import Tech
from modules import Canvas, Group, GuardRing, Res, MimCap
from modules import Rect, Mos, Box, Vias



LAYOUT_FILE = "data/layout_data.txt"
DR_FILE = 'data/dr.csv'
LAYER_FILE = 'data/layer.csv'    

map_dict = {'pmos':'pmos3v','nmos':'nmos3v','res':'rnhpoly','cap':'mimcap'}


LIB='ipm_demo_amp2'
CELL='test2'
AREA=(100,80)
POWER_WIDTH=8
VSS_LEFT= 28








tech = Tech('tsmc18rf', DR_FILE, LAYER_FILE)
layout_data = extract_layout_data(LAYOUT_FILE)

master_mos,inst_data = extract_layout_mos_master(layout_data,tech)


# G = gen_graph(layout_data)
# groups = get_chains(G)



groups=[
        ['I0','M20.1','M20.2','M20.3','M20.4','M20.5','M20.6','M20.7','M20.8','M19.1',
         'M19.2','M19.3','M19.4','M21.1','M21.2','M21.3','M21.4','M21.5','M21.6','M21.7',
         'M21.8','M21.9','M21.10','M21.11','M21.12','M21.13','M21.14','M21.15','M21.16','I1'],
        ['I62', 'M18.1', 'M4.3', 'M4.4', 'M18.2', 'I38'],
        ['I64', 'M4.1', 'M18.4', 'M18.3', 'M4.2', 'I65'],
        ['I13', 'M14.3', 'M14.4', 'M13.3', 'M13.4', 'I12'],
        ['I15', 'M14.1', 'M14.2', 'M13.1', 'M13.2', 'I14'],
        ['M15.1', 'M15.4', 'M15.3', 'M15.2', 'M15.5', 'M15.6', 'M15.7', 'M15.8'],
        ['I51','M16.1','M16.2','M16.3','M16.4','M17.1','M17.2','M17.3','M17.4',
         'M17.5','M17.6','M17.7','M17.8','I53'],
        ['I47', 'M5', 'M6', 'I46'],
        ['I55', 'M7.1', 'M7.2', 'M7.3', 'M7.4', 'I54']]



paras = [ 
        [78.240000, 56.17000,'PMOS','D'], #Ring 1
        [17.280000, 29.36000,'PMOS','D'], #Ring 2
        [17.280000, 6.220000,'PMOS','U'], #Ring 2
        [92.000000, 67.67000,'PMOS','D'], #Ring 2
        [92.000000, 55.41000,'PMOS','U'], #Ring 2
        [93.565000, 4.500000,'NMOS','U'], #Ring 2
        [76.685000, 4.500000,'NMOS','U'], #Ring 2
        [51.365000, 4.430000,'NMOS','U'], #Ring 2
        [38.745000, 4.500000,'NMOS','U']  #Ring 2
        ]


res_setting = [['R2',83.09,17.665],['R3',58.475,20.87]]
cap_setting = [['C1.2',30.615,23.46],['C1.1',63.415,23.46]]


rings = [[0],[1,2],[3,4],[5],[6],[7],[8]]


canvas = Canvas(tech, LIB, CELL, map_dict)



#power
box_vdd = Box([0,AREA[1]-POWER_WIDTH,AREA[0],AREA[1]])
vdd = Rect(tech.layer[tech.M2][0],box_vdd)
box_vss = Box([0,0,AREA[0],POWER_WIDTH])
vss = Rect

canvas.add(vdd)
canvas.add(vss) 
 

group_list = []
ring_list = []

for ring in rings:
    l=10000
    r=-10000
    b=10000
    t=-10000
    for i in ring:
        group = groups[i]
        para = paras[i]
        g1 = Group(tech, para[2], master_mos, inst_data, group)
        g1.draw(para[0],para[1],'LR')
        g1.draw_SD_pin()
        g1.draw_GT_pin(para[3])
        group_list.append(g1)
        l = min(l,g1.box.l)
        r = max(r,g1.box.r)
        b = min(b,g1.box.b)
        t = max(t,g1.box.t)       
        canvas.add(g1)
    gr1 = GuardRing(tech, para[2], 1, Box([l,b,r,t]))
    ring_list.append(gr1)
    canvas.add(gr1)


for data in res_setting:
    name,x,y = data
    res_para = inst_data[name]
    _,w,l,r,s = res_para
    r1 = Res(tech, name, x, y,  w, l, r, s)
    gr1 = GuardRing(tech, 'RES', 1, r1.box)
    canvas.add(r1)

for data in cap_setting:
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
    













canvas.skill('data/test2.il')

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












#test
if __name__ == "__main__" :
    
    pass