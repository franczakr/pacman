import pygame
import sys
import csv
import operator
import time
from pygame.locals import *


# KLASY
class Pacman:
    old_pos = {"row": 2, "column": 2}
    pos = {"row": 2, "column": 2}
    sprite = "right"
    direction = (0, 1)

class Red:
    old_pos = {"row": 1, "column": 1}
    pos = {"row": 1, "column": 1}
    sprite = "right"
    direction = (0, 1)

# STAŁE
# typy powierzchni
WALL = 0
FLOOR = 1

TILESIZE = 50
MAPWIDTH = 16
MAPHEIGHT = 16
DISPLAYSURF = pygame.display.set_mode((MAPWIDTH*TILESIZE, MAPHEIGHT*TILESIZE))
black = (0, 0, 0)
crimson = (105, 0, 21)


# assigning values to X and Y variable
X = 800
Y = 800

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
    "red": pygame.image.load("res/red.png")
}


TILEMAP = [
    [WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL],
    [WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL],
    [WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL],
    [FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL, WALL, FLOOR, FLOOR, WALL, WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR],
    [FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL, WALL, FLOOR, FLOOR, WALL, WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR],
    [WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL],
    [WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL],
    [WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL],
    [WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL],
    [WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL],
    [WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL],
    [FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL, WALL, FLOOR, FLOOR, WALL, WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR],
    [FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL, WALL, FLOOR, FLOOR, WALL, WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR],
    [WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL],
    [WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL],
    [WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL],
]

# ZMIENNE
clock = pygame.time.Clock()
pacman = Pacman()
red=Red()
score = 0
lives = 1
invincible=False
inv_time=400
name="abc"
font_name = pygame.font.match_font('comicsansms')


# DODAWANIE OWOCOW
fruits = set()
for x in range(1,MAPWIDTH-1):
    for y in range(1,MAPHEIGHT-1):
        if TILEMAP[x][y] == FLOOR:
            fruits.add((x, y))
tiles_to_repaint = set()


# FUNKCJE
def write_score():
    global score,name
    tuple1=(int(score),name)
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
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    DISPLAYSURF.blit(text_surface, text_rect)


def repaint_map():
    global tiles_to_repaint
    for column in range(MAPWIDTH):
            DISPLAYSURF.blit(TEXTURES[TILEMAP[0][column]], (TILESIZE*column, TILESIZE*0))
    for (row, column) in tiles_to_repaint:
        DISPLAYSURF.blit(TEXTURES[TILEMAP[row][column]], (TILESIZE * column, TILESIZE * row))
        if (row, column) in fruits:
            DISPLAYSURF.blit(TEXTURES["fruit"], (TILESIZE * column, TILESIZE * row))


def move_pacman(row_diff, column_diff):
    global score, lives, tiles_to_repaint
    teleport = False
    pacman.old_pos["row"] = pacman.pos["row"]
    pacman.old_pos["column"] = pacman.pos["column"]
    tiles_to_repaint.add((pacman.old_pos["row"], pacman.old_pos["column"]))
    if (pacman.old_pos["row"], pacman.old_pos["column"]) in fruits:
        fruits.remove((pacman.old_pos["row"], pacman.old_pos["column"]))
        score += 10
    if column_diff > 0:
        pacman.sprite = "right"
    elif column_diff < 0:
        pacman.sprite = "left"
    elif row_diff > 0:
        pacman.sprite = "down"
    elif row_diff < 0:
        pacman.sprite = "up"
    new_row = pacman.pos["row"] + row_diff
    new_column = pacman.pos["column"] + column_diff

    if new_row < 0:
        new_row = MAPHEIGHT + new_row
        teleport = True
    if new_row >= MAPHEIGHT:
        new_row = new_row - MAPHEIGHT
        teleport = True
    if new_column < 0:
        new_column = MAPWIDTH + new_column
        teleport = True
    if new_column >= MAPWIDTH:
        new_column = new_column - MAPWIDTH
        teleport = True
    if TILEMAP[new_row][new_column] != WALL:
        pacman.pos["row"] = new_row
        pacman.pos["column"] = new_column
        tiles_to_repaint.add((pacman.pos["row"], pacman.pos["column"]))
        if teleport:
            move_pacman(row_diff, column_diff)

