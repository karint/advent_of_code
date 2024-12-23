"""
Part 1:
Part 2:
"""
import os

from collections import defaultdict
from util import run


class Graph(object):
    def __init__(self):
        self.nodes = {}

    def add_node(self, node):
        self.nodes[node.id] = node


class Node(object):
    def __init__(self, id_):
        self.id = id_
        self.neighbor_ids = set()

    def add_neighbor(self, neighbor_id):
        self.neighbor_ids.add(neighbor_id)


def part_1(lines):
    m = defaultdict(set)
    for line in lines:
        line = line.strip()
        id1, id2 = line.split('-')
        m[id1].add(id2)
        m[id2].add(id1)

    count = 0
    sets = set()
    for id1, connected in m.items():
        # id1 and id2 are connected
        for id2 in connected:
            # id2 and id3 are connected
            for id3 in m[id2]:
                if (
                    id3 in m[id1] and
                    id1 != id2 and
                    id1 != id3 and (
                        id1.startswith('t') or
                        id2.startswith('t') or
                        id3.startswith('t')
                    )
                ):
                    s = [id1, id2, id3]
                    s.sort()
                    sets.add(tuple(s))
    return len(sets)


def part_2(lines):
    g = Graph()
    for line in lines:
        line = line.strip()
        id1, id2 = line.split('-')

        if id1 not in g.nodes:
            n1 = Node(id1)
            g.add_node(n1)
        else:
            n1 = g.nodes[id1]

        if id2 not in g.nodes:
            n2 = Node(id2)
            g.add_node(n2)
        else:
            n2 = g.nodes[id2]

        n1.add_neighbor(id2)
        n2.add_neighbor(id1)

    node_map = g.nodes
    party_map = {}
    for node in g.nodes.values():
        party_ids = set([node.id])
        shared_neighbor_ids = node.neighbor_ids

        while shared_neighbor_ids:
            neighbor_id = next(iter(shared_neighbor_ids - party_ids))
            if neighbor_id not in party_ids:
                party_ids.add(neighbor_id)
                shared_neighbor_ids &= node_map[neighbor_id].neighbor_ids
                party_map[tuple(sorted(party_ids))] = set(shared_neighbor_ids)

    biggest_party = sorted(party_map.keys(), key=lambda tup: len(tup), reverse=True)[0]

    return ','.join(sorted(biggest_party))


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)
