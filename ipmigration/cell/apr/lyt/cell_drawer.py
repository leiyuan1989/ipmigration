# -*- coding: utf-8 -*-
"""

@author: leiyuan
"""


'''
Net

'''
from ipmigration.cell.apr.lyt.instance import M1_Rails,NPWELL
from ipmigration.cell.apr.lyt.instance import M1_Route,M2_Route,Pin_Nodes, GT_Route, CT_GT,V1_Nodes, CT_Nodes, EdgeRoute ,AA_SD,POWER

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
        abut_nets = self.cell.apr.abut_nets 
        gg_nets = self.cell.apr.gg_nets
        net_loc = self.cell.apr.net_loc
        size = self.cell.apr.grid_size 
        
        pins = self.pins
        edges = self.edges
        
        ipins = list(self.cell.ckt.ipins.keys())
        opins = list(self.cell.ckt.opins.keys())
        
        end_ps, corner_ps, iso_ps, unused_ps, used_ps = find_special_points(edges,pins)
        #iso pins == ipins
        
        
        
        edges_parallel = cal_parallel_edges(edges)
        eol_type = cal_eol_type( end_ps, corner_ps, unused_ps)
        
        
        gg_nets = list({point[0] for sublist in gg_nets for point in sublist})
        vdd_nets = list({p[0] for p in vdd_nets})
        vss_nets = list({p[0] for p in vss_nets})
                        
        col_mos,col_type = col_data(net_loc)


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
        x_axis = {}
        for i in range(size[0]-1):
            #if have pins
            have_pins = bool(pins[i]) or (i in vdd_nets) or (i in vss_nets)
            #if have parallel edge
            if (i,i+1) in edges_parallel:
                have_parallel_edge = True
            else:
                have_parallel_edge = False

            
            if i in col_type:
                ct = col_type[i]
                if ct == 'S': #left side and must has pins
                    #TODO: temporary use s_aa2
                    space = s_aa2
                    if have_parallel_edge:
                        space = max(space,s_m1)
                    x_axis[(i,i+1)] = max(s_aa2)
                elif  ct == 'D': #right side and must has pins
                    pass
                
                
            else:
                pass    
            
                
                
                
            
            if i == 0: #first
                cols = 'none->aa'
            elif i == size[0] - 1: #last
                cols = 'aa->none'
            else:
                pass
        
        
        '''
            algorithm:
                aa_sd:
                    left
                    
        
        '''
        
        
        
     
        middle = (size[1]-1)/2.0
        
        x = cfgs.cell_offset_x + tech.CT_W.hv + tech.CT_E_AA.v 
        
        for i in range(size[0]):
            aact_p = [t2 for t1,t2 in pins[i] if t2[1]>middle]
            aact_n = [t2 for t1,t2 in pins[i] if t2[1]<middle]
            
            #if have pins
            have_pins = bool(pins[i]) or (i in vdd_nets) or (i in vss_nets)
            #if have parallel edge
            if (i,i+1) in edges_parallel:
                have_parallel_edge = True
            else:
                have_parallel_edge = False
              
            # next_gt =     
              
                
            if i in col_mos:
                pn = col_mos[i]
                pmos = pn['P']
                nmos = pn['N']
                
                #pmos part
                if pmos:
                    if len(pmos) == 1:
                        if pmos[0][1] == 'D':
                            l_mos = pmos[0][0]
                        elif  pmos[0][1] == 'S':
                            r_mos = pmos[0][0]
                            #
                            
                            
                        else:
                            #G
                            
                            #TODO, consider poly connect
                            
                            if i in gg_nets:
                                #if i is pin
                                pass
                        
                    else:
                        #len(pmos) == 2
                        assert len(pmos) == 2
                        l_mos = [t for t in pmos if t[1]=='D'][0][0]
                        r_mos = [t for t in pmos if t[1]=='S'][0][0]
                        #if 
                        
                else:
                    #no pmos
                    pass
                 
                if nmos:
                    pass
                else:
                    pass
                
                
            
            else:
                #aa with two col
                #before is G or D?
                x += s_m1
                
                
                
            
        
        
                        
        
        
        
        
        # x = self.cfgs.cell_offset_x + self.tech.CT_E_AA.v + self.tech.CT_W.hv 
        # x = self.cfgs.cell_offset_x #revise to up if is_start is used in future
        
        
        print('test drawer')
        return True

        route_nets = self.pt_router.route_nets
        routed_edges = self.pt_router.routed_edges
        io_pins = self.pt_router.io_pins
        pw_pins = self.pt_router.pw_pins
        m2_edges = self.pt_router.m2_edges
        v1_pins =  self.pt_router.v1_pins  
            
        l = 0 
        r = self.G.max_col
        
        draw_G = copy.deepcopy(self.G)
        draw_G.remove_edges_from(list(draw_G.edges()))
                
        for k,vs in route_nets.items():
            if k != 'VDD' and k != 'VSS' and len(vs)>1:
                for v in vs:
                    if v[0] != l and v[0] != r and v[2] == 1:
                        draw_G.nodes[v]['aa_ct'] = k
        m1_edges = {}
        gt_edges = {}
        for net, edges in routed_edges.items():
            for edge in list(edges):
                n1,n2 = edge
                if n1[0]==n2[0] and n1[1]==n2[1] and n1[2]!=n2[2]:
                    # gt_ct_nodes.append((n1[0],n1[1]))
                    # print('abc',n1,n2)
                    draw_G.nodes[(n1[0],n1[1],0)]['gt_ct'] = (n1[0],n1[1],1)
                elif n1[2] == 1 and n2[2] == 1:
                    draw_G.add_edge(n1,n2)
                    if net in m1_edges:
                        m1_edges[net].append( ((n1[0],n1[1]),(n2[0],n2[1])) )
                    else:
                        m1_edges[net] = [ ((n1[0],n1[1]),(n2[0],n2[1])) ]
                elif n1[2] == 0 and n2[2] == 0:
                    draw_G.add_edge(n1,n2)
                    if net in gt_edges:
                        gt_edges[net].append( ((n1[0],n1[1]),(n2[0],n2[1])) )
                    else:
                        gt_edges[net] = [ ((n1[0],n1[1]),(n2[0],n2[1])) ]
                else:
                    raise ValueError
        
        # print(aa_ct_nodes)
        draw_data = {i:{} for i in range(r+1)}       
        start = 1
        for i, cols in enumerate(self.pt.grid_columns):
            pn = self.pt.place[i]
            for j in range(cols):
                draw_data[start + j]['P'] = pn['P']
                draw_data[start + j]['N'] = pn['N']
                draw_data[start + j]['type'] = (j+1,cols)
                if  j+1 == 2:
                    draw_data[start + j]['is_gt'] = True
                else:
                    draw_data[start + j]['is_gt'] = False
                
            start = start + cols
        
        draw_data[0]['is_gt'] = False
        draw_data[0]['P'] = None
        draw_data[0]['N'] = None
        draw_data[0]['type'] = (1,1)
        draw_data[start]['is_gt'] = False
        draw_data[start]['P'] = None
        draw_data[start]['N'] = None
        draw_data[start]['type'] = (1,1)
        
        x_axis = self.cal_col_space(start_x, tech, draw_data,draw_G)
        y_axis = [t.c for t in tech.M1_tracks]
        node_loc = {}
        for c, x in enumerate(x_axis):
            for r,y in enumerate(y_axis):
                node_loc[(c,r)] = (x,y)
        
        # print(x_axis)
        
        self.draw_G = draw_G
        self.draw_data = draw_data
        
        
        #
        #1 CT nodes
        gt_cts = []
        aa_cts = []
        for node in draw_G.nodes:
            attr = draw_G.nodes[node]
            if 'aa_ct' in attr:
                aa_cts.append((node[0],node[1]))
            if 'gt_ct' in attr:
                gt_cts.append((node[0],node[1]))        
        ct_lyt = CT_Nodes(tech, gt_cts, aa_cts, node_loc)
        self.data.append(ct_lyt.data)
        
        #pins
        io_pins_list = []
        for k,v in io_pins.items():
            io_pins_list.append((v[0],v[1]))
        io_lyt = Pin_Nodes(tech, io_pins_list, node_loc)
        self.data.append(io_lyt.data)
            
        #add text
        
        #2 m1 route
        #eol first
        eol_nodes = self.end_of_line_examine(draw_G)

        m1_edge_lyt = M1_Route(tech, m1_edges, node_loc, tech.M1_W.v, eol_nodes=eol_nodes)
        self.data.append(m1_edge_lyt.data)
        
        m2_edge_lyt = M2_Route(tech, m2_edges, node_loc)
        self.data.append(m2_edge_lyt.data)
        
        #3 gt route
        gt_edge_lyt = GT_Route(tech, gt_edges, node_loc, tech.GT_W.v, draw_data)
        self.data.append(gt_edge_lyt.data)
        
        #4 aa-gt
        gt_aa_lyt = GT_AA(tech, draw_data, gt_cts, aa_cts, pw_pins, node_loc, self.pt_router)
        self.data.append(gt_aa_lyt.data)
        
        # print('----',v1_pins)
        v1_lyt = V1_Nodes(tech, v1_pins, node_loc)
        self.data.append(v1_lyt.data)
        

        return x_axis[-1] # + tech.M1_S.v + tech.M1_W.v



                    
    def col_spaces(self):
        #m1 
        x_axis = []
        for col,v in draw_data.items():
            x_axis.append(start_x + 366*col)
        #return list of detail axis
        return x_axis

    def draw_pin(self):
        #consider if alignment is needed?
        pass

    


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



