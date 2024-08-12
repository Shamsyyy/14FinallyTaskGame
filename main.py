import random
import time
import os

WIDTH = 10
HEIGHT = 10
TREE = 'T'
WATER = 'W'
FIRE = 'F'
EMPTY = '.'
HELICOPTER = 'H'

class Game:
    def __init__(self):
        self.grid = [[EMPTY for _ in range(WIDTH)] for _ in range(HEIGHT)]
        self.helicopter_pos = (0, 0)
        self.score = 0
        self.lives = 3
        self.water_capacity = 1
        self.steps = 0

        self.generate_trees()
        self.generate_water()

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
        x, y = self.helicopter_pos
        if direction == 'w' and x > 0:
            x -= 1
        elif direction == 's' and x < HEIGHT - 1:
            x += 1
        elif direction == 'a' and y > 0:
            y -= 1
        elif direction == 'd' and y < WIDTH - 1:
            y += 1

        self.helicopter_pos = (x, y)

       
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
        os.system('cls' if os.name == 'nt' else 'clear') 
        for i in range(HEIGHT):
            for j in range(WIDTH):
                if (i, j) == self.helicopter_pos:
                    print(HELICOPTER, end=' ')
                else:
                    print(self.grid[i][j], end=' ')
            print()
        print(f"Очки: {self.score}, Жизни: {self.lives}, Резервуар: {self.water_capacity}")

    def play(self):
        while self.lives > 0:
            self.display()
            move = input("Введите движение (w/a/s/d): ")
            self.move_helicopter(move)
            self.steps += 1

            if self.steps % 12 == 0:
                self.generate_trees()
                self.generate_fire()

if __name__ == "__main__":
    game = Game()
    game.play()
