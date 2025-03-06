# -*- coding: utf-8 -*-
"""

@author: leiyuan
"""

#ferry
#read gds
import os
import time
import klayout.db as db
import shapely #for polygon process
from shapely.geometry import Polygon,MultiPolygon
import networkx as nx
      
from ipmigration.cell.apr.io import cfg
from ipmigration.cell.apr.tech import Tech
from ipmigration.cell.apr.ascell import ASCell

from ipmigration.cell.apr.cir.circuit import Ckt, is_ground_net,is_supply_net
from ipmigration.cell.apr.cir.base import PMos4,NMos4
from ipmigration.cell.apr.cir.graph import MosGraph

import matplotlib.pyplot as plt
import numpy as np


def plot_lvs(data):
    device_numbers = list(data.keys())
    running_times = list(data.values())
    mins = [np.min(times) for times in running_times]
    maxs = [np.max(times) for times in running_times]
    heights = [max - min for min, max in zip(mins, maxs)]

    fig, ax = plt.subplots(figsize=(20, 6))

    bars = ax.bar(device_numbers, heights, bottom=mins, color='skyblue', edgecolor='skyblue')
    

    ax.set_xlabel('Device Number')
    ax.set_ylabel('Running Time(s)')
    ax.set_title('LVS Running Time')
    
    # 显示图形
    plt.show()


class DeviceKL:
    def __init__(self):
        self.G = ''
        self.S = ''
        self.D = ''
        

