"""
Part 1:
Part 2:
"""
import math
import os
import random
import sys

from collections import defaultdict
from itertools import combinations
from util import run


class Node:
    def __init__(self, id_, connected_to):
        self.id = id_
        self.connected_to = set(connected_to)


class Connection:
    def __init__(self, node_a_id, node_b_id):
        self.connected_node_ids = sorted([node_a_id, node_b_id])

    @property
    def id(self):
        return '-'.join(self.connected_node_ids)

    def __repr__(self):
        return self.id


class Subset:
    def __init__(self, id_, parent_id):
        self.id = id_
        self.node_ids = set([parent_id])
        self.parent_id = parent_id
        self.rank = 0


class Graph:
    """ Implements Tarjan's bridge-finding algorithm."""
    def __init__(self, node_map):
        self.node_map = node_map
        self.time = 0
        self.removed_connections = set()

    def set_removed_connections(self, removed_connections):
        self.removed_connections = set()
        for connection in removed_connections:
            self.removed_connections.add((
                connection.connected_node_ids[0],
                connection.connected_node_ids[1],
            ))
            self.removed_connections.add((
                connection.connected_node_ids[1],
                connection.connected_node_ids[0],
            ))

    def find_bridge(self):
        self.time = 0
        visited = set()
        low = {node_id: math.inf for node_id in self.node_map.keys()}
        time_discovered = {node_id: math.inf for node_id in self.node_map.keys()}

        # Find if the remaining graph has a bridge. If so, we found our last wire!
        for node_id in self.node_map.keys():
            if node_id not in visited:
                bridge = self.tarjan(
                    node_id,
                    None,
                    visited,
                    low,
                    time_discovered,
                )
                if bridge:
                    return bridge
        return None

    def tarjan(
        self,
        curr_node_id,
        parent_node_id,
        visited,
        low,
        time_discovered,
    ):
        visited.add(curr_node_id)
        time_discovered[curr_node_id] = self.time
        low[curr_node_id] = self.time
        self.time += 1

        for connected_node_id in self.node_map[curr_node_id].connected_to:
            if (curr_node_id, connected_node_id) in self.removed_connections:
                # Pretend these aren't connected!
                continue

            if connected_node_id == parent_node_id:
                continue

            if connected_node_id in visited:
                low[curr_node_id] = min(low[curr_node_id], time_discovered[connected_node_id])
            else:
                self.tarjan(connected_node_id, curr_node_id, visited, low, time_discovered)
                low[curr_node_id] = min(low[curr_node_id], low[connected_node_id])

                if low[connected_node_id] > time_discovered[curr_node_id]:
                    return Connection(curr_node_id, connected_node_id)

    def karger(self, connection_map):
        runs = 0
        while True:
            runs += 1
            # print('Run', runs)
            subset_map = {
                i: Subset(i, node_id)
                for i, node_id in enumerate(self.node_map.keys())
            }
            node_to_subset = {
                node_id: subset.id
                for subset in subset_map.values()
                for node_id in subset.node_ids
            }
            num_vertices = len(self.node_map)
            connection_pool = set(connection_map.keys())

            while num_vertices > 2:
                connection_id = random.choice(list(connection_pool))
                connection_pool.remove(connection_id)

                [node_a_id, node_b_id] = connection_map[connection_id].connected_node_ids
                subset_a = subset_map[node_to_subset[node_a_id]]
                subset_b = subset_map[node_to_subset[node_b_id]]

                if subset_a.id == subset_b.id:
                    # print('Subsets match', subset_a.id, subset_b.id, num_vertices)
                    continue
                else:
                    # print('Merging!', subset_a.id, subset_b.id, num_vertices)
                    num_vertices -= 1

                    # Combine subsets
                    if subset_a.rank >= subset_b.rank:
                        subset_a.node_ids |= subset_b.node_ids
                        for node_id in subset_b.node_ids:
                            node_to_subset[node_id] = subset_a.id

                        if subset_a.rank == subset_b.rank:
                            subset_a.rank += 1
                    else:
                        subset_b.node_ids |= subset_a.node_ids
                        for node_id in subset_a.node_ids:
                            node_to_subset[node_id] = subset_b.id

            cut_edges = 0
            for connection in connection_map.values():
                [node_a_id, node_b_id] = connection.connected_node_ids
                if node_to_subset[node_a_id] != node_to_subset[node_b_id]:
                    cut_edges += 1

            if cut_edges == 3:
                subsets = defaultdict(set)
                for node_id, subset_id in node_to_subset.items():
                    subsets[subset_id].add(node_id)

                prod = 1
                for subset in subsets.values():
                    # print(len(subset), subset)
                    prod *= len(subset)
                return prod

    def dfs(self, curr_node_id, visited):
        visited.add(curr_node_id)
        for connected_node_id in self.node_map[curr_node_id].connected_to:
            if (curr_node_id, connected_node_id) in self.removed_connections:
                # Pretend these aren't connected!
                continue
            if connected_node_id in visited:
                continue
            self.dfs(connected_node_id, visited)

    def get_components(self):
        self.time = 0
        visited = set()
        last_visited_set = set()
        components = []

        # Find if the remaining graph has a bridge. If so, we found our last wire!
        for node_id in self.node_map.keys():
            if node_id not in visited:
                self.dfs(node_id, visited)
                components.append(set(visited - last_visited_set))
                last_visited_set = set(visited)
        return components


def part_1(lines):
    node_map = {}
    connection_map = {}
    for line in lines:
        line = line.strip()
        line.split(': ')
        key, rest = line.split(': ')
        connected_to = rest.split(' ')
        node_map[key] = Node(key, connected_to)

        for connected_node_id in connected_to:
            c = Connection(key, connected_node_id)
            connection_map[c.id] = c
            if connected_node_id not in node_map:
                node_map[connected_node_id] = Node(connected_node_id, [key])

    for node in node_map.values():
        for connected_node_id in node.connected_to:
            node_map[connected_node_id].connected_to.add(node.id)

    graph = Graph(node_map)
    # cut_two_combos = list(combinations(connection_map.values(), 2))
    # for i, (connection_a, connection_b) in enumerate(cut_two_combos):
    #     if i % 100 == 0:
    #         print('Processing %d/%d...' % (i, len(cut_two_combos)))
    #     graph.set_removed_connections([connection_a, connection_b])
    #     bridge = graph.find_bridge()
    #     if bridge is not None:
    #         connections_to_cut = (connection_a, connection_b, bridge)
    #         graph.set_removed_connections(connections_to_cut)
    #         components = graph.get_components()

    #         if len(components) != 2:
    #             print('Wrong number of components, continuing the search...')

    #         else:
    #             for component in components:
    #                 print(len(component), component)
    #             print('Cutting:', connections_to_cut)
    #             return math.prod(len(components) for components in components)

    return graph.karger(connection_map)


def part_2(lines):
    return part_1(lines)


if __name__ == '__main__':
    sys.setrecursionlimit(10000)
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)
