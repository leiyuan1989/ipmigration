# -*- coding: utf-8 -*-
"""

@author: leiyuan
"""


'''
Net

'''
import networkx as nx
from ipmigration.cell.apr.lyt.instance import M1_Rails,NPWELL,PINMETAL
from ipmigration.cell.apr.lyt.instance import M1_Route,GT_Route
from ipmigration.cell.apr.lyt.instance import GT_Pair,AA_SD 
from ipmigration.cell.apr.pr.pattern_apr import visualize_pins,find_subgraph_with_nodes
import matplotlib.pyplot as plt
# fig, ax = visualize_pins(self.ckt.name, self.m1_pins_result, self.y_lim, edges=self.edges_op)
# plt.show()

PLOT = False

class CellDrawer:
    def __init__(self, cell):
        self.cell = cell 
        self.tech = cell.tech
        self.cfgs = self.cell.cfgs
        self.edges = cell.apr.router.edges_op
        self.placement = cell.apr.placement
        self.pins = cell.apr.router.m1_pins_result
        self.poly_connect = cell.apr.router.poly_connect
        self.pin_loc = cell.apr.pin_loc
        
        
        
        self.data = []

    def draw(self):
        for v in self.data:
            for layer in v:    
                for box in v[layer]:
                    self.cell.db_shapes[layer].insert(box.to_dbBox())
                    
                    
    def run(self):
        tech = self.cell.tech
        cfgs = self.cell.cfgs
        pin_loc = self.pin_loc
        poly_connect = self.poly_connect
        vdd_nets = self.cell.apr.vdd_nets
        vss_nets = self.cell.apr.vss_nets 
        # abut_nets = self.cell.apr.abut_nets 
        gg_nets = self.cell.apr.gg_nets
        
        net_loc = self.cell.apr.net_loc
        size = self.cell.apr.grid_size 
        
        pins = self.pins
        edges = self.edges
        
        ipins = list(self.cell.ckt.ipins.keys()) + [self.cell.ckt.clk_net]
        opins = list(self.cell.ckt.opins.keys())
        
        
        #init process double aa problem 
        # remove_keys = []
        # for k,vs in pins.items():
        #     if len(vs) == 1:
        #         net, loc = vs[0]
        #         next_loc = (loc[0]+1,loc[1],loc[2])
        #         if k+1 in pins:
        #             for t1, t2 in pins[k+1]:
        #                 print(t1,t2,net,next_loc)
        #                 if t1 == net and t2 == next_loc:
        #                     pins[k+1].remove([t1,t2])
        #                     for mos, t3 in net_loc.items():
        #                         if t3 == t2:
        #                             remove_keys.append(mos)
        # for key in remove_keys:
        #     net_loc.pop(key)
        #     print(key)
        
        # print(net_loc)
        
        # self.pins = pins
        
        
        '''
        pins = c2.apr.router.m1_pins_result
        edges = c2.apr.router.edges_op
        net_loc = c2.apr.net_loc
        ipins = list(c2.ckt.ipins.keys()) +[c2.ckt.clk_net]
        opins = list(c2.ckt.opins.keys())
        size = c2.apr.grid_size 
        vdd_nets = c2.apr.vdd_nets
        vss_nets = c2.apr.vss_nets
        gg_nets = c2.apr.gg_nets
        pin_loc = c2.apr.pin_loc
        poly_connect = c2.apr.router.poly_connect
        '''    
        
        edges_op = Edges_Optimizer(size, pin_loc, edges, pins, ipins,opins, gg_nets,
                                  vdd_nets,vss_nets, poly_connect)
        
        self.edges_op = edges_op
        
        #optimize input pins
        edges_op.optimize_inpins()
        if PLOT:
            fig, ax = visualize_pins(self.cell.name + ': input pins 2nd optimization', edges_op.pins, size[1], edges=edges_op.edges)
            plt.show()    
        
        #optimize aa_ct
        edges_op.optimize_ct()
        if PLOT:
            fig, ax = visualize_pins(self.cell.name + ': input pins 3nd optimization', edges_op.pins, size[1], edges=edges_op.edges)
            plt.show() 
        
        #optimize U shape
        iter_num = 1
        while(1):
            result = edges_op.optimize_U_shape()
            if result:
                if PLOT:
                    fig, ax = visualize_pins(self.cell.name + ':route optimization: %d iteration'%(iter_num), edges_op.pins, size[1], edges=edges_op.edges)
                    plt.show() 
            else:
                break
            iter_num+=1
            if iter_num > 20:
                break
        
        fig, ax = visualize_pins(self.cell.name + ':final', edges_op.pins, size[1], edges=edges_op.edges)
        plt.show() 
        col_space = Col_Spaces(cfgs, tech, net_loc, edges_op)
        self.col_space = col_space
        # eol, fail_eol, col_eol_ext 
        eol_direction, eol_extension, col_eol_ext = edges_op.cal_eol_type()
        pc_p,pc_n,poly_connect_edges = edges_op.poly_connect_process()
        # print(poly_connect_edges)
        # end_ps, corner_ps, input_pins, unused_ps, used_ps = find_special_points(edges,pins,ipins)
        # edges_points = edges_to_points(edges)
        
        x_axis = col_space.run(col_eol_ext)
        
        
        # edges_parallel = cal_parallel_edges(edges_points,input_pins)
        
        
        
        # eol, fail_eol, col_eol_ext = cal_eol_type( end_ps, corner_ps, unused_ps,used_ps,edges_points)
        
        # pc_p,pc_n,pc_edges = poly_connect_process(poly_connect,pin_loc)
        # TODO: optimize fail_eol, add a test here
        
        # col_mos,col_type = col_data(net_loc)
        # x_axis = col_spaces(cfgs,tech,size,pins,vdd_nets,vss_nets,edges_parallel,col_eol_ext)
        # self.x_axis = x_axis

       
                
        # #first round: GT
        # #second round: AA
        col_type = col_space.col_type
        col_mos = col_space.col_mos
        vdd_nets_loc = edges_op.vdd_nets_loc
        vss_nets_loc = edges_op.vss_nets_loc
        gg_nets = edges_op.gg_nets
        
        left_gt_aap = None
        left_gt_aan = None
        x = cfgs.cell_offset_x + tech.CT_W.hv + tech.CT_E_AA.v 
        xs = []
        
        gt_pairs = {}
        
        # print(x_axis)
        for i in range(size[0]):
            xs.append(x)
            if  i != size[0]-1 :
                x_space = max([t[1] for t in x_axis[i]])
            else:
                x_space = 0

            if i in col_type:
                aa_type = col_type[i]
                if aa_type == 'S' or aa_type=='DS' and i != size[0]-1 : 
                    if col_type[i+1] == 'DS':
                        next_key = i+2
                        x_space_next = max([t[1] for t in x_axis[i+1]])
                        gt_x = x + x_space + x_space_next
                    else:   
                        next_key = i+1
                        gt_x = x + x_space
                    pn = col_mos[next_key]
                    pmos = pn['P']
                    nmos = pn['N']
                    # pins_sd = pins[i]
                    pins_g = pins[next_key]
                    
                    pin_gp = [[t[1][0],t[1][1]] for t in pins_g if t[1][1] >= pin_loc.gtp]
                    pin_gn = [[t[1][0],t[1][1]] for t in pins_g if t[1][1] <= pin_loc.gtn]
                    is_gt_connect = next_key in gg_nets
                    is_polyconnect_p = next_key in pc_p
                    is_polyconnect_n = next_key in pc_n
                    #draw G first
                    # print(i,pmos, nmos, pin_gp, pin_gn)
                    gt_pair = GT_Pair(tech, pin_loc, gt_x, pmos, nmos, pin_gp, pin_gn,
                                      gt_connect = is_gt_connect,
                                      poly_net_p = is_polyconnect_p,
                                      poly_net_n = is_polyconnect_n)  
                    
                    self.data.append(gt_pair.data)
                    if not(next_key in gt_pairs):
                        gt_pairs[next_key] = gt_pair 
                    # x = x + x_space
              
                if aa_type == 'S' or aa_type=='DS' or aa_type=='D': 
                    pins_sd = pins[i]
                  
                    pin_aap = [[t[1][0],t[1][1]] for t in pins_sd if t[1][1] >= pin_loc.gtp]
                    pin_aan = [[t[1][0],t[1][1]] for t in pins_sd if t[1][1] <= pin_loc.gtn]
                    
                    
                    if i in vdd_nets_loc:
                        vdd_loc = vdd_nets_loc[i]
                    else:
                        vdd_loc = None
                    if i in vss_nets_loc:
                        vss_loc = vss_nets_loc[i]
                    else:
                        vss_loc = None                        
                        
                    right_gt_aap = None
                    right_gt_aan = None
                    if 'AA_P' in gt_pair.box:
                        right_gt_aap = gt_pair.box['AA_P']
                    if 'AA_N' in gt_pair.box:
                        right_gt_aan = gt_pair.box['AA_N']
                
                    aa_sd =  AA_SD(tech, aa_type, x, pin_aap,pin_aan,  
                                      left_pmos_aa = left_gt_aap,
                                      left_nmos_aa = left_gt_aan,
                                      right_pmos_aa = right_gt_aap,
                                      right_nmos_aa = right_gt_aan,
                                      vdd_pin = vdd_loc,
                                      vss_pin = vss_loc,
                                      )
  
                    self.data.append(aa_sd.data)
                
                
                
                
                    x = x + x_space
                elif aa_type == 'G':
                    left_gt_aap = None
                    left_gt_aan = None
                    if 'AA_P' in gt_pair.box:
                        left_gt_aap = gt_pair.box['AA_P']
                    if 'AA_N' in gt_pair.box:
                        left_gt_aan = gt_pair.box['AA_N']
                    
                    x = x + x_space
            
        
            else:
                if i -1 in col_type and i+1 in col_type:
                    if col_type[i-1] == 'G' and  col_type[i+1] == 'DS':
                        pass
                    else:
                         
                        left_gt_aap = None
                        left_gt_aan = None
                else:
                    left_gt_aap = None
                    left_gt_aan = None
                x = x + x_space
        
        
        self.gt_paris = gt_pairs
        #rail    
        rail = M1_Rails(tech,0,x+cfgs.cell_offset_x + tech.CT_W.hv + tech.CT_E_AA.v )
        self.data.append(rail.data)
        npwell = NPWELL(tech,cfgs,rail.border_box)
        self.data.append(npwell.data)
        #M1
        ys = [t.c for t in tech.M1_tracks]
        loc = {}
        for i,x in enumerate(xs):
            for j,y in enumerate(ys):
                loc[(i,j)] = (x,y)
        m1_edges = M1_Route(tech, edges_op.edges, loc, tech.M1_W.v, eol_direction, eol_extension)
        self.data.append(m1_edges.data)
        
        
        #GT Connect
        gt_edges = GT_Route(tech, poly_connect_edges, xs, pin_loc,gt_pairs)
        self.data.append(gt_edges.data)
        
        
        #Pins M1
        txt_db_shapes = self.cell.db_shapes[tech.M1TXT]
        
        
        
        pinmetal = PINMETAL(tech, edges_op.input_pins, edges_op.output_pins, edges_op.pins_area, loc, txt_db_shapes)
        self.data.append(pinmetal.data)
        
        
        
        print('test drawer')
        return True


    


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



