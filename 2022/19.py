import json
import math
import os
import re
import sys

from collections import defaultdict


REGEX = 'Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.'


class Type(object):
    ORE = 'ORE'
    CLAY = 'CLAY'
    OBSIDIAN = 'OBSIDIAN'
    GEODE = 'GEODE'


class Simulation(object):
    ''' A single path that simulates robot mining. '''
    def __init__(self, minutes_left, resources, robots, next_robot_costs, next_robot_type, geode_robot_time_left):
        self.minutes_left = minutes_left
        self.resources = resources
        self.robots = robots
        self.next_robot_costs = next_robot_costs
        self.next_robot_type = next_robot_type
        self.geode_robot_time_left = geode_robot_time_left

    def clone(self, next_robot_costs, next_robot_type):
        return Simulation(
            self.minutes_left,
            {k: v for k, v in self.resources.items()},
            {k: v for k, v in self.robots.items()},
            next_robot_costs,
            next_robot_type,
            {k: v for k, v in self.geode_robot_time_left.items()},
        )

    def can_build_robot(self):
        return all(
            self.resources[resource] >= cost
            for resource, cost in self.next_robot_costs.items()
        )

    def build_next_robot(self, no_next_robot=False):
        '''
        Returns True if building next robot was successful, False if we ran out of time.
        '''
        for i in range(self.minutes_left):
            self.minutes_left -= 1
            # print('\nMinute', i + 1)

            # Spend resources if able
            can_build_next_robot = not no_next_robot and self.can_build_robot()
            if can_build_next_robot:
                for resource, cost in self.next_robot_costs.items():
                    self.resources[resource] -= cost
                # print('Constructing', self.next_robot_type)

            # Collect resources
            for type_, num in self.robots.items():
                self.resources[type_] += num
            # print('Resources:', json.dumps(self.resources, indent=2))

            # Finish constructing robots
            if can_build_next_robot:
                self.robots[self.next_robot_type] += 1
                # print('Robots:', json.dumps(self.robots, indent=2))
                if self.next_robot_type == Type.GEODE:
                    self.geode_robot_time_left[self.robots[Type.GEODE]] = self.minutes_left
                return True

        return False


class Simulator(object):
    def __init__(self, costs, num_minutes):
        self.resources = {
            Type.ORE: 0,
            Type.CLAY: 0,
            Type.OBSIDIAN: 0,
            Type.GEODE: 0,
        }
        self.robots = {
            Type.ORE: 1,
            Type.CLAY: 0,
            Type.OBSIDIAN: 0,
            Type.GEODE: 0,
        }
        self.costs = costs

        self.max_costs_per_robot = {}
        for _, costs in self.costs.items():
            for resource_type, cost in costs.items():
                self.max_costs_per_robot[resource_type] = max(self.max_costs_per_robot.get(resource_type, 0), cost)

        # Only next robot types to build are ones that can be built only from ore
        next_robot_types = set()
        for robot_type in self.robots.keys():
            if (self.costs[robot_type][Type.ORE] and len(self.costs[robot_type]) == 1):
                next_robot_types.add(robot_type)

        self.sims = []
        for next_robot_type in next_robot_types:
            self.sims.append(Simulation(
                num_minutes,
                {k: v for k, v in self.resources.items()},
                {k: v for k, v in self.robots.items()},
                self.costs[next_robot_type],
                next_robot_type,
                {}
            ))

        self.most_minutes_left_at_geode_count = {}
        self.most_geodes = 0

    def get_viable_next_robots(self, sim):
        next_robot_types = set()
        for robot_type in (Type.GEODE, Type.OBSIDIAN, Type.CLAY, Type.ORE):
            if any(
                sim.robots[resource_needed] == 0
                for resource_needed in self.costs[robot_type].keys()
            ):
                continue

            if robot_type in self.max_costs_per_robot and self.robots[robot_type] >= self.max_costs_per_robot[robot_type]:
                # Already have enough robots to produce the robot that needs
                # the most of this material every turn
                continue

            minutes_to_build = None
            for resource_type, cost in self.costs[robot_type].items():
                needed_to_build = cost - sim.resources[resource_type]
                minutes_needed = math.ceil(needed_to_build / sim.robots[resource_type])
                if minutes_to_build is None or minutes_needed > minutes_to_build:
                    minutes_to_build = minutes_needed

            if minutes_to_build > sim.minutes_left:
                continue

            if minutes_to_build > 5:
                continue

            next_robot_types.add(robot_type)
            if len(next_robot_types) > 1:
                break

        return next_robot_types

    def run(self):
        new_sims = []

        for sim in self.sims:
            is_time_left = sim.build_next_robot()

            # Record geodes if surpassed max
            if sim.resources[Type.GEODE] > self.most_geodes:
                self.most_geodes = sim.resources[Type.GEODE]
                print('Most geodes:', self.most_geodes)

            # Prune if no time left
            if not is_time_left:
                continue

            next_robot_types = self.get_viable_next_robots(sim)
            if not next_robot_types:
                # Run down the clock
                sim.build_next_robot(no_next_robot=True)

                # Record geodes if surpassed max
                if sim.resources[Type.GEODE] > self.most_geodes:
                    self.most_geodes = sim.resources[Type.GEODE]
                    print('Most geodes:', self.most_geodes)
                continue

            for next_robot_type in next_robot_types:
                new_sims.append(sim.clone(self.costs[next_robot_type], next_robot_type))

        self.sims = new_sims


