"""
尽量探索出一条最长的路径
"""

import random
import sys
import time
import pygame
import queue


class MyPriorityQueue:
    def __init__(self):
        self.list = []

    def put(self, thing):
        self.list.append(thing)

    def empty(self):
        if len(self.list) == 0:
            return True
        else:
            return False

    def get(self, reserved=True):
        self.list = sorted(self.list, key=lambda x: x[0], reserved=reserved)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Snake Eating')
        self.screen.fill(BACKGROUND)
        pygame.display.update()

        self.snake = Snake()
        self.food = Food(self.snake.airs_list)

        self.draw_screen()
        pygame.display.update()

        time.sleep(ONE_COUNT)

    def draw_screen(self):
        # 覆盖背景
        self.screen.fill(BACKGROUND)
        # 画网格线
        for x in range(0, SCREEN_WIDTH, CELL_SIZE + LINE_SIZE):
            pygame.draw.rect(self.screen, BLACK, (x, 0, LINE_SIZE, SCREEN_HEIGHT), 0)
        for y in range(0, SCREEN_HEIGHT, CELL_SIZE + LINE_SIZE):
            pygame.draw.rect(self.screen, BLACK, (0, y, SCREEN_WIDTH, LINE_SIZE), 0)
        # 画蛇和路径
        # 蛇身
        self.draw_lines(self.snake.body, size=CELL_SIZE, color=LIGHT)
        # 要前往的道路
        self.draw_lines(self.snake.image_road[1:], size=20, color=YELLOW)
        # 蛇尾
        self.draw_lines([self.snake.body[0]], size=20, color=PINK)
        # 蛇头
        if self.snake.action == 'food':
            self.draw_lines([self.snake.body[-1]], size=20, color=GREEN)
        elif self.snake.action == 'long':
            self.draw_lines([self.snake.body[-1]], size=20, color=YELLOW)
        elif self.snake.action == 'tail':
            self.draw_lines([self.snake.body[-1]], size=20, color=RED)
        else:
            pass

        self.draw_lines(self.snake.road_to_goal, size=25, color=WHITE)

        # 画食物
        x = (self.food.x - 1) * CELL_SIZE + self.food.x * LINE_SIZE
        y = (self.food.y - 1) * CELL_SIZE + self.food.y * LINE_SIZE
        pygame.draw.rect(self.screen, ORANGE, (x, y, CELL_SIZE, CELL_SIZE), 0)

    def draw_lines(self, lines, size=20, color=(0, 0, 0)):
        if lines:
            for i in lines:
                x = (i[0] - 1) * CELL_SIZE + i[0] * LINE_SIZE
                y = (i[1] - 1) * CELL_SIZE + i[1] * LINE_SIZE
                pygame.draw.rect(self.screen, color, (x + (CELL_SIZE - size) // 2,
                                                      y + (CELL_SIZE - size) // 2, size, size), 0)

    def run(self):
        pause = False
        count = 0
        while True:
            start_time = time.time()
            count += 1
            # 按键检测
            check_event(pause)

            # 蛇进行思考和行动
            self.snake.think((self.food.x, self.food.y))
            self.snake.move_and_eat(self.food)
            self.food.check(self.snake.airs_list)

            # 可视化
            self.draw_screen()
            pygame.display.update()

            print(len(self.snake.body), no_hole(self.snake.airs_list),
                  len(self.snake.body) + no_hole(self.snake.airs_list))
            self.snake.check_body_road()

            # 检测游戏是否结束
            if self.snake.check():
                print("You have walked " + str(count) + " counts!")
                count = 0
                self.snake = Snake()
                self.food = Food(self.snake.airs_list)

            # 控制游戏帧率
            end_time = time.time()
            if end_time - start_time < ONE_COUNT:
                time.sleep(ONE_COUNT - (end_time - start_time))


class Snake:
    def __init__(self):
        self.road_to_food = []
        self.length = 3
        self.image_body = []
        self.image_road = []
        self.action = None
        self.hungry = 0
        self.direction = (1, 0)
        self.body_priority = []
        self.goal = None
        self.road_to_goal = []

        self.body = []
        for i in range(self.length):
            x = (M + 1) // 2 + i + 1 - self.length
            y = (N + 1) // 2
            self.body.append((x, y))

        self.airs_list = possible_airs(self.body)

    def check(self):
        if len(self.body) == M * N:
            print("YOU WIN!")
            return True
        if self.body[-1] in self.body[:-1]:
            print("YOU EAT YOURSELF!")
            return True
        if self.body[-1][0] in [0, M + 1] or self.body[-1][1] in [0, N + 1]:
            print("YOU EAT THE WALL!")
            return True

    def move_and_eat(self, food):
        self.body.append((self.body[-1][0] + self.direction[0],
                          self.body[-1][1] + self.direction[1]))
        if self.body[-1] == (food.x, food.y):
            # 吃到食物
            self.hungry = 0
            self.road_to_goal = []
        else:
            # 没有吃到食物
            self.body.pop(0)
        self.airs_list = possible_airs(self.body)

    def check_body_road(self):
        self.body_priority = []
        head = self.body[-1]
        for index in range(len(self.body) - 1):
            if search_the_road(head, self.body[index],
                               possible_airs(self.body[0:index] + self.body[index + 1:])) is not None:
                self.body_priority.append(1)
            else:
                self.body_priority.append(0)

    def find_long_road_in_one_direction(self, head, next_cell, direction):

        """
        index_list = []
        if direction == (1, 0):
            index_list = range(head[0], M)
        elif direction == (-1, 0):
            index_list = range(1, head[0]+1)
        elif direction == (0, 1):
            index_list = range(head[1], N)
        elif direction == (0, -1):
            index_list = range(1, head[1]+1)"""
        line1, line2 = [], []
        for index in range(1, max(M, N)):
            x1, y1 = (head[0] + direction[0] * index,
                      head[1] + direction[1] * index)
            x2, y2 = (next_cell[0] + direction[0] * index,
                      next_cell[1] + direction[1] * index)

            if (x1, y1) not in self.airs_list or (x2, y2) not in self.airs_list:
                break
            else:
                line1.append((x1, y1))
                line2.append((x2, y2))
        line2.reverse()
        return line1 + line2 + [next_cell]

    def find_long_road(self, head, next_cell):
        direction = (next_cell[0] - head[0], next_cell[1] - head[1])
        road1 = self.find_long_road_in_one_direction \
            (head, next_cell, (direction[1], direction[0]))
        road2 = self.find_long_road_in_one_direction \
            (head, next_cell, (-direction[1], -direction[0]))
        if len(road1) > len(road2):
            return road1
        else:
            return road2

    def think(self, food):
        head = self.body[-1]
        tail = self.body[0]
        self.hungry += 1

        if len(self.road_to_goal) == 0:
            road_to_tail = search_the_road(head, tail, self.airs_list + [tail])
            road_to_food = search_the_road(head, food, self.airs_list)

            if road_to_food is not None:
                image_road = get_road(head, road_to_food[0], food)
                image_snake = Snake()
                image_snake.body = get_image_body(body=self.body, road=image_road)
                image_snake.airs_list = possible_airs(image_snake.body)
                if search_the_road(image_snake.body[-1], image_snake.body[0],
                                   image_snake.airs_list + [image_snake.body[0]]) is not None:
                    goal = food
                    came_from = road_to_food[0]
                else:
                    goal = tail
                    came_from = road_to_tail[0]
            else:
                goal = tail
                came_from = road_to_tail[0]

            self.image_road = get_road(head, came_from, goal)
            print("self_image_road", self.image_road)
            road_to_goal = []
            image_road = [head] + self.image_road
            for index in range(len(image_road) - 1):
                print(image_road[index],
                      image_road[index + 1])
                road_to_goal = road_to_goal + \
                               self.find_long_road(image_road[index],
                                                   image_road[index + 1])
            self.road_to_goal = road_to_goal
            print("self goal", self.goal)
            print("body", self.body)
            print("road", self.road_to_goal)
            next_cell = self.road_to_goal.pop(0)
        else:
            self.image_road = self.road_to_goal
            next_cell = self.road_to_goal.pop(0)
        self.direction = (next_cell[0] - head[0], next_cell[1] - head[1])


class Food:
    def __init__(self, possible_airs_list):
        self.x = random.randint(1, M)
        self.y = random.randint(1, N)
        self.check(possible_airs_list)

    def check(self, possible_airs_list):
        if len(possible_airs_list) == 0:
            return
        if (self.x, self.y) not in possible_airs_list:
            random_number = random.randint(0, len(possible_airs_list) - 1)
            self.x, self.y = possible_airs_list[random_number]


def possible_airs(body=[]):
    airs_list = [(x, y) for x in range(1, M + 1) for y in range(1, N + 1)]
    print("body:", body)
    for (x, y) in body:
        airs_list.remove((x, y))
    return airs_list


def check_event(pause):
    global ONE_COUNT
    while True:
        # 按键检测
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    ONE_COUNT /= 2
                elif event.key == pygame.K_DOWN:
                    ONE_COUNT *= 2
                elif event.key == pygame.K_p:
                    if pause:
                        pause = False
                    else:
                        pause = True
        if not pause:
            break


def airs_near_the_cell(current, airs_list):
    near = []
    for (x, y) in [(current[0] + 1, current[1]), (current[0] - 1, current[1]),
                   (current[0], current[1] + 1), (current[0], current[1] - 1)]:
        if (x, y) in airs_list:
            near.append((x, y))
    return near


def get_road(start, came_from, goal):
    if goal not in came_from:
        return None
    road = []
    current = goal
    count = 0
    while True:
        count += 1
        road.append(current)
        if came_from[current] == start:
            break
        current = came_from[current]
        if count > len(came_from):
            print("Finding Road Error")
            return None
    road.reverse()
    return road


def get_image_body(body, road):
    image_body = []
    image_body += body

    image_body += road
    return image_body[len(road) - 1:]


def no_hole(possible_airs_list):
    frontier = [possible_airs_list[0]]
    used_cells = [possible_airs_list[0]]
    while len(frontier) != 0:
        current = frontier.pop()
        for next_cell in airs_near_the_cell(current, possible_airs_list):
            if next_cell not in used_cells:
                used_cells.append(next_cell)
                if next_cell not in frontier:
                    frontier.append(next_cell)
    return len(used_cells)


def contain(mother_list, son_list):
    """
    :param mother_list: 母集
    :param son_list: 子集
    :return: 布尔值
    """
    for x in son_list:
        if x not in mother_list:
            return False
    return True


def search_the_road(start, goal, airs_list):
    """
    :param start: 起点 接受一个含两个元素的元组(x, y)
    :param goal:  目标 接受一个含两个元素的元组(x, y)
    :param airs_list: 可以行走的路径
    :return: 返回两个字典 一个是描述了格子来自哪里 一个描述了每个格子花费的代价
    A*寻路算法 能够找到起点和终点之间的最短路径（如果存在的话） 但是无法对路径的弯曲程度等属性进行调整
    """
    frontier = queue.PriorityQueue()
    frontier.put((0, start))
    came_from, cost_so_far = {}, {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()[1]
        if current == goal:
            break
        for next_cell in airs_near_the_cell(current, airs_list):
            new_cost = cost_so_far[current] + 1

            if next_cell not in cost_so_far or new_cost < cost_so_far[current]:
                cost_so_far[next_cell] = new_cost
                priority = new_cost + abs(next_cell[0] - goal[0]) + abs(next_cell[1] - goal[1])
                frontier.put((priority, next_cell))
                came_from[next_cell] = current
    if goal not in came_from:
        return None
    return came_from, cost_so_far


CELL_SIZE = 30
LINE_SIZE = 1
M, N = 5, 5
SCREEN_WIDTH = CELL_SIZE * M + LINE_SIZE * (M + 1)
SCREEN_HEIGHT = CELL_SIZE * N + LINE_SIZE * (N + 1)
ONE_COUNT = 0.5

WHITE = (255, 255, 255)
ORANGE = (255, 120, 40)
GREY = (255, 245, 255)
DARK = (100, 100, 100)
LIGHT = (200, 200, 200)
GREEN = (180, 230, 30)
PINK = (255, 170, 200)
RED = (230, 30, 30)
BLUE = (100, 100, 180)
YELLOW = (255, 240, 0)
BACKGROUND = (40, 40, 60)
BLACK = (0, 0, 0)

if __name__ == '__main__':
    game = Game()
    game.run()