# class ColDrawer:
#     def __init__(self, tech, pn, edges, pins, left_mos_pair, is_left,is_right):
#         pass
    











# #Generation Part

# def find_special_points(edges, pins, ipins):
#     """
#     从edges中查找端点和直角点，并提取特殊pin点及未被访问的网格点
    
#     参数:
#     edges -- 边数据，字典格式，键为名称，值为点对列表
#     pins -- 引脚数据，字典格式，键为数字，值为点信息列表
    
#     返回:
#     end_points -- 端点列表（属于pin的点）
#     corner_points -- 直角点列表（属于pin的点）
#     isolated_pins -- 不在任何边上的pin点
#     unused_grid_points -- 网格中未被任何边经过的点
#     """
#     # 1. 从pins中提取所有pin的坐标（只取x和y）
#     pin_points = set()
#     for pin_data in pins.values():
#         for point_info in pin_data:
#             if point_info:  # 确保点信息存在
#                 coords = point_info[1]
#                 pin_points.add((coords[0], coords[1]))  # 只取x和y坐标
    
#     # 2. 统计所有边中的点坐标（只取x和y）
#     edge_points = set()
#     all_edge_points_count = {}
    
#     for key in edges:
#         for line in edges[key]:
#             for point in line:
#                 xy_point = (point[0], point[1])  # 只取x和y坐标
#                 edge_points.add(xy_point)
                
#                 # 统计每个点的出现次数
#                 if xy_point in all_edge_points_count:
#                     all_edge_points_count[xy_point] += 1
#                 else:
#                     all_edge_points_count[xy_point] = 1
    