class CellLayout:
    def __init__(self, cell, layer2index):
        self.name = cell.name.upper()
        self.cell = cell
        self.index = layer2index
        self.data = {}
        self.draw_shapes = {}
        self.draw_layers = ['NW','AA','GT','SP','SN','CT','M1']
        self.text_layers = ['M1TXT']        
        self.nets   = {} #net include keys
        self.nets_r = {} #key to net
        self.pins = {}
    
    def extract_ckt(self):

        self.merge_layers()
        self.get_pins()
        self.split_aa() #careful hulls and holes
        
        self.set_contacts()
        self.extract_nets()
        self.gen_ckt()
        # self.set_nets_gt()
        # self.search_inst()



    def merge_layers(self):
        """
        shapes: Dict[str, db.Shapes]
        Merge all polygons on all shapes.
        """
        layers = self.draw_layers
        
        for layer in layers:
            index = self.index[layer]    
            s =  self.cell.shapes(index)
            # texts = [t.text for t in s.each() if t.is_text()]
            r = db.Region(s)
            r.merge()
            s.clear()
            s.insert(r)
            
            keys = []
            for i,shape in enumerate(s):
                if shape.is_polygon():
                    key = '%s_%d'%(layer,i)
                    self.data[key] = shape.polygon
                    keys.append(key)
            
            # # Copy text labels.
            # for t in texts:
            #     s.insert(t)   
            self.draw_shapes[layer] = keys
            
            
    def get_pins(self):
        #only support text label in m1
        m1_shapes = self.draw_shapes['M1']
        for layer in self.text_layers:
            index = self.index[layer]    
            s =  self.cell.shapes(index)
            texts = [t.text for t in s.each() if t.is_text()]
            for text in texts:
                for shape in m1_shapes:
                    polygon = self.data[shape]
                    if self.p_in_s((text.x,text.y), polygon):
                        name = text.string
                        if is_ground_net(name):
                            name = 'VSS'
                        elif is_supply_net(name):
                            name = 'VDD'
                        else:
                            name = name.upper()
                        self.pins[name] = shape
    
    def split_aa(self):
        self.aa_gts = []
        self.aa_gts_p = []
        self.aa_gts_n = []
        self.aa_sds = []
        for aa_key in self.draw_shapes['AA']:
            aa_polygon = self.data[aa_key]   
            aa_data = {'key':aa_key, 'shape':aa_polygon}
            
            for key in self.draw_shapes['SN']:
                if aa_polygon.touches(self.data[key]):
                    aa_data['np'] = 'SN'
            for key in self.draw_shapes['SP']:
                if aa_polygon.touches(self.data[key]):
                    aa_data['np'] = 'SP'
            assert 'np' in aa_data
                        
            cross_gts = {}
            for gt_key in self.draw_shapes['GT']:
                gt_polygon = self.data[gt_key]  
                if aa_polygon.touches(gt_polygon):
                    cross_gts[gt_key] = gt_polygon

            # assert len(cross_gts)>0 #not a must, see csmc011 aoi2m1d2
            
            aa_data['cross_gts'] = cross_gts
            aa = AA(**aa_data)
            aa_gts, aa_sds = aa.split()
            self.aa_gts += aa_gts
            self.aa_sds += aa_sds
        
        #sort boxes from left to right          
        self.aa_gts = sorted(self.aa_gts, key=lambda aa_gts: aa_gts.c[0])
        self.aa_gts_p = [t for t in self.aa_gts if t.np == 'SP']
        self.aa_gts_n = [t for t in self.aa_gts if t.np == 'SN']
        
        
        keys = []
        for i, aa_sd in enumerate(self.aa_sds):
            name = 'AASD_%d'%(i)
            self.data[name] = aa_sd
            keys.append(name)
        self.draw_shapes['AASD'] = keys

    def set_contacts(self):
        self.contacts = []    
        ct_keys = self.draw_shapes['CT']
        for ct_key in ct_keys:
            ct_polygon = self.data[ct_key]
            ct_data = {'key':ct_key, 'down_l':'none', 
                       'down_s':'none', 'up_s':'none'}
            #is ct on gt or aa
            gt_ct = []
            aa_ct = []
            for gt_key in self.draw_shapes['GT']:
                if ct_polygon.touches(self.data[gt_key]):
                    gt_ct.append(gt_key)
            
            for aasd_key in self.draw_shapes['AASD']:
                aasd = self.data[aasd_key]
                if ct_polygon.touches(aasd.polygon):
                    aa_ct.append(aasd_key)                
            if len(gt_ct) == 1:
                ct_data['down_l'] = 'GT'
                ct_data['down_s'] = gt_ct[0] #key
            elif len(aa_ct) ==1:
                ct_data['down_l'] = 'AA'
                ct_data['down_s'] = aa_ct[0] 
            else:
                raise ValueError
            
            m1_ct = []
            for m1_key in self.draw_shapes['M1']:
                m1_polygon = self.data[m1_key]
                if ct_polygon.touches(m1_polygon):
                    m1_ct.append(m1_key)
            if len(m1_ct) == 1:
                ct_data['up_s'] = m1_ct[0]
            else:
                raise ValueError
            self.contacts.append(ct_data)    
            
            
            
    def extract_nets(self):
        graph = nx.Graph()
        shapes = ['M1','GT','AASD']
        for shape in shapes:
            for key in self.draw_shapes[shape]:
                graph.add_node(key, shape=shape)
                
        for data in self.contacts:
            ct = data['key']
            graph.add_node(ct,shape='CT')
            graph.add_edge(ct, data['down_s'])
            graph.add_edge(ct, data['up_s'])           
        
        pins_r = {v:k for k,v in self.pins.items()}  
        count = 0
        self.components = list(nx.connected_components(graph))
        for component in nx.connected_components(graph):
            net_names = []
            for key in list(component):
                if key in pins_r:
                    net_names.append(pins_r[key])
            if len(net_names)>0:
                net_name = net_names[0]            
            else:
                net_name = 'net%d_%d'%(count,len(component))
                count += 1
            for key in list(component):
                self.nets_r[key]=net_name
        
        for k,v in self.nets_r.items():
            if v in self.nets:
                self.nets[v].append(k)
            else:
                self.nets[v] = [k]
        
    def gen_ckt(self):
        lyt_ckt = Ckt(self.name,pins=list(self.pins.keys()))
        
        aa_sd_p = {k:self.data[k] for k in self.draw_shapes['AASD'] if self.data[k].np =='SP'}
        aa_sd_n = {k:self.data[k] for k in self.draw_shapes['AASD'] if self.data[k].np =='SN'}
        
        for i,aa_gt in enumerate(self.aa_gts_p):
            name = 'PM%d'%(i)
            pins = {'G':self.nets_r[aa_gt.gt_key]}
            nets_S = []
            nets_D = []
            for key, aa_sd in aa_sd_p.items():
                if aa_sd.polygon.touches(aa_gt.box_left):
                    nets_S.append(key)
                if aa_sd.polygon.touches(aa_gt.box_right):
                    nets_D.append(key)                    
            assert len(nets_S) == 1 
            assert len(nets_D) == 1             
            pins['S'] = self.nets_r[nets_S[0]]
            pins['D'] = self.nets_r[nets_D[0]]          
            pins['B'] = 'VDD'
            parameters = {'W':aa_gt.W,'L':aa_gt.L}
            lyt_ckt.add_device(PMos4(name, pins, parameters))


        for i,aa_gt in enumerate(self.aa_gts_n):
            name = 'NM%d'%(i)
            pins = {'G':self.nets_r[aa_gt.gt_key]}
            nets_S = []
            nets_D = []
            for key, aa_sd in aa_sd_n.items():
                if aa_sd.polygon.touches(aa_gt.box_left):
                    nets_S.append(key)
                if aa_sd.polygon.touches(aa_gt.box_right):
                    nets_D.append(key)                    
            assert len(nets_S) == 1 
            assert len(nets_D) == 1             
            pins['S'] = self.nets_r[nets_S[0]]
            pins['D'] = self.nets_r[nets_D[0]]          
            pins['B'] = 'VSS'
            parameters = {'W':aa_gt.W,'L':aa_gt.L}
            lyt_ckt.add_device(NMos4(name, pins, parameters))       
        
        self.ckt = lyt_ckt
        

   
    def set_nets_gt(self):
        self.nets['GT']  = {}
        self.nets_r['GT']  = {}

        for gt_key in self.draw_shapes['GT']:
            gt_polygon = self.data[gt_key]   
            for ct_key,net in self.nets_r['CT'].items():
                ct_polygon = self.data[ct_key]           
                if gt_polygon.touches(ct_polygon): 
                    if net in self.nets['GT']:
                        self.nets['GT'][net].append(gt_key)
                    else:
                        self.nets['GT'][net] = [gt_key]
                    self.nets_r['GT'][gt_key] = net
        
        
        


    @staticmethod
    def p_in_s(point,polygon):
        #point inside shape
        x,y = point
        fake_box = db.Box(x,y,x,y)
        return polygon.touches(fake_box)
           
        
    def lvs(self, ckt):
        s_time = time.time()
        self.sche_ckt = ckt
        ckt.combine_parallel()
        self.ckt.combine_parallel()
        G_ckt = MosGraph(ckt)
        G_lyt = MosGraph(self.ckt)
        is_same,matches = G_ckt.match(G_lyt)
        if is_same:
            return True, time.time() - s_time
        else:
            return False, 0


