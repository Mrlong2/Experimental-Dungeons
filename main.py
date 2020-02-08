import pygame
import tcod
import config
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
        #todo add a material type

class prop:
    '''This object never gets ticked, and cannot act on it's own.  '''
    def __init__(self, x, y, name_object):

class actor:
    '''This object includes people, creatures, animals, some traps, and machines'''
    def __init__(self, x, y, name_o):
        self.x = x
        self.y = y

    #subclasses

    class creature:
        pass


#   ____ ___  __  __ ____   ___  _   _ _____ _   _ _____ ____
#  / ___/ _ \|  \/  |  _ \ / _ \| \ | | ____| \ | |_   _/ ___|
# | |  | | | | |\/| | |_) | | | |  \| |  _| |  \| | | | \___ \
# | |__| |_| | |  | |  __/| |_| | |\  | |___| |\  | | |  ___) |
#  \____\___/|_|  |_|_|    \___/|_| \_|_____|_| \_| |_| |____/

# eh maybe


#    _    ___
#    / \  |_ _|
#   / _ \  | |
#  / ___ \ | |
# /_/   \_\___|


#  __  __
# |  \/  | __ _ _ __
# | |\/| |/ _` | '_ \
# | |  | | (_| | |_) |
# |_|  |_|\__,_| .__/
#              |_|

def map_create():
    pass

#  ____                     _
# |  _ \ _ __ __ ___      _(_)_ __   __ _
# | | | | '__/ _` \ \ /\ / / | '_ \ / _` |
# | |_| | | | (_| |\ V  V /| | | | | (_| |
# |____/|_|  \__,_| \_/\_/ |_|_| |_|\__, |
#                                   |___/

def draw_game():
    pass

#also the camera

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
        #player


        #get inputs
        get_inputs()

        #process gameticks

        pass

def game_initialize():
    pygame.init()

    global SURFACE_MAIN, GAME_MAP, MAP_OBJECTS

    SURFACE_MAIN = pygame.display.set_mode((config.GAME_HEIGHT, config.GAME_WIDTH))

    GAME_MAP = map_create()


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