def move_red(row_diff, column_diff):
    teleport = False
    red.old_pos["row"] = Red.pos["row"]
    red.old_pos["column"] = Red.pos["column"]
    tiles_to_repaint.add((red.old_pos["row"], red.old_pos["column"]))
    new_row = red.pos["row"] + row_diff
    new_column = red.pos["column"] + column_diff

    if new_row < 0:
        new_row = MAPHEIGHT + new_row
        teleport = True
    if new_row >= MAPHEIGHT:
        new_row = new_row - MAPHEIGHT
        teleport = True
    if new_column < 0:
        new_column = MAPWIDTH + new_column
        teleport = True
    if new_column >= MAPWIDTH:
        new_column = new_column - MAPWIDTH
        teleport = True
    if TILEMAP[new_row][new_column] != WALL:
        red.pos["row"] = new_row
        red.pos["column"] = new_column
        tiles_to_repaint.add((red.pos["row"], red.pos["column"]))
        if teleport:
            move_red(row_diff, column_diff)


def main(playername):
    global tiles_to_repaint,lives,inv_time,invincible,name
    name=playername
    pygame.init()
    pygame.display.set_caption("Pacman")
    move_counter = 0
    max_move_counter = 30  # im mniej tym szybszy ruch pacmana, im więcej tym płynniejszy
    for row in range(MAPHEIGHT):
        for column in range(MAPWIDTH):
            DISPLAYSURF.blit(TEXTURES[TILEMAP[row][column]], (TILESIZE*column, TILESIZE*row))
    for fruit in fruits:
        DISPLAYSURF.blit(TEXTURES["fruit"], (TILESIZE * fruit[1], TILESIZE * fruit[0]))
    while True:
        if move_counter == max_move_counter:
            tiles_to_repaint = set()
            move_counter = 0
            move_pacman(pacman.direction[0], pacman.direction[1])
            move_red(red.direction[0], red.direction[1])
        # obsługa eventów i klawiszy
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    pacman.direction = (0, 1)
                elif event.key == K_LEFT:
                    pacman.direction = (0, -1)
                elif event.key == K_DOWN:
                    pacman.direction = (1, 0)
                elif event.key == K_UP:
                    pacman.direction = (-1, 0)
        # rysowanie mapy
        repaint_map()  # odświeża tylko pola, które trzeba odświeżyć
        # rysowanie pacmana (średnia ważona starej i nowej pozycji, aby ruch był płynny)
        DISPLAYSURF.blit(PACMAN_SPRITES[pacman.sprite],
                         (((TILESIZE * pacman.old_pos["column"] * (max_move_counter-move_counter)) +
                          (TILESIZE * pacman.pos["column"] * move_counter))/max_move_counter,
                          ((TILESIZE * pacman.old_pos["row"] * (max_move_counter - move_counter)) +
                          (TILESIZE * pacman.pos["row"] * move_counter))/max_move_counter))

        DISPLAYSURF.blit(GHOST_SPRITES["red"],
                         (((TILESIZE * red.old_pos["column"] * (max_move_counter - move_counter)) +
                           (TILESIZE * red.pos["column"] * move_counter)) / max_move_counter,
                          ((TILESIZE * red.old_pos["row"] * (max_move_counter - move_counter)) +
                           (TILESIZE * red.pos["row"] * move_counter)) / max_move_counter))

        draw_text("Score: " + str(score), 20, 400, 10)
        draw_text("Player: " + playername, 20, 80, 10)
        for i in range(lives):
            DISPLAYSURF.blit(TEXTURES["heart"], (500+40*i, 10))

        if (red.old_pos["column"] == pacman.old_pos["column"] and red.old_pos["row"] == pacman.old_pos["row"] and invincible==False):
            lives = lives - 1
            invincible=True
            inv_time=400
            if (lives < 1):
                write_score()
                display_surface = pygame.display.set_mode((X, Y))
                pygame.display.set_caption('DEATH')
                font = pygame.font.Font('gothic.ttf', 100)
                text = font.render('YOU DIED', True, crimson, black)
                textRect = text.get_rect()
                textRect.center = (X // 2, Y // 2)
                while True:
                    display_surface.fill(black)
                    display_surface.blit(text, textRect)
                    for event in pygame.event.get():
                        if event.type == pygame.KEYUP:
                            time.sleep(5)
                            pygame.display.quit()
                            pygame.quit()
                            sys.exit(1)
                            quit()
                        pygame.display.update()
        if(invincible==True):
            inv_time=inv_time-1
            if(inv_time==0):
                invincible=False
        move_counter += 1
        pygame.display.update()
        clock.tick(100)