#     # 3. 识别端点（只属于pin且只被一条边经过的点）
#     end_points = [point for point in pin_points 
#                   if point in all_edge_points_count and all_edge_points_count[point] == 1]
    
#     # 4. 构建每个点的相邻点集合
#     adjacent_points = {}
#     for key in edges:
#         for line in edges[key]:
#             p1, p2 = line
#             xy_p1, xy_p2 = (p1[0], p1[1]), (p2[0], p2[1])
            
#             # 添加相邻关系
#             if xy_p1 in adjacent_points:
#                 adjacent_points[xy_p1].add(xy_p2)
#             else:
#                 adjacent_points[xy_p1] = {xy_p2}
                
#             if xy_p2 in adjacent_points:
#                 adjacent_points[xy_p2].add(xy_p1)
#             else:
#                 adjacent_points[xy_p2] = {xy_p1}
    
#     # 5. 识别直角点（属于pin且被两条垂直边经过的点）
#     corner_points = []
#     for point in pin_points:
#         if point in adjacent_points:
#             neighbors = adjacent_points[point]
#             # 至少需要两个相邻点才能形成直角
#             if len(neighbors) == 2:
#                 # 检查是否存在垂直的相邻点对
#                 n1,n2 = list(neighbors)
#                 dx1, dy1 = n1[0] - point[0], n1[1] - point[1]
#                 dx2, dy2 = n2[0] - point[0], n2[1] - point[1]
            
#                 # 直角条件：向量点积为0
#                 if dx1 * dx2 + dy1 * dy2 == 0:
#                     corner_points.append(point)

    
#     # 去重处理
#     corner_points = list(set(corner_points))
    
#     # 6. 提取不在任何边上的pin点
#     input_pins = {}
#     for k, v in pins.items():
#         if len(v) == 1:
#             if v[0][0] in ipins:
#                 input_pins[v[0][0]] = (v[0][1][0],v[0][1][1]) 
    
#     isolated_pins = [point for point in pin_points if point not in edge_points]
    
#     # 7. 提取网格中未被任何边经过的点
#     # 确定网格范围
#     if edge_points:
#         min_x = min(point[0] for point in edge_points)
#         max_x = max(point[0] for point in edge_points)
#         min_y = min(point[1] for point in edge_points)
#         max_y = max(point[1] for point in edge_points)
        
#         # 生成所有网格点
#         all_grid_points = set()
#         for x in range(min_x, max_x + 1):
#             for y in range(min_y, max_y + 1):
#                 all_grid_points.add((x, y))
        
#         # 未被访问的网格点
#         unused_grid_points = all_grid_points - edge_points
#     else:
#         unused_grid_points = set()
    
#     #get used pins
#     all_points = set()
#     for values in edges.values():
    
#         for point_pair in values:
#             all_points.add(point_pair[0])
#             all_points.add(point_pair[1])

#     used_points = sorted(all_points)
    
    
    
#     return end_points, corner_points, input_pins, unused_grid_points, used_points


# def cal_parallel_edges(edges_points,input_pins):
    
#     data = edges_points.copy()
#     for k,v in input_pins.items():
#         data[k] = [v]
    
#     # 初始化结果字典
#     result = {}
    
#     # 获取所有键的列表
#     keys = list(data.keys())
    
#     # 遍历所有可能的键对（i < j 避免重复计数）
#     for i in range(len(keys)):
#         for j in range(i + 1, len(keys)):
#             key1 = keys[i]
#             key2 = keys[j]
            
#             # 遍历key1中的所有点
#             for x1, y1 in data[key1]:
#                 # 遍历key2中的所有点
#                 for x2, y2 in data[key2]:
#                     # 检查横坐标是否相差为1且纵坐标相等
#                     if (abs(x1 - x2) == 1) and (y1 == y2):
#                         # 确定较小的横坐标作为元组的第一个元素
#                         pair = (min(x1, x2), max(x1, x2))
                        
#                         # 更新结果字典
#                         if pair in result:
#                             result[pair] += 1
#                         else:
#                             result[pair] = 1
    
#     return result

# def col_data(net_loc):
#     col_mos = {}
#     for key, value in net_loc.items():
#         first_element = value[0]
#         if first_element not in col_mos:
#             col_mos[first_element] = {'P':[],'N':[] }
#         if key[0].T == 'P':
#             col_mos[first_element]['P'].append(key)
#         else:
#             col_mos[first_element]['N'].append(key)
        
#     col_type = {}
#     for key, value in col_mos.items():
#         unique_connections = set()
#         for list_key in ['P', 'N']:
#             for element in value[list_key]:
#                 unique_connections.add(element[1])
#         sorted_connections = sorted(unique_connections)
#         col_type[key] = ''.join(sorted_connections)
#     return col_mos, col_type



# #TODO: 
# def cal_space_SD_to_G(tech, sd_pins, g_pins, transistors):
#     p = transistors['P']


#     n = transistors['N']

# def edges_to_points(edges):
#     points = {}
#     for k,v in edges.items():
#         points[k] = []
#         for t in v:
#             points[k].append(t[0])
#             points[k].append(t[1])
#         points[k] = list(set(points[k]))
#     return points
    
# def cal_eol_type(end_ps, corner_ps, unused_ps, used_ps, edges_points):
#     eol_direction = {} #pin: sublist of [left,right,up,down]
#     fail_eol_direction  = {}

#     for p in end_ps:
#         net_points = [v for k,v in edges_points.items() if p in v][0]
        
#         x,y = p
#         if (x-1,y) in net_points:
#             if (x,y-1) in unused_ps and (x,y+1) in unused_ps:
#                 eol_direction[p] = ['up','down']
#             elif (x+1,y) in unused_ps:
#                 eol_direction[p] = ['right']
#             else:
#                 # eol_direction[p] = ['right']
#                 fail_eol_direction[p] = ['right']
            
#         elif (x+1,y) in net_points:
#             if (x,y-1) in unused_ps and (x,y+1) in unused_ps:
#                 eol_direction[p] = ['up','down']
#             elif (x-1,y) in unused_ps:
#                 eol_direction[p] = ['left']
#             else:
#                 # eol_direction[p] = ['left']
#                 fail_eol_direction[p] = ['left']
#         elif (x,y-1) in net_points:
#             if (x-1,y) in unused_ps and (x+1,y) in unused_ps:
#                 eol_direction[p] = ['left','right']
#             elif (x,y+1) in unused_ps:
#                 eol_direction[p] = ['up']
#             else:
#                 fail_eol_direction[p] = []
#                 if not((x-1,y) in unused_ps):
#                     fail_eol_direction[p].append('left')
#                 if not((x+1,y) in unused_ps):
#                     fail_eol_direction[p].append('right') 
                  
