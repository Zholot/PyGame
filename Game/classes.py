# COMMON FUNCTIONS


import pygame

from Game.func import *
from Game.data import *

debug = True

player_image = pygame.image.load(PLAYER)

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
walls_groups = pygame.sprite.Group()


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x + 15, TILE_HEIGHT * pos_y + 5)

    def update(self, dx=0, dy=0):
        x = self.rect.x
        y = self.rect.y
        self.rect.x += dx
        collisons = pygame.sprite.groupcollide(player_group, walls_groups, False, False)
        if collisons:
            self.rect.x = x
        self.rect.y += dy
        collisons = pygame.sprite.groupcollide(player_group, walls_groups, False, False)
        if collisons:
            self.rect.y = y


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = pygame.image.load(TILE_IMAGES[tile_type])
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target, dx, dy):
        self.dx = WIDTH // 2 - (target.rect.x + target.rect.w // 2) - 5*dx
        self.dy = HEIGHT // 2 - (target.rect.y + target.rect.h // 2) - 5*dy
