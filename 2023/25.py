"""
Part 1: Find the 3 connections to cut that creates two components.
Part 2: Get 50 stars!
"""
import math
import os
import random

from collections import defaultdict
from util import run

NUM_VERTICES_TO_CUT = 3


class Connection:
    def __init__(self, node_a_id, node_b_id):
        self.connected_node_ids = set([node_a_id, node_b_id])

    @property
    def id(self):
        return '-'.join(sorted(self.connected_node_ids))

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return self.id


class Subset:
    def __init__(self, id_, initial_node):
        self.id = id_
        self.node_ids = set([initial_node])


class Graph:
    def __init__(self, connections):
        self.connections = connections

    def karger(self):
        """
        Really cool probabilistic algorithm!
        https://en.wikipedia.org/wiki/Karger's_algorithm
        """
        all_node_ids = set()
        for connection in self.connections:
            all_node_ids |= connection.connected_node_ids

        while True:
            subset_map = {
                i: Subset(i, node_id)
                for i, node_id in enumerate(all_node_ids)
            }
            node_to_subset = {
                node_id: subset.id
                for subset in subset_map.values()
                for node_id in subset.node_ids
            }
            num_vertices = len(all_node_ids)
            connection_pool = set(self.connections)

            while num_vertices > 2:
                connection = random.choice(list(connection_pool))
                connection_pool.remove(connection)

                [node_a_id, node_b_id] = connection.connected_node_ids
                subset_a = subset_map[node_to_subset[node_a_id]]
                subset_b = subset_map[node_to_subset[node_b_id]]

                if subset_a.id == subset_b.id:
                    continue
                else:
                    # Combine subsets
                    num_vertices -= 1
                    subset_a.node_ids |= subset_b.node_ids
                    node_to_subset.update({
                        node_id: subset_a.id
                        for node_id in subset_b.node_ids
                    })

            # Calculate the edges we have left
            remaining_vertices = 0
            for connection in self.connections:
                [node_a_id, node_b_id] = connection.connected_node_ids
                if node_to_subset[node_a_id] != node_to_subset[node_b_id]:
                    remaining_vertices += 1

            if remaining_vertices == NUM_VERTICES_TO_CUT:
                subsets = defaultdict(set)
                for node_id, subset_id in node_to_subset.items():
                    subsets[subset_id].add(node_id)
                return math.prod(len(subset) for subset in subsets.values())


def part_1(lines):
    connections = []
    for line in lines:
        key, rest = line.strip().split(': ')
        for connected_node_id in rest.split(' '):
            connections.append(Connection(key, connected_node_id))
    return Graph(connections).karger()


def part_2(lines):
    return None


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)
