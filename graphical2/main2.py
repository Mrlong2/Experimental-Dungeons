import pygame
from graphical2 import map1gen
from graphical2 import config
import os
import json
import tcod
import time
import random
import numpy
from graphical2 import astar_1

# Things that are too annoying to fix right now but should be incorporated in v3:
# SMART SPRITES(tm) - no need for annoying prams for every single little thing.
# Better maze finding!


###############################################################################################################
#                                               INFO
###############################################################################################################
# quality of life / fun
# TODO smart object layering (Slicing)
# I just decided to go max spaghetti on this one, I can optimize later.
# TODO some type of dictionary were we can summon pre-constructed items
# TODO Ranged weapons
# TODO better attack system
# DONE find out if its faster to make the sorting thing change the thing.  It's not but i did it anyway.

# DONE! particle controller
#   todo make particles use floats and have time to turn for fractional values

# important!
# DONE turn system


global ACTORS, PROPS, SELECTED, RUN_GAME, SURFACE_MAIN, FONTS, TIMESINCE, start_time, PARTICLES, DEBUG, STATE


# keyboard inputs
def get_inputs():
    global RUN_GAME, SELECTED
    for event in pygame.event.get():
        # if exit is pressed
        if event.type == pygame.QUIT:
            RUN_GAME = False  # set to false

        if event.type == pygame.KEYDOWN:  # if the event is a key down press
            # player controls
            if event.key == pygame.K_w:
                SELECTED.dy = -1

            if event.key == pygame.K_s:
                SELECTED.dy = 1

            if event.key == pygame.K_a:
                SELECTED.dx = -1

            if event.key == pygame.K_d:
                SELECTED.dx = 1
            # debug/fps menu
            if event.key == pygame.K_F1:
                DEBUG["showfps"] = not (DEBUG["showfps"])

            if event.key == pygame.K_UP:
                STATE['camera pos'] = (STATE['camera pos'][0], STATE['camera pos'][1] + 32)

            if event.key == pygame.K_DOWN:
                STATE['camera pos'] = (STATE['camera pos'][0], STATE['camera pos'][1] - 32)

            if event.key == pygame.K_LEFT:
                STATE['camera pos'] = (STATE['camera pos'][0] + 32, STATE['camera pos'][1])

            if event.key == pygame.K_RIGHT:
                STATE['camera pos'] = (STATE['camera pos'][0] - 32, STATE['camera pos'][1])

        # mouse controls
        if event.type == pygame.MOUSEBUTTONDOWN:
            # print(event.button)
            # if (pygame.mouse.get_pressed() == 1):
            xm, ym = pygame.mouse.get_pos()
            itemsfound = query_click_location(xm, ym)
            for thing in itemsfound:
                print(thing.type)
            # print(xm, ym)


###############################################################################################################
#                                           OBJECT CONTROL
###############################################################################################################

# actors
# game objects need x, y, type, health, inventory,
class obj_entity:
    def __init__(self, x, y, objtype, sprite, blockpath=False, health=None, inventory=None, ondeath=None, attack=None,
                 ai_persona="none", special=None):
        # moving and location
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0

        # object type
        self.type = objtype
        self.blockpath = blockpath
        self.ai_persona = ai_persona

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

        self.special = special
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
        self.dead = False  # allows you to know if you're dead
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

    def drawself(self, surf, offset_x, offset_y):
        surf.blit(self.img, (
            (self.owner.x * config.CELL_WIDTH) + (self.spriteoffsetx * config.CELL_WIDTH) + offset_x,
            (self.owner.y * config.CELL_HEIGHT) + (self.spriteoffsety * config.CELL_HEIGHT) + offset_y))


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


class com_special:
    def __init__(self, special_data):
        self.owner = None
        self.data = special_data


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
        global PROPS, ACTORS
        self.owner.sprite.img = self.deathimg
        self.owner.blockpath = self.blockafterdeath
        self.owner.sprite.layering = 2
        self.owner.sprite.spriteoffsetx = self.spriteoffsetx
        self.owner.sprite.spriteoffsety = self.spriteoffsety
        self.owner.ai_persona = "none"
        self.owner.health.dead = True
        print(self.owner.type, 'Died!')


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

    def draw_self(self, surf, offsetx, offsety):
        surf.blit(self.sprite, (
            (self.x + offsetx),
            (self.y + offsety)))


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