class CT:
    def __init__(self, key, down_l, down_s, up_s):
        self.key = key
        self.type = down_l
        self.down = down_s
        self.up = up_s
        
class AA_GT:
    def __init__(self, points, aa_key, gt_key, np):
        self.points = points
        self.master_aa_key = aa_key
        self.gt_key = gt_key
        self.np = np
        
        self.polygon = db.Polygon(points)
        self.left = self.polygon.bbox().p1.x
        self.bottom = self.polygon.bbox().p1.y
        self.right = self.polygon.bbox().p2.x
        self.top = self.polygon.bbox().p2.y
        self.c = (self.polygon.bbox().center().x, self.polygon.bbox().center().y)
        self.box_left = db.Box(self.left,self.bottom,self.c[0],self.top)
        self.box_right = db.Box(self.c[0],self.bottom,self.right,self.top) 
        
        self.W = self.top-self.bottom
        self.L = self.right - self.left
        
    def __repr__(self):
        return '%d, %d; %d, %d'%(self.left,self.bottom,self.right,self.top)
        
class AA_SD:
    def __init__(self, points, aa_key,np):
        self.points = points
        self.aa_key = aa_key
        self.np = np
        self.polygon = db.Polygon(points)
        # self.gt_key_l = gt_key_l
        # self.gt_key_r = gt_key_r