#         elif (x,y+1) in net_points:
#             if (x-1,y) in unused_ps and (x+1,y) in unused_ps:
#                 eol_direction[p] = ['left','right']
#             elif (x,y-1) in unused_ps:
#                 eol_direction[p] = ['down']
#             else:
#                 fail_eol_direction[p] = []
#                 if not((x-1,y) in unused_ps):
#                     fail_eol_direction[p].append('left')
#                 if not((x+1,y) in unused_ps):
#                     fail_eol_direction[p].append('right')           
#         else:
#             raise ValueError
            
#     for p in corner_ps:
#         net_points = [v for k,v in edges_points.items() if p in v][0]
#         x,y = p
#         if (x-1,y) in net_points and (x,y+1) in net_points:
#             if (x+1,y) in unused_ps:
#                 eol_direction[p] = ['right']
#             elif (x,y-1) in unused_ps:
#                 eol_direction[p] = ['down']
#             else:
#                 # eol_direction[p] = ['right']
#                 fail_eol_direction[p] = ['right']    
                
#         elif (x-1,y) in net_points and (x,y-1) in net_points:
#             if (x+1,y) in unused_ps:
#                 eol_direction[p] = ['right']
#             elif (x,y+1) in unused_ps:
#                 eol_direction[p] = ['up']
#             else:
#                 # eol_direction[p] = ['right']
#                 fail_eol_direction[p] = ['right']    
                
#         elif (x+1,y) in net_points and (x,y-1) in net_points:
#             if (x-1,y) in unused_ps:
#                 eol_direction[p] = ['left']
#             elif (x,y+1) in unused_ps:
#                 eol_direction[p] = ['up']
#             else:
#                 # eol_direction[p] = ['left']
#                 fail_eol_direction[p] = ['left']         
#         elif (x+1,y) in net_points and (x,y+1) in net_points:
#             if (x-1,y) in unused_ps:
#                 eol_direction[p] = ['left']
#             elif (x,y-1) in unused_ps:
#                 eol_direction[p] = ['down']
#             else:
#                 # x_extend_pins[p] = ['left']
#                 fail_eol_direction[p] = ['left']         
#         else:
#             raise ValueError
    
#     data = []
#     for k,v in fail_eol_direction.items():
#         for t in v:
#             data.append((k[0],t))
#     col_eol_ext = []
#     for t in data:
#         if t[0]>0:
#             if t[1] =='right':
#                 col_eol_ext.append((t[0],t[0]+1))
#             else:
#                 col_eol_ext.append((t[0]-1,t[0]))
            
#     col_eol_ext = list(set(col_eol_ext))
#     return eol_direction, fail_eol_direction,col_eol_ext




# def poly_connect_process(poly_connect,pin_loc):
#     poly_connect_p = []
#     poly_connect_n = []
#     poly_connect_edges = []
    
#     for p1,p2 in poly_connect.values():
#         if p1[1] == p2[1]:
#             poly_connect_edges.append([(p1[0],p2[0]), 'm','max'])
#         else:
#             m = int(0.5*(p1[0] + p2[0]))
#             if p1[1] ==pin_loc.aap:
#                 poly_connect_p.append(p1[0])
#                 poly_connect_edges.append([(p1[0], m), 'p', 'min'])
#             else:
#                 poly_connect_n.append(p1[0])
#                 poly_connect_edges.append([(p1[0], m), 'n', 'min'])
#             if p2[1] ==pin_loc.aap:
#                 poly_connect_p.append(p2[0])
#                 poly_connect_edges.append([(p2[0], m), 'p', 'min'])
#             else:
#                 poly_connect_n.append(p2[0])
#                 poly_connect_edges.append([(p2[0], m), 'n', 'min'])     
                
#             poly_connect_edges.append([(m, m), 'pn','min'])
#     return poly_connect_p,poly_connect_n,poly_connect_edges

# # def optimize_U_route(edges,pins):
    
    








