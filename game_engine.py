import pygame
import sys
import csv
import operator
import time
from pygame.locals import QUIT, KEYDOWN, K_RIGHT, K_UP, K_LEFT, K_DOWN
from map import Map, Position, FR, WL, MAPHEIGHT, MAPWIDTH
from astar import astar
from random import randint
from math import sqrt
import map_loader
import menu

TILESIZE = 50
DISPLAYSURF = pygame.display.set_mode((MAPWIDTH * TILESIZE, MAPHEIGHT * TILESIZE))
black = (0, 0, 0)
crimson = (105, 0, 21)
font_name = "gothic.ttf"

X = MAPWIDTH * TILESIZE
Y = MAPHEIGHT * TILESIZE


def main(name):
    (lives, score) = (5, 0)
    maps_files = map_loader.load_maps()
    for map_file in maps_files:
        if lives > 0:
            if score > 0:
                win_map(score)
            game = Game(name, map_file, lives, score)
            (lives, score) = game.start()
        else:
            break
    write_score(name, score)
    if lives > 0:
        end_win(score)
    else:
        end_lost(score)
    menu.mainloop(name)


class Game:
    TEXTURES = {
        WL: pygame.image.load("res/wall.png"),
        FR: pygame.image.load("res/floor.png"),
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

    def __init__(self, playername, map_file, lives=5, score=0):
        self.name = playername
        self.clock = pygame.time.Clock()
        tilemap = map_loader.parse_map(map_file)
        self.map = Map(tilemap)
        self.map.init_fruits()
        self.lives = lives
        self.score = score
        self.pacman = Pacman(1, 1, 30)
        # GHOSTS
        red = Ghost(14, 14, 45, "red_ghost")
        blue = Ghost(12, 8, 50, "blue_ghost")
        pink = Ghost(7, 7, 60, "pink_ghost")
        yellow = Ghost(1, 14, 70, "yellow_ghost")
        self.ghosts = [red, blue, pink, yellow]

    def repaint_map(self, *sprites_on_map):
        for column in range(MAPWIDTH):
            DISPLAYSURF.blit(self.TEXTURES[self.map.tilemap[0][column]], (TILESIZE*column, 0))
        for sprite in sprites_on_map:
            for pos in [sprite.pos, sprite.old_pos]:
                DISPLAYSURF.blit(self.TEXTURES[self.map.tilemap[pos.y][pos.x]],
                                 (TILESIZE * pos.x, TILESIZE * pos.y))
                if pos in self.map.fruits:
                    DISPLAYSURF.blit(self.TEXTURES["fruit"],
                                     (TILESIZE * pos.x, TILESIZE * pos.y))

    # zwraca jedną składową pozycji (x lub y)
    def get_position(self, old_pos, pos, move_counter, current_move_counter):
        return (old_pos * (move_counter - current_move_counter) + pos * current_move_counter)\
               * TILESIZE / move_counter

    # zwraca odległość od jednej postaci do drugiej
    def get_distance(self, sprite1, sprite2, ticks):
        x1 = self.get_position(sprite1.old_pos.x, sprite1.pos.x, sprite1.move_counter, ticks % sprite1.move_counter)
        x2 = self.get_position(sprite2.old_pos.x, sprite2.pos.x, sprite2.move_counter, ticks % sprite2.move_counter)
        y1 = self.get_position(sprite1.old_pos.y, sprite1.pos.y, sprite1.move_counter, ticks % sprite1.move_counter)
        y2 = self.get_position(sprite2.old_pos.y, sprite2.pos.y, sprite2.move_counter, ticks % sprite2.move_counter)
        return sqrt((x2-x1)**2 + (y2-y1)**2)

    # rysowanie pacmana i duszków (średnia ważona starej i nowej pozycji, aby ruch był płynny)
    def paint_sprite(self, sprite, is_pacman, ticks):
        current_move_counter = ticks % sprite.move_counter
        if is_pacman:
            DISPLAYSURF.blit(self.PACMAN_SPRITES[sprite.sprite],
                             (self.get_position(sprite.old_pos.x, sprite.pos.x, sprite.move_counter,
                                                current_move_counter),
                              self.get_position(sprite.old_pos.y, sprite.pos.y, sprite.move_counter,
                                                current_move_counter)))
        else:
            DISPLAYSURF.blit(self.GHOST_SPRITES[sprite.sprite],
                             (self.get_position(sprite.old_pos.x, sprite.pos.x, sprite.move_counter,
                                                current_move_counter),
                              self.get_position(sprite.old_pos.y, sprite.pos.y, sprite.move_counter,
                                                current_move_counter)))

    def start(self):
        pygame.init()
        pygame.display.set_caption("Pacman")
        ticks = 0
        for row in range(MAPHEIGHT):
            for column in range(MAPWIDTH):
                DISPLAYSURF.blit(self.TEXTURES[self.map.tilemap[row][column]],
                                 (TILESIZE*column, TILESIZE*row))
        for fruit in self.map.fruits:
            DISPLAYSURF.blit(self.TEXTURES["fruit"],
                             (TILESIZE * fruit.x, TILESIZE * fruit.y))
        while True:
            self.repaint_map(self.pacman, *self.ghosts)  # odświeża tylko pola, które trzeba odświeżyć
            # obsługa eventów i klawiszy
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_RIGHT:
                        self.pacman.direction = "right"
                    elif event.key == K_LEFT:
                        self.pacman.direction = "left"
                    elif event.key == K_DOWN:
                        self.pacman.direction = "down"
                    elif event.key == K_UP:
                        self.pacman.direction = "up"
            # ruch
            if ticks % self.pacman.move_counter == 0:
                self.pacman.move(self)
            for ghost in self.ghosts:
                if ticks % ghost.move_counter == 0:
                    ghost.move(self)

            if not self.pacman.invincible or ticks % 5 != 0:  # miganie jeśli pacman jest niewrazliwy
                self.paint_sprite(self.pacman, True, ticks)
            for ghost in self.ghosts:
                self.paint_sprite(ghost, False, ticks)

            draw_text("Score: " + str(self.score), 35, 380, 15)
            draw_text("Player: " + self.name, 35, 140, 15)
            for i in range(self.lives):
                DISPLAYSURF.blit(self.TEXTURES["heart"], (500+40*i, 10))

            for ghost in self.ghosts:
                if self.get_distance(self.pacman, ghost, ticks) < TILESIZE * 2 / 3 and not self.pacman.invincible:
                    self.lives -= 1
                    self.pacman.invincible = True
                    self.pacman.inv_time = 200
                    if self.lives < 1:
                        return self.lives, self.score

            if not self.map.fruits:
                return self.lives, self.score

            if self.pacman.invincible:
                self.pacman.inv_time -= 1
                if self.pacman.inv_time == 0:
                    self.pacman.invincible = False
            ticks += 1
            pygame.display.update()
            self.clock.tick(100)


class Pacman:
    pos = Position(0, 0)
    old_pos = Position(0, 0)
    direction = "right"
    sprite = "right"
    invincible = False
    inv_time = 400

    def __init__(self, x, y, move_counter):
        self.pos = Position(x, y)
        self.old_pos = Position(x, y)
        self.move_counter = move_counter

    def move(self, game):
        self.sprite = self.direction
        teleport = False
        self.old_pos = self.pos
        if self.old_pos in game.map.fruits:
            game.map.fruits.remove(self.old_pos)
            game.score += 10

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
        if game.map.tilemap[new_y][new_x] != WL:
            self.pos = Position(new_x, new_y)
            if teleport:
                self.move(game)


class Ghost:
    pos = Position(0, 0)
    old_pos = Position(0, 0)
    direction = "right"

    def __init__(self, x, y, move_counter, sprite):
        self.pos = Position(x, y)
        self.old_pos = Position(x, y)
        self.move_counter = move_counter
        self.sprite = sprite

    def move(self, game):
        x = int(game.pacman.pos.x)
        y = int(game.pacman.pos.y)
        tmp = Position(x, y)
        if self.sprite == "blue_ghost":
            if game.pacman.direction == "right":
                tmp.x = min(MAPWIDTH - 2, (tmp.x + 4))
            if game.pacman.direction == "left":
                tmp.x = max((tmp.x - 4), 2)
            if game.pacman.direction == "up":
                tmp.y = min((tmp.y + 4), MAPHEIGHT - 2)
            if game.pacman.direction == "down":
                tmp.y = max((tmp.y - 4), 2)

        if self.sprite == "pink_ghost":
            tmp.x = (self.pos.x + game.pacman.pos.x) // 2
            tmp.y = (self.pos.y + game.pacman.pos.y) // 2

        if self.sprite == "yellow_ghost":
            tmp.x = game.pacman.pos.x + randint(0, 4)
            tmp.y = game.pacman.pos.y + randint(0, 4)

        if tmp.x < 0 or tmp.x >= MAPWIDTH or tmp.y < 0 or tmp.y >= MAPHEIGHT or \
                game.map.tilemap[tmp.y][tmp.x] == WL:
            tmp.x = game.pacman.pos.x
            tmp.y = game.pacman.pos.y

        path = astar(game.map.tilemap, self.pos, tmp)
        if path is not None and path.__len__() > 1:
            path = path[1]
            if path.y > self.pos.y:
                self.direction = "down"
            elif path.y < self.pos.y:
                self.direction = "up"
            elif path.x > self.pos.x:
                self.direction = "right"
            elif path.x < self.pos.x:
                self.direction = "left"
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
        if game.map.tilemap[new_y][new_x] != WL:
            self.pos = Position(new_x, new_y)
            if teleport:
                self.move(game)


def draw_text(text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    DISPLAYSURF.blit(text_surface, text_rect)


def write_score(name, score):
    tuple1 = (int(score), name)
    with open(menu.LEADERBOARD_FILE, 'r') as file:
        rd = csv.reader(file, delimiter=";")
        score_list = list(rd)
    file.close()
    file = open(menu.LEADERBOARD_FILE, 'w')
    file.close()
    with open(menu.LEADERBOARD_FILE, 'w', newline='') as file:
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


def win_map(score):
    show_end_screen('You win this level', 'Your current score is ' + str(score), 'Press any key to continue', 70)


def end_win(score):
    show_end_screen('YOU WIN THE GAME', 'Your score is ' + str(score), 'Press any key to exit', 70)


def end_lost(score):
    show_end_screen('YOU DIED', 'Your score is ' + str(score), 'Press any key to exit')


def show_end_screen(big_text, medium_text, small_text, big_text_font_size=100):
    font = pygame.font.Font('gothic.ttf', big_text_font_size)
    text = font.render(big_text, True, crimson)
    text_rect = text.get_rect()
    text_rect.center = (X // 2, Y // 2)
    font2 = pygame.font.Font('gothic.ttf', 30)
    text2 = font2.render(medium_text, True, crimson)
    text_rect2 = text2.get_rect()
    text_rect2.center = (X // 2, Y * 2 // 3)
    text3 = font2.render(small_text, True, crimson)
    text_rect3 = text3.get_rect()
    text_rect3.center = (X // 2, Y * 2 // 3 + 30)
    DISPLAYSURF.fill(black)
    DISPLAYSURF.blit(text, text_rect)
    pygame.display.update()
    DISPLAYSURF.blit(text2, text_rect2)
    pygame.display.update()
    time.sleep(1)
    DISPLAYSURF.blit(text3, text_rect3)
    pygame.display.update()
    pygame.event.get()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP:
                return
