#imports
#basic
import pygame
import time
import random
import os
import json
import numpy


#other
import graphical3.defs
import graphical3.kb
import graphical3.obj
import graphical3.com

#declriations

###############################################################################################################
#                                               INFO                                                          #
###############################################################################################################

#


###############################################################################################################
#                                               DRAWING                                                       #
###############################################################################################################

#


###############################################################################################################
#                                           OBJECT PROCESSING                                                 #
###############################################################################################################

#


###############################################################################################################
#                                           GAME LOGIC AND FUNCTIONS                                          #
###############################################################################################################
def game_main_loop():
    pass


###########################
####    GAME STATE     ####
###########################

###########################
####    INITIALIZE     ####
###########################

def game_initialize():
    global INSTANCES, ACTORS, PROPS, STATE, DEBUG, SURFACE_MAIN, FONTS
    #instance
    #    floor
    #        actors
    #        props

    #Init actors.  Actors get ticked every turn so they can act.
    ACTORS = []
    # Init props.  props do not get ticked every turn, so they are best for things that don't do anything without being.
    #interacted with.
    PROPS = []

    STATE = {'selected' : None}



#run
if __name__ == '__main__':
    print("working directory is" + os.getcwd())
    game_initialize()
    game_main_loop()


