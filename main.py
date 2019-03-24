import pygame
import sys
from pygame.locals import *

#typy powierzchni
WALL = 0
FLOOR = 1


pacman_pos = {"row": 2, "column": 2}
pacman_sprite = "pacman_right"

TILESIZE = 50
MAPWIDTH = 16
MAPHEIGHT = 16
DISPLAYSURF = pygame.display.set_mode((MAPWIDTH*TILESIZE, MAPHEIGHT*TILESIZE))

SPRITES = {
    WALL: pygame.image.load("res/wall.png"),
    FLOOR: pygame.image.load("res/floor.png"),
    "pacman_up": pygame.image.load("res/pacman_u.png"),
    "pacman_right": pygame.image.load("res/pacman_r.png"),
    "pacman_down": pygame.image.load("res/pacman_d.png"),
    "pacman_left": pygame.image.load("res/pacman_l.png")
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


clock = pygame.time.Clock()


def move_pacman(row_diff, column_diff):
    global pacman_sprite
    if column_diff > 0:
        pacman_sprite = "pacman_right"
    elif column_diff < 0:
        pacman_sprite = "pacman_left"
    elif row_diff > 0:
        pacman_sprite = "pacman_down"
    elif row_diff < 0:
        pacman_sprite = "pacman_up"
    new_row = pacman_pos["row"] + row_diff
    new_column = pacman_pos["column"] + column_diff

    if new_row < 0:
        new_row = MAPHEIGHT + new_row

    if new_row >= MAPHEIGHT:
        new_row = new_row - MAPHEIGHT

    if new_column < 0:
        new_column = MAPWIDTH + new_column

    if new_column >= MAPWIDTH:
        new_column = new_column - MAPWIDTH

    if TILEMAP[new_row][new_column] != WALL:
        pacman_pos["row"] = new_row
        pacman_pos["column"] = new_column


def main():
    pygame.init()
    pygame.display.set_caption("Pacman")
    while True:
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            move_pacman(0, 1)
        elif pygame.key.get_pressed()[pygame.K_LEFT]:
            move_pacman(0, -1)
        elif pygame.key.get_pressed()[pygame.K_DOWN]:
            move_pacman(1, 0)
        elif pygame.key.get_pressed()[pygame.K_UP]:
            move_pacman(-1, 0)
        # obsługa eventów i klawiszy
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # rysowanie mapy
        for row in range(MAPHEIGHT):
            for column in range(MAPWIDTH):
                DISPLAYSURF.blit(SPRITES[TILEMAP[row][column]], (TILESIZE*column, TILESIZE*row))
        DISPLAYSURF.blit(SPRITES[pacman_sprite], (TILESIZE * pacman_pos["column"], TILESIZE * pacman_pos["row"]))
        pygame.display.update()
        clock.tick(30)


if __name__ == "__main__":
    main()
