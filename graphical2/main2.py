import pygame
from graphical2 import map1gen
from graphical2 import config
import os
import json
import tcod
import time

global ACTORS, PROPS, TILES, SELECTED, RUN_GAME, SURFACE_MAIN, FONTS, TIMESINCE, start_time


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


###############################################################################################################
#                                           OBJECT CONTROL
###############################################################################################################

# actors
# game objects need x, y, type, health, inventory,
class obj_entity:
    def __init__(self, x, y, objtype, sprite, blockpath=False, health=None, inventory=None):
        # moving and location
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0

        # object type
        self.type = objtype
        self.blockpath = blockpath

        # Question: what the heck is up with that retarded "self.owner" stuff?
        # Answer: it's a workaround, python doesn't have a proper "parent" reference.  We need to get stuff from other
        # components, so that's the work around.

        # sprite and drawing
        self.sprite = sprite
        if self.sprite:
            self.sprite.owner = self

        # health
        self.health = health
        if self.health:
            self.health.owner = self

        # inventory
        self.inventory = inventory
        if self.inventory:
            self.inventory.owner = self


#### OBJECT COMPONENTS ####

# controls an object's health
class com_health:
    def __init__(self):
        self.owner = None


# controls drawing and stuff
class com_sprite:
    def __init__(self, img, spriteoffsetx=0, spriteoffsety=0):
        self.img = img
        self.spriteoffsetx = spriteoffsetx
        self.spriteoffsety = spriteoffsety
        self.owner = None

    def drawself(self, surf):
        surf.blit(self.img, (
            (self.owner.x * config.CELL_WIDTH) + self.spriteoffsetx,
            (self.owner.y * config.CELL_HEIGHT) + self.spriteoffsety))


# things have inventories
class com_inventory:
    def __init__(self):
        self.owner = None


# some objects can be picked up and used as weapons.
class com_item:
    def __init__(self):
        self.owner = None


###############################################################################################################
#                                           GAME LOGIC AND FUNCTIONS
###############################################################################################################


# functions for stuff
def query_object(x, y, actors=True, props=True):
    found = []
    for obj in ACTORS:
        if (obj.x == x) and (obj.y == y):
            found += obj

    for obj in PROPS:
        if (obj.x == x) and (obj.y == y):
            found += obj

    return found


def query_blocked(x, y, actors=True, props=True):
    # set block to false
    block = False
    # The object must be BOTH at the same x and y values, AND be blocking
    # break out because multiple blocks is redundant.
    for obj in ACTORS:
        if ((obj.x == x) and (obj.y == y)) and (obj.blockpath == True):
            block = True
            break
    for obj in PROPS:
        if ((obj.x == x) and (obj.y == y)) and (obj.blockpath == True):
            block = True
            break
    return block


# object processing
def move_objects():
    global ACTORS
    for act in ACTORS:
        # if either one changes
        if (act.dx != 0) or (act.dy != 0):
            # make note of where it should go
            x, y = act.dx + act.x, act.dy + act.y
            # print(x, y)
            # check if that space is blocked
            if not (query_blocked(x, y)):
                # move there
                act.x = x
                act.y = y
            # either way, set our desired move back to zero
            act.dx, act.dy = 0, 0


# drawing
def draw_game():
    # global ACTORS, PROPS, TILES, SELECTED, RUN_GAME, SURFACE_MAIN
    global TIMESINCE
    SURFACE_MAIN.fill((0, 0, 0))
    for obj in PROPS:
        obj.sprite.drawself(SURFACE_MAIN)

    for obj in ACTORS:
        obj.sprite.drawself(SURFACE_MAIN)
    # fps counter
    # fpstxt = FONTS['fps'].render(TIMESINCE, 0, (255, 255, 255))
    # SURFACE_MAIN.blit(fpstxt, (100, 100))

    pygame.display.flip()


# game loop
def game_main_loop():
    # global ACTORS, PROPS, TILES, SELECTED, RUN_GAME, SURFACE_MAIN
    global start_time, TIMESINCE
    while RUN_GAME:
        start_time = time.time()
        # game states

        # check keyboard
        get_inputs()

        # process game objects
        move_objects()
        # enemy ai

        # draw on screen
        draw_game()
        TIMESINCE = str("FPS: " + str(1.0 / (time.time() - start_time)))
        # print("FPS: " + str(1.0 / (time.time() - start_time)))


# initialize game
def game_initialize():
    pygame.init()
    # global variables
    global ACTORS, PROPS, TILES, SELECTED, RUN_GAME, SURFACE_MAIN, FONTS, TIMESINCE

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
    ACTORS, PROPS, SELECTED = map1gen.map_1_generate(25, 6)
    # set a font i guess.  wow there's a lot of globals even though someone told me globals are bad
    FONTS = {"fps": pygame.font.SysFont("Arial", 80)}
    TIMESINCE = "0.0"


if __name__ == '__main__':
    print("working directory is" + os.getcwd())
    game_initialize()
    game_main_loop()
