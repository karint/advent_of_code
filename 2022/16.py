import json
import os
import re

from collections import defaultdict
from util import run

REGEX = 'Valve (\w+) has flow rate=(\d+); (.+) to valve(\w*) (.+)'


class Valve:
    def __init__(self, id_, flow_rate, connected_valve_ids):
        self.id = id_
        self.flow_rate = flow_rate
        self.connected_valve_ids = connected_valve_ids


class Solver:
    def __init__(self, lines):
        self.valves = {}
        self.populate_valves(lines)

        self.flows = {
            valve.id: valve.flow_rate for valve in self.valves.values() if valve.flow_rate > 0
        }
        self.total_time = 26
        self.distances = defaultdict(dict)
        self.populate_distances()

    def populate_valves(self, lines):
        for line in lines:
            line = line.strip()
            matches = re.match(REGEX, line)
            valve_id, flow_rate, connected_valve_ids = [
                matches.group(1),
                matches.group(2),
                matches.group(5),
            ]
            self.valves[valve_id] = Valve(valve_id, int(flow_rate), set(connected_valve_ids.split(', ')))

    def populate_distances(self):
        all_valve_ids = set(self.valves.keys())

        def get_shortest_distance(from_valve_id, to_valve_id, already_visited):
            if from_valve_id == to_valve_id:
                return 0

            from_valve = self.valves[from_valve_id]
            if to_valve_id in from_valve.connected_valve_ids:
                self.distances[from_valve_id][to_valve_id] = 1
                return 1

            distances = []
            new_already_visited = set(already_visited)
            for new_from_valve_id in from_valve.connected_valve_ids:
                if new_from_valve_id != to_valve_id and new_from_valve_id not in already_visited:
                    new_already_visited.add(new_from_valve_id)
                    distance = get_shortest_distance(new_from_valve_id, to_valve_id, new_already_visited)
                    if distance is not None:
                        distances.append(distance)

            if not distances:
                return None

            shortest = min(distances) + 1
            return shortest

        for from_valve_id in all_valve_ids:
            for to_valve_id in all_valve_ids:
                if from_valve_id == to_valve_id or to_valve_id in self.distances[from_valve_id]:
                    continue

                distance = get_shortest_distance(from_valve_id, to_valve_id, set())
                self.distances[from_valve_id][to_valve_id] = distance
                self.distances[to_valve_id][from_valve_id] = distance

    def get_total_time_needed(self, order):
        from_valve_id = order[0]
        total_time_needed = 0
        for to_valve_id in order[1:]:
            # Need one minute per path to travel
            total_time_needed += self.distances[from_valve_id][to_valve_id]
            from_valve_id = to_valve_id

            # 1 minute to open
            total_time_needed += 1

        return total_time_needed

    def calculate_pressure_released(self, order):
        curr_valve_id = order[0]
        minutes_left = self.total_time
        pressure_released = 0
        current_flow = 0

        for to_valve_id in order[1:]:
            distance = self.distances[curr_valve_id][to_valve_id]

            if distance + 1 >= minutes_left:
                # Not worth going, just calculate rest of pressure
                break
            else:
                time_needed_for_valve = distance + 1
                minutes_left -= time_needed_for_valve
                pressure_released += time_needed_for_valve * current_flow
                current_flow += self.valves[to_valve_id].flow_rate
                curr_valve_id = to_valve_id

        pressure_released += minutes_left * current_flow
        return pressure_released   

    def solve(self):
        all_valve_ids = list(self.flows.keys())
        most_pressure = 0
        best_order = None

        path_to_pressures = {} # size = 33540

        # Get all paths you could travel in total_time
        orders_to_expand = [['AA']]
        while True:
            new_orders_to_expand = []
            for order in orders_to_expand:
                pressure = self.calculate_pressure_released(order)
                path_to_pressures[tuple(order)] = pressure

                # Record if this is the best path so far
                if pressure > most_pressure:
                    most_pressure = pressure
                    best_order = order

                for valve_id in all_valve_ids:
                    if valve_id in order:
                        continue

                    new_order = order + [valve_id]
                    time_needed = self.get_total_time_needed(new_order)
                    if time_needed < self.total_time:
                        new_orders_to_expand.append(new_order)

            if not new_orders_to_expand:
                break

            orders_to_expand = new_orders_to_expand

        all_pressures = [
            (pressure, order[1:])
            for order, pressure in path_to_pressures.items()
        ]
        all_pressures.sort(reverse=True)

        # Find most common start in the top
        counts = defaultdict(int)
        for _, order in all_pressures[:50]:
            counts[order[0]] += 1

        best_start_id = None
        max_count = 0
        for valve_id, count in counts.items():
            if count > max_count:
                max_count = count
                best_start_id = valve_id

        all_other_pressures = [
            (pressure, order)
            for pressure, order in all_pressures
            if best_start_id not in order
        ]

        most_pressure = 0
        for pressure, order in all_pressures[:500]:
            order = set(order)
            for pressure_2, order_2 in all_other_pressures[:500]:
                if order & set(order_2):
                    continue

                if pressure + pressure_2 > most_pressure:
                    most_pressure = pressure + pressure_2

        return most_pressure


def part_1(lines):
    solver = Solver(lines)
    most_pressure = solver.solve()
    return most_pressure


def part_2(lines):
    return part_1(lines)


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)