def solution(lines):
    num_minutes = 24
    total_quality_levels = 0

    for line in lines:
        line = line.strip()
        matches = re.match(REGEX, line)
        [
            id_,
            ore_robot_ore_cost,
            clay_robot_ore_cost,
            obsidian_robot_ore_cost,
            obsidian_robot_clay_cost,
            geode_robot_ore_cost,
            geode_robot_obsidian_cost,
        ] = map(int, [
            matches.group(1),
            matches.group(2),
            matches.group(3),
            matches.group(4),
            matches.group(5),
            matches.group(6),
            matches.group(7),
        ])

        costs = {
            Type.ORE: {
                Type.ORE: ore_robot_ore_cost
            },
            Type.CLAY: {
                Type.ORE: clay_robot_ore_cost
            },
            Type.OBSIDIAN: {
                Type.ORE: obsidian_robot_ore_cost,
                Type.CLAY: obsidian_robot_clay_cost,
            },
            Type.GEODE: {
                Type.ORE: geode_robot_ore_cost,
                Type.OBSIDIAN: geode_robot_obsidian_cost,
            },
        }

        simulator = Simulator(costs, num_minutes)

        while simulator.sims:
            print('sims left:', len(simulator.sims))
            simulator.run()

        quality_level = id_ * simulator.most_geodes
        print(id_, simulator.most_geodes, quality_level)
        total_quality_levels += quality_level

    return total_quality_levels
    

def solution2(lines):
    num_minutes = 32
    multiplied = 1
    max_blueprints = 3

    for line in lines[:max_blueprints]:
        line = line.strip()
        matches = re.match(REGEX, line)
        [
            id_,
            ore_robot_ore_cost,
            clay_robot_ore_cost,
            obsidian_robot_ore_cost,
            obsidian_robot_clay_cost,
            geode_robot_ore_cost,
            geode_robot_obsidian_cost,
        ] = map(int, [
            matches.group(1),
            matches.group(2),
            matches.group(3),
            matches.group(4),
            matches.group(5),
            matches.group(6),
            matches.group(7),
        ])

        costs = {
            Type.ORE: {
                Type.ORE: ore_robot_ore_cost
            },
            Type.CLAY: {
                Type.ORE: clay_robot_ore_cost
            },
            Type.OBSIDIAN: {
                Type.ORE: obsidian_robot_ore_cost,
                Type.CLAY: obsidian_robot_clay_cost,
            },
            Type.GEODE: {
                Type.ORE: geode_robot_ore_cost,
                Type.OBSIDIAN: geode_robot_obsidian_cost,
            },
        }

        simulator = Simulator(costs, num_minutes)

        while simulator.sims:
            print('sims left:', len(simulator.sims))
            simulator.run()

        print(id_, simulator.most_geodes)
        multiplied *= simulator.most_geodes

    return multiplied


if __name__ == '__main__':
    args = sys.argv
    is_test = len(args) > 1 and args[1] == 't'
    part_2 = len(args) > 2 and args[2] == '2'

    day = os.path.basename(__file__).replace('.py', '')

    with open('%s%s.txt' % (day, '_test' if is_test else ''), 'r') as file:
        lines = file.readlines()

    if part_2:
        print(solution2(lines))
    else:
        print(solution(lines))