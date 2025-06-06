nets = {'N_6': [(3, 0, 0),
  (10, 0, 0),
  (0, 0, 1),
  (24, 0, 0),
  (3, 1, 0),
  (8, 1, 0),
  (0, 1, 1),
  (26, 1, 0)],
 'N_4': [(4, 0, 1), (8, 0, 0), (26, 0, 0), (4, 1, 1), (10, 1, 0), (24, 1, 0)],
 'D': [(6, 0, 0), (6, 1, 0)],
 'N_5': [(9, 0, 1), (9, 0, 1), (15, 0, 0), (9, 1, 1), (9, 1, 1), (15, 1, 0)],
 'N_7': [(12, 0, 0),
  (16, 0, 1),
  (16, 0, 1),
  (22, 0, 0),
  (12, 1, 0),
  (18, 1, 1),
  (18, 1, 1),
  (22, 1, 0)],
 'CKN': [(1, 0, 0), (1, 1, 0)],
 'N_23': [(14, 0, 1), (18, 0, 1), (18, 0, 1)],
 'N_10': [(17, 0, 0),
  (33, 0, 0),
  (37, 0, 1),
  (17, 1, 0),
  (33, 1, 0),
  (37, 1, 1)],
 'SN': [(19, 0, 0), (35, 0, 0), (19, 1, 0), (35, 1, 0)],
 'N_8': [(25, 0, 1),
  (25, 0, 1),
  (31, 0, 0),
  (25, 1, 1),
  (25, 1, 1),
  (31, 1, 0)],
 'N_9': [(28, 0, 0),
  (32, 0, 1),
  (32, 0, 1),
  (45, 0, 0),
  (40, 0, 0),
  (28, 1, 0),
  (34, 1, 1),
  (34, 1, 1),
  (45, 1, 0),
  (40, 1, 0)],
 'N_21': [(34, 0, 1), (34, 0, 1), (30, 0, 1)],
 'QN': [(46, 0, 1), (46, 1, 1)],
 'RN': [(38, 0, 0), (38, 1, 0)],
 'N_11': [(41, 0, 1), (43, 0, 0), (41, 1, 1), (43, 1, 0)],
 'Q': [(42, 0, 1), (42, 1, 1)]}

max_height = 10
max_width = 46
mid_height = 5

new_nets = {}
for k,v in nets.items():
    new_v = []
    for t in v:
        if t[1] == 1:
            new_v.append((t[0],max_height-2,t[2]))
        else:
            new_v.append((t[0],1,t[2]))
    new_nets[k] = new_v






import networkx as nx
import matplotlib.pyplot as plt

def create_two_layer_grid(width, height):
    """
    创建一个两层的网格图
    
    参数:
    width (int): 网格的宽度
    height (int): 网格的高度
    
    返回:
    networkx.Graph: 生成的两层网格图
    """
    G = nx.Graph()
    
    # 添加所有节点
    for layer in [0, 1]:
        for x in range(width):
            for y in range(height):
                G.add_node((x, y, layer))
    
    # 在第1层添加相邻节点之间的边
    for x in range(width):
        for y in range(height):
            # 水平边
            if x < width - 1:
                G.add_edge((x, y, 1), (x + 1, y, 1))
            # 垂直边
            if y < height - 1:
                G.add_edge((x, y, 1), (x, y + 1, 1))
    
    # 添加两层之间的垂直连接（相同x,y坐标的节点）
    for x in range(width):
        for y in range(height):
            G.add_edge((x, y, 0), (x, y, 1))
    
    return G

def visualize_two_layer_grid(G, width, height):
    """可视化两层网格图，使两层节点具有错落感，并且图形大小根据网格尺寸调整"""
    pos = {}
    offset = 0.3  # 斜向偏移量
    
    # 为每个节点计算位置，第0层节点位于第1层节点的斜上方
    for x in range(width):
        for y in range(height):
            pos[(x, y, 1)] = (x, y)  # 第1层节点保持原始位置
            pos[(x, y, 0)] = (x + offset, y + offset)  # 第0层节点位于斜上方
    
    # 根据网格的宽高比调整图形大小，添加额外空间以容纳标签
    # aspect_ratio = (width + 1) / (height + 1)  # 增加1以考虑标签空间
    fig_width = width + 1  # 基础宽度
    fig_height = height + 1
    
    # 创建图形
    plt.figure(figsize=(fig_width, fig_height))
    
    # 绘制第0层节点（红色）
    nx.draw_networkx_nodes(
        G, pos, 
        nodelist=[(x, y, 0) for x in range(width) for y in range(height)],
        node_color='r', node_size=300, label='Layer 0'
    )
    
    # 绘制第1层节点（蓝色）
    nx.draw_networkx_nodes(
        G, pos, 
        nodelist=[(x, y, 1) for x in range(width) for y in range(height)],
        node_color='b', node_size=300, label='Layer 1'
    )
    
    # 绘制层间连接（灰色）
    inter_edges = [((x, y, 0), (x, y, 1)) for x in range(width) for y in range(height)]
    nx.draw_networkx_edges(G, pos, edgelist=inter_edges, edge_color='gray', alpha=0.5)
    
    # 绘制第1层内部连接（黑色）
    intra_edges = [e for e in G.edges() if e[0][2] == 1 and e[1][2] == 1]
    nx.draw_networkx_edges(G, pos, edgelist=intra_edges, edge_color='black')
    
    # 绘制节点标签
    labels = {(x, y, layer): f"({x},{y},{layer})" for layer in [0, 1] for x in range(width) for y in range(height)}
    nx.draw_networkx_labels(G, pos, labels, font_size=8)
    
    plt.title(f"两层网格图 (Width={width}, Height={height})")
    plt.axis('off')
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # 设置网格尺寸
    width = 50  # 尝试不同的宽度和高度
    height = 10
    
    # 创建并可视化网格图
    G = create_two_layer_grid(width, height)
    visualize_two_layer_grid(G, width, height)
    
    # 打印一些图的基本信息
    print(f"图中节点总数: {G.number_of_nodes()}")
    print(f"图中边的总数: {G.number_of_edges()}")    








