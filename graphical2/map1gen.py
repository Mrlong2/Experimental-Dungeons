import pygame
from graphical2.main2 import gameobject
from graphical2 import config


def map_1_generate(width, height):
    actors = []
    props = []
    # make a floor
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            floor = [gameobject(x, y, "floor", sprite=config.S_FLOOR)]
            props += floor

    actors += [gameobject(1, 1, "Adverturer", config.S_GIRL, spriteoffsetx=0, spriteoffsety=-32)]
    selected = actors[0]

    return actors, props, selected
