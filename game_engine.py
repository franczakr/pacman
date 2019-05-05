import pygame
import sys
import csv
import operator
import time
from Map import Map, Position
from astar import astar
from pygame.locals import *

# STAŁE
# typy powierzchni
FLOOR = 0
WALL = 1
TILESIZE = 50
MAPWIDTH = 16
MAPHEIGHT = 16
DISPLAYSURF = pygame.display.set_mode((MAPWIDTH*TILESIZE, MAPHEIGHT*TILESIZE))
black = (0, 0, 0)
crimson = (105, 0, 21)

# assigning values to X and Y variable
X = MAPWIDTH * TILESIZE
Y = MAPHEIGHT * TILESIZE

TEXTURES = {
    WALL: pygame.image.load("res/wall.png"),
    FLOOR: pygame.image.load("res/floor.png"),
    "fruit": pygame.image.load("res/fruit.png"),
    "heart": pygame.image.load("res/heart.png")
}

PACMAN_SPRITES = {
    "up": pygame.image.load("res/pacman_u.png"),
    "right": pygame.image.load("res/pacman_r.png"),
    "down": pygame.image.load("res/pacman_d.png"),
    "left": pygame.image.load("res/pacman_l.png"),
}

GHOST_SPRITES = {
    "red_ghost": pygame.image.load("res/red.png"),
    "blue_ghost": pygame.image.load("res/blue.png"),
    "pink_ghost": pygame.image.load("res/pink.png"),
    "yellow_ghost": pygame.image.load("res/yellow.png")
}


# KLASY

class Pacman:
    pos = Position(0, 0)
    old_pos = Position(0, 0)
    direction = "right"
    sprite = "right"
    invincible = False
    inv_time = 400

    def __init__(self, x, y):
        self.pos = Position(x, y)
        self.old_pos = Position(x, y)

    def move(self):
        global score, map
        self.sprite = self.direction
        teleport = False
        self.old_pos = self.pos
        if self.old_pos in map.fruits:
            map.fruits.remove(self.old_pos)
            score += 10

        new_x = self.pos.x
        new_y = self.pos.y
        if self.direction == "right":
            new_x += 1
        elif self.direction == "left":
            new_x -= 1
        elif self.direction == "down":
            new_y += 1
        elif self.direction == "up":
            new_y -= 1

        if new_y < 0:
            new_y = MAPHEIGHT + new_y
            teleport = True
        if new_y >= MAPHEIGHT:
            new_y = new_y - MAPHEIGHT
            teleport = True
        if new_x < 0:
            new_x = MAPWIDTH + new_x
            teleport = True
        if new_x >= MAPWIDTH:
            new_x = new_x - MAPWIDTH
            teleport = True
        if map.tilemap[new_y][new_x] != WALL:
            self.pos = Position(new_x, new_y)
            if teleport:
                self.move()


class Ghost:
    pos = Position(0, 0)
    old_pos = Position(0, 0)
    direction = "right"
    sprite = "red_ghost"

    def __init__(self, x, y, sprite="red_ghost", type="closest"):
        self.pos = Position(x, y)
        self.old_pos = Position(x, y)
        self.sprite = sprite
        self.type = type

    def move(self):
        global map
        if self.type == "closest":
            path = astar(map.tilemap, red.pos, pacman.pos)
            if path.__len__() > 1:
                path = path[1]
                if path.y > red.pos.y:
                    red.direction = "down"
                elif path.y < red.pos.y:
                    red.direction = "up"
                elif path.x > red.pos.x:
                    red.direction = "right"
                elif path.x < red.pos.x:
                    red.direction = "left"
        # elif type=="":               inne schematy ruchu duszków
        teleport = False
        self.old_pos = self.pos
        new_x = self.pos.x
        new_y = self.pos.y
        if self.direction == "right":
            new_x += 1
        elif self.direction == "left":
            new_x -= 1
        elif self.direction == "down":
            new_y += 1
        elif self.direction == "up":
            new_y -= 1

        if new_y < 0:
            new_y = MAPHEIGHT + new_y
            teleport = True
        if new_y >= MAPHEIGHT:
            new_y = new_y - MAPHEIGHT
            teleport = True
        if new_x < 0:
            new_x = MAPWIDTH + new_x
            teleport = True
        if new_x >= MAPWIDTH:
            new_x = new_x - MAPWIDTH
            teleport = True
        if map.tilemap[new_y][new_x] != WALL:
            self.pos = Position(new_x, new_y)
            if teleport:
                self.move()


# ZMIENNE
clock = pygame.time.Clock()
map = Map()
map.init_map()
map.init_fruits()
pacman = Pacman(2, 2)
red = Ghost(7, 7)
name = ""
font_name = "gothic.ttf"
score = 0
lives = 5


