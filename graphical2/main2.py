import pygame
from graphical2 import map1gen
from graphical2 import config
import os
import json
import tcod
import time
import random

# Things that are too annoying to fix right now but should be incorporated in v3:
# SMART SPRITES(tm) - no need for annoying prams for every single little thing.


###############################################################################################################
#                                               INFO
###############################################################################################################
# quality of life / fun
# TODO smart object layering (Slicing)
# I just decided to go max spagetti on this one, I can optimize later.
# TODO some type of dictionary were we can summon pre-constructed items
# TODO Ranged weapons
# TODO better attack system
# TODO find out if its faster to make the sorting thing change the thing

# DONE! particle controller
#   todo make particles use floats and have time to turn for fractional values

# important!
# TODO turn system


global ACTORS, PROPS, TILES, SELECTED, RUN_GAME, SURFACE_MAIN, FONTS, TIMESINCE, start_time, PARTICLES, DEBUG


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

            if event.key == pygame.K_F1:
                DEBUG["showfps"] = not (DEBUG["showfps"])


###############################################################################################################
#                                           OBJECT CONTROL
###############################################################################################################

# actors
# game objects need x, y, type, health, inventory,
class obj_entity:
    def __init__(self, x, y, objtype, sprite, blockpath=False, health=None, inventory=None, ondeath=None, attack=None):
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

        self.attack = attack
        if self.attack:
            self.attack.owner = self

        # inventory
        self.inventory = inventory
        if self.inventory:
            self.inventory.owner = self

        self.ondeath = ondeath
        if self.ondeath:
            self.ondeath.owner = self

        self.ondeath = ondeath
        if self.ondeath:
            self.ondeath.owner = self


###########################
#### OBJECT COMPONENTS ####
###########################


# controls an object's health
class com_health:
    def __init__(self, hp, maxhp=None):
        self.owner = None
        self.hp = hp
        if maxhp == None:
            self.maxhp = hp
        else:
            self.maxhp = maxhp


# controls drawing and stuff
class com_sprite:
    def __init__(self, img, spriteoffsetx=0, spriteoffsety=0, layering=0):
        self.img = img
        self.spriteoffsetx = spriteoffsetx
        self.spriteoffsety = spriteoffsety
        self.layering = layering  # IMPORTANT! Higher numbers makes it go down, not up!
        self.owner = None

    def drawself(self, surf):
        surf.blit(self.img, (
            (self.owner.x * config.CELL_WIDTH) + (self.spriteoffsetx * config.CELL_WIDTH),
            (self.owner.y * config.CELL_HEIGHT) + (self.spriteoffsety * config.CELL_HEIGHT)))


# things have inventories
class com_inventory:
    def __init__(self):
        self.owner = None


# some objects can be picked up and used as weapons.
class com_item:
    def __init__(self):
        self.owner = None


class com_attack:
    def __init__(self, attackdamage):
        self.owner = None
        self.attackdamage = attackdamage


###########################
#### SPECIAL FUNCTIONS ####
###########################


class com_ondeath:
    def __init__(self, deathimg=None, spriteoffsetx=0, spriteoffsety=0, blockafterdeath=False):
        self.owner = None
        self.deathimg = deathimg
        self.blockafterdeath = blockafterdeath
        self.spriteoffsetx = spriteoffsetx
        self.spriteoffsety = spriteoffsety

    def die(self):
        self.owner.sprite.img = self.deathimg
        self.owner.blockpath = self.blockafterdeath
        self.owner.sprite.layering = 2
        self.owner.sprite.spriteoffsetx = self.spriteoffsetx
        self.owner.sprite.spriteoffsety = self.spriteoffsety


###########################
####     PARTICLES     ####
###########################

class particle:
    def __init__(self, sprite, lifetime, x, y, dx=1, dy=1, speed_decay=1):
        self.sprite = sprite
        self.lifetime = lifetime
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.ticks_until_move_x = 0
        self.ticks_until_move_y = 0
        self.speed_decay = speed_decay

    def draw_self(self, surf):
        surf.blit(self.sprite, (
            (self.x),
            (self.y)))


###############################################################################################################
#                                           GAME LOGIC AND FUNCTIONS
###############################################################################################################


def create_particles(x, y, numb, partype, sprite=config.S_SPARK, lifetime=150):
    global PARTICLES
    xa, ya = pos_to_abs(x, y)

    if partype == 'spark':
        for ring in range(0, numb):
            dx = random.randint(-3, 3)
            dy = random.randint(-3, 3)
            lifetime_d = random.randint(10, lifetime)
            PARTICLES += [particle(sprite, lifetime_d, xa, ya, dx, dy)]

    if partype == 'smoke':
        for ring in range(0, numb):
            dx = random.randint(-3, 3)
            dy = random.randint(1, 3)
            lifetime_d = random.randint(10, lifetime)
            PARTICLES += [particle(sprite, lifetime_d, xa, ya, dx, dy)]


