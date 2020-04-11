import pygame
from graphical2.main import gameobject
from graphical2 import config


def map_1_generate(width, height):
    actors = []
    props = []

    for y in range(1, height-1):
        for x in range(1,width-1):
            props += gameobject(x,y, "floor", sprite=config.S_FLOOR)

    return actors, props
