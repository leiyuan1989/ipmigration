from collections import OrderedDict

def process_x_coordinates(data):
    """处理原始数据，生成按x坐标排序的点集合"""
    x_coordinate_dict = {}
    
    # 遍历每个网络和对应的坐标点
    for net, points in data.items():
        for point in points:
            x, y, z = point
            # 如果x坐标尚未作为键存在，创建新列表
            if x not in x_coordinate_dict:
                x_coordinate_dict[x] = []
            # 添加点信息到对应x坐标的列表中
            x_coordinate_dict[x].append([net, [point]])
    
    # 对每个x坐标下的点按y值从小到大排序
    for x in x_coordinate_dict:
        x_coordinate_dict[x].sort(key=lambda p: p[1][0][1])
    
    # 确定x坐标的范围
    if x_coordinate_dict:
        min_x = min(x_coordinate_dict.keys())
        max_x = max(x_coordinate_dict.keys())
        # 确保从min_x到max_x的每个整数x都在字典中，没有pin的x对应空列表
        for x in range(min_x, max_x + 1):
            if x not in x_coordinate_dict:
                x_coordinate_dict[x] = []
    
    # 按x坐标从小到大排序字典
    sorted_x = sorted(x_coordinate_dict.keys())
    x_coordinate_dict = OrderedDict((x, x_coordinate_dict[x]) for x in sorted_x)
    
    return x_coordinate_dict

def generate_interval_dict(x_coordinate_dict):
    """根据x_coordinate_dict生成区间到网络的映射"""
    interval_dict = {}
    
    # 收集所有存在点的x坐标
    existing_x = [x for x, points in x_coordinate_dict.items() if points]
    
    # 如果没有任何点，直接返回空的interval_dict
    if not existing_x:
        return interval_dict
    
    # 为每个存在点的x值创建区间(x, x+1)
    for x in existing_x:
        interval = (x, x + 1)
        interval_dict[interval] = []
    
    # 构建网络到其x坐标范围的映射
    net_x_range = {}
    # 遍历x_coordinate_dict中的每个x坐标
    for x, points in x_coordinate_dict.items():
        # 遍历每个点的信息
        for point_info in points:
            net, point_list = point_info
            if not point_list:
                continue
            # 提取点的x坐标
            point_x = point_list[0][0]
            # 更新网络的x坐标范围
            if net not in net_x_range:
                net_x_range[net] = (point_x, point_x)
            else:
                current_min, current_max = net_x_range[net]
                net_x_range[net] = (min(current_min, point_x), max(current_max, point_x))
    
    # 确定哪些网络属于每个区间
    for interval, _ in interval_dict.items():
        x, x_plus_1 = interval
        for net, (min_x, max_x) in net_x_range.items():
            # 检查网络是否跨越区间(x, x+1)
            if min_x <= x and max_x >= x_plus_1:
                interval_dict[interval].append(net)
    
    return interval_dict

def process_data(data):
    """主函数：处理数据并返回两个字典"""
    x_coordinate_dict = process_x_coordinates(data)
    interval_dict = generate_interval_dict(x_coordinate_dict)
    return x_coordinate_dict, interval_dict

# 示例数据
data = {
    'N_6': [(26, 4, 0), (24, 1, 0), (0, 4, 1), (10, 1, 0), (3, 2.5, 0), (8, 4, 0), (0, 1, 1)],
    'N_4': [(8, 1, 0), (10, 4, 0), (4, 1, 1), (4, 4, 1), (26, 1, 0), (24, 4, 0)],
    'D': [(6, 2.5, 0)],
    'N_5': [(9, 1, 1), (9, 4, 1), (15, 2.5, 0)],
    'N_7': [(18, 4, 1), (22, 2.5, 0), (16, 1, 1), (12, 2.5, 0)],
    'CKN': [(1, 2.5, 0)],
    'N_23': [(18, 1, 1), (14, 1, 1)],
    'N_10': [(37, 1, 1), (37, 4, 1), (17, 2.5, 0), (33, 2.5, 0)],
    'SN': [(35, 2.5, 0), (19, 2.5, 0)],
    'N_8': [(25, 4, 1), (31, 2.5, 0), (25, 1, 1)],
    'N_9': [(28, 2.5, 0), (45, 2.5, 0), (40, 2.5, 0), (34, 4, 1), (32, 1, 1)],
    'N_21': [(30, 1, 1), (34, 1, 1)],
    'QN': [(46, 4, 1), (46, 1, 1)],
    'RN': [(38, 2.5, 0)],
    'N_11': [(41, 4, 1), (43, 2.5, 0), (41, 1, 1)],
    'Q': [(42, 1, 1), (42, 4, 1)]
}

# 处理数据
x_coordinate_dict, interval_dict = process_data(data)

# 输出结果
print("任务1结果：按x坐标分组的点集合（x从小到大排序，y从小到大排序）")
for x, points in x_coordinate_dict.items():
    print(f"{x}: {points}")

print("\n任务2结果：区间(x, x+1)对应的网络集合")
for interval, nets in interval_dict.items():
    print(f"{interval}: {nets}")