def process_particles():
    global PARTICLES
    for par in PARTICLES:
        # okay, this is something I was playing with due to the fact that processing angles with integers gets messy

        if par.ticks_until_move_x <= 0:  # this makes all particles move at the same speed.  Maybe??
            par.x += par.dx
            par.ticks_until_move_x = par.dx
        if par.ticks_until_move_y <= 0:  # this makes all particles move at the same speed.  Maybe??
            par.y += par.dy
            par.ticks_until_move_y = par.dy
        # par.lifetime += -1
        par.ticks_until_move_y += -par.speed_decay
        par.ticks_until_move_x += -par.speed_decay
        par.lifetime += -(abs(par.dx) + abs(par.dy))

        if (par.lifetime < 0) or (abs(par.dx) + abs(par.dy) == 0):
            PARTICLES.remove(par)


def pos_to_abs(x, y):
    # converts grid chords to screen chords
    abs_x = (x * config.CELL_WIDTH) + (config.CELL_WIDTH / 2)
    abs_y = (y * config.CELL_HEIGHT) + (config.CELL_HEIGHT / 2)
    return abs_x, abs_y


def query_click_location(x, y, actors=True, props=True):
    found = []
    cposx, cposy = STATE['camera pos']
    # Question:  Why is camera subtracted?  Answer:  Because the top left corner is 0,0
    xl = ((x - cposx) // config.CELL_WIDTH)
    yl = ((y - cposy) // config.CELL_HEIGHT)
    print(xl, yl)
    # The object must be BOTH at the same x and y values, AND be blocking
    # break out because multiple blocks is redundant.
    if actors:
        for obj in ACTORS:
            if (obj.x == xl) and (obj.y == yl):
                found += [obj]

    if props:
        for obj in PROPS:
            if (obj.x == xl) and (obj.y == yl):
                found += [obj]

    return found


# functions for stuff
def query_object(x, y, actors=True, props=True, breakonblock=False):
    # set block to false
    block = False
    found = []
    # The object must be BOTH at the same x and y values, AND be blocking
    # break out because multiple blocks is redundant.
    if actors:
        for obj in ACTORS:
            if (obj.x == x) and (obj.y == y):
                found += [obj]
                if obj.blockpath:
                    block = True
                    if breakonblock:
                        break
    if props:
        for obj in PROPS:
            if (obj.x == x) and (obj.y == y):
                found += [obj]
                if obj.blockpath:
                    block = True
                    if breakonblock:
                        break
    return block, found


###############################################################################################################
#                                           OBJECT PROCESSING                                                 #
###############################################################################################################


def tick_objects():
    pass


#    AI programs!

def ai_moves():
    global ACTORS
    for ai in ACTORS:
        if ai.ai_persona == "random":
            # so this chooses a random direction and avoids moving diagonally.
            if random.randint(0, 2):
                ai.dx = random.randint(-1, 1)
            else:
                ai.dy = random.randint(-1, 1)
            #
        ####  Astar movment, just always attacks without any thinking
        if ai.ai_persona == "dumb_attack":
            # attacks directly at the player.
            blockmap = numpy.zeros((config.MAP_1_GEN_SIZE[0], config.MAP_1_GEN_SIZE[1]))
            for ent in ACTORS:
                if ent.blockpath and ent != ai:
                    blockmap[ent.x, ent.y] = 1
            for ent in PROPS:
                if ent.blockpath and ent != ai:
                    blockmap[ent.x, ent.y] = 1
            blockmap.astype(int)
            blockmap2 = blockmap.astype(int).tolist()
            # Wow!  Coding this was a horrible experience
            astar = astar_1.Astar(blockmap)
            result = astar.run((ai.x, ai.y), (SELECTED.x, SELECTED.y))
            ai.dx, ai.dy = result[1][0] - ai.x, result[1][1] - ai.y


def move_objects():  #### MOVING AND ATTACKING ####
    global ACTORS, STATE, PROPS
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
                    if objf.health and act.attack and not (objf.health.dead):
                        # health checks that it's attackable, act.attack checks if the thing moving can attack, and
                        # not(objf.health.dead) checks if the object is already dead!  This was a problem because
                        # I was having problems with death functions running multiple times.
                        # I could change it to only check actors, but the divide is for performance reasons.
                        create_particles(objf.x, objf.y, 7, "spark")  # attack sparks!
                        print(act.type, "(", act.health.hp, "hp)", "attacks", objf.type, "(", objf.health.hp, "hp)")
                        objf.health.hp -= act.attack.attackdamage
                        if objf.ondeath and objf.health.hp <= 0:  # the attack killed him
                            objf.ondeath.die()
                            if objf in ACTORS:
                                ACTORS.remove(objf)
                            PROPS += [objf]
            if act == SELECTED:
                print('action: player moved')
                STATE['player action'] = True

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

# UI controller
def draw_ui():
    pass


def draw_game():
    # global ACTORS, PROPS, TILES, SELECTED, RUN_GAME, SURFACE_MAIN
    global TIMESINCE, STATE
    # camera location:
    cposx, cposy = STATE['camera pos']
    SURFACE_MAIN.fill((0, 0, 0))
    for obj in PROPS:
        obj.sprite.drawself(SURFACE_MAIN, cposx, cposy)
    for obj in ACTORS:
        obj.sprite.drawself(SURFACE_MAIN, cposx, cposy)
    # fps counter
    if DEBUG['showfps']:
        fpstxt = FONTS['fps'].render(TIMESINCE['frame'], 0, (255, 255, 255))
        SURFACE_MAIN.blit(fpstxt, (100, 100))
    for par in PARTICLES:
        par.draw_self(SURFACE_MAIN, cposx, cposy)

    pygame.display.flip()


###########################
####    GAME STATE     ####
###########################

def process_gamestate():
    global TIMESINCE
    # game states
    # if STATE['turn'] == 'thinking':
    #     # print('back to player')
    #     print(time.time())
    #     TIMESINCE['delay'] = time.time()
    #     STATE['turn'] = 'delay'
    #
    # if STATE['turn'] == 'delay':
    #     # print('back to player')
    #     print(time.time() - TIMESINCE['delay'])
    #     if time.time() - TIMESINCE['delay'] > config.WAIT_TIME:
    #         STATE['turn'] = 'player'
    if STATE['turn'] == 'thinking':
        # no delay
        STATE['turn'] = 'player'

    if STATE['turn'] == 'enemy':
        ai_moves()
        # print('ai moves')
        STATE['turn'] = 'thinking'

    # check keyboard
    if STATE['turn'] == 'player':
        get_inputs()


###########################
####     GAME LOOP     ####
###########################


# game loop
def game_main_loop():
    # global ACTORS, PROPS, TILES, SELECTED, RUN_GAME, SURFACE_MAIN
    global start_time, TIMESINCE, ACTORS, PROPS
    while RUN_GAME:
        start_time = time.time()

        # do whatever should be done on that state.
        process_gamestate()

        # process game objects
        move_objects()
        # tick_objects()
        # PROPS = sort_objects(PROPS) #might not be necessary to call every time
        # particles
        process_particles()

        # draw on screen
        draw_game()
        TIMESINCE['frame'] = str("FPS: " + str(1.0 / (time.time() - start_time)))
        # print("FPS: " + str(1.0 / (time.time() - start_time)))

        # finally, switch to ai if played did an action
        if STATE['player action']:
            STATE['turn'] = 'enemy'
            STATE['player action'] = False


# initialize game
def game_initialize():
    pygame.init()
    # global variables
    global ACTORS, PROPS, SELECTED, RUN_GAME, SURFACE_MAIN, FONTS, TIMESINCE, PARTICLES, DEBUG, STATE

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
    ACTORS, PROPS, SELECTED = map1gen.map_1_generate(config.MAP_1_GEN_SIZE[0], config.MAP_1_GEN_SIZE[1])
    ACTORS = sort_objects(ACTORS)
    # set a font i guess.  wow there's a lot of globals even though someone told me globals are bad
    FONTS = {"fps": pygame.font.SysFont("Arial", 60)}
    TIMESINCE = {'frame': "0.0", 'delay': None}
    # controls particles!
    PARTICLES = []
    DEBUG = {"showfps": False}
    #turn decides who's turn it is, camera controls camera position, picked is what is clicked.
    STATE = {"turn": "player", "player action": False, "camera pos": (32, 32), "picked": []}




if __name__ == '__main__':
    print("working directory is" + os.getcwd())
    game_initialize()
    game_main_loop()
