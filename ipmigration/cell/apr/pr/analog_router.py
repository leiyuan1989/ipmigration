import networkx as nx
import matplotlib.pyplot as plt
import random
from itertools import permutations



class AnalogRouter1:
    def __init__(self, pattern, graph, terminal_sets, M2=False):
        self.pattern = pattern
        self.graph = graph
        self.terminal_sets = terminal_sets
        self.M2 = M2

    def run(self,occupy_nodes=[]):
        terminal_sets = self.terminal_sets
        paths,new_terminal_sets  = self.find_non_overlapping_paths(self.graph,terminal_sets,occupy_nodes)
        if paths:
            return 1, paths,new_terminal_sets
        else:
            if self.M2:
                #delete any one
                #TODO maybe expand to delete n elements
                new_set = [(terminal_sets[:i] + terminal_sets[i+1:], terminal_sets[i]) for i in range(len(terminal_sets))]
                paths_l = []
                new_terminal_sets_l = []
                result = False
                for terminal_sets, net, in new_set:    
                    paths,new_terminal_sets  = self.find_non_overlapping_paths(self.graph,terminal_sets,net)
                    paths_l.append(paths)
                    new_terminal_sets_l.append((new_terminal_sets,net))
                    if paths:
                        result = True
                if result:
                    return 2, paths_l,new_terminal_sets_l

        return 0, None, None

    def find_subgraph_with_nodes(self, G, nodes):
        # 检查图是否为空
        if G.number_of_nodes() == 0:
            return "错误: 输入的图为空。"
    
        # 找出图的所有连通分量
        connected_components = list(nx.connected_components(G))
    
        # 遍历每个连通分量
        for component in connected_components:
            component_subgraph = G.subgraph(component)
            # 检查当前连通分量是否包含所有指定的节点
            if all(node in component_subgraph for node in nodes):
                return component_subgraph
    
        return None


    def find_non_overlapping_paths(self, G, terminal_sets, occupy_nodes):
        all_permutations = list(permutations(terminal_sets))
        try_num=0
        total_num = len(all_permutations)
        for terminal_order in all_permutations:
            print('Try %d/%d'%(try_num,total_num))
            if try_num>50:
                break #for test
            
            try_num+=1
            all_paths = []
            used_edges = set()
            used_nodes = set(occupy_nodes)
            # print(used_nodes)
            for terminals in terminal_order:

                subgraph = G.copy()
                # delete other nodes
                other_nodes = []
                for t in terminal_order:
                    for node in list(t):
                        if not(node in list(terminals)):

                            other_nodes.append(node)
                subgraph.remove_nodes_from(other_nodes)
                
                # 移除已使用的边和节点                
                subgraph.remove_edges_from(used_edges)
                subgraph.remove_nodes_from(used_nodes)
                # print('abc',len(subgraph.nodes),terminals)
                # print('ccc',subgraph.nodes)
                subgraph = self.find_subgraph_with_nodes(subgraph, terminals)
                
                # steiner_tree = nx.algorithms.approximation.steiner_tree(subgraph, terminals, method='kou')
                try:
                    if subgraph:
                        steiner_tree = nx.algorithms.approximation.steiner_tree(subgraph, terminals, method='kou')
                        all_paths.append(steiner_tree)
                        # 更新已使用的边和节点
                        used_edges.update(steiner_tree.edges())
                        used_nodes.update(steiner_tree.nodes())
                    else:
                        # print(f"Cannot find sub-graph for order:{terminal_order} ")
                        all_paths = None
                        break
                except nx.NetworkXError:
                    # print(f"Cannot find path for order: {terminal_order}")
                    all_paths = None
                    break
            if all_paths is not None:
                print('--------success!!!')
                return all_paths,terminal_order

    # [lst[:i] + lst[i+1:] for i in range(len(lst))]
# 

        return None,None

if __name__ == "__main__":
    # 创建一个 10x10 的网格图
    G = nx.grid_2d_graph(10, 10)
    
    # 示例终端点集
    terminal_sets = [
        {(1, 1), (3, 3), (3, 8)},
        {(2, 2), (4, 4), (2, 5),(7,4),(7,2)},
        {(0, 0), (5, 5), (7, 7)},
        {(4,3), (6, 6), (8, 8)}
    ]
    # 不能成功例子
    # terminal_sets = [
    #     {(1, 1), (3, 3), (3, 9),(6,2)},
    #     {(2, 2), (4, 4), (2, 5),(7,4),(7,2)},
    #     {(0, 0), (5, 5), (7, 7)},
    #     {(4,3), (6, 6), (8, 8)}
    # ]    
    
    used_nodes = [(5,1)]
    # used_nodes = []
    
    
    
    
    # 计算不交叉不接触的路径
    router = AnalogRouter1(0, G, terminal_sets)
    result, paths,terminal_sets = router.run(used_nodes)
    
    if result==1:
        # 可视化部分
        plt.figure(figsize=(12, 12))
        pos = {node: node for node in G.nodes()}
        nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=200)
        nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=0.3)
    
        # 定义颜色列表
        colors = ['red', 'green', 'blue', 'yellow', 'purple', 'orange', 'cyan', 'magenta']
        for i, (path, terminals) in enumerate(zip(paths, terminal_sets)):
            color = colors[i % len(colors)]
            if path is not None:
                # 绘制路径，使用指定颜色
                nx.draw_networkx_edges(G, pos, edgelist=path.edges(), edge_color=color, width=2)
            # 绘制终端点集，使用和路径相同的颜色
            nx.draw_networkx_nodes(G, pos, nodelist=list(terminals), node_color=color, node_size=300)
    
        # 绘制节点标签
        nx.draw_networkx_labels(G, pos, font_size=8)
        plt.title('Non - overlapping paths in the graph')
        plt.axis('off')
        plt.show()
        print('success!')
    else:
        if result == 2:
            print(terminal_sets )
        else:
            print("尝试了所有顺序，仍无法为所有终端点集找到路径。")
    