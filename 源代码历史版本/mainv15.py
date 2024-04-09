"""
不管不顾的随机之蛇 效率低到令人发指
但是好歹理论上它能够填满整个屏幕了
所以姑且算是一个解法了
接下来想要提高效率 就得对整体结构进行大的改动了

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
        self.food = Food()
        self.food.check(self.snake)

        self.draw_screen()
        pygame.display.update()
        time.sleep(SPEED * TIMES)

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
        # 想象中的蛇身
        # self.draw_lines(self.snake.image_body, size=20, color=GREEN)
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
        # 画眼睛
        self.draw_eyes()

        # 画食物
        x = (self.food.x - 1) * CELL_SIZE + self.food.x * LINE_SIZE
        y = (self.food.y - 1) * CELL_SIZE + self.food.y * LINE_SIZE
        pygame.draw.rect(self.screen, ORANGE, (x, y, CELL_SIZE, CELL_SIZE), 0)

    def draw_eyes(self):
        pass
        # pygame.draw.rect(self.screen, BLACK, (x + (CELL_SIZE - size) // 2,
        # y + (CELL_SIZE - size) // 2, size, size), 0)

    def draw_lines(self, lines, size=20, color=(0, 0, 0)):
        if lines:
            for i in lines:
                x = (i[0] - 1) * CELL_SIZE + i[0] * LINE_SIZE
                y = (i[1] - 1) * CELL_SIZE + i[1] * LINE_SIZE
                pygame.draw.rect(self.screen, color, (x + (CELL_SIZE - size) // 2,
                                                      y + (CELL_SIZE - size) // 2, size, size), 0)

    def run(self):
        global TIMES
        pause = False
        count = 0
        while True:
            count += 1
            start_time = time.time()
            while True:
                # 按键检测
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT and self.snake.direction != (1, 0):
                            self.snake.direction = (-1, 0)
                        elif event.key == pygame.K_RIGHT and self.snake.direction != (-1, 0):
                            self.snake.direction = (1, 0)
                        elif event.key == pygame.K_UP and self.snake.direction != (0, 1):
                            TIMES /= 2
                        elif event.key == pygame.K_DOWN and self.snake.direction != (0, -1):
                            TIMES *= 2
                        elif event.key == pygame.K_p:
                            if pause:
                                pause = False
                            else:
                                pause = True
                if not pause:
                    break

            self.snake.think(self.food)
            self.snake.move_and_eat(self.food)

            if self.snake.check():
                print("You have walked " + str(count) + " counts!")
                count = 0
                self.snake = Snake()

            # 展示
            self.draw_screen()

            self.food.check(self.snake)

            pygame.display.update()
            end_time = time.time()
            if end_time - start_time < SPEED * TIMES:
                time.sleep(SPEED * TIMES - (end_time - start_time))


class Snake:
    def __init__(self):
        self.road_to_food = []
        self.x, self.y = (M + 1) // 2, (N + 1) // 2
        self.length = 3
        self.body = []
        self.image_body = []
        self.image_road = []
        self.action = None
        self.hungry = 0
        for i in range(self.length):
            x = (M + 1) // 2 + i + 1 - self.length
            y = (N + 1) // 2
            self.body.append((x, y))
        self.direction = (1, 0)

    def check(self):
        if len(self.body) == M * N:
            print("YOU WIN!")
            return True
        if (self.x, self.y) in self.body[:-1]:
            print("YOU EAT YOURSELF!")
            return True
        if self.x == 0 or self.y == 0 or self.x == M + 1 or self.y == N + 1:
            print("YOU EAT THE WALL!")
            return True

    def move_and_eat(self, food):
        self.x = self.body[-1][0] + self.direction[0]
        self.y = self.body[-1][1] + self.direction[1]
        self.body.append((self.x, self.y))
        if self.body[-1] == (food.x, food.y):
            # 吃到食物
            self.hungry = 0
            food.check(self)
        else:
            # 没有吃到食物
            self.body.pop(0)

    def turn_direction(self):
        self.direction = (self.direction[1], self.direction[0])
        if random.random() < 0.5:
            self.change_head()

    def change_head(self):
        self.direction = (-self.direction[0], -self.direction[1])

    def long_way(self, food):
        near_head = near_the_cell(self.body[-1])
        possible_cells = []
        for (x, y) in near_head:
            if (x, y) in self.body:
                pass
            else:
                possible_cells.append((x, y))

        possible_goals = []
        while len(possible_cells) != 0:
            goal = possible_cells.pop()
            image_body = []
            image_body += self.body
            image_body.append(goal)
            if goal != (food.x, food.y):
                image_body.pop(0)

            road_to_tail = search_the_road(image_body[-1], image_body[0], image_body[1:])
            if road_to_tail is not None:
                possible_goals.append(goal)

        if len(possible_goals) == 0:
            return None
        else:
            goals = queue.PriorityQueue()
            body_direction_x, body_direction_y = 0, 0
            for index in range(-6, 0):
                body_direction_x += self.body[index + 1][0] - self.body[index][0]
                body_direction_y += self.body[index + 1][1] - self.body[index][1]
            for (x, y) in possible_goals:
                cost = 10
                if abs(body_direction_x) >= 2 and x - self.x != 0:
                    cost -= 1
                elif abs(body_direction_y) >= 2 and y - self.y != 0:
                    cost -= 1
                else:
                    if x - self.x == self.x - self.body[-2][0] and \
                            y - self.y == self.y - self.body[-1][1]:
                        cost -= 1
                goals.put((cost, (x, y)))
            return goals.get()[1]

    def get_image_road(self, came_from, goal):
        if goal not in came_from:
            return []
        self.image_road = []
        while True:
            self.image_road.append(goal)
            if came_from[goal] == (self.x, self.y):
                break
            goal = came_from[goal]
        self.image_road.reverse()

    def get_image_body(self):
        self.image_body = []
        self.image_body += self.body

        move_len = len(self.image_road) - 1
        self.image_body += self.image_road
        self.image_body = self.image_body[move_len:]

    def scanning(self):
        frontier = []
        used_cells = []
        frontier.append(self.image_body[-1])
        possible_cells = M * N - len(self.image_body)
        while frontier:
            current = frontier.pop()
            for next_cell in near_the_cell(current):
                if next_cell in self.image_body or next_cell[0] in [0, M + 1] \
                        or next_cell[1] in [0, N + 1]:
                    pass
                elif next_cell not in used_cells and next_cell not in frontier:
                    frontier.append(next_cell)
            possible_cells -= 1
            if current != self.image_body[-1]:
                used_cells.append(current)
        return len(used_cells)

    def get_random_road(self, food):
        near_head = near_the_cell((self.body[-1][0], self.body[-1][1]))
        possible_cells = []
        for (x, y) in near_head:
            if (x, y) not in self.body:
                possible_cells.append((x, y))

        possible_goals = []
        for goal in possible_cells:
            image_body = []
            image_body += self.body
            image_body.append(goal)
            if goal != (food.x, food.y):
                image_body.pop(0)
            road_to_tail = search_the_road(image_body[-1], image_body[0], image_body[1:])
            if road_to_tail is not None:
                possible_goals.append(goal)
        if len(possible_goals) == 0:
            return None
        return possible_goals[random.randint(0, len(possible_goals) - 1)]

    def think(self, food):
        self.hungry += 1

        road_to_tail = search_the_road((self.x, self.y), self.body[0]
                                       , self.body[1:])
        road_to_food = search_the_road((self.x, self.y), (food.x, food.y)
                                       , self.body[1:])

        if not road_to_food:
            # 无法前往食物 前往尾巴
            self.road_to_food = []
            goal = self.body[0]
            long_road = self.long_way(food)
            if long_road is not None:
                self.action = "long"
                goal = long_road
                came_from = {goal: self.body[-1]}
            else:
                self.action = "tail"
                came_from, cost_so_far = road_to_tail
        elif len(self.body) == M * N - 1:
            goal = (food.x, food.y)
            came_from, cost_so_far = road_to_food
        else:
            # 可以前往食物 判断是否安全
            self.action = "food"
            goal = (food.x, food.y)
            came_from, cost_so_far = road_to_food
            self.get_image_road(came_from, goal)
            self.road_to_food = []
            self.road_to_food += self.image_road
            self.get_image_body()
            if not search_the_road(self.image_body[-1], self.image_body[0],
                                   self.image_body[1:]):
                # 不安全 前往尾巴
                goal = self.body[0]

                long_road = self.long_way(food)
                if long_road is not None:
                    self.action = "long"
                    goal = long_road
                    came_from = {goal: self.body[-1]}
                else:
                    self.action = "tail"
                    came_from, cost_so_far = road_to_tail
            else:
                pass

        random_goal = self.get_random_road(food)
        if self.hungry >= M * N and random_goal is not None:
            self.direction = (random_goal[0] - self.body[-1][0],
                              random_goal[1] - self.body[-1][1])
        else:
            self.get_image_road(came_from, goal)
            # 前进
            self.direction = (self.image_road[0][0] - self.x, self.image_road[0][1] - self.y)


class Food:
    def __init__(self):
        self.x = random.randint(1, M)
        self.y = random.randint(1, N)

    def check(self, snake):
        if (self.x, self.y) not in snake.body:
            return
        possible_cells = []
        for x in range(1, M + 1):
            for y in range(1, N + 1):
                if (x, y) not in snake.body:
                    possible_cells.append((x, y))
        if len(possible_cells) == 0:
            return
        random_number = random.randint(0, len(possible_cells) - 1)
        self.x, self.y = possible_cells[random_number]


def near_the_cell(current):
    near = []
    for (x, y) in [(current[0] + 1, current[1]), (current[0] - 1, current[1]),
                   (current[0], current[1] + 1), (current[0], current[1] - 1)]:
        if 0 < x < M + 1 and 0 < y < N + 1:
            near.append((x, y))
    return near


def search_the_road(start, goal, body):
    frontier = queue.PriorityQueue()
    frontier.put((0, start))
    came_from, cost_so_far = {}, {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()[1]
        if current == goal:
            break
        for next in near_the_cell(current):
            new_cost = cost_so_far[current] + 1

            if next in body or next[0] in [0, M + 1] or next[1] in [0, N + 1]:
                pass
            elif next not in cost_so_far or new_cost < cost_so_far[current]:
                cost_so_far[next] = new_cost
                priority = new_cost + abs(next[0] - goal[0]) + abs(next[1] - goal[1])
                frontier.put((priority, next))
                came_from[next] = current
    if goal not in came_from:
        return None
    return came_from, cost_so_far


CELL_SIZE = 30
LINE_SIZE = 1
M, N = 10, 10
SCREEN_WIDTH = CELL_SIZE * M + LINE_SIZE * (M + 1)
SCREEN_HEIGHT = CELL_SIZE * N + LINE_SIZE * (N + 1)
SPEED = 0.06
TIMES = 1

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
