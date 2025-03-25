import matplotlib.pyplot as plt
import networkx as nx
from heapq import heappop
from collections import defaultdict

def create_grid_graph(grid_size):
    """创建网格图，每个节点连接四个邻居"""
    G = nx.grid_2d_graph(grid_size, grid_size)
    return G

def heuristic(a, b):
    """A*启发式函数（曼哈顿距离）"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_occupied_nodes(paths, grid_size):
    """获取被占用的节点（包含路径节点及其周围区域）"""
    occupied = set()
    for path in paths:
        for (x, y) in path:
            # 添加路径节点本身
            occupied.add((x, y))
            # 添加周围相邻节点（上下左右）
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < grid_size and 0 <= ny < grid_size:
                    occupied.add((nx, ny))
    return occupied

def find_path(start, end, occupied, grid_size):
    """使用networkx的A*算法寻找路径"""
    G = create_grid_graph(grid_size)
    # 移除被占用的节点
    G.remove_nodes_from(occupied)
    try:
        return nx.astar_path(G, start, end, heuristic=heuristic)
    except nx.NetworkXNoPath:
        return None

def rip_reroute(terminal_sets, grid_size=10, max_iter=100):
    """改进的rip-up and reroute算法"""
    paths = []
    # 生成初始路径（考虑周围间距）
    for start, end in terminal_sets:
        occupied = get_occupied_nodes(paths, grid_size)
        path = find_path(start, end, occupied, grid_size)
        if not path:
            print(f"初始路径生成失败：{start} -> {end}")
            return None
        paths.append(path)
    
    # 迭代优化
    for _ in range(max_iter):
        # 构建占用图（节点+周边）
        all_occupied = get_occupied_nodes(paths, grid_size)
        
        # 检测冲突
        conflict_found = False
        for i in range(len(paths)):
            # 检查当前路径是否与其他路径冲突
            for node in paths[i]:
                if node in all_occupied - get_occupied_nodes([paths[i]], grid_size):
                    conflict_found = True
                    break
            if conflict_found:
                break
        
        if not conflict_found:
            break
        
        # 重新路由第一条冲突路径
        old_path = paths.pop(i)
        occupied = get_occupied_nodes(paths, grid_size)
        new_path = find_path(terminal_sets[i][0], terminal_sets[i][1], occupied, grid_size)
        
        if new_path:
            paths.insert(i, new_path)
        else:
            paths.insert(i, old_path)  # 回退旧路径
    
    # 最终冲突检查
    final_occupied = set()
    for path in paths:
        path_nodes = set(path)
        if len(final_occupied & path_nodes) > 0:
            return None  # 存在未解决的冲突
        final_occupied.update(path_nodes)
        final_occupied.update([(x+dx, y+dy) for (x, y) in path 
                              for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]
                              if 0 <= x+dx < grid_size and 0 <= y+dy < grid_size])
    return paths

def visualize(grid_size, paths, terminals):
    """增强的可视化函数"""
    plt.figure(figsize=(10, 10))
    ax = plt.gca()
    
    # 绘制网格
    for x in range(grid_size+1):
        ax.plot([x, x], [0, grid_size], 'k-', alpha=0.2)
    for y in range(grid_size+1):
        ax.plot([0, grid_size], [y, y], 'k-', alpha=0.2)
    
    # 绘制路径
    colors = plt.cm.tab10.colors
    for idx, path in enumerate(paths):
        color = colors[idx % len(colors)]
        xs = [x+0.5 for (x, y) in path]
        ys = [y+0.5 for (x, y) in path]
        ax.plot(xs, ys, linewidth=2, marker='o', markersize=6, color=color)
        # 绘制路径缓冲区（显示安全间距）
        for (x, y) in path:
            rect = plt.Rectangle((x, y), 1, 1, color=color, alpha=0.1)
            ax.add_patch(rect)
    
    # 标记终端点
    for i, (start, end) in enumerate(terminals):
        ax.plot(start[0]+0.5, start[1]+0.5, 's', markersize=15, 
               markeredgewidth=2, markerfacecolor='lime', markeredgecolor='black')
        ax.plot(end[0]+0.5, end[1]+0.5, 'D', markersize=15,
               markeredgewidth=2, markerfacecolor='red', markeredgecolor='black')
    
    ax.set_xlim(0, grid_size)
    ax.set_ylim(grid_size, 0)
    ax.set_xticks(range(grid_size+1))
    ax.set_yticks(range(grid_size+1))
    ax.set_title("安全间距路径规划结果", fontsize=14)
    plt.tight_layout()
    plt.show()

# 测试用例
if __name__ == "__main__":
    grid_size = 10
    terminal_sets = [
        ((0, 0), (9, 9)),    # 对角线1
        ((0, 9), (9, 0)),    # 对角线2
        ((2, 2), (7, 7)),    # 平行路径
        ((3, 6), (6, 3)),    # 交叉测试
    ]
    
    final_paths = rip_reroute(terminal_sets, grid_size=grid_size)
    
    if final_paths:
        print("成功找到所有路径")
        visualize(grid_size, final_paths, terminal_sets)
    else:
        print("无法找到无冲突路径")