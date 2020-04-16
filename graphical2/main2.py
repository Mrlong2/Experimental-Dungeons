import pygame
from graphical2 import map1gen
from graphical2 import config
import os
import json
import tcod
import time

global ACTORS, PROPS, TILES, SELECTED, RUN_GAME, SURFACE_MAIN


# keyboard inputs
def get_inputs():
    global RUN_GAME, SELECTED
    for event in pygame.event.get():
        # if exit is pressed
        if event.type == pygame.QUIT:
            RUN_GAME = False  # set to false

        if event.type == pygame.KEYDOWN:  # if the event is a key down press
            if event.key == pygame.K_UP:
                SELECTED.dy = -1

            if event.key == pygame.K_DOWN:
                SELECTED.dy = 1

            if event.key == pygame.K_LEFT:
                SELECTED.dx = -1

            if event.key == pygame.K_RIGHT:
                SELECTED.dx = 1


# actors
# game objects need x, y, type, health, inventory,
class gameobject:
    def __init__(self, x, y, objtype, sprite=None, spriteoffsetx=0, spriteoffsety=0):
        # moving and location
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0

        # object type
        self.type = objtype
        self.sprite = sprite
        self.spriteoffsetx = spriteoffsetx
        self.spriteoffsety = spriteoffsety

    def drawself(self, surf):
        #I LITERALLY SPENT HOURS DEBUGGING THIS WHY CANT I USE SURFACE MAIN, WHY CANT I USE IT?!!?!?!?!?
        surf.blit(self.sprite, ((self.x * config.CELL_WIDTH)+self.spriteoffsetx, (self.y * config.CELL_HEIGHT)+self.spriteoffsety))


# components

#object processing
def move_objects():
    global ACTORS
    for act in ACTORS:
        if act.dx != 0:
            act.x += act.dx
            act.dx = 0
        if act.dy != 0:
            act.y += act.dy
            act.dy = 0




# drawing
def draw_game():
    # global ACTORS, PROPS, TILES, SELECTED, RUN_GAME, SURFACE_MAIN
    SURFACE_MAIN.fill((255, 255, 255))
    for obj in PROPS:
        obj.drawself(SURFACE_MAIN)

    for obj in ACTORS:
        obj.drawself(SURFACE_MAIN)
    pygame.display.flip()


# game loop
def game_main_loop():
    # global ACTORS, PROPS, TILES, SELECTED, RUN_GAME, SURFACE_MAIN
    while RUN_GAME:
        #start_time = time.time()
        # game states

        # check keyboard
        get_inputs()

        # process game objects
        move_objects()
        # enemy ai

        # draw on screen
        draw_game()
        #print("FPS: ", 1.0 / (time.time() - start_time))


# initialize game
def game_initialize():
    pygame.init()
    # global variables
    global ACTORS, PROPS, TILES, SELECTED, RUN_GAME, SURFACE_MAIN

    # Actors are objects that get ticked every cycle to see if they need to do something.  This isn't a good idea for
    # things that don't need to get ticked. (A plant needs ticks to grow, furnace needs ticks to smelt.)
    ACTORS = []
    # Props do not get ticked, and thus need something else to interact with them. (like random garbage on the ground.)
    PROPS = []
    # Who you're controlling.
    SELECTED = None
    # Checks whether the game should exit.
    RUN_GAME = True
    # set the screen
    SURFACE_MAIN = pygame.display.set_mode((800, 600))
    ACTORS, PROPS, SELECTED = map1gen.map_1_generate(10, 10)


if __name__ == '__main__':
    print("working directory is" + os.getcwd())
    game_initialize()
    game_main_loop()
