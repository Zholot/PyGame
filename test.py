import os
import random

import pygame

pygame.init()

size = width, height = 800, 600

screen = pygame.display.set_mode(size)

pygame.display.flip()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


screen_rect = (0, 0, width, height)


class FireBall(pygame.sprite.Sprite):
    """Фаерболлы. Что умеют:
    при попадании во врага убивают его и исчезают"""
    image = pygame.transform.scale(load_image("fireball.png", -1), (20, 20))

    def __init__(self, x, y, vector, *groups):
        super().__init__(*groups)
        self.image = FireBall.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.v = 20
        self.vector = vector

    def update(self, *args):
        if pygame.sprite.spritecollideany(self, enemy_group):
            self.kill()
        if not self.rect.colliderect(screen_rect):
            self.kill()
        else:
            if self.vector == 1:
                self.rect.x += self.v
            if self.vector == 2:
                self.rect.x -= self.v
            if self.vector == 3:
                self.rect.y -= self.v
            if self.vector == 4:
                self.rect.y += self.v


class MainHero(pygame.sprite.Sprite):
    """Класс главного героя. Что умеет:
    1. бегает
    2. стреляет фаерболлами"""
    image = load_image("hero.png", -1)

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = MainHero.image
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 10
        self.vector = 1

    def update(self, *args):
        if pygame.key.get_pressed()[pygame.K_UP]:
            self.rect.y -= 10
            self.vector = 3
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            self.rect.y += 10
            self.vector = 4
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.rect.x += 10
            self.vector = 1
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.rect.x -= 10
            self.vector = 2

    def fire(self):
        FireBall(self.rect.x, self.rect.y, self.vector, all_sprites, fireballs)


class Enemy(pygame.sprite.Sprite):
    """Класс врагов. Что умеют:
    1.умирать от попадания фаерболла,
    2.бегать за героем если он находится в радиусе видимости"""
    image = pygame.transform.scale(load_image("creep.png", -1), (50, 50))

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = Enemy.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, width)
        self.rect.y = random.randint(0, height)
        # скорость врага
        self.v = 0

    def update(self, *args):
        for elem in fireballs:
            # проверяем попадает ли герой в область видимости врага
            if self.rect.colliderect(elem):
                self.kill()
                elem.kill()
        # движение врагов
        if ((self.rect.x - hero.rect.x) ** 2 + (self.rect.y - hero.rect.y) ** 2) < 50000 and not self.rect.colliderect(
                hero):
            self.v = 3
            x1 = (self.rect.x + self.v - hero.rect.x) ** 2 + (self.rect.y - hero.rect.y) ** 2
            x2 = (self.rect.x - self.v - hero.rect.x) ** 2 + (self.rect.y - hero.rect.y) ** 2
            y1 = (self.rect.y + self.v - hero.rect.y) ** 2 + (self.rect.x - hero.rect.x) ** 2
            y2 = (self.rect.y - self.v - hero.rect.y) ** 2 + (self.rect.x - hero.rect.x) ** 2
            ok = min([x1, x2, y1, y2])
            if ok == x1:
                self.rect.x += self.v
            elif ok == x2:
                self.rect.x -= self.v
            elif ok == y1:
                self.rect.y += self.v
            elif ok == y2:
                self.rect.y -= self.v

        # if pygame.sprite.spritecollideany(self, fireballs):
        # self.kill()


all_sprites = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
fireballs = pygame.sprite.Group()

for i in range(10):
    Enemy(all_sprites, enemy_group)

hero = MainHero(all_sprites)

clock = pygame.time.Clock()
running = True
fps = 60
while running:
    screen.fill(pygame.Color("white"))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                hero.fire()

    all_sprites.update(event)
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(fps)
