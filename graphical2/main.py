import pygame
from graphical2 import map1gen
from graphical2 import config
import json
import tcod


# keyboard inputs
def get_inputs():
    global RUN_GAME, SELECTED
    for event in pygame.event.get():
        # if exit is pressed
        if event.type == pygame.QUIT:
            RUN_GAME = False  # set to false

        if event.type == pygame.KEYDOWN:  # if the event is a key down press
            if event.key == pygame.K_UP:
                SELECTED.dx = (0, 1)

            if event.key == pygame.K_DOWN:
                SELECTED.dx = (0, -1)

            if event.key == pygame.K_LEFT:
                SELECTED.dx = (1, 0)

            if event.key == pygame.K_RIGHT:
                SELECTED.dx = (-1, 0)


# actors
# game objects need x, y, type, health, inventory,
class gameobject:
    def __init__(self, x, y, objtype, sprite=None, spriteoffsetx=0, spriteoffsety=0):
        #moving and location
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0

        #object type
        self.type = objtype
        self.sprite = sprite
        self.spriteoffsetx = spriteoffsetx
        self.spriteoffsety = spriteoffsety




    def drawself(self):
        SURFACE_MAIN.bilt(self.sprite,(self.x * config.CELL_WIDTH, self.y * config.CELL_HEIGHT))





# components
class spritecontroler:
    pass

# drawing
def draw_game():
    for object in PROPS:
        object.drawself()

    for object in ACTORS:
        object.drawself()
    SURFACE_MAIN.flip()


# game loop
def game_main_loop():
    while RUN_GAME:
        # game states

        # check keyboard
        get_inputs()

        # process game objects

        # enemy ai

        # draw on screen
        draw_game()

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
    #set the screen
    SURFACE_MAIN = pygame.display.set_mode((800, 600))
    ACTORS, PROPS = map1gen.map_1_generate(10, 10)


if __name__ == '__main__':
    game_initialize()
    game_main_loop()
