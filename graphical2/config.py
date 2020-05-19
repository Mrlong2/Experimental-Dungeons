import pygame
CELL_WIDTH = 64
CELL_HEIGHT = 64

#Sprites
S_WALL = pygame.transform.scale(pygame.image.load("images/wall2.png"), (CELL_WIDTH, CELL_HEIGHT))
S_FLOOR = pygame.transform.scale(pygame.image.load("images/floor2.png"), (CELL_WIDTH, CELL_HEIGHT))
S_SPARK = pygame.transform.scale(pygame.image.load("images/spark1.png"), (CELL_WIDTH//4, CELL_HEIGHT//4))

#crab
S_CRAB = pygame.transform.scale(pygame.image.load("images/crab.png"), (CELL_WIDTH, CELL_HEIGHT))
S_CRAB_DIE = pygame.transform.scale(pygame.image.load("images/crab_dead.png"), (CELL_WIDTH, CELL_HEIGHT))
#human sprite
S_HUMAN = pygame.transform.scale(pygame.image.load("images/human2.png"), (1 * CELL_WIDTH, 2 * CELL_HEIGHT))
#skaven
S_SKAVEN = pygame.transform.scale(pygame.image.load("images/skaven.png"), (1 * CELL_WIDTH, 2 * CELL_HEIGHT))
S_SKAVEN_DIE = pygame.transform.scale(pygame.image.load("images/skaven_dead.png"), (CELL_WIDTH, CELL_HEIGHT))