class ColDrawer:
    def __init__(self, tech, pn, edges, pins, left_mos_pair, is_left,is_right):
        pass
    











#Generation Part

def find_special_points(edges, pins):
    """
    从edges中查找端点和直角点，并提取特殊pin点及未被访问的网格点
    
    参数:
    edges -- 边数据，字典格式，键为名称，值为点对列表
    pins -- 引脚数据，字典格式，键为数字，值为点信息列表
    
    返回:
    end_points -- 端点列表（属于pin的点）
    corner_points -- 直角点列表（属于pin的点）
    isolated_pins -- 不在任何边上的pin点
    unused_grid_points -- 网格中未被任何边经过的点
    """
    # 1. 从pins中提取所有pin的坐标（只取x和y）
    pin_points = set()
    for pin_data in pins.values():
        for point_info in pin_data:
            if point_info:  # 确保点信息存在
                coords = point_info[1]
                pin_points.add((coords[0], coords[1]))  # 只取x和y坐标
    
    # 2. 统计所有边中的点坐标（只取x和y）
    edge_points = set()
    all_edge_points_count = {}
    
    for key in edges:
        for line in edges[key]:
            for point in line:
                xy_point = (point[0], point[1])  # 只取x和y坐标
                edge_points.add(xy_point)
                
                # 统计每个点的出现次数
                if xy_point in all_edge_points_count:
                    all_edge_points_count[xy_point] += 1
                else:
                    all_edge_points_count[xy_point] = 1
    
    # 3. 识别端点（只属于pin且只被一条边经过的点）
    end_points = [point for point in pin_points 
                  if point in all_edge_points_count and all_edge_points_count[point] == 1]
    
    # 4. 构建每个点的相邻点集合
    adjacent_points = {}
    for key in edges:
        for line in edges[key]:
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
    
    # 5. 识别直角点（属于pin且被两条垂直边经过的点）
    corner_points = []
    for point in pin_points:
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
    
    # 6. 提取不在任何边上的pin点
    isolated_pins = [point for point in pin_points if point not in edge_points]
    
    # 7. 提取网格中未被任何边经过的点
    # 确定网格范围
    if edge_points:
        min_x = min(point[0] for point in edge_points)
        max_x = max(point[0] for point in edge_points)
        min_y = min(point[1] for point in edge_points)
        max_y = max(point[1] for point in edge_points)
        
        # 生成所有网格点
        all_grid_points = set()
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                all_grid_points.add((x, y))
        
        # 未被访问的网格点
        unused_grid_points = all_grid_points - edge_points
    else:
        unused_grid_points = set()
    
    #get used pins
    all_points = set()
    for values in edges.values():
    
        for point_pair in values:
            all_points.add(point_pair[0])
            all_points.add(point_pair[1])

    used_points = sorted(all_points)
    
    
    
    return end_points, corner_points, isolated_pins, unused_grid_points,used_points


