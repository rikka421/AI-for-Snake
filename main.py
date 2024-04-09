import random
import sys
import time
import pygame
import queue


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Snake')

        self.game_mode = None

        self.snake = Snake()
        self.food = Food(self.snake.airs_list)

        self.draw_start_screen()

        self.scores_list = []

        time.sleep(ONE_COUNT)

    def draw_screen(self):
        # 覆盖背景
        self.screen.fill(BACKGROUND)
        # 画网格线
        for x in range(0, SCREEN_WIDTH, CELL_SIZE + LINE_SIZE):
            pygame.draw.rect(self.screen, BLACK, (x, 0, LINE_SIZE, SCREEN_HEIGHT), 0)
        for y in range(0, SCREEN_HEIGHT, CELL_SIZE + LINE_SIZE):
            pygame.draw.rect(self.screen, BLACK, (0, y, SCREEN_WIDTH, LINE_SIZE), 0)

        # 画食物
        x = (self.food.x - 1) * CELL_SIZE + self.food.x * LINE_SIZE
        y = (self.food.y - 1) * CELL_SIZE + self.food.y * LINE_SIZE
        pygame.draw.rect(self.screen, ORANGE, (x, y, CELL_SIZE, CELL_SIZE), 0)
        # 画蛇和路径
        # 蛇身
        self.draw_body(LIGHT, PINK)
        # 要前往的道路
        self.draw_lines(self.snake.image_road[1:-1], color=YELLOW)
        # 蛇眼
        self.draw_eyes(PURPLE)
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

        pygame.display.update()

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

    def check_event(self, pause):
        global ONE_COUNT
        change_direction = False
        while True:
            # 按键检测
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and self.game_mode is not None:
                    if event.key == pygame.K_UP:
                        ONE_COUNT /= 2
                    elif event.key == pygame.K_DOWN:
                        ONE_COUNT *= 2
                    elif event.key == pygame.K_p:
                        if pause:
                            pause = False
                        else:
                            pause = True
                    if self.game_mode == 1 and not change_direction:
                        change_direction = True
                        if event.key == pygame.K_w and self.snake.direction != (0, 1):
                            self.snake.direction = (0, -1)
                        elif event.key == pygame.K_s and self.snake.direction != (0, -1):
                            self.snake.direction = (0, 1)
                        elif event.key == pygame.K_a and self.snake.direction != (1, 0):
                            self.snake.direction = (-1, 0)
                        elif event.key == pygame.K_d and self.snake.direction != (-1, 0):
                            self.snake.direction = (1, 0)
                if event.type == pygame.MOUSEBUTTONDOWN and self.game_mode is None:
                    mouse_xy = event.pos
                    if SCREEN_WIDTH / 3 < mouse_xy[0] < SCREEN_WIDTH / 3 * 2 and \
                            SCREEN_HEIGHT / 14 * 4 < mouse_xy[1] < SCREEN_HEIGHT / 14 * 6:
                        self.game_mode = 1
                    elif SCREEN_WIDTH / 3 < mouse_xy[0] < SCREEN_WIDTH / 3 * 2 and \
                            SCREEN_HEIGHT / 14 * 7 < mouse_xy[1] < SCREEN_HEIGHT / 14 * 9:
                        self.game_mode = 2
                    elif SCREEN_WIDTH / 3 < mouse_xy[0] < SCREEN_WIDTH / 3 * 2 and \
                            SCREEN_HEIGHT / 14 * 10 < mouse_xy[1] < SCREEN_HEIGHT / 14 * 12:
                        pygame.quit()
                        sys.exit()
            if not pause:
                break

    def draw_start_screen(self):
        # 覆盖背景
        self.screen.fill(DARK)

        # 展示游戏名称
        font1 = pygame.font.SysFont(None, int(SCREEN_HEIGHT * 3 / 14))
        f_width, f_height = font1.size('Snake')
        f_x = (SCREEN_WIDTH - f_width) // 2
        f_y = SCREEN_HEIGHT // 14
        self.screen.blit(font1.render("Snake", True, ORANGE), (f_x, f_y))

        # 画界面按钮
        width = SCREEN_WIDTH / 3
        height = SCREEN_HEIGHT / 7
        x = (SCREEN_WIDTH - width) // 2
        y = SCREEN_HEIGHT * 4 / 14

        font2 = pygame.font.SysFont(None, int(SCREEN_HEIGHT / 7))
        f_width, f_height = font2.size('Player')
        f_x = (SCREEN_WIDTH - f_width) // 2
        f_y = y + (SCREEN_HEIGHT / 7 - f_height) / 2
        # 按钮1
        pygame.draw.rect(self.screen, LIGHT, (x, y, width, height), 0)
        self.screen.blit(font2.render("Player", True, BLACK), (f_x, f_y))
        # 按钮2
        y += height / 2 * 3
        f_width, f_height = font2.size('AI')
        f_x = (SCREEN_WIDTH - f_width) // 2
        f_y = y + (SCREEN_HEIGHT / 7 - f_height) / 2
        pygame.draw.rect(self.screen, LIGHT, (x, y, width, height), 0)
        self.screen.blit(font2.render("AI", True, BLACK), (f_x, f_y))
        # 按钮3
        y += height / 2 * 3
        f_width, f_height = font2.size('Exit')
        f_x = (SCREEN_WIDTH - f_width) // 2
        f_y = y + (SCREEN_HEIGHT / 7 - f_height) / 2
        pygame.draw.rect(self.screen, LIGHT, (x, y, width, height), 0)
        self.screen.blit(font2.render("Exit", True, BLACK), (f_x, f_y))
        # 游戏操作说明
        font3 = pygame.font.SysFont(None, int(SCREEN_HEIGHT/16))
        f_width = max(font3.size('Press "UP" or "DOWN" to control the speed.')[0],
                      font3.size('Press "P" to pause.')[0],
                      font3.size('Press "W""A""S""D" to move.')[0])
        f_height = sum([font3.size('Press "UP" or "DOWN" to control the speed.')[1],
                        font3.size('Press "P" to pause.')[1],
                        font3.size('Press "W""A""S""D" to move.')[1]])
        self.screen.blit(font3.render('Press "UP" or "DOWN" to control the speed.',
                                      True, BLACK), ((SCREEN_WIDTH - f_width) / 2,
                                                     SCREEN_HEIGHT - f_height))
        self.screen.blit(font3.render('Press "P" to pause.',
                                      True, BLACK), ((SCREEN_WIDTH - f_width) / 2,
                                                     SCREEN_HEIGHT - f_height / 3))
        self.screen.blit(font3.render('Press "W""A""S""D" to move.',
                                      True, BLACK), ((SCREEN_WIDTH - f_width) / 2,
                                                     SCREEN_HEIGHT - f_height / 3 * 2))

        pygame.display.update()

    def run(self):
        pause = False
        count = 0
        while True:
            # 按键检测
            self.check_event(pause)
            if self.game_mode == 1 or self.game_mode == 2:
                if self.snake.start is None:
                    self.snake.start = time.time()
                start_time = time.time()
                count += 1
                if self.game_mode == 2:
                    # 蛇进行思考和行动
                    self.snake.think((self.food.x, self.food.y))

                self.snake.move_and_eat(self.food)

                # 检测游戏是否胜利或陷入死循环
                if self.snake.check() or len(self.snake.choose) > 50*M*N:
                    game_start = self.snake.start
                    game_over = time.time()
                    game_time = game_over - game_start
                    print("You have walked " + str(count) + " counts!")
                    print("You have cost " + "%.2f" % game_time + " second!")
                    if self.game_mode == 1:
                        pygame.quit()
                        sys.exit()
                    elif self.game_mode == 2:
                        self.scores_list.append(count)
                        print('average count: ' + "%.2f" % (sum(self.scores_list)/len(self.scores_list)))
                        if len(self.scores_list) < 75:
                            print('max count:', max(self.scores_list), 'min count:', min(self.scores_list))
                            self.snake = Snake()
                            count = 0
                            self.food = Food(self.snake.airs_list)
                        else:
                            print("sort_body_rect: ", self.snake.sort_body_rect)
                            print("Game have run 75 times!")
                            pygame.quit()
                            sys.exit()

                self.food.check(self.snake.airs_list)

                # 可视化
                self.draw_screen()

                # 控制游戏帧率
                end_time = time.time()
                if end_time - start_time < ONE_COUNT:
                    time.sleep(ONE_COUNT - (end_time - start_time))
            elif self.game_mode is None:
                self.draw_start_screen()


