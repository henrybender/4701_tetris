import pygame
import random
import tetris_player
import numpy as np


colors = [          # rbg color values for tetromino shapes
    (0, 0, 0),
    (128, 0, 255),   # purple
    (255, 0, 255),   # magenta
    (255, 20, 147),   # pink
    (255, 0, 128),   # red pink
    (255, 165, 0),   # light orange
    (255, 153, 51),   # orange
    (255, 255, 0),   # yellow
    (153, 255, 0),   # lime green
    (0, 250, 154),   # spring green
    (51, 255, 255),   # light blue
    (0, 191, 255),   # sky blue
    (100, 149, 237),   # flower blue
    (102, 102, 255)   # blue
]


class Figure:
    x = 0
    y = 0

    #   tetromino defined by the following 4 x 4 matrix

    #    0   1   2   3
    #    4   5   6   7
    #    8   9   10  11
    #    12  13  14  15

    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],      # I
        [[4, 5, 9, 10], [2, 6, 5, 9]],      # Z
        [[6, 7, 9, 10], [1, 5, 6, 10]],     # S
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],      # J
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],      # L
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],      # T
        [[1, 2, 5, 6]],     # O

        # smaller tetromino pieces
        [[1, 1, 1, 1]],      # 1p
        [[1, 1, 2, 2], [3, 3, 7, 7]],      # 2p
        [[5, 5, 6, 7], [2, 2, 6, 10]],      # 3pI
        [[0, 1, 1, 5], [6, 10, 10, 11], [6, 2, 2, 3], [0, 4, 4, 5]],      # 3pL
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])


class Tetris:
    level = 2
    score = 0
    cleared = 0
    pieces = 0
    state = "start"
    field = []
    height = 0
    width = 0
    x = 100
    y = 100
    zoom = 20
    figure = None

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.pieces = 0
        self.state = "start"
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def new_figure(self):
        self.figure = Figure(3, 0)
        self.pieces += 1

    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.cleared += lines
        self.score += lines ** 2

    def get_holes(self):
        holes = 0
        # for i in range(self.height):
        for col in zip(*self.field):
            row = 0
            while row < self.height and col[row] == 0:
                row += 1
            holes += len([x for x in col[row + 1:] if x == 0])
            # if self.field[i][j] == 0:
            #   holes += 1
        print("holes : " + str(holes) + "\n")
        return holes

    def get_height_variability(self):
        mask = np.array(self.field) != 0
        invert_heights = np.where(
            mask.any(axis=0), np.argmax(mask, axis=0), self.height)
        heights = self.height - invert_heights
        total_height = np.sum(heights)
        currs = heights[:-1]
        nexts = heights[1:]
        diffs = np.abs(currs - nexts)
        variability = np.sum(diffs)
        print("total height : " + str(total_height) + "\n")
        print("variability : " + str(variability) + "\n")
        return total_height, variability

    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j +
                                                  self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"

    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation


# initialize game engine
pygame.init()

# rgb colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)

SCREEN_WIDTH = 500  # 400
SCREEN_HEIGHT = 800  # 500
size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Tetris")

# loop until user closes
done = False
pause = False
clock = pygame.time.Clock()
fps = 25
game = Tetris(30, 15)  # Tetris(20, 10)
counter = 0

pressing_down = False

while not done:
    if game.figure is None:
        game.new_figure()
    counter += 1
    if counter > 100000:
        counter = 0

    if counter % (fps // game.level // 2) == 0 or pressing_down:
        if game.state == "start":
            game.go_down()

    for event in list(pygame.event.get()) + tetris_player.random_move():
        # for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotate()
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                game.go_side(-1)
            if event.key == pygame.K_RIGHT:
                game.go_side(1)
            if event.key == pygame.K_SPACE:
                game.go_space()
            if event.key == pygame.K_ESCAPE:
                game.__init__(20, 10)

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_DOWN:
            pressing_down = False

    screen.fill(WHITE)

    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, GRAY, [
                             game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, colors[game.field[i][j]],
                                 [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

    if game.figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.figure.image():
                    pygame.draw.rect(screen, colors[game.figure.color],
                                     [game.x + game.zoom * (j + game.figure.x) + 1,
                                      game.y + game.zoom *
                                      (i + game.figure.y) + 1,
                                      game.zoom - 2, game.zoom - 2])

    font_small = pygame.font.SysFont('Corbel', 24, True, False)
    font_large = pygame.font.SysFont('Corbel', 60, True, False)
    font_med = pygame.font.SysFont('Corbel', 36, True, False)
    text_score = font_small.render("Score: " + str(game.score), True, BLACK)
    text_pieces = font_small.render("Pieces: " + str(game.pieces), True, BLACK)
    text_game_over = font_large.render("Game Over", True, BLACK)
    text_game_over1 = font_med.render("Press ESC", True, BLACK)

    screen.blit(text_score, [12, 12])
    screen.blit(text_pieces, [12, 36])
    if game.state == "gameover":
        screen.blit(text_game_over, [
                    (SCREEN_WIDTH-text_game_over.get_width())/2, 200])
        screen.blit(text_game_over1, [
                    (SCREEN_WIDTH-text_game_over1.get_width())/2, 265])
        pause = True
        done = True
        game.get_holes()
        game.get_height_variability()

    pygame.display.flip()
    clock.tick(fps)

while pause:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
