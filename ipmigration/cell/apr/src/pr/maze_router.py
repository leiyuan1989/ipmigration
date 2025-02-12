# -*- coding: utf-8 -*-
"""

@author: leiyuan
"""

from typing import Dict, Iterable, Mapping, TypeVar, AbstractSet, Any, List
from itertools import product, tee, count
from heapq import heappush, heappop
import networkx as nx


class SignalRouter:
    def __init__(self, ):
        pass
    
    

    def route(self, G: nx.Graph,
              terminals,
              node_cost_fn,
              edge_cost_fn
              ) -> nx.Graph:
        pass
    
    
def all_max(args: Iterable, key = None) -> List:
    """ Find all global maxima in `args`.
    :param args
    :param key: Key function.
    :return: List of maxima.
    """

    if key is None:
        def key(x):
            return x

    maxima = []
    max_key = None

    for x in args:
        val = key(x)
        if max_key is None or val > max_key:
            maxima.clear()
            max_key = val
        if val == max_key:
            maxima.append(x)

    return maxima


def all_min(args: Iterable, key = None) -> List:
    """ Find all global minima in `args`.
    :param args:
    :param key: Key function.
    :return: List of minima.
    """

    if key is None:
        def key(x):
            return x

    minima = []
    min_key = None

    for x in args:
        val = key(x)
        if min_key is None or val < min_key:
            minima.clear()
            min_key = val
        if val == min_key:
            minima.append(x)

    return minima


class DijkstraRouter(SignalRouter):

    def __init__(self):
        pass

    def route(self, G: nx.Graph,
              terminals: List[Any],
              node_cost_fn,
              edge_cost_fn
              ) -> nx.Graph:
        return spanning_subtree(
            G,
            terminals,
            node_cost_fn,
            edge_cost_fn,
        )
    
    
def spanning_subtree(
        G: nx.Graph,
        terminals: List,
        node_cost_fn,
        edge_cost_fn,
        heuristic_fn=None,
) -> nx.Graph:
    """ Creates a spanning subtree connecting all terminals.
    Assumes a connected graph G.

    Based on PathFinder and Prim's algorithm.

    Parameters
    ----------
    G: nx.Graph
            Routing graph
    terminal: List of terminal nodes
            Terminal nodes of signals to be connected.
    node_cost_fn: node -> number
    edge_cost_fn  node, node -> number
    heuristic_fn: function source, target -> number
            See `dijkstra_traverse` function
    """

    S = nx.Graph()
    #
    # center, center_dist = absolute_1_center(
    #     G,
    #     terminals,
    #     node_cost_fn,
    #     edge_cost_fn
    # )
    #
    # source = center

    sinks = set(terminals)
    if len(terminals) > 0:
        source = terminals[0]
        sinks -= {source}
        S.add_node(source)

    while sinks:
        # Initialize priority queue with current routing tree at cost 0.

        sources = set(S.nodes)

        path = shortest_path(G,
                             sources,
                             sinks,
                             node_cost_fn,
                             edge_cost_fn,
                             heuristic_fn=heuristic_fn
                             )

        nx.add_path(S, path)
        end = path[-1]
        sinks.remove(end)

    if len(S) > 0:
        assert nx.is_tree(S)
    return S

def shortest_path(
        G,
        sources,
        terminals,
        node_cost_fn,
        edge_cost_fn,
        heuristic_fn=None
):
    """ Finds the shortest path from the source to one of the terminals.

    Based on PathFinder and Prim's algorithm.

    Parameters
    ----------
    sources: Nodes to start the search from.
    terminals: Destinations.
    """
    sinks = None
    if terminals:
        sinks = set(terminals)

    if heuristic_fn is None:
        multi_target_heuristic = None
    else:
        if terminals:
            def multi_target_heuristic(source):
                return min((heuristic_fn(source, t) for t in terminals))
        else:
            def multi_target_heuristic(source):
                return 0

    closest_terminal = []

    def node_handler_fn(n):
        if sinks:
            # Continue as long as n is not a sink.
            if n in sinks:
                closest_terminal.append(n)
                return False
            return True
        else:
            return True

    distance_map = dijkstra_traverse(
        G,
        sources,
        node_cost_fn,
        edge_cost_fn,
        node_handler_fn,
        heuristic_fn=multi_target_heuristic
    )

    # Find path from closest terminal to a sink.
    assert len(closest_terminal) == 1
    closest_terminal = closest_terminal[0]
    assert closest_terminal in sinks

    result = trace_back(G, distance_map, closest_terminal, sources)

    return result


