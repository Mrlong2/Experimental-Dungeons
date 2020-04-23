import pygame
from graphical2.main2 import gameobject
from graphical2 import config


# This map generator makes a simple <height> by <width> room with some things to mess with.

def map_1_generate(width, height):
    actors = []
    props = []
    # make a player character
    actors += [gameobject(1, 1, "Adverturer", config.S_HUMAN, spriteoffsetx=0, spriteoffsety=-32, blockpath=True)]
    selected = actors[0]
    actors += [gameobject(3, 2, "Crabby the Crab", config.S_CRAB, spriteoffsetx=0, spriteoffsety=0, blockpath=True)]

    #make a floor
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            floor = [gameobject(x, y, "floor", sprite=config.S_FLOOR)]
            props += floor

    # walls
    # top
    for x in range(0, width):
        y = 0
        wall = [gameobject(x, y, "wall", sprite=config.S_WALL, blockpath=True)]
        props += wall
    # left
    for y in range(1, height - 1):
        x = 0
        wall = [gameobject(x, y, "wall", sprite=config.S_WALL, blockpath=True)]
        props += wall
    # right
    for y in range(1, height - 1):
        x = width - 1
        wall = [gameobject(x, y, "wall", sprite=config.S_WALL, blockpath=True)]
        props += wall
    # bottom
    for x in range(0, width):
        y = height - 1
        wall = [gameobject(x, y, "wall", sprite=config.S_WALL, blockpath=True)]
        props += wall

    props += [gameobject(5, 4, "wall", sprite=config.S_WALL, blockpath=True)]

    return actors, props, selected
