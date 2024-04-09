"""
不死之蛇 但是会陷入无法到达重点的真实
会进入死循环的胆小笨蛇
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
        self.draw_lines(self.snake.image_body, size=20, color=GREEN)
        # 要前往的道路
        self.draw_lines(self.snake.image_road[1:], size=20, color=YELLOW)
        # 蛇尾
        self.draw_lines([self.snake.body[-1]], size=20, color=PINK)
        # 蛇头
        self.draw_lines([self.snake.body[0]], size=20, color=BLUE)
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
            if count % 1000 == 0:
                print(count)
            if self.snake.check():
                print("You have walked " + str(count) + "time!")
                input()
                pygame.quit()
                sys.exit()

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
        for i in range(self.length):
            x = (M + 1) // 2 + i + 1 - self.length
            y = (N + 1) // 2
            self.body.append((x, y))
        self.direction = (1, 0)

    def check(self):
        if self.length == M * N:
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
            self.length += 1
            food.check(self)
        else:
            # 没有吃到食物
            self.body.pop(0)
        pass

    def turn_direction(self):
        self.direction = (self.direction[1], self.direction[0])
        if random.random() < 0.5:
            self.change_head()

    def change_head(self):
        self.direction = (-self.direction[0], -self.direction[1])

    def long_way(self):
        for i in range(len(self.body) - 3):
            goal = self.body[i + 1]
            road_to_tail = search_the_road((self.x, self.y), goal, self.body[:i + 1] + self.body[i + 2:])
            if road_to_tail:
                break
        return road_to_tail, goal

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

    def go_behind(self):
        pass

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

    def think(self, food):
        # 前往尾巴
        road_to_tail = search_the_road((self.x, self.y), self.body[0]
                                       , self.body[1:])

        # 可以前往尾巴
        road_to_food = search_the_road((self.x, self.y), (food.x, food.y)
                                       , self.body)
        if not road_to_food:
            # 无法前往食物 前往尾巴
            print("no road")
            self.road_to_food = []
            goal = self.body[0]
            came_from, cost_so_far = road_to_tail
        else:
            # 可以前往食物 判断是否安全
            goal = (food.x, food.y)
            came_from, cost_so_far = road_to_food
            self.get_image_road(came_from, goal)
            self.road_to_food = []
            self.road_to_food += self.image_road
            self.get_image_body()

            if not search_the_road(self.image_body[-1], self.image_body[0],
                                   self.image_body[1:]) or self.scanning() != M * N - len(self.image_body):
                # 不安全 前往尾巴
                print("not safe")
                goal = self.body[0]
                came_from, cost_so_far = road_to_tail
            else:
                pass

        if goal != (food.x, food.y):
            self.get_image_road(came_from, goal)

        # 前进
        self.direction = (self.image_road[0][0] - self.x, self.image_road[0][1] - self.y)


class Food:
    def __init__(self):
        self.x = random.randint(1, M)
        self.y = random.randint(1, N)

    def check(self, snake):
        while (self.x, self.y) in snake.body:
            self.x = random.randint(1, M)
            self.y = random.randint(1, N)


def near_the_cell(current):
    return [(current[0] + 1, current[1]), (current[0] - 1, current[1]),
            (current[0], current[1] + 1), (current[0], current[1] - 1)]


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
            new_cost = cost_so_far[current] + 1 + 0.1
            # 倾向于沿着身体前进
            for cell in near_the_cell(next):
                if cell in body:
                    new_cost -= 1 / (M * N) * len(body)
            """            # 倾向于不拐弯
            if (came_from[current] is not None) and \
                    came_from[current][0] - current[0] == current[0] - next[0] \
                    and came_from[current][1] - current[1] == current[1] - next[1]:
                new_cost -= 0.1"""

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
M, N = 48, 24
SCREEN_WIDTH = CELL_SIZE * M + LINE_SIZE * (M + 1)
SCREEN_HEIGHT = CELL_SIZE * N + LINE_SIZE * (N + 1)

WHITE = (255, 255, 255)
ORANGE = (255, 120, 40)
GREY = (255, 245, 255)
DARK = (100, 100, 100)
LIGHT = (200, 200, 200)
GREEN = (180, 230, 30)
PINK = (255, 170, 200)
BLUE = (100, 100, 180)
YELLOW = (255, 240, 0)
BACKGROUND = (40, 40, 60)
BLACK = (0, 0, 0)
SPEED = 0.06
TIMES = 1
TEST = True
if TEST:
    M, N = 30, 20
    TIMES = 10
    SCREEN_WIDTH = CELL_SIZE * M + LINE_SIZE * (M + 1)
    SCREEN_HEIGHT = CELL_SIZE * N + LINE_SIZE * (N + 1)

if __name__ == '__main__':
    game = Game()
    game.run()
