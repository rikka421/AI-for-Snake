"""
加入A*算法 说实话效果很一般
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
        self.food = Food()
        self.food.check(self.snake)

    def draw_screen(self):
        # 覆盖背景
        self.screen.fill(BACKGROUND)
        # 画网格线
        for x in range(0, SCREEN_WIDTH, CELL_SIZE + LINE_SIZE):
            pygame.draw.rect(self.screen, BLACK, (x, 0, LINE_SIZE, SCREEN_HEIGHT), 0)
        for y in range(0, SCREEN_HEIGHT, CELL_SIZE + LINE_SIZE):
            pygame.draw.rect(self.screen, BLACK, (0, y, SCREEN_WIDTH, LINE_SIZE), 0)
        # 画蛇
        for i in self.snake.body:
            x = (i[0] - 1) * CELL_SIZE + i[0] * LINE_SIZE
            y = (i[1] - 1) * CELL_SIZE + i[1] * LINE_SIZE
            pygame.draw.rect(self.screen, LIGHT, (x, y, CELL_SIZE, CELL_SIZE), 0)
        # 画食物
        x = (self.food.x - 1) * CELL_SIZE + self.food.x * LINE_SIZE
        y = (self.food.y - 1) * CELL_SIZE + self.food.y * LINE_SIZE
        pygame.draw.rect(self.screen, ORANGE, (x, y, CELL_SIZE, CELL_SIZE), 0)

    def run(self):
        pause = False
        while True:

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
                            self.snake.direction = (0, -1)
                        elif event.key == pygame.K_DOWN and self.snake.direction != (0, -1):
                            self.snake.direction = (0, 1)
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
                # time.sleep(1)
                pygame.quit()
                sys.exit()

            self.food.check(self.snake)
            self.draw_screen()

            pygame.display.update()
            if TEST:
                time.sleep(min(SPEED + 0.002 * self.snake.length, MIN_SPEED)*TEST_TIMES)
            else:
                time.sleep(min(SPEED + 0.002 * self.snake.length, MIN_SPEED))


class Snake:
    def __init__(self):
        self.x, self.y = (M + 1) // 2, (N + 1) // 2
        self.length = 3
        self.body = []
        for i in range(self.length):
            x = (M + 1) // 2 + i + 1 - self.length
            y = (N + 1) // 2
            self.body.append((x, y))
        self.direction = (1, 0)

    def check(self):
        if self.length == 100:
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

    def A_star_search(self, start, goal):
        frontier = queue.PriorityQueue()
        frontier.put((0, start))
        came_from, cost_so_far = {}, {}
        came_from[start] = None
        cost_so_far[start] = 0

        while not frontier.empty():
            current = frontier.get()[1]
            if current == goal:
                break
            for next in [(current[0]+1, current[1]), (current[0]-1, current[1]),
                         (current[0], current[1]+1), (current[0], current[1]-1)]:
                new_cost = cost_so_far[current] + 1
                if next in self.body or next[0] in [0, M+1] or next[1] in [0, N+1]:
                    pass
                elif next not in cost_so_far or  new_cost < cost_so_far[current]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + 1
                    frontier.put((priority, next))
                    came_from[next] = current

        return came_from, cost_so_far

    def think(self, food):
        came_from, cost_so_far = self.A_star_search((self.x, self.y), (food.x, food.y))

        if (food.x, food.y) not in came_from:
            return
        current = (food.x, food.y)
        while came_from[current] != (self.x, self.y):
            current = came_from[current]
            pass
        self.direction = (current[0] - self.x, current[1] - self.y)

    def original_think(self, food):
        walk_x, walk_y = food.x - self.x, food.y - self.y
        if (walk_x == self.direction[0] == 0 and walk_y * self.direction[1] < 0) \
                or (walk_y == self.direction[1] == 0 and walk_x * self.direction[0] < 0):
            self.turn_direction()
        else:
            if walk_x > 0 and self.direction != (-1, 0):
                self.direction = (1, 0)
            elif walk_x < 0 and self.direction != (1, 0):
                self.direction = (-1, 0)
            elif walk_y > 0 and self.direction != (0, -1):
                self.direction = (0, 1)
            elif walk_y < 0 and self.direction != (0, 1):
                self.direction = (0, -1)
        next_x, next_y = (self.x + self.direction[0], self.y + self.direction[1])
        if (next_x, next_y) in self.body \
                or next_x * next_y == 0 or next_x == M + 1 or next_y == N + 1:
            self.turn_direction()
            print(self.direction)
        next_x, next_y = (self.x + self.direction[0], self.y + self.direction[1])
        if (next_x, next_y) in self.body \
                or next_x * next_y == 0 or next_x == M + 1 or next_y == N + 1:
            self.change_head()
            print(self.direction)
            print()


class Food:
    def __init__(self):
        self.x = random.randint(1, M)
        self.y = random.randint(1, N)

    def check(self, snake):
        while (self.x, self.y) in snake.body:
            self.x = random.randint(1, M)
            self.y = random.randint(1, N)


CELL_SIZE = 40
LINE_SIZE = 1
M, N = 10, 10
SCREEN_WIDTH = CELL_SIZE * M + LINE_SIZE * (M + 1)
SCREEN_HEIGHT = CELL_SIZE * N + LINE_SIZE * (N + 1)

WHITE = (255, 255, 255)
ORANGE = (255, 120, 40)
GREY = (255, 245, 255)
DARK = (100, 100, 100)
LIGHT = (200, 200, 200)
BACKGROUND = (40, 40, 60)
BLACK = (0, 0, 0)
SPEED = 0.01
MIN_SPEED = 0.3
TEST = False
TEST_TIMES = 5

if __name__ == '__main__':
    game = Game()
    game.run()
