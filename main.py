import random
import time
import os
import pygame   # pip install pygame

WIDTH = 10
HEIGHT = 10
TILE_SIZE = 40
TREE = 'T'
WATER = 'W'
FIRE = 'F'
EMPTY = '.'
HELICOPTER = 'H' # Желтый-вертолет

class Game:
    def __init__(self):
        self.grid = [[EMPTY for _ in range(WIDTH)] for _ in range(HEIGHT)]
        self.helicopter_pos = [0, 0]
        self.score = 0
        self.lives = 3
        self.water_capacity = 1
        self.steps = 0

        self.generate_trees()
        self.generate_water()

        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH * TILE_SIZE, HEIGHT * TILE_SIZE))
        pygame.display.set_caption("Helicopter Game")
        self.clock = pygame.time.Clock()

    def generate_trees(self):
        for _ in range(5):
            x = random.randint(0, HEIGHT - 1)
            y = random.randint(0, WIDTH - 1)
            if self.grid[x][y] == EMPTY:
                self.grid[x][y] = TREE

    def generate_water(self):
        for _ in range(3):
            x = random.randint(0, HEIGHT - 1)
            y = random.randint(0, WIDTH - 1)
            if self.grid[x][y] == EMPTY:
                self.grid[x][y] = WATER

    def generate_fire(self):
        for _ in range(2):
            x = random.randint(0, HEIGHT - 1)
            y = random.randint(0, WIDTH - 1)
            if self.grid[x][y] == TREE:
                self.grid[x][y] = FIRE

    def move_helicopter(self, direction):
        if direction == 'up' and self.helicopter_pos[0] > 0:
            self.helicopter_pos[0] -= 1
        elif direction == 'down' and self.helicopter_pos[0] < HEIGHT - 1:
            self.helicopter_pos[0] += 1
        elif direction == 'left' and self.helicopter_pos[1] > 0:
            self.helicopter_pos[1] -= 1
        elif direction == 'right' and self.helicopter_pos[1] < WIDTH - 1:
            self.helicopter_pos[1] += 1

        self.check_interaction()

    def check_interaction(self):
        x, y = self.helicopter_pos
        if self.grid[x][y] == TREE:
            print("Вы прошли мимо дерева.")
        elif self.grid[x][y] == WATER:
            print("Вы набрали воду")
            self.water_capacity += 1
        elif self.grid[x][y] == FIRE:
            if self.water_capacity > 0:
                print("Вы потушили пожар!")
                self.score += 5
                self.water_capacity -= 1
                self.grid[x][y] = EMPTY
            else:
                print("Нет воды для тушения пожара!")

    def display(self):
        self.screen.fill((255, 255, 255)) 
        for i in range(HEIGHT):
            for j in range(WIDTH):
                color = (0, 255, 0) if self.grid[i][j] == TREE else (0, 0, 255) if self.grid[i][j] == WATER else (255, 0, 0) if self.grid[i][j] == FIRE else (255, 255, 255)
                pygame.draw.rect(self.screen, color, (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        helicopter_color = (255, 255, 0) 
        pygame.draw.rect(self.screen, helicopter_color, (self.helicopter_pos[1] * TILE_SIZE, self.helicopter_pos[0] * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        pygame.display.flip() 

    def play(self):
        while self.lives > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.move_helicopter('up')
                    elif event.key == pygame.K_s:
                        self.move_helicopter('down')
                    elif event.key == pygame.K_a:
                        self.move_helicopter('left')
                    elif event.key == pygame.K_d:
                        self.move_helicopter('right')

            self.steps += 1

            if self.steps % 12 == 0:
                self.generate_trees()
                self.generate_fire()

            self.display()
            self.clock.tick(10)  

if __name__ == "__main__":
    game = Game()
    game.play()
