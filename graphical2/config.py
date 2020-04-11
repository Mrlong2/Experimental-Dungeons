import pygame
CELL_WIDTH = 32
CELL_HEIGHT = 32

#Sprites
S_WALL = pygame.transform.scale(pygame.image.load("images/wall2.png"), (CELL_WIDTH, CELL_HEIGHT))
S_FLOOR = pygame.transform.scale(pygame.image.load("images/floor2.png"), (CELL_WIDTH, CELL_HEIGHT))
S_GIRL = pygame.transform.scale(pygame.image.load("images/human2.png"), (1*CELL_WIDTH, 2*CELL_HEIGHT))
