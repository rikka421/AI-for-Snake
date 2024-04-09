"""
对奇偶性进行了一点研究
下一步打算尝试 9+X 的思路
以及UI的构建和升级
"""

import random
import sys
import time
import pygame
import queue


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
        self.draw_body(LIGHT, PINK)
        # 要前往的道路
        self.draw_lines(self.snake.image_road[1:], color=YELLOW)
        # 蛇头 表明小蛇当前做出决策
        """
        if self.snake.action == 'food':
            self.draw_lines([self.snake.body[-1]], size=CELL_SIZE, color=GREEN)
        elif self.snake.action == 'long':
            self.draw_lines([self.snake.body[-1]], size=CELL_SIZE, color=YELLOW)
        elif self.snake.action == 'tail':
            self.draw_lines([self.snake.body[-1]], size=CELL_SIZE, color=RED)
        else:
            self.draw_lines([self.snake.body[-1]], size=CELL_SIZE, color=GREEN)
        """
        self.draw_eyes(PURPLE)

        # 画食物
        x = (self.food.x - 1) * CELL_SIZE + self.food.x * LINE_SIZE
        y = (self.food.y - 1) * CELL_SIZE + self.food.y * LINE_SIZE
        pygame.draw.rect(self.screen, ORANGE, (x, y, CELL_SIZE, CELL_SIZE), 0)

    def draw_body(self, body_color, figure_color, body_figure=False):
        # 画出小蛇的每一节身体
        self.draw_lines(self.snake.body, size=CELL_SIZE, color=LIGHT)
        # 填满小蛇每节身体之间的空隙
        for index in range(len(self.snake.body) - 1):
            cell = self.snake.body[index]
            x = (cell[0] - 1) * CELL_SIZE + cell[0] * LINE_SIZE
            y = (cell[1] - 1) * CELL_SIZE + cell[1] * LINE_SIZE
            direction = (self.snake.body[index + 1][0] - cell[0],
                         self.snake.body[index + 1][1] - cell[1])
            pygame.draw.rect(self.screen,
                             body_color,
                             (x + CELL_SIZE // 2 * direction[0],
                              y + CELL_SIZE // 2 * direction[1],
                              CELL_SIZE, CELL_SIZE), 0)
            if figure_color is None:
                continue
            elif index == 0:
                self.draw_lines([self.snake.body[0]], 20, figure_color)
            # 当参数为真时 给小蛇加上花纹
            elif body_figure:
                pygame.draw.rect(
                    self.screen,
                    figure_color, (x + CELL_SIZE // 6 * abs(direction[0]),
                                   y + CELL_SIZE // 6 * abs(direction[1]),
                                   (abs(direction[1]) * 5 + 1) * CELL_SIZE // 6,
                                   (abs(direction[0]) * 5 + 1) * CELL_SIZE // 6), 0)
                pygame.draw.rect(
                    self.screen,
                    figure_color, (x + CELL_SIZE // 6 * abs(direction[0]) * 3,
                                   y + CELL_SIZE // 6 * abs(direction[1]) * 3,
                                   (abs(direction[1]) * 5 + 1) * CELL_SIZE // 6,
                                   (abs(direction[0]) * 5 + 1) * CELL_SIZE // 6), 0)
                pygame.draw.rect(
                    self.screen,
                    figure_color, (x + CELL_SIZE // 6 * abs(direction[0]) * 5,
                                   y + CELL_SIZE // 6 * abs(direction[1]) * 5,
                                   (abs(direction[1]) * 5 + 1) * CELL_SIZE // 6,
                                   (abs(direction[0]) * 5 + 1) * CELL_SIZE // 6), 0)

    def draw_eyes(self, color):
        # 画出小蛇的眼睛
        head = self.snake.body[-1]
        direction = (head[0] - self.snake.body[-2][0],
                     head[1] - self.snake.body[-2][1])
        x = (head[0] - 1) * CELL_SIZE + head[0] * LINE_SIZE
        y = (head[1] - 1) * CELL_SIZE + head[1] * LINE_SIZE
        if direction == (1, 0):
            pygame.draw.rect(self.screen, color,
                             (x + CELL_SIZE * 2 / 5,
                              y + CELL_SIZE * 1 / 5,
                              3 / 5 * CELL_SIZE, 1 / 5 * CELL_SIZE), 0)
            pygame.draw.rect(self.screen, color,
                             (x + CELL_SIZE * 2 / 5,
                              y + CELL_SIZE * 3 / 5,
                              3 / 5 * CELL_SIZE, 1 / 5 * CELL_SIZE), 0)
        elif direction == (-1, 0):
            pygame.draw.rect(self.screen, color,
                             (x,
                              y + CELL_SIZE * 1 / 5,
                              3 / 5 * CELL_SIZE, 1 / 5 * CELL_SIZE), 0)
            pygame.draw.rect(self.screen, color,
                             (x,
                              y + CELL_SIZE * 3 / 5,
                              3 / 5 * CELL_SIZE, 1 / 5 * CELL_SIZE), 0)
        elif direction == (0, 1):
            pygame.draw.rect(self.screen, color,
                             (x + CELL_SIZE * 1 / 5,
                              y + CELL_SIZE * 2 / 5,
                              1 / 5 * CELL_SIZE, 3 / 5 * CELL_SIZE), 0)
            pygame.draw.rect(self.screen, color,
                             (x + CELL_SIZE * 3 / 5,
                              y + CELL_SIZE * 2 / 5,
                              1 / 5 * CELL_SIZE, 3 / 5 * CELL_SIZE), 0)
        elif direction == (0, -1):
            pygame.draw.rect(self.screen, color,
                             (x + CELL_SIZE * 1 / 5,
                              y,
                              1 / 5 * CELL_SIZE, 3 / 5 * CELL_SIZE), 0)
            pygame.draw.rect(self.screen, color,
                             (x + CELL_SIZE * 3 / 5,
                              y,
                              1 / 5 * CELL_SIZE, 3 / 5 * CELL_SIZE), 0)

    def draw_lines(self, lines, size=20, color=(0, 0, 0)):
        # 在屏幕上画出一系列的方格
        if len(lines) != 0:
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

            # 检测游戏是否结束
            if self.snake.check() or self.snake.hungry > 50*M*N:
                game_start = self.snake.start
                game_over = time.time()
                game_time = game_over - game_start
                print("You have walked " + str(count) + " counts!")
                print("You have cost " + "%.2f" % game_time + " second!")
                self.snake = Snake()
                count = 0
                self.food = Food(self.snake.airs_list)

            # 控制游戏帧率
            end_time = time.time()
            if end_time - start_time < ONE_COUNT:
                time.sleep(ONE_COUNT - (end_time - start_time))


class Snake:
    def __init__(self):
        self.start = time.time()

        self.length = 3
        self.image_body = []
        self.image_road = []
        self.action = None
        self.hungry = 0
        self.direction = (1, 0)

        self.choose = []

        self.sort_body = 0
        self.body = []
        for i in range(self.length):
            x = (M + 1) // 2 + i + 1 - self.length
            y = (N + 1) // 2
            self.body.append((x, y))

        self.airs_list = possible_airs(self.body)

    def check(self):
        # 检测是否已经满足了游戏结束的条件
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
        # 对于蛇移动和可能的进食进行相关处理
        self.body.append((self.body[-1][0] + self.direction[0],
                          self.body[-1][1] + self.direction[1]))
        if self.body[-1] == (food.x, food.y):
            # 吃到食物
            self.hungry = 0
            self.choose = []
            if len(self.body) < M * N / 3:
                self.sort_body = 0
            else:
                self.sort_body = len(self.body)
        else:
            # 没有吃到食物
            self.body.pop(0)
        self.airs_list = possible_airs(self.body)

    def check_safe(self, target, food):
        # 对于前往目标方格的安全性做出判断
        image_body = self.get_image_body(target, food)
        if search_the_road(image_body[-1], image_body[0], possible_airs(image_body) + [image_body[0]]) \
                is not None:
            return True
        else:
            return False

    def get_image_body(self, target, food):
        # 对于下一步要前往的目标格子 获取想象中的下一步的身体
        image_body = []
        image_body += self.body
        image_body += [target]
        if target == food:
            pass
        else:
            image_body.pop(0)
        return image_body

    def get_long_road(self, food, target=None, circle=False):
        # 获取一个尽可能离目标远的格子坐标
        head = self.body[-1]
        tail = self.body[0]
        # 当没有传入目标时 默认目标是尾巴
        if target is None:
            target = tail

        targets_list = []
        if M % 2 == 1 and N % 2 == 1 and food[1] != 0:
            airs_list = airs_near_the_cell(head,
                                           possible_airs(self.body, y_min=1) + [tail])
        elif M % 2 == 1 and N % 2 == 1 and food[1] != N:
            airs_list = airs_near_the_cell(head,
                                           possible_airs(self.body, y_max=N-1) + [tail])
        else:
            airs_list = airs_near_the_cell(head,
                                           possible_airs(self.body) + [tail])
        for (x, y) in airs_list:
            if self.check_safe((x, y), food):
                cost = abs(x - target[0]) + abs(y - target[1])
                targets_list.append(((x, y), cost))

        if len(targets_list) != 0:
            targets_list = sorted(targets_list, key=lambda item: item[1], reverse=True)
            possible_targets = []
            min_cost = targets_list[0][1]
            for target in targets_list:
                if target[1] == min_cost:
                    possible_targets.append(target[0])

            if circle:
                for target in possible_targets:
                    if (head, target) not in self.choose:
                        self.choose.append((head, target))
                        return target
            if N % 2 == 0:
                return possible_targets[0]
            elif M % 2 == 0:
                return possible_targets[-1]
            else:
                return possible_targets[0]
        else:
            return -1, -1

    def think(self, food):
        head = self.body[-1]
        self.hungry += 1

        road_to_food = search_the_road(head, food, self.airs_list)

        if road_to_food is not None and self.sort_body <= 0:
            road = get_road(head, road_to_food[0], food)
            target = road[0]
            self.image_body = get_image_body(self.body, road)

            if len(self.body) == M * N - 1 and target == food:
                self.action = 'food'
                next_cell = target
            elif self.check_safe(target, food) and \
                    (search_the_road(self.image_body[-1], self.image_body[0],
                     possible_airs(self.image_body[1:]))):
                if len(road) <= M + N:
                    self.image_road = road
                    self.action = 'food'
                    next_cell = target
                else:
                    next_cell = None
            else:
                next_cell = None
        else:
            next_cell = None

        if next_cell is None:
            self.action = 'long'
            next_cell = self.get_long_road(food)
            self.sort_body -= 1

        if self.hungry > 3 * len(self.body):
            self.action = 'tail'
            next_cell = self.get_long_road(food, circle=True)
            self.sort_body -= 1
        if next_cell == (-1, -1):
            print("ERROR")
            input()

        self.choose.append((head, next_cell))
        self.direction = (next_cell[0] - head[0], next_cell[1] - head[1])


class Food:
    # 食物类 有着坐标属性和被吃之后重新生成的方法
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


def possible_airs(body=[], x_max=None, y_max=None, x_min=1, y_min=1):
    # 对于某一刻的蛇身 处理并返回此刻地图上空着的格子
    if x_max is None:
        x_max = M
    if y_max is None:
        y_max = N
    airs_list = [(x, y) for x in range(x_min, x_max + 1)
                 for y in range(y_min, y_max + 1)]
    for (x, y) in body[:]:
        airs_list.remove((x, y))
    return airs_list


def check_event(pause):
    # 对于用户的按键做出检测并做出反应
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
    # 对于某个方格 返回它周围的空着的方格的坐标列表
    near = []
    for (x, y) in [(current[0] + 1, current[1]), (current[0] - 1, current[1]),
                   (current[0], current[1] + 1), (current[0], current[1] - 1)]:
        if (x, y) in airs_list:
            near.append((x, y))
    return near


def get_road(start, came_from, goal):
    # 对于传入的字典 对字典中蕴含的信息进行处理 返回一个路径坐标的列表
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
    # 对于想象中的路径 返回走完这条路径后的想象中的身体
    image_body = []
    image_body += body

    image_body += road
    return image_body[len(road) - 1:]


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
LINE_SIZE = 4
M, N = 10, 10
SCREEN_WIDTH = CELL_SIZE * M + LINE_SIZE * (M + 1)
SCREEN_HEIGHT = CELL_SIZE * N + LINE_SIZE * (N + 1)
ONE_COUNT = 0.1

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
PURPLE = (160, 70, 160)

if __name__ == '__main__':
    game = Game()
    game.run()