class AA:
    def __init__(self, key, shape, np, cross_gts):
        self.key = key
        self.shape = shape
        self.np = np
        self.cross_gts = cross_gts

    def split(self):
        #use shapely 
        aa_points = [(t.x,t.y) for t in self.shape.each_point_hull()]
        aa_points_holes = []
        for i in range(self.shape.holes()):
            aa_points_hole = [(t.x,t.y) for t in self.shape.each_point_hole(i)]
            aa_points_holes.append(aa_points_hole)  

        aa_polygon = Polygon(aa_points, holes=aa_points_holes)
        
        if self.cross_gts:
            aa_gts = []
            for gt_key, gt_shape in self.cross_gts.items(): 
                #care holes in gt #e.g. csmc011 ah01d3->around 8255 1556
                gt_points_hull = [(t.x,t.y) for t in gt_shape.each_point_hull()]
                gt_points_holes = []
                for i in range(gt_shape.holes()):
                    gt_points_hole = [(t.x,t.y) for t in gt_shape.each_point_hole(i)]
                    gt_points_holes.append(gt_points_hole)        
                
                gt_polygon = Polygon(gt_points_hull, holes=gt_points_holes)
                   
                intersection = aa_polygon.intersection(gt_polygon)  #overlap
                if isinstance(intersection,Polygon): 
                    aa_gt_points = list(intersection.exterior.coords)
                    assert len(aa_gt_points) == 5
                    aa_gt_points = aa_gt_points[:-1]
                    aa_gts.append(AA_GT(aa_gt_points, self.key, gt_key, self.np))
      
                elif isinstance(intersection,MultiPolygon): #U shape poly
                    for i in intersection.geoms:
                        aa_gt_points = list(i.exterior.coords)
                        assert len(aa_gt_points) == 5
                        aa_gt_points = aa_gt_points[:-1]
                        aa_gts.append(AA_GT(aa_gt_points, self.key, gt_key, self.np))
                else:
                    raise ValueError
            
            split_aa = aa_polygon
            for i, aa_gt in enumerate(aa_gts):
                aa_gt_polygon = Polygon(aa_gt.points)
                split_aa = split_aa.difference(aa_gt_polygon)
                # if only one polygon in difference (see csmc011 dfanrq1) 
                '''
                condider following recursive example
                ext = [(0, 0), (10, 0), (10, 3), (0, 3)]
                hole = [(1, 1), (9, 1), cut2 = Polygon([(5,0),(6,0),(6,1),(5,1)])(9, 2), (1, 2)]
                cut1 = Polygon([(1,0),(2,0),(2,1),(1,1)])
                cut2 = Polygon([(5,0),(6,0),(6,1),(5,1)])
                cut = Polygon(ext,holes = [hole])
                for t in [cut1,cut2]:
                    cut = cut.difference(t)
                '''
            aa_sds = [] 
            for polygon in split_aa.geoms:
                aa_sd_points = list(polygon.exterior.coords)
                aa_sd_points = aa_sd_points[:-1]
                aa_sds.append(AA_SD(aa_sd_points, self.key, self.np))
            return aa_gts,aa_sds
            
            # print([t.points  for t in aa_gts])
        else:
            aa_sd_points = aa_points
            return [],[AA_SD(aa_sd_points, self.key, self.np)]
        


# p1 = Polygon([(0, 1), (3, 1), (3, 2), (0, 2)])
# p2 = Polygon([(1, 0), (2, 0), (2, 3), (1, 3)])
# p3 = Polygon([(3, 0), (4, 0), (4, 3), (3, 3)])

# intersection = p2.intersection(p1)  # 覆盖部分
# difference = p1.difference(p2)      # 两侧部分

# list(difference.geoms)

# # 输出结果
# print("overlap:", list(intersection.exterior.coords))
# print("sides:", list(difference.geoms))
        