class Edges_Optimizer:
    def __init__(self, size, pin_loc, edges, pins, ipins,opins, gg_nets, 
                 vdd_nets, vss_nets, poly_connect):
        self.ipins = ipins
        self.opins = opins
        self.edges = edges
        self.pins = pins
        self.size = size
        self.pin_loc = pin_loc
        self.block_pins = []
        
        self.gg_nets = list({point[0] for sublist in gg_nets for point in sublist})
        self.vdd_nets = list({p[0] for p in vdd_nets})
        self.vss_nets = list({p[0] for p in vss_nets})
        self.poly_connect = poly_connect
        
    @property 
    def edge_points(self):
        points = {}
        for k,v in self.edges.items():
            points[k] = []
            for t in v:
                points[k].append(t[0])
                points[k].append(t[1])
            points[k] = list(set(points[k]))
        return points
  
    @property
    def all_pin_points(self):
        # 从pins中提取所有pin的坐标（只取x和y）
        pin_points = set()
        for pin_data in self.pins.values():
            for point_info in pin_data:
                if point_info:  # 确保点信息存在
                    coords = point_info[1]
                    pin_points.add((coords[0], coords[1]))  # 只取x和y坐标
        return pin_points

    @property
    def pin_points(self):
        # 从pins中提取所有pin的坐标（只取x和y）
        pin_points = {}
        for pin_data in self.pins.values():
            for point_info in pin_data:
                if point_info:  # 确保点信息存在
                    coords = point_info[1]
                    if not(point_info[0] in pin_points):
                        pin_points[point_info[0]] = []
                    pin_points[point_info[0]].append((coords[0], coords[1]))  # 只取x和y坐标
        return pin_points
   
    @property
    def col_pins(self):
        col_pins = {k:{} for k in self.pins}
        for col, pins in self.pins.items():
            if pins:
                for net,t in pins:
                    if t[2] == 1:
                        if t[1] >= self.pin_loc.gtp:
                            col_pins[col]['paa'] = [net,t]
                        if t[1] <= self.pin_loc.gtn:
                            col_pins[col]['naa'] = [net,t]
                    if t[2] == 0:
                        if t[1] >= self.pin_loc.gtp:
                            col_pins[col]['pgt'] = [net,t]
                        if t[1] <= self.pin_loc.gtn:
                            col_pins[col]['ngt'] = [net,t]  
        return col_pins
    
    @property  
    def vdd_nets_loc(self):
        #process vdd pin loc: if to rail directly or grid
        vdd_nets_loc = {}
        used_ps,unused_ps = self.used_points
        size = self.size
        for t in self.vdd_nets:
            if (t, size[1]-1) in unused_ps and (t, size[1]-2) in unused_ps:
                vdd_nets_loc[t] =  [size[1]-1, 'down']
            elif (t, size[1]-1) in unused_ps and (t-1, size[1]-1) in unused_ps and (t+1, size[1]-1) in unused_ps:
                vdd_nets_loc[t] =  [size[1]-1, 'lr']               
            else:
                vdd_nets_loc[t] =  [-1,'']
        return vdd_nets_loc
                    
    @property  
    def vss_nets_loc(self):                    
        vss_nets_loc = {}
        used_ps,unused_ps = self.used_points
        # size = self.size
        for t in self.vss_nets:
            if (t, 0) in unused_ps and (t, 1) in unused_ps:
                vss_nets_loc[t] =  [0, 'up']
            elif (t, 0) in unused_ps and (t-1, 0) in unused_ps and (t+1, 0) in unused_ps:
                vss_nets_loc[t] =  [0, 'lr']
            else:
                vss_nets_loc[t] =  [-1,'']         

        return vss_nets_loc
    
    
    @property
    def used_points(self):
        
        edge_points_l = set([t2 for t1 in self.edge_points.values() for t2 in t1])
        pin_points_l  = self.all_pin_points
       
        used_points = edge_points_l.union( pin_points_l)
       
        all_grid_points = set()
        for x in range(self.size[0]+1):
            for y in range(self.size[1]):
                all_grid_points.add((x, y))
               
        unused_points = all_grid_points - used_points    
               
        return used_points,unused_points
    @property
    def input_pins(self):   
        input_pins = {}
        for k, v in self.pins.items():
            if len(v) == 1:
                if v[0][0] in self.ipins:
                    input_pins[v[0][0]] = (v[0][1][0],v[0][1][1]) 
       
        return input_pins
    @property
    def output_pins(self):   
        output_pins = {}
        for k, vs in self.pins.items():
            for v in vs:
                if v[0] in self.opins:
                    if not(v[0] in output_pins):
                        output_pins[v[0]] = []
                    output_pins[v[0]].append( (v[1][0],v[1][1])) 
       
        return output_pins
    
    def which_edge(self, point):
        for net, ps in self.edge_points.items():
            for p in ps:
                if point == p:
                    return net
        for net, p in self.input_pins.items():
            if point == p:
                return net
        
        return ''
        
        
    
    def get_edges(self, net):
        edges = self.edges
        if net in edges:
            return edges[net], self.edge_points[net]
        else:
            return []
        
    def get_pins(self, net):
        pin_points = self.pin_points
        if net in pin_points:
            return pin_points[net]
        else:
            return []



    @property
    def eol_points(self):
       edge_points = set()
       all_edge_points_count = {}
       
       for key in self.edges:
           for line in self.edges[key]:
               for point in line:
                   xy_point = (point[0], point[1])  # 只取x和y坐标
                   edge_points.add(xy_point)
                   
                   # 统计每个点的出现次数
                   if xy_point in all_edge_points_count:
                       all_edge_points_count[xy_point] += 1
                   else:
                       all_edge_points_count[xy_point] = 1
       
       # 识别端点（只属于pin且只被一条边经过的点）
       end_points = [point for point in self.all_pin_points 
                     if point in all_edge_points_count and all_edge_points_count[point] == 1]
       
       # 构建每个点的相邻点集合
       adjacent_points = {}
       for key in self.edges:
           for line in self.edges[key]:
               p1, p2 = line
               xy_p1, xy_p2 = (p1[0], p1[1]), (p2[0], p2[1])
               
               # 添加相邻关系
               if xy_p1 in adjacent_points:
                   adjacent_points[xy_p1].add(xy_p2)
               else:
                   adjacent_points[xy_p1] = {xy_p2}
                   
               if xy_p2 in adjacent_points:
                   adjacent_points[xy_p2].add(xy_p1)
               else:
                   adjacent_points[xy_p2] = {xy_p1}
       
       # 识别直角点（属于pin且被两条垂直边经过的点）
       corner_points = []
       for point in self.all_pin_points:
           if point in adjacent_points:
               neighbors = adjacent_points[point]
               # 至少需要两个相邻点才能形成直角
               if len(neighbors) == 2:
                   # 检查是否存在垂直的相邻点对
                   n1,n2 = list(neighbors)
                   dx1, dy1 = n1[0] - point[0], n1[1] - point[1]
                   dx2, dy2 = n2[0] - point[0], n2[1] - point[1]
               
                   # 直角条件：向量点积为0
                   if dx1 * dx2 + dy1 * dy2 == 0:
                       corner_points.append(point)

       
       # 去重处理
       corner_points = list(set(corner_points))
       return end_points,corner_points
    
    def cal_eol_type(self):
        end_ps, corner_ps = self.eol_points
        edges_points = self.edge_points
        used_ps, unused_ps = self.used_points
        
        eol_direction = {} #pin: sublist of [left,right,up,down]
        eol_extension = {}

        for p in end_ps:
            net_points = self.get_edges(self.which_edge(p))[1]       
            x,y = p
            if (x-1,y) in net_points:
                if (x,y-1) in unused_ps and (x,y+1) in unused_ps:
                    eol_direction[p] = ['up','down']
                elif (x+1,y) in unused_ps:
                    eol_direction[p] = ['right']
                else:
                    eol_direction[p] = ['right']
                    eol_extension[p] = ['right']
                
            elif (x+1,y) in net_points:
                if (x,y-1) in unused_ps and (x,y+1) in unused_ps:
                    eol_direction[p] = ['up','down']
                elif (x-1,y) in unused_ps:
                    eol_direction[p] = ['left']
                else:
                    eol_direction[p] = ['left']
                    eol_extension[p] = ['left']
            elif (x,y-1) in net_points:
                if (x-1,y) in unused_ps and (x+1,y) in unused_ps:
                    eol_direction[p] = ['left','right']
                elif (x,y+1) in unused_ps:
                    eol_direction[p] = ['up']
                else:
                    eol_direction[p] = ['left','right']
                    eol_extension[p] = []
                    if not((x-1,y) in unused_ps):
                        eol_extension[p].append('left')
                    if not((x+1,y) in unused_ps):
                        eol_extension[p].append('right') 
                      
            elif (x,y+1) in net_points:
                if (x-1,y) in unused_ps and (x+1,y) in unused_ps:
                    eol_direction[p] = ['left','right']
                elif (x,y-1) in unused_ps:
                    eol_direction[p] = ['down']
                else:
                    eol_direction[p] = ['left','right']
                    eol_extension[p] = []
                    if not((x-1,y) in unused_ps):
                        eol_extension[p].append('left')
                    if not((x+1,y) in unused_ps):
                        eol_extension[p].append('right')           
            else:
                raise ValueError
                
        for p in corner_ps:
            net_points = [v for k,v in edges_points.items() if p in v][0]
            x,y = p
            if (x-1,y) in net_points and (x,y+1) in net_points:
                if (x+1,y) in unused_ps:
                    eol_direction[p] = ['right']
                elif (x,y-1) in unused_ps:
                    eol_direction[p] = ['down']
                else:
                    eol_direction[p] = ['right']
                    eol_extension[p] = ['right']    
                    
            elif (x-1,y) in net_points and (x,y-1) in net_points:
                if (x+1,y) in unused_ps:
                    eol_direction[p] = ['right']
                elif (x,y+1) in unused_ps:
                    eol_direction[p] = ['up']
                else:
                    eol_direction[p] = ['right']
                    eol_extension[p] = ['right']    
                    
            elif (x+1,y) in net_points and (x,y-1) in net_points:
                if (x-1,y) in unused_ps:
                    eol_direction[p] = ['left']
                elif (x,y+1) in unused_ps:
                    eol_direction[p] = ['up']
                else:
                    eol_direction[p] = ['left']
                    eol_extension[p] = ['left']         
            elif (x+1,y) in net_points and (x,y+1) in net_points:
                if (x-1,y) in unused_ps:
                    eol_direction[p] = ['left']
                elif (x,y-1) in unused_ps:
                    eol_direction[p] = ['down']
                else:
                    eol_direction[p] = ['left']
                    eol_extension[p] = ['left']         
            else:
                raise ValueError
        
        data = []
        for k,v in eol_extension.items():
            for t in v:
                data.append((k[0],t))
        col_eol_ext = []
        for t in data:
            if t[0]>0:
                if t[1] =='right':
                    col_eol_ext.append((t[0],t[0]+1))
                else:
                    col_eol_ext.append((t[0]-1,t[0]))
                
        col_eol_ext = list(set(col_eol_ext))
        return eol_direction, eol_extension, col_eol_ext



    def poly_connect_process(self):
        poly_connect = self.poly_connect
        pin_loc = self.pin_loc
        poly_connect_p = []
        poly_connect_n = []
        poly_connect_edges = []
        
        for p1,p2 in poly_connect.values():
            if p1[1] == p2[1]:
                poly_connect_edges.append({'start':min(p1[0], p2[0]),'end':max(p1[0], p2[0]), 
                                           'start_ext':'','end_ext':'' ,'y':'m', 'w':'max','type':'h'})
            else:
                
                if p1[1] ==pin_loc.aap:
                    poly_connect_p.append(p1[0])
                    poly_connect_n.append(p2[0])
                    
                    x1,y1,_ = p1
                    x2,y2,_ = p2
                    
                    poly_connect_edges.append({'start':x1,'end':x2-1, 'start_ext':'p',
                                               'end_ext':'min' ,'y':'p', 'w':'min','type':'h'})
                    poly_connect_edges.append({'start':x2-1,'end':x2, 'start_ext':'min',
                                               'end_ext':'n' ,'y':'n', 'w':'min','type':'h'})                    
                    
                    poly_connect_edges.append({'start':'p','end':'n', 'start_ext':'',
                                               'end_ext':'' ,'x':x2-1, 'w':'min','type':'v'})
                
                
                else:
                    x1,y1,_ = p1
                    x2,y2,_ = p2
                    poly_connect_p.append(p2[0])
                    poly_connect_n.append(p1[0])
                    
                    poly_connect_edges.append({'start':x1,'end':x2, 'start_ext':'n',
                                               'end_ext':'p' ,'y':'p', 'w':'min','type':'h'})
                                       
                    poly_connect_edges.append({'start':'p','end':'n', 'start_ext':'',
                                               'end_ext':'' ,'x':x1, 'w':'n','type':'v'})
                    
        return poly_connect_p,poly_connect_n,poly_connect_edges
    
    def optimize_inpins(self):
        
        expands = [
                 [[ 0, 1],[ 0,-1],[ 1, 0],[ 1, 1],[ 1,-1]],
                 [[ 0, 1],[ 0,-1],[-1, 0],[-1, 1],[-1,-1]],
                 [[ 0, 1],[ 0,-1],[ 1, 0],[ 1, 1]],
                 [[ 0, 1],[ 0,-1],[ 1, 0],[ 1, -1]],
                 [[ 0, 1],[ 0,-1],[-1, 0],[-1, 1]],           
                 [[ 0, 1],[ 0,-1],[-1, 0],[-1,-1]], 
                 [[ 0, 1],[ 0,-1],[ 1, 0]],
                 [[ 0, 1],[ 0,-1],[ -1, 0]],
                 [[ 0, 1],[ 0,-1]],
            ]
        
        pins_area = {}
        blks = []
        for pin, (x,y) in self.input_pins.items():
            for expand in expands:
                pin_area = [(x+t[0],y+t[1]) for t in expand]
                result,edges = self.ripup_reroute( pin_area+blks)
                # print('1',result)
                if result:
                    pins_area[pin] = pin_area
                    blks+=pin_area
                    self.edges = edges
                    break
            if not(pin in pins_area): 
                pins_area[pin] = []
        # print('2',pins_area)
        self.pins_area = pins_area
        for ps in self.pins_area.values():
            self.block_pins += ps
    
    def optimize_ct(self):
        for col, ps in self.col_pins.items():
            if 'paa' in ps or 'naa' in ps:
                if 'paa' in ps:
                    net,pin = ps['paa']
                    u = self.size[1]
                    b = pin[1]
                    for i in range(b+1, u):
                        pin_new = (pin[0], i, pin[2])
                        result = self.ripup_reroute_2(pin, pin_new)
                        if not(result):
                            break
                        else:
                            pin = pin_new
   
                if 'naa' in ps:
                    net,pin = ps['naa']
                    b = 0 - 1
                    u = pin[1] - 1
                    for i in range(u, b, -1):
                        pin_new = (pin[0], i, pin[2])
                        result = self.ripup_reroute_2(pin, pin_new)
                        if not(result):
                            break
                        else:
                            pin = pin_new
                                      
                             
    
    
    def ipins_edges(self):
        pass
        
    

    def optimize_U_shape(self):
        all_pin_points = list(self.all_pin_points.copy())
        edge_points = self.edge_points
   
        op = False
        for net,points in edge_points.items():
            for p1 in points:
                x,y = p1
                p2 = (x + 1, y)
                p3 = (x, y + 1)
                p4 = (x + 1, y + 1)
                
                if p2 in points and p3 in points and p4 in points:
                    edges =normalize_edges(self.edges[net])
                    t_points = [k for k,v in count_edges_using_point(edges).items() if v>2]  
                    all_pin_points += t_points
                    
                    ps =[]
                    if not((p1,p2) in edges) and (p3,p4) in edges and (p1,p3) in edges and (p2,p4) in edges:
                        old_edges = [(p3,p4),(p1,p3),(p2,p4)]
                        new_edges = [(p1,p2)]
                        if p3 in all_pin_points:
                            new_edges.append((p1,p3))
                            ps = [p1]
                        if p4 in all_pin_points:
                            new_edges.append((p2,p4))
                            ps = [p2]
                        print('bottom',p1,p2)
                        op = True
                    elif not((p3,p4) in edges) and (p1,p2) in edges and (p1,p3) in edges and (p2,p4) in edges:
                        old_edges = [(p1,p2),(p1,p3),(p2,p4)]
                        new_edges = [(p3,p4)]
                        if p1 in all_pin_points:
                            new_edges.append((p1,p3))
                            ps = [p3]
                        if p2 in all_pin_points:
                            new_edges.append((p2,p4))
                            ps = [p4]
                        print('top',p3,p4)
                        op = True
                    if op:
                        self.edges = self.revise_edges(self.edges, net, old_edges, new_edges)
                        return True  
        return False              
  
        
        
        
   
    
    def ripup_reroute(self, block_nodes):
        #if pass return true and new_edges
        edges = self.edges.copy()
        pin_points = self.pin_points.copy()

        used_ps, unused_ps = self.used_points
        used_ps = list(used_ps)
        unused_ps = list(unused_ps)
        
        blks = list(self.input_pins.values()).copy() + block_nodes
        # print('test1',block_nodes)
        for node in block_nodes:
            if node in unused_ps:
                pass
                # blks.append(node)
                # print('1',blks)
            else:
    
                net = self.which_edge(node)  
                terminals = pin_points[net]
                # print('2',node,net,terminals,blks)
                used_edges = [v for k,v in edges.items() if k != net]
                used_nodes = []
                for used_edge in used_edges:
                    for n1,n2 in used_edge:
                        used_nodes.append(n1)
                        used_nodes.append(n2)
                for t in blks:
                    # print(t)
                    used_nodes.append(t)
                used_nodes.append(node)
                used_nodes = list(set(used_nodes))  
                # print(used_nodes)
                G = nx.grid_2d_graph(self.size[0], self.size[1])
                G.remove_nodes_from(used_nodes)       
                subgraph = find_subgraph_with_nodes(G, terminals)
                if subgraph:
                    steiner_tree = nx.algorithms.approximation.steiner_tree(subgraph, terminals,method='mehlhorn')
                    # print('4')
                    blks.append(node)
                    edges[net] = list(steiner_tree.edges)
                else:
                    # print('5')
                    return False,node
        return True, edges
    
    def ripup_reroute_2(self, pin, pin_new):
        #if pin_new can be re-routed
        pin_points = self.pin_points.copy()
        used_ps, unused_ps = self.used_points
        used_ps = list(used_ps)
        unused_ps = list(unused_ps)
        blk_ps = self.block_pins
        
        net_pin = self.which_edge((pin[0],pin[1]))
        net_pin_new = self.which_edge((pin_new[0],pin_new[1]))
        result = False
        if net_pin_new:
            if net_pin_new == net_pin:
                self.pins = self.revise_pins(self.pins.copy(), pin, pin_new)
                result = True
                #already have edge
            else:
                #most hard work:
                terminals = pin_points[net_pin_new]
                # print('2',node,net,terminals,blks)
                used_edges = [v for k,v in self.edges.items() if k != net_pin_new]
                used_nodes = []
                for used_edge in used_edges:
                    for n1,n2 in used_edge:
                        used_nodes.append(n1)
                        used_nodes.append(n2)
                for t in blk_ps:
                    used_nodes.append(t)
                used_nodes.append((pin_new[0],pin_new[1]))
                used_nodes = list(set(used_nodes))  
                # print(used_nodes)
                G = nx.grid_2d_graph(self.size[0], self.size[1])
                G.remove_nodes_from(used_nodes)       
                subgraph = find_subgraph_with_nodes(G, terminals)
                if subgraph:
                    steiner_tree = nx.algorithms.approximation.steiner_tree(subgraph, terminals,method='mehlhorn')
                    # print('4')
          
                    self.edges[net_pin_new] = list(steiner_tree.edges)
                    self.pins = self.revise_pins(self.pins.copy(), pin, pin_new)
                    self.edges[net_pin].append( ( (pin[0],pin[1]),(pin_new[0],pin_new[1]) ) )
                    result = True
                else:
                    pass
                    
                    
            
        else:
            if (pin_new[0],pin_new[1]) in unused_ps and not((pin_new[0],pin_new[1]) in blk_ps):
                self.pins = self.revise_pins(self.pins.copy(), pin, pin_new)
                self.edges[net_pin].append( ( (pin[0],pin[1]),(pin_new[0],pin_new[1]) ) )
                result = True
            
        return result
        

    
    def revise_pins(self, pins, old_pin, new_pin):
        # 遍历所有 pin 编号
        for pin_number, connections in pins.items():
            # 遍历每个 pin 的连接列表
            for i, (net_name, pin_coords) in enumerate(connections):
                # 如果找到匹配的旧坐标
                if pin_coords == old_pin:
                    # 替换为新坐标
                    pins[pin_number][i] = (net_name, new_pin)
                    # print(f"已将 pin {pin_number} 的连接 {old_pin} 替换为 {new_pin}")
        
        return pins      
        
    def revise_edges(self, edges, net, old_edges, new_edges):

        edges = edges.copy()

        
        # 检查网络是否存在
        if net not in edges:
            print(f"Warning: Net '{net}' is none, no actions")
            return edges
        
        # 获取指定网络的边列表
        edge_list = edges[net]
        
        # 规范化旧边和新边
        normalized_old = [normalize_edge(edge) for edge in old_edges]
        normalized_new = [normalize_edge(edge) for edge in new_edges]
        
        # 删除旧边：过滤掉规范化后在旧边列表中的边
        new_edge_list = []
        removed_count = 0
        for edge in edge_list:
            normalized = normalize_edge(edge)
            if normalized not in normalized_old:
                new_edge_list.append(edge)
            else:
                removed_count += 1
        
        # 添加新边：只添加不在当前边列表中的新边
        added_count = 0
        current_normalized = [normalize_edge(e) for e in new_edge_list]
        for new_edge in new_edges:
            normalized_new_edge = normalize_edge(new_edge)
            if normalized_new_edge not in current_normalized:
                new_edge_list.append(new_edge)
                added_count += 1
                current_normalized.append(normalized_new_edge)
        
        # 更新边列表
        edges[net] = new_edge_list
        
        # 打印操作结果
        print(f"Net {net}: remove {removed_count} old edges, add {added_count} new edges")
        
        return edges   
   
    @property
    def parallel_edges(self):
        #TODO: for parallel_edges == 1, if we can reroute to reduce parallel number
        data = self.edge_points.copy()
        for k,vs in self.pins_area.items():
            data[k] = []
            for v in vs:
                data[k].append(v)
        
        # 初始化结果字典
        result = {}
        
        # 获取所有键的列表
        keys = list(data.keys())
        
        # 遍历所有可能的键对（i < j 避免重复计数）
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                key1 = keys[i]
                key2 = keys[j]
                
                # 遍历key1中的所有点
                for x1, y1 in data[key1]:
                    # 遍历key2中的所有点
                    for x2, y2 in data[key2]:
                        # 检查横坐标是否相差为1且纵坐标相等
                        if (abs(x1 - x2) == 1) and (y1 == y2):
                            # 确定较小的横坐标作为元组的第一个元素
                            pair = (min(x1, x2), max(x1, x2))
                            
                            # 更新结果字典
                            if pair in result:
                                result[pair] += 1
                            else:
                                result[pair] = 1
        
        return result
    

    
