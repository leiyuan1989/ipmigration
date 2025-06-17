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
    
    return end_points, corner_points, isolated_pins, unused_grid_points

# 示例数据（与原代码相同）
edges = {
    'N_4': [((20, 5), (19, 5)), ((20, 5), (21, 5)), ((0, 1), (0, 0)), ((0, 1), (0, 2)),
            ((10, 5), (9, 5)), ((10, 5), (11, 5)), ((1, 2), (0, 2)), ((1, 2), (2, 2)),
            ((22, 5), (21, 5)), ((22, 5), (23, 5)), ((3, 4), (4, 4)), ((3, 4), (3, 3)),
            ((18, 5), (17, 5)), ((18, 5), (19, 5)), ((9, 5), (8, 5)), ((0, 2), (0, 3)),
            ((11, 5), (12, 5)), ((2, 2), (2, 3)), ((12, 5), (13, 5)), ((23, 5), (24, 5)),
            ((13, 5), (14, 5)), ((14, 5), (15, 5)), ((4, 4), (4, 5)), ((15, 5), (16, 5)),
            ((5, 5), (4, 5)), ((5, 5), (6, 5)), ((6, 5), (7, 5)), ((8, 5), (7, 5)),
            ((2, 3), (3, 3)), ((16, 5), (17, 5))],
    'N_5': [((12, 4), (13, 4)), ((12, 4), (12, 3)), ((23, 1), (22, 1)), ((23, 1), (24, 1)),
            ((13, 4), (14, 4)), ((14, 4), (15, 4)), ((24, 1), (24, 2)), ((4, 3), (4, 2)),
            ((15, 4), (16, 4)), ((9, 2), (8, 2)), ((9, 2), (9, 3)), ((18, 3), (19, 3)),
            ((18, 3), (18, 4)), ((21, 2), (21, 1)), ((21, 2), (21, 3)), ((19, 3), (20, 3)),
            ((20, 3), (21, 3)), ((16, 4), (17, 4)), ((17, 4), (18, 4)), ((5, 2), (4, 2)),
            ((5, 2), (6, 2)), ((6, 2), (7, 2)), ((9, 3), (9, 4)), ((22, 1), (21, 1)),
            ((10, 4), (9, 4)), ((10, 4), (11, 4)), ((11, 3), (12, 3)), ((11, 3), (11, 4)),
            ((7, 2), (8, 2))],
    'N_6': [((11, 1), (10, 1)), ((11, 1), (12, 1)), ((12, 1), (13, 1)), ((13, 1), (14, 1)),
            ((14, 1), (14, 2)), ((10, 1), (10, 2)), ((16, 2), (15, 2)), ((10, 3), (10, 2)),
            ((14, 2), (15, 2))],
    'N_7': [((17, 1), (17, 2)), ((16, 3), (15, 3)), ((16, 3), (17, 3)), ((17, 3), (17, 2)),
            ((13, 3), (14, 3)), ((13, 3), (13, 2)), ((14, 3), (15, 3)), ((17, 2), (18, 2)),
            ((18, 2), (19, 2))],
    'N_8': [((25, 0), (26, 0)), ((25, 0), (25, 1)), ((25, 3), (24, 3)), ((25, 3), (25, 2)),
            ((28, 0), (27, 0)), ((28, 0), (29, 0)), ((29, 0), (30, 0)), ((30, 0), (31, 0)),
            ((31, 0), (32, 0)), ((32, 0), (32, 1)), ((23, 2), (23, 3)), ((32, 3), (32, 2)),
            ((25, 1), (25, 2)), ((32, 1), (32, 2)), ((23, 3), (24, 3)), ((26, 0), (27, 0))],
    'N_9': [((30, 4), (31, 4)), ((30, 4), (30, 3)), ((31, 4), (32, 4)), ((32, 4), (33, 4)),
            ((33, 3), (34, 3)), ((33, 3), (33, 4)), ((28, 3), (27, 3)), ((28, 3), (29, 3)),
            ((29, 3), (30, 3)), ((30, 3), (30, 2)), ((26, 3), (27, 3))],
    'Q': [((31, 1), (31, 2)), ((31, 2), (31, 3))],
    'QN': [((35, 3), (35, 2)), ((35, 3), (35, 4)), ((35, 1), (35, 0)), ((35, 1), (35, 2))]
}

pins = {
    0: [['N_4', (0, 3, 1)], ['N_4', (0, 0, 1)]],
    1: [['CKN', (1, 3, 0)]],
    2: [],
    3: [['N_4', (3, 3, 0)]],
    4: [['N_5', (4, 3, 1)], ['N_5', (4, 2, 1)]],
    5: [],
    6: [['D', (6, 3, 0)]],
    7: [],
    8: [['N_5', (8, 2, 0)], ['N_4', (8, 5, 0)]],
    9: [],
    10: [['N_6', (10, 3, 1)], ['N_6', (10, 1, 1)]],
    11: [['N_5', (11, 3, 0)]],
    12: [],
    13: [['N_7', (13, 2, 0)]],
    14: [],
    15: [],
    16: [['N_6', (16, 2, 0)]],
    17: [['N_7', (17, 3, 1)], ['N_7', (17, 1, 1)]],
    18: [],
    19: [['N_7', (19, 2, 0)]],
    20: [],
    21: [['N_5', (21, 3, 0)]],
    22: [],
    23: [['N_8', (23, 3, 1)], ['N_8', (23, 2, 1)]],
    24: [['N_5', (24, 2, 0)], ['N_4', (24, 5, 0)]],
    25: [],
    26: [['N_9', (26, 3, 0)]],
    27: [],
    28: [],
    29: [],
    30: [['N_9', (30, 3, 1)], ['N_9', (30, 2, 1)]],
    31: [['Q', (31, 3, 1)], ['Q', (31, 1, 1)]],
    32: [['N_8', (32, 3, 0)]],
    33: [],
    34: [['N_9', (34, 3, 0)]],
    35: [['QN', (35, 4, 1)], ['QN', (35, 0, 1)]]
}

# 调用函数查找特殊点
end_points, corner_points, isolated_pins, unused_grid_points = find_special_points(edges, pins)

# 输出结果
print("端点列表(属于pin的点):")
for point in end_points:
    print(point)

print("\n直角点列表(属于pin的点):")
for point in corner_points:
    print(point)

print("\n不在任何边上的pin点:")
for point in isolated_pins:
    print(point)

print("\n网格中未被任何边经过的点:")
for point in sorted(unused_grid_points):
    print(point)