def process_particles():
    global PARTICLES
    for par in PARTICLES:
        #okay, this is something I was playing with due to the fact that processing angles with integers gets messy

        if par.ticks_until_move_x <= 0: # this makes all particles move at the same speed.  Maybe??
            par.x += par.dx
            par.ticks_until_move_x = par.dx
        if par.ticks_until_move_y <= 0: # this makes all particles move at the same speed.  Maybe??
            par.y += par.dy
            par.ticks_until_move_y = par.dy
        # par.lifetime += -1
        par.ticks_until_move_y += -par.speed_decay
        par.ticks_until_move_x += -par.speed_decay
        par.lifetime += -(abs(par.dx) + abs(par.dy))

        if (par.lifetime < 0) or (abs(par.dx) + abs(par.dy) == 0):
            PARTICLES.remove(par)




def pos_to_abs(x, y):
    abs_x = (x * config.CELL_WIDTH) + (config.CELL_WIDTH/2)
    abs_y = (y * config.CELL_HEIGHT) + (config.CELL_HEIGHT/2)
    return abs_x, abs_y


# functions for stuff
def query_object(x, y, actors=True, props=True, breakonblock=False):
    # set block to false
    block = False
    found = []
    # The object must be BOTH at the same x and y values, AND be blocking
    # break out because multiple blocks is redundant.
    for obj in ACTORS:
        if (obj.x == x) and (obj.y == y):
            found += [obj]
            if obj.blockpath:
                block = True
                if breakonblock:
                    break
    for obj in PROPS:
        if (obj.x == x) and (obj.y == y):
            found += [obj]
            if obj.blockpath:
                block = True
                if breakonblock:
                    break
    return block, found


###########################
#### OBJECT PROCESSING ####
###########################

def tick_objects():
    pass


def move_objects():  #### MOVING AND ATTACKING ####
    global ACTORS
    recalc = False
    for act in ACTORS:
        # if either one changes
        if (act.dx != 0) or (act.dy != 0):
            # Something moved, recalculate sprite layering
            recalc = True
            # make note of where it should go
            x, y = act.dx + act.x, act.dy + act.y
            # print(x, y)
            # check if that space is blocked
            block, objects_found = query_object(x, y)
            if not block:
                # move there
                act.x = x
                act.y = y
            else:
                # we got something
                for objf in objects_found:
                    if objf.health:  # if it bleeds we can kill it
                        create_particles(objf.x, objf.y, 6, "spark")
                        print(act.type, "(", act.health.hp, "hp)", "attacks", objf.type, "(", objf.health.hp, "hp)")
                        objf.health.hp -= act.attack.attackdamage
                        if objf.ondeath and objf.health.hp <= 0:  # the attack killed him
                            objf.ondeath.die()

            # either way, set our desired move back to zero
            act.dx, act.dy = 0, 0
    if recalc:
        ACTORS = sort_objects(ACTORS)


# sort list of objects for rendering niceness
def sort_objects(group):
    outgoing = sorted(group, key=lambda x: x.sprite.layering - x.y, reverse=True)
    return outgoing


###########################
####     DRAWING       ####
###########################

def draw_game():
    # global ACTORS, PROPS, TILES, SELECTED, RUN_GAME, SURFACE_MAIN
    global TIMESINCE
    SURFACE_MAIN.fill((0, 0, 0))
    for obj in PROPS:  # todo fix this hack-y workaround
        obj.sprite.drawself(SURFACE_MAIN)

    for obj in ACTORS:
        obj.sprite.drawself(SURFACE_MAIN)
    # fps counter
    if DEBUG['showfps']:
        fpstxt = FONTS['fps'].render(TIMESINCE, 0, (255, 255, 255))
        SURFACE_MAIN.blit(fpstxt, (100, 100))
    for par in PARTICLES:
        par.draw_self(SURFACE_MAIN)

    pygame.display.flip()


# game loop
def game_main_loop():
    # global ACTORS, PROPS, TILES, SELECTED, RUN_GAME, SURFACE_MAIN
    global start_time, TIMESINCE, ACTORS, PROPS
    while RUN_GAME:
        start_time = time.time()
        # game states

        # check keyboard
        get_inputs()

        # process game objects
        move_objects()
        tick_objects()
        # PROPS = sort_objects(PROPS) #might not be necessary to call every time
        # particles
        process_particles()

        # enemy ai

        # draw on screen
        draw_game()
        TIMESINCE = str("FPS: " + str(1.0 / (time.time() - start_time)))
        # print("FPS: " + str(1.0 / (time.time() - start_time)))


# initialize game
def game_initialize():
    pygame.init()
    # global variables
    global ACTORS, PROPS, TILES, SELECTED, RUN_GAME, SURFACE_MAIN, FONTS, TIMESINCE, PARTICLES, DEBUG

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
    ACTORS, PROPS, SELECTED = map1gen.map_1_generate(8, 8)
    # set a font i guess.  wow there's a lot of globals even though someone told me globals are bad
    FONTS = {"fps": pygame.font.SysFont("Arial", 60)}
    TIMESINCE = "0.0"
    # controls particles!
    PARTICLES = []
    DEBUG = {"showfps": False}


if __name__ == '__main__':
    print("working directory is" + os.getcwd())
    game_initialize()
    game_main_loop()
