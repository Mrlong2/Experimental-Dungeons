import pygame

#game sizes
GAME_WIDTH = 1200
GAME_HEIGHT = 800
CELL_WIDTH = 64
CELL_HEIGHT = 64

#MAP VARS
MAP_WIDTH = 15
MAP_HEIGHT = 15


#color definintions
COLOR_BLACK = (0, 0, 0,)
COLOR_WHITE = (255, 255, 255)
COLOR_GREY = (100, 100, 100)

#game colors
COLOR_DEFAULT_BG = COLOR_GREY

#Sprites
S_WALL = pygame.transform.scale(pygame.image.load("wall1.png"), (CELL_WIDTH, CELL_HEIGHT))
S_FLOOR = pygame.transform.scale(pygame.image.load("floor1.png"), (CELL_WIDTH, CELL_HEIGHT))
S_GIRL = pygame.transform.scale(pygame.image.load("girl1.png"), (2*CELL_WIDTH, 4*CELL_HEIGHT))
