from collections import OrderedDict

def split_dict_by_increment(original_dict, increment=5):
    """
    按递增间隔拆分OrderedDict
    
    参数:
    original_dict - 原始OrderedDict
    increment - 每次增加的间隔
    
    返回:
    拆分后的字典列表
    """
    result = []
    keys = list(original_dict.keys())
    
    # 计算最大key值
    max_key = max(keys) if keys else 0
    
    # 生成间隔列表
    intervals = [i for i in range(increment, max_key + 1, increment)]
    
    # 如果最大值不是间隔的倍数，添加一个额外的间隔
    if max_key % increment != 0:
        intervals.append(max_key)
    
    # 为每个间隔创建一个新字典
    for interval in intervals:
        new_dict = OrderedDict()
        for key in keys:
            if key <= interval:
                new_dict[key] = original_dict[key]
        result.append(new_dict)
    
    return result

# 示例使用
original_dict = OrderedDict([
    (0, [['N_4', (0, 1, 1)], ['N_4', (0, 4, 1)]]),
    (1, [['CKN', (1, 2.5, 0)]]),
    (2, []),
    (3, [['N_4', (3, 2.5, 0)]]),
    (4, [['N_5', (4, 1, 1)], ['N_5', (4, 4, 1)]]),
    (5, []),
    (6, [['D', (6, 2.5, 0)]]),
    (7, []),
    (8, [['N_5', (8, 2, 0)], ['N_4', (8, 5, 0)]]),
    (9, [['N_6', (9, 1, 1)], ['N_6', (9, 4, 1)]]),
    (10, [['N_5', (10, 3, 0)]])
])

# 按每次增加5个键拆分
split_dicts = split_dict_by_increment(original_dict, increment=5)

# 打印结果
for i, d in enumerate(split_dicts):
    print(f"拆分字典 {i+1} (键范围 1-{list(d.keys())[-1]}):")
    for key, value in d.items():
        print(f"  {key}: {value}")
    print()