class Col_Spaces:
    def __init__(self, cfgs, tech, net_loc, edges_op):
        self.cfgs = cfgs
        self.tech = tech
        self.net_loc = net_loc
        self.edges_op = edges_op

    @property
    def col_mos(self):
        net_loc = self.net_loc
        col_mos = {}
        for key, value in net_loc.items():
            first_element = value[0]
            if first_element not in col_mos:
                col_mos[first_element] = {'P':[],'N':[] }
            if key[0].T == 'P':
                col_mos[first_element]['P'].append(key)
            else:
                col_mos[first_element]['N'].append(key)
        return col_mos
    
    @property
    def col_type(self):             
        col_mos = self.col_mos
        col_type = {}
        for key, value in col_mos.items():
            unique_connections = set()
            for list_key in ['P', 'N']:
                for element in value[list_key]:
                    unique_connections.add(element[1])
            sorted_connections = sorted(unique_connections)
            col_type[key] = ''.join(sorted_connections)
        return col_type
    
    

                
    def run(self,col_eol_ext):
    
        '''
            algorithm:
    
                m1. if parallel m1 exists, m1 space + m1 width
                m2. if parallel m1 exists, and EOL on x exists, m1 space + m1 width + m1 EOL 
         
                gt1. if not pin exists, half of ( GT space + left mos L + right mos L)
                gt2.
                gt3. if paralle gt exists, gt space + half (GT width) + half(max(mos L))
                gt4. if paralle gt exists, gt space + half (GT width) + max( half(max(mos L)) , half(CT_W) + CT_E_GT) )
    
                aa1. if pin exists, and no L shape AA, 
                aa2. if pin exists, and L shape AA, 
                
        
        '''
        cfgs = self.cfgs
        tech = self.tech
        size = self.edges_op.size
        vdd_nets = self.edges_op.vdd_nets
        vss_nets = self.edges_op.vss_nets
        parallel_edges = self.edges_op.parallel_edges
        pins = self.edges_op.pins
        
        
        mos_L = max(cfgs.gate_length)
    
        #
        s_m1 = tech.M1_S.v + tech.M1_W.v + tech.CT_E_M1.v
        s_m2 = tech.M1_S.v + tech.M1_W.v + tech.CT_E_M1_END.v
        
        #
        s_gt1 = tech.GT_S.v + tech.GT_W.hv + half( mos_L )
        s_gt2 = tech.GT_S.v + tech.GT_W.hv + max( half(mos_L), tech.CT_W.hv + tech.CT_E_GT.v)
        
        # s_aa_nct1. if no pin exists, two transistor Ws are equal, 
        # s_aa_nct2. if no pin exists, two transistor Ws are not equal  
        s_aa_nct1 = half(tech.GT_S.v + mos_L)
        s_aa_nct2 = tech.CT_W.hv + half(mos_L) + tech.CT_E_AA.v + tech.GT_S_LAA_GT.v
       
        # s_aa1. if pin exists, and no L shape AA, 
        # s_aa2. if pin exists, and L shape AA, 
        s_aa1 = tech.CT_W.hv + tech.CT_S_GT.v + half(mos_L)
        s_aa2 = tech.CT_W.hv + max( tech.CT_E_AA.v + tech.GT_S_LAA_GT.v, tech.CT_S_GT.v) + half(mos_L)
        
        
        #col space
        x = cfgs.cell_offset_x + tech.CT_W.hv + tech.CT_E_AA.v 
        x_axis = []
        for i in range(size[0]-1):
            space = []
            #if have pins
            #More detail
            # print(pins)
            
            have_pins = bool(pins[i]) or (i in vdd_nets) or (i in vss_nets)
            
            if have_pins:
                space.append(['s_aa2',s_aa2])
            else:
                #TODO: not best solution
                space.append(['s_aa_nct2',s_aa_nct2])
            
            #if have parallel edge
            if (i,i+1) in parallel_edges:
                space.append(['s_m1',s_m1])
            if (i,i+1) in col_eol_ext:   
                space.append(['s_m1',s_m2])
            x_axis.append(space) 
            #if gt parallel exist
            
            
        return x_axis



def half(x):
    return int(0.5*x)

    
def normalize_edge(edge):
    """规范化边的表示，确保顺序统一"""
    return tuple(sorted(edge))
def normalize_edges(edges):
    return  [normalize_edge(edge) for edge in edges]

def count_edges_using_point(edges):
    """统计每个点被多少条边公用"""
    point_count = {}
    
    # 遍历所有边
    for edge in edges:
        # 每条边包含两个点
        point1, point2 = edge
        
        # 统计第一个点的出现次数
        if point1 in point_count:
            point_count[point1] += 1
        else:
            point_count[point1] = 1
        
        # 统计第二个点的出现次数
        if point2 in point_count:
            point_count[point2] += 1
        else:
            point_count[point2] = 1
    
    return point_count