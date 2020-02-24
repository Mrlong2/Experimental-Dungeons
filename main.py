import pygame
import tcod
import constants
import map1


#   ___  _     _           _
#  / _ \| |__ (_) ___  ___| |_ ___
# | | | | '_ \| |/ _ \/ __| __/ __|
# | |_| | |_) | |  __/ (__| |_\__ \
#  \___/|_.__// |\___|\___|\__|___/
#           |__/
class tile:
    '''Tiles, to be improved at a later date'''

    def __init__(self, block_path):
        self.block_path = block_path
        # todo add a material type


class prop:
    '''This object never gets ticked, and cannot act on it's own.  '''

    def __init__(self, x, y, name_object):
        pass

    def draw(self):
        pass


class actor:

    def __init__(self, x, y, nametype, sprite=None, health=None, inventory=None):

        self.x = x
        self.y = y
        self.nametype = nametype
        self.sprite = sprite

        if health:
            self.health = health

        if inventory:
            self.inventory = inventory

    def draw(self):
        SURFACE_MAIN.blit(self.sprite, (self.x * constants.CELL_WIDTH, (self.y * constants.CELL_HEIGHT)-constants.CELL_HEIGHT*1.2))
    # subclasses


#   ____ ___  __  __ ____   ___  _   _ _____ _   _ _____ ____
#  / ___/ _ \|  \/  |  _ \ / _ \| \ | | ____| \ | |_   _/ ___|
# | |  | | | | |\/| | |_) | | | |  \| |  _| |  \| | | | \___ \
# | |__| |_| | |  | |  __/| |_| | |\  | |___| |\  | | |  ___) |
#  \____\___/|_|  |_|_|    \___/|_| \_|_____|_| \_| |_| |____/


class com_health:

    def __init__(self, maxhp, currenthp=None):
        self.maxhp = maxhp
        if currenthp:
            self.currenthp = currenthp
        else:
            self.currenthp = maxhp


class com_inventory:
    def __init__(self, items):
        self.items = items


class item:
    def __init__(self, name):
        self.name = name


#    _    ___
#    / \  |_ _|
#   / _ \  | |
#  / ___ \ | |
# /_/   \_\___|

# yeah eventually

#  __  __
# |  \/  | __ _ _ __
# | |\/| |/ _` | '_ \
# | |  | | (_| | |_) |
# |_|  |_|\__,_| .__/
#              |_|


def map_create():
    return map1.map_gen_1()


#  ____                     _
# |  _ \ _ __ __ ___      _(_)_ __   __ _
# | | | | '__/ _` \ \ /\ / / | '_ \ / _` |
# | |_| | | | (_| |\ V  V /| | | | | (_| |
# |____/|_|  \__,_| \_/\_/ |_|_| |_|\__, |
#                                   |___/

def draw_game():
    SURFACE_MAIN.fill(constants.COLOR_DEFAULT_BG)

    # draw the map
    draw_map(MAP_TILES)

    # draw the character
    for obj in MAP_ACTORS:
        obj.draw()

    # update the display
    pygame.display.flip()


def draw_map(map_to_draw):
    for x in range(0, constants.MAP_WIDTH):
        for y in range(0, constants.MAP_HEIGHT):
            if map_to_draw[x][y].block_path == True:
                # draw wall
                SURFACE_MAIN.blit(constants.S_WALL, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))
            else:
                SURFACE_MAIN.blit(constants.S_FLOOR, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))


# also the camera

#   ____
#  / ___| __ _ _ __ ___   ___
# | |  _ / _` | '_ ` _ \ / _ \
# | |_| | (_| | | | | | |  __/
#  \____|\__,_|_| |_| |_|\___|

def game_main_loop():
    '''This is where we loop the main game'''
    game_quit = False

    # exit when click exit
    while not game_quit:
        # player

        # get inputs
        inputs_list = pygame.event.get()
        for event in inputs_list:
            if event.type == pygame.QUIT:
                game_quit = True

        # process gameticks
        for object in MAP_ACTORS:
            pass

        draw_game()


def game_initialize():
    pygame.init()

    global SURFACE_MAIN, MAP_ACTORS, MAP_PROPS, MAP_TILES, TEAM_TURN

    SURFACE_MAIN = pygame.display.set_mode((constants.GAME_WIDTH, constants.GAME_HEIGHT))

    MAP_TILES = map_create()

    MAP_ACTORS = [actor(2, 2, "human adventurer", sprite=constants.S_GIRL, health=com_health(10), inventory=com_inventory(item("sword")))]




def get_inputs():
    events_list = pygame.event.get()

    # process
    for event in events_list:
        if event.type == pygame.QUIT:
            return


#############################################################
###################################################   #######
###############################################   /~\   #####
############################################   _- `~~~', ####
##########################################  _-~       )  ####
#######################################  _-~          |  ####
####################################  _-~            ;  #####
##########################  __---___-~              |   #####
#######################   _~   ,,                  ;  `,,  ##
#####################  _-~    ;'                  |  ,'  ; ##
###################  _~      '                    `~'   ; ###
############   __---;                                 ,' ####
########   __~~  ___                                ,' ######
#####  _-~~   -~~ _                               ,' ########
##### `-_         _                              ; ##########
#######  ~~----~~~   ;                          ; ###########
#########  /          ;                        ; ############
#######  /             ;                      ; #############
#####  /                `                    ; ##############
###  /                                      ; ###############
#                                            ################

if __name__ == '__main__':
    game_initialize()
    game_main_loop()
