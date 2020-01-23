import pygame
import random
import Game.fallout
from Game.classes import *
from Game.func import *
from Game.data import *

LABELS = ['Альбион', 'Новая игра', 'Продолжить', 'Достижения', 'Настройки', 'Выход']
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # , pygame.FULLSCREEN
clock = pygame.time.Clock()
pygame.display.set_caption('Super Game')
tile_width = tile_height = 50


def load_image(name):
    return pygame.image.load('data/' + name)


def music(name, volume=1):
    if name[-3:] == 'mp3':
        pygame.mixer.music.load('data/' + name)
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(volume)
    elif name[-3:] == 'ogg' or name[-3:] == 'wav':
        return pygame.mixer.Sound('data/' + name)
    else:
        print('error sound')


def static_labels():
    font = pygame.font.Font(None, 25)
    pygame.draw.rect(screen, (76, 60, 24), (435, 90, 150, 30), 0)
    pygame.draw.rect(screen, (76, 60, 24), (90 + xl, 140 + yl, 130, 30), 0)
    screen.blit(font.render(LABELS[0], 1, (189, 132, 40), (76, 60, 24)), (450, 100))
    screen.blit(font.render(LABELS[1], 1, (189, 132, 40), (76, 60, 24)), (100 + xl, 150 + yl))
    if save:
        pygame.draw.rect(screen, (76, 60, 24), (90 + xl, 190 + yl, 130, 30), 0)
        screen.blit(font.render(LABELS[2], 1, (189, 132, 40), (76, 60, 24)), (100 + xl, 200 + yl))
    else:
        pygame.draw.rect(screen, (76, 60, 24), (90 + xl, 190 + yl, 130, 30), 0)
        screen.blit(font.render(LABELS[2], 1, (149, 92, 0), (76, 60, 24)), (100 + xl, 200 + yl))
    pygame.draw.rect(screen, (76, 60, 24), (90 + xl, 240 + yl, 130, 30), 0)
    pygame.draw.rect(screen, (76, 60, 24), (90 + xl, 290 + yl, 130, 30), 0)
    pygame.draw.rect(screen, (76, 60, 24), (90 + xl, 340 + yl, 130, 30), 0)
    screen.blit(font.render(LABELS[3], 1, (189, 132, 40), (76, 60, 24)), (100 + xl, 250 + yl))
    screen.blit(font.render(LABELS[4], 1, (189, 132, 40), (76, 60, 24)), (100 + xl, 300 + yl))
    screen.blit(font.render(LABELS[5], 1, (189, 132, 40), (76, 60, 24)), (100 + xl, 350 + yl))


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('$')
    return list(map(lambda x: x.ljust(max_width, '$'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                walls_groups.add(Tile('wall', x, y))
            elif level[y][x] == '@':
                minigames_groups.add(Tile('mg', x, y))
                # Tile('wall', x, y)
            elif level[y][x] == '$':
                Tile('dark', x, y)
            elif level[y][x] == ')':
                walls_groups.add(Tile('wall_r', x, y))
            elif level[y][x] == '(':
                walls_groups.add(Tile('wall_l', x, y))
            elif level[y][x] == '^':
                walls_groups.add(Tile('wall_u', x, y))
            elif level[y][x] == '*':
                walls_groups.add(Tile('wall_ul', x, y))
            elif level[y][x] == '+':
                walls_groups.add(Tile('wall_rl', x, y))
            elif level[y][x] == '-':
                walls_groups.add(Tile('wall_ur', x, y))
            elif level[y][x] == '%':
                walls_groups.add(Tile('wall_lu', x, y))
                # new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


def Saves(save='r'):
    global K, Flag, dialog, menu
    saves = open("saves.txt", save)
    if save == 'r':
        s = saves.readlines()
        if s == []:
            return False
        else:
            K, Flag, dialog, menu = int(s[0].split()[0]), *[bool(int(i)) for i in s[0].split()[1:]]
            return True
    if save == 'w':
        saves.write(str(K) + ' ' + str(int(Flag)) + ' ' + str(int(dialog)) + ' ' + str(int(menu)))


screen_rect = (0, 0, WIDTH, HEIGHT)


class Player(pygame.sprite.Sprite):
    image = load_image("hero.png")

    def __init__(self, frames_right, frames_left, frames_stand_left, frames_stand_right, start_pos, *groups):
        super().__init__(player_group, *groups)
        self.frames_right = frames_right
        self.frames_left = frames_left
        self.frames_stand_left = frames_stand_left
        self.frames_stand_right = frames_stand_right
        self.cur_frame = 0
        self.frame_count = 0
        self.image = self.frames_right[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.x = start_pos[0]
        self.rect.y = start_pos[1]
        self.mask = pygame.mask.from_surface(self.image)
        self.vector = 1
        self.vector_left_right = 1
        self.vector_stand = 1
        # проверка на остановку
        self.stand = True
        # чтобы перс не застрявал в верхних стенах
        self.in_wall_prison = False

    def update(self, *args):
        buttons = pygame.key.get_pressed()
        if buttons[pygame.K_w]:  # and not pygame.sprite.collide_mask(self, walls):
            self.vector = 3
            self.rect.y -= 3
            if pygame.sprite.groupcollide(player_group, walls_groups, False, False) or pygame.sprite.groupcollide(player_group, minigames_groups, False, False):
                self.rect.y += 4
            else:
                self.stand = False
            # else:
            # self.in_wall_prison = True

        if buttons[pygame.K_s]:
            self.vector = 4
            if pygame.sprite.groupcollide(player_group, walls_groups, False, False) or pygame.sprite.groupcollide(player_group, minigames_groups, False, False):
                self.rect.y -= 4
            else:
                self.stand = False
                self.rect.y += 3

        if buttons[pygame.K_d]:  # and not pygame.sprite.collide_mask(self, walls):
            self.vector = 1
            self.vector_left_right = 1
            self.rect.x += 3
            if pygame.sprite.groupcollide(player_group, walls_groups, False, False) or pygame.sprite.groupcollide(player_group, minigames_groups, False, False):  # or self.in_wall_prison:
                self.rect.x -= 4
            else:
                self.stand = False

        if buttons[pygame.K_a]:  # and not pygame.sprite.collide_mask(self, walls):
            self.vector = 2
            self.vector_left_right = 2
            self.rect.x -= 3
            if pygame.sprite.groupcollide(player_group, walls_groups, False, False) or pygame.sprite.groupcollide(player_group, minigames_groups, False, False):  # or self.in_wall_prison:
                self.rect.x += 4
            else:
                self.stand = False

        if self.frame_count % 5 == 0:
            if not self.stand:
                if self.vector_left_right == 1:
                    self.cur_frame = (self.cur_frame + 1) % len(self.frames_right)
                    self.image = self.frames_right[self.cur_frame]
                if self.vector_left_right == 2:
                    self.cur_frame = (self.cur_frame + 1) % len(self.frames_left)
                    self.image = self.frames_left[self.cur_frame]
            else:
                if self.vector_left_right == 1:
                    self.cur_frame = (self.cur_frame + 1) % len(self.frames_right)
                    self.image = self.frames_stand_right[self.cur_frame]
                if self.vector_left_right == 2:
                    self.cur_frame = (self.cur_frame + 1) % len(self.frames_left)
                    self.image = self.frames_stand_left[self.cur_frame]
            self.mask = pygame.mask.from_surface(self.image)
        if not (buttons[pygame.K_UP] or buttons[pygame.K_DOWN] or buttons[pygame.K_RIGHT] or buttons[pygame.K_LEFT]):
            self.stand = True
        self.frame_count += 1


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, *args):
        self.dx = -(args[0].rect.x + args[0].rect.w // 2 - WIDTH // 2)
        self.dy = -(args[0].rect.y + args[0].rect.h // 2 - HEIGHT // 2)


camera = Camera()

all_sprites = pygame.sprite.Group()
tile_images = {'wall': load_image('wall.png'), 'empty': load_image('wall1.png'), 'dark': load_image('dark.png'),
               'wall_l': load_image('wall_l.png'), 'wall_r': load_image('wall_r.png'),
               'wall_u': load_image('wall_u.png'), 'wall_ul': load_image('wall_ul.png'),
               'wall_rl': load_image('wall_rl.png'), 'wall_ur': load_image('wall_ur.png'),
               'mg': load_image('mg.png'), 'wall_lu': load_image('wall_lu.png'), 'curs': load_image('curs.png')}
player_image = load_image('bomzh_vlevo_okonchat6.png')

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
walls_groups = pygame.sprite.Group()
minigames_groups = pygame.sprite.Group()
k = 0
clock = pygame.time.Clock()
fps = 60
K = -1
xl, yl = 0, 50
save = False
Flag = False
dialog = False
gamerun = True
menu = True
lvl = False
music('battleThemeA.mp3')
fon = load_image('фон_1.png')
walls = load_image('стены_1.png')
player, level_x, level_y = generate_level(load_level('map.txt'))
future = False
is_hero = False
while gamerun:
    if dialog:
        font = pygame.font.Font(None, 20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gamerun = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if Flag == False and K < 14:
                        K += 1
                        Flag = True
                    elif Flag == True and K < 14:
                        K += 1
                    else:
                        Flag = False
                        lvl = True
                        dialog = False
        screen.fill((10, 10, 10))
        # if Flag:
        #   if K not in [2, 5]:
        #      screen.blit(font.render(Frases[K], 1, (255, 0, 0), (0, 0, 0)), (0, 401))
        #  elif K == 2:
        #      screen.blit(font.render(Frases[K], 1, (255, 0, 0), (0, 0, 0)), (0, 401))
        # elif K == 5:
        #      pass
        pygame.draw.line(screen, (123, 0, 123), [0, 400], [1000, 400], 1)
        pygame.display.flip()
    elif menu:
        screen.fill((10, 10, 10))
        screen.blit(pygame.transform.scale(load_image('worldmap.png'), (WIDTH, HEIGHT)), (0, 0))
        static_labels()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gamerun = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if event.button == 1 and (90 < (x - xl) < 220) and (140 < (y - yl) < 170):
                    # dialog = True
                    lvl = True
                    menu = False
                if event.button == 1 and (90 < (x - xl) < 220) and (340 < (y - yl) < 370):
                    Saves('w')
                    gamerun = False
                if event.button == 1 and (90 < (x - xl) < 220) and ((290 < (y - yl) < 320) or (240 < (y - yl) < 270)):
                    future = True
                    menu = False
    elif lvl:
        if not is_hero:
            is_hero = True
            hero = Player([load_image("bomzh_vprapo_okonchat0.png"), load_image("bomzh_vprapo_okonchat1.png"),
                           load_image("bomzh_vprapo_okonchat2.png"), load_image("bomzh_vprapo_okonchat3.png"),
                           load_image("bomzh_vprapo_okonchat4.png"), load_image("bomzh_vprapo_okonchat5.png"),
                           load_image("bomzh_vprapo_okonchat6.png"),
                           load_image("bomzh_vprapo_okonchat7.png")],
                          [load_image("bomzh_vlevo_okonchat0.png"), load_image("bomzh_vlevo_okonchat1.png"),
                           load_image("bomzh_vlevo_okonchat2.png"), load_image("bomzh_vlevo_okonchat3.png"),
                           load_image("bomzh_vlevo_okonchat4.png"), load_image("bomzh_vlevo_okonchat5.png"),
                           load_image("bomzh_vlevo_okonchat6.png"), load_image("bomzh_vlevo_okonchat7.png")],
                          [load_image("stait_vlevo00.png"), load_image("stait_vlevo01.png"),
                           load_image("stait_vlevo02.png"), load_image("stait_vlevo03.png"),
                           load_image("stait_vlevo04.png"), load_image("stait_vlevo14.png"),
                           load_image("stait_vlevo15.png"), load_image("stait_vlevo16.png"),
                           load_image("stait_vlevo17.png")],
                          [load_image("stait_vpravo00.png"), load_image("stait_vpravo01.png"),
                           load_image("stait_vpravo02.png"), load_image("stait_vpravo03.png"),
                           load_image("stait_vpravo04.png"), load_image("stait_vpravo14.png"),
                           load_image("stait_vpravo15.png"), load_image("stait_vpravo16.png"),
                           load_image("stait_vpravo17.png")], (800, 300),
                          all_sprites)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 420 <= x <= 580 and 190 <= y <= 410:
                    for sprite in all_sprites:
                        camera.apply(sprite)
                        if sprite in minigames_groups:
                            if sprite.rect.x <= x <= sprite.rect.x + 50 and sprite.rect.y <= y <= sprite.rect.y + 50:
                                Game.fallout.main(screen)
            if event.type == pygame.QUIT:
                lvl = False
                gamerun = False
        buttons = pygame.key.get_pressed()
        screen.fill((0, 0, 0))
        camera.update(hero)
        for sprite in all_sprites:
            camera.apply(sprite)
        all_sprites.update(event)
        all_sprites.draw(screen)
    elif future:
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 25)
        screen.blit(font.render('Эта опция появится в будущих версиях.', 1, (255, 0, 0), (0, 0, 0)), (100, 100))
        screen.blit(font.render('Вернуться в меню.', 1, (255, 0, 0), (0, 0, 0)), (420, 410))
        pygame.draw.rect(screen, (123, 0, 123), (400, 400, 200, 30), 1)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if event.button == 1 and (400 < x < 600) and (400 < y < 430):
                    future = False
                    menu = True
    pygame.display.update()
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()
