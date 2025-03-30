import networkx as nx
import matplotlib.pyplot as plt
import random
import matplotlib.patches as patches


def find_paths_with_square_constraints(square_positions, net_assignments, square_size, min_line_spacing):
    # 创建一个图，节点为正方形的中心
    G = nx.Graph()
    for net in set(net_assignments.values()):
        nodes_in_net = [pos for pos, n in net_assignments.items() if n == net]
        for i in range(len(nodes_in_net)):
            for j in range(i + 1, len(nodes_in_net)):
                G.add_edge(nodes_in_net[i], nodes_in_net[j])

    all_paths = []
    used_edges = {}  # 存储已使用的边及其占用的宽度

    def is_edge_available(edge, width):
        """检查边是否可用，即是否满足线宽和间距要求"""
        u, v = edge
        if edge in used_edges:
            return used_edges[edge] + width + min_line_spacing <= 1
        if (v, u) in used_edges:
            return used_edges[(v, u)] + width + min_line_spacing <= 1
        return True

    def mark_edge_used(edge, width):
        """标记边已使用，并记录占用的宽度"""
        if edge in used_edges:
            used_edges[edge] += width
        elif (v, u) in used_edges:
            used_edges[(v, u)] += width
        else:
            used_edges[edge] = width

    for net in set(net_assignments.values()):
        nodes_in_net = [pos for pos, n in net_assignments.items() if n == net]
        subgraph = G.copy()
        for edge, width in used_edges.items():
            # 移除不满足间距要求的边
            subgraph.remove_edge(*edge)

        try:
            # 计算 Steiner 树
            steiner_tree = nx.algorithms.approximation.steiner_tree(subgraph, nodes_in_net, method='kou')
            path = []
            for u, v in steiner_tree.edges():
                edge = (u, v)
                if is_edge_available(edge, square_size):
                    mark_edge_used(edge, square_size)
                    path.append(edge)
                else:
                    print(f"无法使用边 {edge} 来连接 net {net}，不满足线宽或间距要求。")
                    path = None
                    break
            all_paths.append(path)
        except nx.NetworkXError:
            print(f"无法为 net {net} 找到路径。")
            all_paths.append(None)

    return all_paths


# 示例数据
# 正方形的位置
square_positions = [(1, 1), (3, 3), (3, 8), (2, 2), (4, 4), (2, 5), (0, 0), (5, 5), (7, 7), (4, 3), (6, 6), (8, 8)]
# 每个正方形所属的 net
net_assignments = {
    (1, 1): 1, (3, 3): 1, (3, 8): 1,
    (2, 2): 2, (4, 4): 2, (2, 5): 2,
    (0, 0): 3, (5, 5): 3, (7, 7): 3,
    (4, 3): 4, (6, 6): 4, (8, 8): 4
}
# 正方形的边长
square_size = 0.5
# 线间距的最小要求
min_line_spacing = 0.2

# 计算满足约束的路径
paths = find_paths_with_square_constraints(square_positions, net_assignments, square_size, min_line_spacing)

# 可视化部分
fig, ax = plt.subplots(figsize=(12, 12))
# 绘制正方形
for pos, net in net_assignments.items():
    rect = patches.Rectangle((pos[0] - square_size / 2, pos[1] - square_size / 2), square_size, square_size,
                             edgecolor='black', facecolor='none')
    ax.add_patch(rect)

# 定义颜色列表
colors = ['red', 'green', 'blue', 'yellow', 'purple', 'orange', 'cyan', 'magenta']
for i, path in enumerate(paths):
    if path is not None:
        color = colors[i % len(colors)]
        for edge in path:
            u, v = edge
            ax.plot([u[0], v[0]], [u[1], v[1]], color=color, linewidth=square_size * 10)

ax.set_xlim(-1, 10)
ax.set_ylim(-1, 10)
ax.set_aspect('equal')
plt.title('Paths connecting squares with line width and spacing constraints')
plt.show()
    