def dijkstra_traverse(
        G,
        sources,
        node_cost_fn,
        edge_cost_fn,
        node_handler_fn,
        heuristic_fn=None
) -> Dict[Any, float]:
    """ Create a distance map from all nodes to the source.
    Nodes are visited in increasing distance order and passed to `node_handler_fn`. The search is continued
    as long as `node_handler_fn` returns `True` and there are unvisited nodes left.

    Parameters
    ----------
    :param sources: Nodes to start the search from.
    :param node_cost_fn: Node cost function. node -> cost
    :param edge_cost_fn: Edge cost function. (node, node) -> cost
    :param node_handler_fn: A function Node -> Bool
            Each node will be passed to this function in increasing distance order. The search will be aborted if the handler returns `False`.

    :param heuristic_fn: Source -> Estimated cost to reach target.
            Heuristic function to estimate the cost from a node to a target.
            Shortest paths are found as long as the heuristic does not overestimate costs.

    :return: Returns a dictionary like {node: distance to source, ...}.
    """

    if heuristic_fn is None:
        def h(n):
            return 0

        heuristic_fn = h

    class PQElement:
        def __init__(self, priority, value):
            self.priority = priority
            self.value = value

        def __cmp__(self, other):
            if self.priority < other.priority:
                return -1
            elif self.priority > other.priority:
                return 1
            return 0

        def __lt__(self, other):
            return self.priority < other.priority

        def __gt__(self, other):
            return self.priority > other.priority

        def as_tuple(self):
            return self.priority, self.value

    # Initialize priority queue with source node at cost 0.
    pq = [PQElement(node_cost_fn(n), n) for n in sources]

    c = count()
    result = dict()
    # result = {n: node_cost_fn(n) for n in sources}
    visited = set()
    enqueued = dict()
    n_nodes = len(G)
    # Storage for trace.
    prev_node = dict()
    while pq:
        # Continue search from lowest-cost node.
        cost_m, m = heappop(pq).as_tuple()

        if m in visited:
            continue
        visited.add(m)

        result[m] = cost_m

        if node_handler_fn is not None:
            if not node_handler_fn(m):
                break

        if len(visited) == n_nodes:
            break

        # Loop over fanout nodes
        for edge in G.edges(m, data=True):
            _, n, data = edge

            if n in visited:
                continue

            effective_cost = edge_cost_fn((m, n)) + node_cost_fn(n)

            # Get previous node if any.
            previous = prev_node.get(n, None)

            cost_n = cost_m + effective_cost

            # old_cost_h = enqueued.get(n, None)
            # if old_cost_h is not None:
            #     # h was already computed, no need to recompute it again.
            #     cost_old, h = old_cost_h
            #
            #     if cost_old <= cost_n:
            #         # We already have a better candidate.
            #         continue
            # else:
            #     h = heuristic_fn(n)

            h = heuristic_fn(n)
            heappush(pq, PQElement(cost_n + h, n))
            # Cache h
            # enqueued[n] = cost_n, h

            # Remember node if it is augmenting the path.
            if previous is not None:
                prev_node[n] = min(previous, (cost_n, m), key=lambda x: x[0])
            else:
                prev_node[n] = (cost_n, m)

    return result

N = TypeVar('N')
def trace_back(G: nx.Graph, distance_map: Mapping[N, int], source: N, targets: AbstractSet[N]):
    """ Find the shortest path from `source` to one of the targets
    by tracing back based on a distance map.

    Parameters
    ----------
    G: nx.Graph
    distance_map: Distance to the source.
    source: Start node.
    targets: End nodes.
    """

    targets = set(targets)

    current = source

    trace = [current]

    while current not in targets:
        neighbors = G.neighbors(current)
        neighbors = filter(lambda n: n in distance_map, neighbors)

        # neighbors = sorted(neighbors)
        closest_nodes = all_min(neighbors, key=lambda n: distance_map[n])
        # TODO: Which node is next if there are multiple closest nodes?
        next_node = closest_nodes[0]
        trace.append(next_node)
        current = next_node

    trace.reverse()

    return trace



if __name__ == "__main__":
    """
    Create a routing tree for a single on a mesh graph signal and plot it.
    :return:
    """
    import matplotlib.pyplot as plt

    # Construct the graph.
    G = nx.Graph()

    num_x = 10
    num_y = 10
    x = range(0, num_x)
    y = range(0, num_y)

    # Store drawing positions of vertices. For plotting only.
    pos = {}

    # Construct mesh
    for name, (x, y) in enumerate(product(x, y)):
        G.add_node((x, y))
        pos[(x, y)] = (x, y)

        w = 1

        if x < num_x - 1 and not (1 <= y < 5 and x == 4):
            G.add_edge((x, y), (x + 1, y), weight=w, orientation='h')

        if y < num_y - 1:
            G.add_edge((x, y), (x, y + 1), weight=w, orientation='v')

    G.add_edge((8, 0), (9, 0), multi_via=2)
    G.remove_node((1,3))
    # Plot the mesh.
    nx.draw_networkx(G, pos=pos, node_color='gray', node_size=8, edge_color='lightgray')

    # This are the terminals to be connected.
    terminals = [(0, 0), (8, 5), (7, 7), (6, 3), (8, 0), (1, 8), (3, 3), (8, 4)]

    # Find the routing tree.
    router = DijkstraRouter()
    tree = router.route(G, terminals, node_cost_fn=lambda x: 1, edge_cost_fn=lambda x: 1)
    assert nx.is_tree(tree), "Routing solution should be a tree!"
    for n in terminals:
        assert n in tree, "Terminal is not in routing tree!"

    # Plot the result.

    edges = list(tree.edges)
    nx.draw_networkx_edges(G, pos, edgelist=edges, width=4, edge_color='red')

    nx.draw_networkx_nodes(G, pos, nodelist=terminals, node_size=32, node_color='black')
    # edge_labels = {(a, b): "%.2f" % data.get('weight', 0) for (a, b, data) in G.edges(data=True)}
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.draw()
    plt.show()
   