class Snake:
    def __init__(self):
        self.sort_body_rect = 1
        self.circle = 0
        self.start = None
        # 基本属性
        self.length = 3
        self.image_body = []
        self.image_road = []
        self.action = 'food'
        self.direction = (1, 0)
        self.body = []
        # 记住自己做出的选择 判断多久没有吃到食物 避免死循环
        self.choose = []
        # 整理自己身体的倾向
        self.sort_body = 0
        # 生成身体
        for i in range(self.length):
            x = (M + 1) // 2 + i + 1 - self.length
            y = (N + 1) // 2
            self.body.append((x, y))
        # 寻找未被身体占用的格子
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
        # 生成未被占用的空气格子
        self.airs_list = possible_airs(self.body)

    def move_and_eat(self, food):
        # 对于蛇移动和可能的进食进行相关处理
        # 蛇身移动 在蛇头前增加一个格子
        self.body.append((self.body[-1][0] + self.direction[0],
                          self.body[-1][1] + self.direction[1]))
        if self.body[-1] == (food.x, food.y):
            # 吃到食物 将历史选择的列表清空 并且对整理身体的参数进行设置
            self.choose = []
            if len(self.body) < 3 * min(M, N):
                self.sort_body = 0
            else:
                self.sort_body = len(self.body) * self.sort_body_rect
        else:
            # 没有吃到食物 将尾巴格子取出
            self.body.pop(0)

    def check_safe(self, target, food):
        # 对于下一步的目标target 判断这一目标是否安全
        image_body = self.get_image_body(target, food)
        if search_the_road(image_body[-1], image_body[0], possible_airs(image_body) + [image_body[0]]) \
                is not None:
            return True
        else:
            return False

    def get_image_body(self, target, food):
        # 对于下一步的目标，获取走完这一步的想象中的身体
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
        # 获取目标附近的空的格子
        targets_list = []
        airs_list = airs_near_the_cell(head, possible_airs(self.body) + [tail])
        for (x, y) in airs_list:
            cost = abs(x - target[0]) + abs(y - target[1])
            targets_list.append(((x, y), cost))

        targets_list = sorted(targets_list, key=lambda item: item[1], reverse=True)
        # 获取目标附近的安全的空格子
        possible_targets = []
        for target in targets_list:
            if self.check_safe(target[0], food):
                possible_targets.append(target[0])

        if circle:
            # 处于循环中且蛇身几乎铺满屏幕时 前往与之前不同的方向
            if len(self.body) > M * N - 2*max(M, N):
                for _ in range(len(airs_list)):
                    air = airs_list.pop(random.randint(0, len(airs_list)-1))
                    if self.check_safe(air, food) and (head, air) not in self.choose:
                        return air
            # 处于循环但蛇身较短时 选择一个随机的安全方向
            else:
                for _ in range(len(airs_list)):
                    air = airs_list.pop(random.randint(0, len(airs_list)-1))
                    if self.check_safe(air, food):
                        return air
        # 当高度为偶数时 倾向于沿着横线方向行走
        if N % 2 == 0:
            return possible_targets[0]
        # 当宽度为偶数时 倾向于沿着竖线方向行走
        elif M % 2 == 0:
            return possible_targets[-1]
        # 当地图为奇数*奇数时 依然沿着横线行走
        else:
            return possible_targets[0]

    def think(self, food):
        # 判断小蛇是否处于循环状态 即判断最近几次选择是否全都已经在之前做出过
        if len(self.choose) > 3 and \
                self.choose[-3] in self.choose[:-3] and \
                self.choose[-2] in self.choose[:-3] and \
                self.choose[-1] in self.choose[:-3]:
            # 如果进入循环 将circle参数设为身体长度
            self.circle = len(self.body)
            self.choose = []
        # 对当前状态做出判断 并做出最有利的选择
        self.image_road = []
        head = self.body[-1]
        # 生成前往食物的路
        road_to_food = search_the_road(head, food, self.airs_list)
        # 有前往食物的路
        if road_to_food is not None:
            road = get_road(head, road_to_food[0], food)
            target = road[0]
            self.image_body = get_image_body(self.body, road)
            # 如果吃完这个食物游戏就胜利了 那么直接吃
            if len(self.body) == M * N - 1 and target == food:
                self.action = 'food'
                next_cell = target
            # 否则 判断吃食物是否安全
            elif self.check_safe(target, food) and \
                    (search_the_road(self.image_body[-1], self.image_body[0],
                     possible_airs(self.image_body[1:]))):
                # 安全 且没有整理身体的需要 那么前去吃食物
                if self.sort_body <= 0:
                    self.image_road = road
                    self.action = 'food'
                    next_cell = target
                # 否则 开始整理身体 前往离尾巴最远的那条路
                else:
                    next_cell = None
            else:
                next_cell = None
        else:
            next_cell = None

        if self.circle > 0:
            # 循环状态下摆脱循环的尝试 每进行一步circle参数都会减一 知道circle小于0
            self.action = 'tail'
            next_cell = self.get_long_road(food, circle=True)
            self.sort_body -= 1
            self.circle -= 1
        elif next_cell is None:
            # 不处于循环状态 正常地前往沿着尾巴的最长路径 对蛇身进行整理
            self.action = 'long'
            next_cell = self.get_long_road(food)
            self.sort_body -= 1
        # 记录下小蛇每一步做出的选择
        self.choose.append((head, next_cell))
        # 改变方向
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


# 每个格子的大小
CELL_SIZE = 30
# 格子之间缝隙的大小
LINE_SIZE = 4
# 地图格子大小 M为宽度 N为长度 可修改
M, N = 12, 12
# 生成窗口的大小
SCREEN_WIDTH = CELL_SIZE * M + LINE_SIZE * (M + 1)
SCREEN_HEIGHT = CELL_SIZE * N + LINE_SIZE * (N + 1)
# 每一个时间步会停留的时间（s）
ONE_COUNT = 0.4

# 可视化部分用到的一些颜色
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
