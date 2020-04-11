import pygame

#game sizes
GAME_WIDTH = 1920
GAME_HEIGHT = 1000
CELL_WIDTH = 128
CELL_HEIGHT = 128

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
S_WALL = pygame.transform.scale(pygame.image.load("images/wall2.png"), (CELL_WIDTH, CELL_HEIGHT))
S_FLOOR = pygame.transform.scale(pygame.image.load("images/floor2.png"), (CELL_WIDTH, CELL_HEIGHT))
S_GIRL = pygame.transform.scale(pygame.image.load("images/human2.png"), (1*CELL_WIDTH, 2*CELL_HEIGHT))
