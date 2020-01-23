# COMMON FUNCTIONS


import os
import pygame

from Game.classes import *


#def load_image(type, name, color_key=None):
#    fullname = os.path.join('Data', 'textures', type, name)
#    image = pygame.image.load(fullname).convert()
#    if color_key is not None:
#        if color_key == -1:
#            color_key = image.get_at((0, 0))
#        image.set_colorkey(color_key)
#    else:
#        image = image.convert_alpha()
#    return image


def load_level(filename):
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                walls_groups.add(Tile('wall', x, y))
                # Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


def rect(screen, color, cord):
    pygame.draw.rect(screen, color, (cord[0], cord[1], cord[0] + cord[2], cord[1] + cord[3]), 1)