# FUNKCJE
def write_score():
    global score, name
    tuple1=(int(score), name)
    with open('L.csv', 'r') as file:
        rd = csv.reader(file, delimiter=";")
        score_list = list(rd)
    file.close()
    file = open('L.csv', 'w')
    file.close()
    with open('L.csv', 'w', newline='') as file:
        for r in score_list:
            r[0] = int(r[0])
        tplist = [tuple(r) for r in score_list]
        tplist.sort(key=operator.itemgetter(0), reverse=True)
        tplist.append(tuple1)
        tplist.sort(key=operator.itemgetter(0), reverse=True)
        del tplist[10:]
        file.truncate(0)
        wrt = csv.writer(file, delimiter=";")
        for t in tplist:
            wrt.writerow(t)


def draw_text(text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (175, 20, 61))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    DISPLAYSURF.blit(text_surface, text_rect)


def repaint_map(*sprites_on_map):
    global map
    for column in range(MAPWIDTH):
            DISPLAYSURF.blit(TEXTURES[map.tilemap[0][column]], (TILESIZE*column, TILESIZE*0))
    for sprite in sprites_on_map:
        for pos in [sprite.pos, sprite.old_pos]:
            DISPLAYSURF.blit(TEXTURES[map.tilemap[pos.y][pos.x]], (TILESIZE * pos.x, TILESIZE * pos.y))
            if pos in map.fruits:
                DISPLAYSURF.blit(TEXTURES["fruit"], (TILESIZE * pos.x, TILESIZE * pos.y))


# rysowanie pacmana i duszków (średnia ważona starej i nowej pozycji, aby ruch był płynny)
def paint_sprite(sprite, is_pacman, max_move_counter, move_counter):
    if is_pacman:
        DISPLAYSURF.blit(PACMAN_SPRITES[sprite.sprite],
                         (((TILESIZE * sprite.old_pos.x * (max_move_counter - move_counter)) +
                           (TILESIZE * sprite.pos.x * move_counter)) / max_move_counter,
                          ((TILESIZE * sprite.old_pos.y * (max_move_counter - move_counter)) +
                           (TILESIZE * sprite.pos.y * move_counter)) / max_move_counter))
    else:
        DISPLAYSURF.blit(GHOST_SPRITES[sprite.sprite],
                         (((TILESIZE * sprite.old_pos.x * (max_move_counter - move_counter)) +
                           (TILESIZE * sprite.pos.x * move_counter)) / max_move_counter,
                          ((TILESIZE * sprite.old_pos.y * (max_move_counter - move_counter)) +
                           (TILESIZE * sprite.pos.y * move_counter)) / max_move_counter))


def koniec():
    write_score()
    display_surface = pygame.display.set_mode((X, Y))
    pygame.display.set_caption('DEATH')
    font = pygame.font.Font('gothic.ttf', 100)
    text = font.render('YOU DIED', True, crimson, black)
    text_rect = text.get_rect()
    text_rect.center = (X // 2, Y // 2)
    time.sleep(1)
    while True:
        display_surface.fill(black)
        display_surface.blit(text, text_rect)
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
        pygame.display.update()
        clock.tick()


def main(playername="mleko"):
    global lives, name, score
    name = playername
    pygame.init()
    pygame.display.set_caption("Pacman")
    ticks = 0
    pacman_move_counter = 30
    red_move_counter = 60
    for row in range(MAPHEIGHT):
        for column in range(MAPWIDTH):
            DISPLAYSURF.blit(TEXTURES[map.tilemap[row][column]], (TILESIZE*column, TILESIZE*row))
    for fruit in map.fruits:
        DISPLAYSURF.blit(TEXTURES["fruit"], (TILESIZE * fruit.x, TILESIZE * fruit.y))
    while True:
        # obsługa eventów i klawiszy
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    pacman.direction = "right"
                elif event.key == K_LEFT:
                    pacman.direction = "left"
                elif event.key == K_DOWN:
                    pacman.direction = "down"
                elif event.key == K_UP:
                    pacman.direction = "up"
        # ruch
        if ticks % pacman_move_counter == 0:
            pacman.move()
        if ticks % red_move_counter == 0:
            red.move()
        # rysowanie mapy
        repaint_map(pacman, red)  # odświeża tylko pola, które trzeba odświeżyć

        if not pacman.invincible or ticks % 5 != 0:  # miganie jeśli pacman jest niewrazliwy
            paint_sprite(pacman, True, pacman_move_counter, ticks % pacman_move_counter)
        paint_sprite(red, False, red_move_counter, ticks % red_move_counter)

        draw_text("Score: " + str(score), 30, 380, 15)
        draw_text("Player: " + name, 30, 140, 15)
        for i in range(lives):
            DISPLAYSURF.blit(TEXTURES["heart"], (500+40*i, 10))

        if (red.old_pos == pacman.old_pos or red.pos == pacman.old_pos or red.old_pos == pacman.pos) and not pacman.invincible:
            lives -= 1
            pacman.invincible = True
            pacman.inv_time = 400
            if lives < 1:
                koniec()

        if pacman.invincible:
            pacman.inv_time -= 1
            if pacman.inv_time == 0:
                pacman.invincible = False
        ticks += 1
        pygame.display.update()
        clock.tick(100)