log_level = 'INFO'
data = {'c110': ['demo/cell_apr/setting_c110.csv', 'resources/cell/gds/csmc011.gds'],
        
        }

for tech_name, paths in data.items():

    cfgs  = cfg.Cfg(paths[0], log_level)
    tech  = Tech(cfgs)
    cells = ASCell(cfgs,tech)

    # ck1 = cells.netlist['XR03D2']
    # ck2 = cells.netlist['LANHB1']
    gds_file = paths[1]
    layout = db.Layout()
    layout.read(gds_file)
    
    layer2index = {}
    gds2index = {k.to_s() :v for k,v in zip(layout.layer_infos(),layout.layer_indexes())}
    name2gds2 = {k : '%d/%d'%(v[0],v[1]) for k,v in tech.output_map.items()}
    for name, gds2 in name2gds2.items():
        if gds2 in gds2index:
            layer2index[name]=gds2index[gds2]
        else:
            layer2index[name]=-1
    
    

    
    
    lyt_di = {t.name.upper():t for t in layout.each_cell()}
    
    count = 0
    lvs_data = {}
    fail_lvs = []
    for name, cell_ckt in cells.netlist.ckt_di.items():
        print('------------name:', name)
        cell_lyt = CellLayout(lyt_di[name],layer2index)
        cell_lyt.extract_ckt()

        print(len(cell_ckt.nets)==len(cell_lyt.nets),len(cell_ckt.nets),len(cell_lyt.nets))
        print(len(cell_ckt.devices)==len(cell_lyt.ckt.devices),len(cell_ckt.devices),len(cell_lyt.ckt.devices))
        is_same, run_time = cell_lyt.lvs(cell_ckt) #consider parallel devices
        print(is_same, run_time)
        print(len(cell_ckt.devices)==len(cell_lyt.ckt.devices),len(cell_ckt.devices),len(cell_lyt.ckt.devices))
        
        if is_same:
            device_num = len(cell_lyt.ckt.devices) 
            if device_num in lvs_data:
                lvs_data[device_num].append(run_time)
            else:
                lvs_data[device_num] = [run_time]
        else:
            fail_lvs.append(name)
        
        count+=1
    
        #
        # if count>=100:
        #     break
    plot_lvs(lvs_data)
        #merge all shapes

        # labels = get_texts(cell_lyt, 'M1TXT', layer2index)
        # m1_shapes = cell_lyt.shapes(layer2index['M1'])
        # find_pin_shape(labels, m1_shapes)
        #find text
        
        #find AA overlap SN/SP overlap GT
        
        #find m1
        
        #find text
        
        #find 
        
        #each_touching_shape(layer_index, box):
        #NP & GT & AA is mos
        #CT and AA is SD
        #AA 
        


    #lvs
    
    

# for ly_id in layout.layer_indices():
#   ly_info = layout.get_info(ly_id)
#   print(ly_info.to_s())



'''
klaytout:
    Layout:
        layout.layer_indexes()
        layout.layer_indices() #same with indexes
        layout.layer_infos()
        
        Cell:    
            Shapes: A collection of shapes(box,polygon,text...)
                shape:
                    Box
                    Text
                    SimplePolygon
                        Point
            
            Reginos: for merge shapes


marks:
shape touch doesn't consider layer    

klayout
t1.insert_hole(hole)



#shapely version '2.0.7'

from shapely.geometry import Polygon

p1 = Polygon([(0, 1), (3, 1), (3, 2), (0, 2)])
p2 = Polygon([(1, 0), (2, 0), (2, 3), (1, 3)])
p3 = Polygon([(3, 0), (4, 0), (4, 3), (3, 3)])

intersection = p2.intersection(p1)  # 覆盖部分
difference = p1.difference(p2)      # 两侧部分

list(difference.geoms)

# 输出结果
print("overlap:", list(intersection.exterior.coords))
print("sides:", list(difference.geoms))
p1.touches(p2)
p1.touches(p3)
shapely.overlaps(p1,p2)
shapely.overlaps(p1,p3)
'''