def cal_parallel_edges(edges):
    vertical_edges = {}    
    # 遍历每个网络及其边
    for net, edges_ in edges.items():
        for edge in edges_:
            (x1, y1), (x2, y2) = edge
            # 检查是否为垂直方向的边（x坐标相同，y坐标不同）
            if x1 == x2 and y1 != y2:
                x = x1  # 公共的x坐标
                # 将边添加到对应的x坐标组中
                if x not in vertical_edges:
                    vertical_edges[x] = []
                vertical_edges[x].append(edge)
    result = {}
    
    for x in vertical_edges:
        next_x = x + 1
        if next_x in vertical_edges:
            current_edges = vertical_edges[x]
            next_edges = vertical_edges[next_x]
            count = 0
    
            for edge1 in current_edges:
                y1_min = min(edge1[0][1], edge1[1][1])
                y1_max = max(edge1[0][1], edge1[1][1])
    
                for edge2 in next_edges:
                    y2_min = min(edge2[0][1], edge2[1][1])
                    y2_max = max(edge2[0][1], edge2[1][1])
    
                    if y1_min == y2_min and y1_max == y2_max:
                        count += 1
    
            if count > 0:
                result[(x, next_x)] = count

    return result

def col_data(net_loc):
    col_mos = {}
    for key, value in net_loc.items():
        first_element = value[0]
        if first_element not in col_mos:
            col_mos[first_element] = {'P':[],'N':[] }
        if key[0].T == 'P':
            col_mos[first_element]['P'].append(key)
        else:
            col_mos[first_element]['N'].append(key)
        
    col_type = {}
    for key, value in col_mos.items():
        unique_connections = set()
        for list_key in ['P', 'N']:
            for element in value[list_key]:
                unique_connections.add(element[1])
        sorted_connections = sorted(unique_connections)
        col_type[key] = ''.join(sorted_connections)
    return col_mos, col_type