import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Define the data
data = {0: {'cross': ['N_6'], 'pin': [('N_6', (0, 2, 1)), ('N_6', (0, 0, 1))]},
 1: {'cross': ['N_6', 'CKN'], 'pin': [('CKN', (1, 1, 0))]},
 2: {'cross': ['N_6'], 'pin': []},
 3: {'cross': ['N_6'], 'pin': [('N_6', (3, 1, 0))]},
 4: {'cross': ['N_6', 'N_4'], 'pin': [('N_4', (4, 0, 1)), ('N_4', (4, 2, 1))]},
 5: {'cross': ['N_6', 'N_4'], 'pin': []},
 6: {'cross': ['N_6', 'N_4', 'D'], 'pin': [('D', (6, 1, 0))]},
 7: {'cross': ['N_6', 'N_4'], 'pin': []},
 8: {'cross': ['N_6', 'N_4'], 'pin': [('N_6', (8, 2, 0)), ('N_4', (8, 0, 0))]},
 9: {'cross': ['N_6', 'N_4', 'N_5'],
  'pin': [('N_5', (9, 2, 1)), ('N_5', (9, 0, 1))]},
 10: {'cross': ['N_6', 'N_4', 'N_5'],
  'pin': [('N_6', (10, 0, 0)), ('N_4', (10, 2, 0))]},
 11: {'cross': ['N_6', 'N_4', 'N_5'], 'pin': []},
 12: {'cross': ['N_6', 'N_4', 'N_5', 'N_7'], 'pin': [('N_7', (12, 1, 0))]},
 13: {'cross': ['N_6', 'N_4', 'N_5', 'N_7'], 'pin': []},
 14: {'cross': ['N_6', 'N_4', 'N_5', 'N_7', 'N_23'],
  'pin': [('N_23', (14, 0, 1))]},
 15: {'cross': ['N_6', 'N_4', 'N_5', 'N_7', 'N_23'],
  'pin': [('N_5', (15, 1, 0))]},
 16: {'cross': ['N_6', 'N_4', 'N_7', 'N_23'], 'pin': [('N_7', (16, 0, 1))]},
 17: {'cross': ['N_6', 'N_4', 'N_7', 'N_23', 'N_10'],
  'pin': [('N_10', (17, 1, 0))]},
 18: {'cross': ['N_6', 'N_4', 'N_7', 'N_23', 'N_10'],
  'pin': [('N_7', (18, 2, 1)), ('N_23', (18, 0, 1))]},
 19: {'cross': ['N_6', 'N_4', 'N_7', 'N_10', 'SN'],
  'pin': [('SN', (19, 1, 0))]},
 20: {'cross': ['N_6', 'N_4', 'N_7', 'N_10', 'SN'], 'pin': []},
 21: {'cross': ['N_6', 'N_4', 'N_7', 'N_10', 'SN'], 'pin': []},
 22: {'cross': ['N_6', 'N_4', 'N_7', 'N_10', 'SN'],
  'pin': [('N_7', (22, 1, 0))]},
 23: {'cross': ['N_6', 'N_4', 'N_10', 'SN'], 'pin': []},
 24: {'cross': ['N_6', 'N_4', 'N_10', 'SN'],
  'pin': [('N_6', (24, 0, 0)), ('N_4', (24, 2, 0))]},
 25: {'cross': ['N_6', 'N_4', 'N_10', 'SN', 'N_8'],
  'pin': [('N_8', (25, 2, 1)), ('N_8', (25, 0, 1))]},
 26: {'cross': ['N_6', 'N_4', 'N_10', 'SN', 'N_8'],
  'pin': [('N_6', (26, 2, 0)), ('N_4', (26, 0, 0))]},
 27: {'cross': ['N_10', 'SN', 'N_8'], 'pin': []},
 28: {'cross': ['N_10', 'SN', 'N_8', 'N_9'], 'pin': [('N_9', (28, 1, 0))]},
 29: {'cross': ['N_10', 'SN', 'N_8', 'N_9'], 'pin': []},
 30: {'cross': ['N_10', 'SN', 'N_8', 'N_9', 'N_21'],
  'pin': [('N_21', (30, 0, 1))]},
 31: {'cross': ['N_10', 'SN', 'N_8', 'N_9', 'N_21'],
  'pin': [('N_8', (31, 1, 0))]},
 32: {'cross': ['N_10', 'SN', 'N_9', 'N_21'], 'pin': [('N_9', (32, 0, 1))]},
 33: {'cross': ['N_10', 'SN', 'N_9', 'N_21'], 'pin': [('N_10', (33, 1, 0))]},
 34: {'cross': ['N_10', 'SN', 'N_9', 'N_21'],
  'pin': [('N_9', (34, 2, 1)), ('N_21', (34, 0, 1))]},
 35: {'cross': ['N_10', 'SN', 'N_9'], 'pin': [('SN', (35, 1, 0))]},
 36: {'cross': ['N_10', 'N_9'], 'pin': []},
 37: {'cross': ['N_10', 'N_9'],
  'pin': [('N_10', (37, 2, 1)), ('N_10', (37, 0, 1))]},
 38: {'cross': ['N_9', 'RN'], 'pin': [('RN', (38, 1, 0))]},
 39: {'cross': ['N_9'], 'pin': []},
 40: {'cross': ['N_9'], 'pin': [('N_9', (40, 1, 0))]},
 41: {'cross': ['N_9', 'N_11'],
  'pin': [('N_11', (41, 2, 1)), ('N_11', (41, 0, 1))]},
 42: {'cross': ['N_9', 'N_11', 'Q'],
  'pin': [('Q', (42, 2, 1)), ('Q', (42, 0, 1))]},
 43: {'cross': ['N_9', 'N_11'], 'pin': [('N_11', (43, 1, 0))]},
 44: {'cross': ['N_9'], 'pin': []},
 45: {'cross': ['N_9'], 'pin': [('N_9', (45, 1, 0))]},
 46: {'cross': ['QN'], 'pin': [('QN', (46, 2, 1)), ('QN', (46, 0, 1))]}}

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def visualize_pins(data):
    """
    可视化数据中的引脚信息
    
    参数:
    data (dict): 包含引脚信息的数据结构
    
    返回:
    fig, ax: matplotlib的图形和轴对象
    """
    # 提取引脚数据
    filtered_pins1 = []  # 存储第三元素为0的引脚
    filtered_pins2 = []  # 存储第三元素为1的引脚
    
    for key, value in data.items():
        for pin in value['pin']:
            if pin[1][2] == 0:  # 检查第三个元素是否为0
                filtered_pins1.append(pin)
            else:
                filtered_pins2.append(pin)
    
    # 创建散点图
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # 绘制第三元素为0的引脚(蓝色)
    x1 = [pin[1][0] for pin in filtered_pins1]
    y1 = [pin[1][1] for pin in filtered_pins1]
    ax.scatter(x1, y1, color='blue', marker='o', s=100, label='Poly Pins')
    
    # 为蓝色点添加标签
    for i, pin in enumerate(filtered_pins1):
        ax.annotate(pin[0],  # 标签文本
                    (x1[i], y1[i]),  # 标签位置
                    textcoords="offset points",  # 文本坐标相对于点的位置
                    xytext=(0, 10),  # 偏移量
                    ha='center')  # 水平对齐方式
    
    # 绘制第三元素为1的引脚(红色)
    x2 = [pin[1][0] for pin in filtered_pins2]
    y2 = [pin[1][1] for pin in filtered_pins2]
    ax.scatter(x2, y2, color='red', marker='o', s=100, label='M1 Pins')
    
    # 为红色点添加标签
    for i, pin in enumerate(filtered_pins2):
        ax.annotate(pin[0],  # 标签文本
                    (x2[i], y2[i]),  # 标签位置
                    textcoords="offset points",  # 文本坐标相对于点的位置
                    xytext=(0, 10),  # 偏移量
                    ha='center')  # 水平对齐方式
    
    # 添加网格
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # 设置坐标轴标签和标题
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    ax.set_title('Visualization of Pins')
    
    # 设置坐标轴范围
    max_x = max(x1 + x2) if x1 + x2 else 0
    ax.set_xlim(-1, max_x + 1)
    ax.set_ylim(-1, 3)  # 设置y轴范围为0-2，显示所有可能的y值
    
    # 添加参考线
    ax.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
    ax.axhline(y=1, color='gray', linestyle='-', alpha=0.3)
    ax.axhline(y=2, color='gray', linestyle='-', alpha=0.3)
    
    # 添加图例
    ax.legend()
    
    plt.tight_layout()
    return fig, ax

# 使用示例
if __name__ == "__main__":
    # 这里使用您提供的数据

    fig, ax = visualize_pins(data)
    plt.show()  # 显示图形
