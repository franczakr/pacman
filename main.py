import pygame
import sys
from pygame.locals import *


# KLASY
class Pacman:
    old_pos = {"row": 2, "column": 2}
    pos = {"row": 2, "column": 2}
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

TEXTURES = {
    WALL: pygame.image.load("res/wall.png"),
    FLOOR: pygame.image.load("res/floor.png"),
    "fruit": pygame.image.load("res/fruit.png")
}

PACMAN_SPRITES = {
    "up": pygame.image.load("res/pacman_u.png"),
    "right": pygame.image.load("res/pacman_r.png"),
    "down": pygame.image.load("res/pacman_d.png"),
    "left": pygame.image.load("res/pacman_l.png"),
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
fruits = {
    (1, 5),
    (2, 5),
    (2, 6)
}


# FUNKCJE
def move_pacman(row_diff, column_diff):
    teleport = False
    pacman.old_pos["row"] = pacman.pos["row"]
    pacman.old_pos["column"] = pacman.pos["column"]
    if (pacman.old_pos["row"], pacman.old_pos["column"]) in fruits:
        fruits.remove((pacman.old_pos["row"], pacman.old_pos["column"]))
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
        if teleport:
            move_pacman(row_diff, column_diff)


def main():
    pygame.init()
    pygame.display.set_caption("Pacman")
    move_counter = 0
    max_move_counter = 30  # im mniej tym szybszy ruch pacmana
    while True:
        if move_counter == max_move_counter:
            move_counter = 0
            move_pacman(pacman.direction[0], pacman.direction[1])
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
        for row in range(MAPHEIGHT):
            for column in range(MAPWIDTH):
                DISPLAYSURF.blit(TEXTURES[TILEMAP[row][column]], (TILESIZE*column, TILESIZE*row))
        for fruit in fruits:
            DISPLAYSURF.blit(TEXTURES["fruit"], (TILESIZE * fruit[1], TILESIZE * fruit[0]))
        # rysowanie pacmana (średnia ważona starej i nowej pozycji, aby ruch był płynny)
        DISPLAYSURF.blit(PACMAN_SPRITES[pacman.sprite],
                         (((TILESIZE * pacman.old_pos["column"] * (max_move_counter-move_counter)) +
                          (TILESIZE * pacman.pos["column"] * move_counter))/max_move_counter,
                          ((TILESIZE * pacman.old_pos["row"] * (max_move_counter - move_counter)) +
                          (TILESIZE * pacman.pos["row"] * move_counter))/max_move_counter))
        move_counter += 1
        pygame.display.update()
        clock.tick(100)


if __name__ == "__main__":
    main()