#TODO: 
def cal_space_SD_to_G(tech, sd_pins, g_pins, transistors):
    p = transistors['P']
    n = transistors['N']
    
    
def cal_eol_type(end_ps, corner_ps, unused_ps, used_ps):
    eol_direction = {} #pin: sublist of [left,right,up,down]
    fail_eol_direction  = {}
    for p in end_ps:
        x,y = p
        if (x-1,y) in used_ps:
            if (x,y-1) in unused_ps and (x,y+1) in unused_ps:
                eol_direction[p] = ['up','down']
            elif (x+1,y) in unused_ps:
                eol_direction[p] = ['right']
            else:
                # eol_direction[p] = ['right']
                fail_eol_direction[p] = ['right']
            
        elif (x+1,y) in used_ps:
            if (x,y-1) in unused_ps and (x,y+1) in unused_ps:
                eol_direction[p] = ['up','down']
            elif (x-1,y) in unused_ps:
                eol_direction[p] = ['left']
            else:
                # eol_direction[p] = ['left']
                fail_eol_direction[p] = ['left']
        elif (x,y-1) in used_ps:
            if (x-1,y) in unused_ps and (x+1,y) in unused_ps:
                eol_direction[p] = ['left','right']
            elif (x,y+1) in unused_ps:
                eol_direction[p] = ['up']
            else:
                # eol_direction[p] = ['left','right']
                fail_eol_direction[p] = ['left','right']      
        elif (x,y+1) in used_ps:
            if (x-1,y) in unused_ps and (x+1,y) in unused_ps:
                eol_direction[p] = ['left','right']
            elif (x,y-1) in unused_ps:
                eol_direction[p] = ['down']
            else:
                # x_extend_pins[p] = ['left','right']
                fail_eol_direction[p] = ['left','right']           
        else:
            raise ValueError
            
    for p in corner_ps:
        x,y = p
        if (x-1,y) in used_ps and (x,y+1) in used_ps:
            if (x+1,y) in unused_ps:
                eol_direction[p] = ['right']
            elif (x,y-1) in unused_ps:
                eol_direction[p] = ['down']
            else:
                # eol_direction[p] = ['right']
                fail_eol_direction[p] = ['right']    
                
        elif (x-1,y) in used_ps and (x,y-1) in used_ps:
            if (x+1,y) in unused_ps:
                eol_direction[p] = ['right']
            elif (x,y+1) in unused_ps:
                eol_direction[p] = ['up']
            else:
                # eol_direction[p] = ['right']
                fail_eol_direction[p] = ['right']    
                
        elif (x+1,y) in used_ps and (x,y-1) in used_ps:
            if (x-1,y) in unused_ps:
                eol_direction[p] = ['left']
            elif (x,y+1) in unused_ps:
                eol_direction[p] = ['up']
            else:
                # eol_direction[p] = ['left']
                fail_eol_direction[p] = ['left']         
        elif (x+1,y) in used_ps and (x,y+1) in used_ps:
            if (x-1,y) in unused_ps:
                eol_direction[p] = ['left']
            elif (x,y-1) in unused_ps:
                eol_direction[p] = ['down']
            else:
                # x_extend_pins[p] = ['left']
                fail_eol_direction[p] = ['left']         
        else:
            raise ValueError
    
    return eol_direction, fail_eol_direction

def half(x):
    return int(0.5*x)


def visualization():
    pass