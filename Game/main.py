import pygame

import Game.fallout
from Game.classes import *
from Game.func import *


pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

player, level_x, level_y = generate_level(load_level(MAP))

camera = Camera()
running = True
yd = yu = 0
xr = xl = 0
a = 0
pos = (-1, -1)

while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                yd = +2
            if event.key == pygame.K_w:
                yu = -2
            if event.key == pygame.K_d:
                xr = +2
            if event.key == pygame.K_a:
                xl = -2

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            a = 1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                yd = 0
            if event.key == pygame.K_w:
                yu = 0
            if event.key == pygame.K_d:
                xr = 0
            if event.key == pygame.K_a:
                xl = 0

    dy = yd + yu
    dx = xl + xr

    camera.update(player, dx, dy)
    for sprite in all_sprites:
        camera.apply(sprite)
        if sprite in walls_groups:
            if sprite.rect.x <= pos[0] <= sprite.rect.x + TILE_WIDTH and sprite.rect.y <= pos[1] <= sprite.rect.y + TILE_HEIGHT and a == 1:
                a = 0
                Game.fallout.main(screen)

    tiles_group.draw(screen)
    player_group.draw(screen)
    all_sprites.update(dx, dy)
    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()
