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
    "fruit": pygame.image.load("res/fruit.png"),
    "heart": pygame.image.load("res/heart.png")
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
score = 0
lives = 5
font_name = pygame.font.match_font('comicsansms')
fruits = set()
for x in range(MAPWIDTH):
    for y in range(MAPHEIGHT):
        if TILEMAP[x][y] == FLOOR:
            fruits.add((x, y))
tiles_to_repaint = set()


# FUNKCJE
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


def main():
    global tiles_to_repaint
    pygame.init()
    pygame.display.set_caption("Pacman")
    move_counter = 0
    max_move_counter = 20  # im mniej tym szybszy ruch pacmana, im więcej tym płynniejszy
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
        repaint_map()  #
        # rysowanie pacmana (średnia ważona starej i nowej pozycji, aby ruch był płynny)
        DISPLAYSURF.blit(PACMAN_SPRITES[pacman.sprite],
                         (((TILESIZE * pacman.old_pos["column"] * (max_move_counter-move_counter)) +
                          (TILESIZE * pacman.pos["column"] * move_counter))/max_move_counter,
                          ((TILESIZE * pacman.old_pos["row"] * (max_move_counter - move_counter)) +
                          (TILESIZE * pacman.pos["row"] * move_counter))/max_move_counter))
        draw_text("Score: " + str(score), 20, 200, 10)
        for i in range(lives):
            DISPLAYSURF.blit(TEXTURES["heart"], (500+40*i, 10))
        move_counter += 1
        pygame.display.update()
        clock.tick(100)


if __name__ == "__main__":
    main()


