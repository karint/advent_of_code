"""
Part 1:
Part 2:
"""
import os

from util import run


class Robot(object):
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def move(self, width, height):
        self.x += self.dx
        self.y += self.dy

        if self.x >= width:
            self.x = self.x % width

        while self.x < 0:
            self.x += width

        if self.y >= height:
            self.y = self.y % height
        while self.y < 0:
            self.y += height



def part_1(lines):
    robots = []
    width = 101
    height = 103

    half_width = width // 2
    half_height = height // 2

    num_seconds = 100
    for line in lines:
        line = line.strip()
        pos, vel = line.split(' ')
        x, y = map(int, pos[2:].split(','))
        dx, dy = map(int, vel[2:].split(','))
        robots.append(Robot(x, y, dx, dy))

    q1, q2, q3, q4 = 0, 0, 0, 0
    for robot in robots:
        for _ in range(num_seconds):
            robot.move(width, height)


        if robot.x < half_width:
            if robot.y < half_height:
                q1 += 1
            elif robot.y >= height - half_height:
                q3 += 1
        elif robot.x >= width - half_width:
            if robot.y < half_height:
                q2 += 1
            elif robot.y >= height - half_height:
                q4 += 1

    return q1 * q2 * q3 * q4


def print_grid(width, height, robots, file):
    robot_coords = set((robot.x, robot.y) for robot in robots)
    for y in range(height):
        row = ''.join(('X' if (x, y) in robot_coords else ' ') for x in range(width))
        print(row, file=file)


def part_2(lines):
    """
    I didn't do this purely by code. Instead I printed out a bunch of grids and visually determined
    that a vertical cluster happened at s=10 and every 101 pictures after that, and a horizontal cluster
    happened at s=88 and every 103 pictures after that. I then determined that 6474 was the
    first time both of these series would converge. I jumped to that picture that behold, a tree!
    Then I just added one since things were 0-indexed.
    """

    # robots = []
    # width = 101
    # height = 103

    # for line in lines:
    #     line = line.strip()
    #     pos, vel = line.split(' ')
    #     x, y = map(int, pos[2:].split(','))
    #     dx, dy = map(int, vel[2:].split(','))
    #     robots.append(Robot(x, y, dx, dy))

    # with open('temp2.txt', 'w+') as file:
    #     for s in range(10000):
    #         for robot in robots:
    #             robot.move(width, height)

    #         print('---------------------', file=file)
    #         print(s, file=file)
    #         print('---------------------', file=file)
    #         print_grid(width, height, robots, file)

    return 6474 + 1



if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)
