import pygame
from graphical2.main2 import obj_entity, com_sprite, com_health, com_ondeath, com_attack
from graphical2 import config


# This map generator makes a simple <height> by <width> room with some things to mess with.

def map_1_generate(width, height):
    actors = []
    props = []
    # make a player character
    actors += [obj_entity(1, 1, "Adventurer", sprite=com_sprite(config.S_HUMAN, spriteoffsetx=0, spriteoffsety=-1),
                          blockpath=True, health=com_health(20), attack=com_attack(1))]
    selected = actors[0]
    actors += [obj_entity(3, 1, "Crabby the Crab", sprite=com_sprite(config.S_CRAB, spriteoffsetx=0, spriteoffsety=0),
                          blockpath=True, ondeath=com_ondeath(config.S_CRAB_DIE), health=com_health(5))]

    actors += [obj_entity(3, 3, "Pipi the Skaven", sprite=com_sprite(config.S_SKAVEN, spriteoffsetx=0, spriteoffsety=-1),
                          blockpath=True, ondeath=com_ondeath(config.S_SKAVEN_DIE), health=com_health(25))]

    #make a floor
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            floor = [obj_entity(x, y, "floor", sprite=com_sprite(config.S_FLOOR))]
            props += floor

    # walls
    # top
    for x in range(0, width):
        y = 0
        wall = [obj_entity(x, y, "wall", sprite=com_sprite(config.S_WALL), blockpath=True)]
        props += wall
    # left
    for y in range(1, height - 1):
        x = 0
        wall = [obj_entity(x, y, "wall", sprite=com_sprite(config.S_WALL), blockpath=True)]
        props += wall
    # right
    for y in range(1, height - 1):
        x = width - 1
        wall = [obj_entity(x, y, "wall", sprite=com_sprite(config.S_WALL), blockpath=True)]
        props += wall
    # bottom
    for x in range(0, width):
        y = height - 1
        wall = [obj_entity(x, y, "wall", sprite=com_sprite(config.S_WALL), blockpath=True)]
        props += wall

    props += [obj_entity(5, 4, "wall", sprite=com_sprite(config.S_WALL), blockpath=True)]

    return actors, props, selected
