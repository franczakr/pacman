import pygame
import sys
from pygame.locals import *

#typy powierzchni
WALL = 0
FLOOR = 1
PACMAN = 2

pacman_pos = {"row": 2, "column": 2}

TILESIZE = 50
MAPWIDTH = 8
MAPHEIGHT = 8
DISPLAYSURF = pygame.display.set_mode((MAPWIDTH*TILESIZE, MAPHEIGHT*TILESIZE))

COLORS = {
    WALL: pygame.image.load("res/wall.png"),
    FLOOR: pygame.image.load("res/floor.png"),
    PACMAN: pygame.image.load("res/pacman.png")
}

TILEMAP = [
    [WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL],
    [WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL],
    [WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL],
    [FLOOR, FLOOR, FLOOR, WALL, WALL, FLOOR, FLOOR, FLOOR],
    [WALL, FLOOR, FLOOR, WALL, WALL, FLOOR, FLOOR, WALL],
    [WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL],
    [WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL],
    [WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL],
]


def move_pacman(row_diff, column_diff):
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
        # obsługa eventów i klawiszy
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    move_pacman(0, -1)
                elif event.key == K_RIGHT:
                    move_pacman(0, 1)
                elif event.key == K_UP:
                    move_pacman(-1, 0)
                elif event.key == K_DOWN:
                    move_pacman(1, 0)

        # rysowanie mapy
        for row in range(MAPHEIGHT):
            for column in range(MAPWIDTH):
                DISPLAYSURF.blit(COLORS[TILEMAP[row][column]], (TILESIZE*column, TILESIZE*row))
        DISPLAYSURF.blit(COLORS[PACMAN], (TILESIZE * pacman_pos["column"], TILESIZE * pacman_pos["row"]))
        pygame.display.update()


if __name__ == "__main__":
    main()
