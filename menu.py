# coding=utf-8

# Import pygame and libraries
from pygame.locals import *
from random import randrange
import os
import pygame
import game_engine
import csv
import pygameMenu
from pygameMenu.locals import *

name = "temporary"
# Import pygameMenu


ABOUT = ['PAKMAN {0}'.format(0.7),
         'Authors:',
         PYGAMEMENU_TEXT_NEWLINE,
         "Rafal Franaczak   and   Dominik Guz"]
COLOR_BACKGROUND = (77, 0, 0)
COLOR_BLACK = (255,255,255)
COLOR_WHITE = (105, 0, 21)
FPS = 60.0
MENU_BACKGROUND_COLOR = (0, 0, 0)
WINDOW_SIZE = (800, 800)

# -----------------------------------------------------------------------------
# Init pygame
pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Create pygame screen and objects
surface = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('MENU_TEST')
clock = pygame.time.Clock()
dt = 1 / FPS

# Global variables
DIFFICULTY = ['EASY']


# -----------------------------------------------------------------------------

def play_function():
    game_engine.main(name)

    while True:

        # Clock tick
        clock.tick(60)


def main_background():
    surface.fill(COLOR_BACKGROUND)


# -----------------------------------------------------------------------------
# PLAY MENU
play_menu = pygameMenu.Menu(surface,
                            bgfun=main_background,
                            color_selected=COLOR_WHITE,
                            font="gothic.ttf",
                            font_color=COLOR_BLACK,
                            font_size=25,
                            menu_alpha=90,
                            font_size_title=50,
                            menu_color=MENU_BACKGROUND_COLOR,
                            menu_color_title=COLOR_WHITE,
                            menu_height=int(WINDOW_SIZE[1] * 0.7),
                            menu_width=int(WINDOW_SIZE[0] * 0.7),
                            onclose=PYGAME_MENU_DISABLE_CLOSE,
                            option_shadow=False,
                            title='Play menu',
                            window_height=WINDOW_SIZE[1],
                            window_width=WINDOW_SIZE[0]
                            )


# ABOUT MENU
about_menu = pygameMenu.TextMenu(surface,
                                 bgfun=main_background,
                                 color_selected=COLOR_WHITE,
                                 font="gothic.ttf",
                                 font_color=COLOR_BLACK,
                                 font_size_title=50,
                                 font_title="gothic.ttf",
                                 menu_color=MENU_BACKGROUND_COLOR,
                                 menu_color_title=COLOR_WHITE,
                                 menu_height=int(WINDOW_SIZE[1] * 0.6),
                                 menu_width=int(WINDOW_SIZE[0] * 0.6),
                                 onclose=PYGAME_MENU_DISABLE_CLOSE,
                                 option_shadow=False,
                                 text_color=COLOR_BLACK,
                                 text_fontsize=16,
                                 title='About',
                                 window_height=WINDOW_SIZE[1],
                                 window_width=WINDOW_SIZE[0]
                                 )
for m in ABOUT:
    about_menu.add_line(m)
about_menu.add_line(PYGAMEMENU_TEXT_NEWLINE)
about_menu.add_option('Return to menu', PYGAME_MENU_BACK)




# LEADERBOARD_MENU
board_menu = pygameMenu.TextMenu(surface,
                                 bgfun=main_background,
                                 color_selected=COLOR_WHITE,
                                 font="gothic.ttf",
                                 font_color=COLOR_BLACK,
                                 font_size_title=50,
                                 font_title="gothic.ttf",
                                 menu_color=MENU_BACKGROUND_COLOR,
                                 menu_color_title=COLOR_WHITE,
                                 menu_height=int(WINDOW_SIZE[1] * 0.6),
                                 menu_width=int(WINDOW_SIZE[0] * 0.6),
                                 onclose=PYGAME_MENU_DISABLE_CLOSE,
                                 option_shadow=False,
                                 text_color=COLOR_BLACK,
                                 text_fontsize=16,
                                 title='Leaderboard',
                                 window_height=WINDOW_SIZE[1],
                                 window_width=WINDOW_SIZE[0]
                                 )

# Read the csv.
with open('L.csv', 'r',) as file:
    rd = csv.reader(file, delimiter=";")
    score_list = list(rd)
    i = 1
    board_menu.add_line("POS                         SCORE                             NAME")
    for row in score_list:
        board_menu.add_line(str(i)+"                                  "+row[0]+"                             "+row[1])
        i = i+1
    file.close()
board_menu.add_line(PYGAMEMENU_TEXT_NEWLINE)
board_menu.add_option('Return to menu', PYGAME_MENU_BACK)

# TIPS_MENU
tip_menu = pygameMenu.TextMenu(surface,
                                 bgfun=main_background,
                                 color_selected=COLOR_WHITE,
                                 font="gothic.ttf",
                                 font_color=COLOR_BLACK,
                                 font_size_title=50,
                                 font_title="gothic.ttf",
                                 menu_color=MENU_BACKGROUND_COLOR,
                                 menu_color_title=COLOR_WHITE,
                                 menu_height=int(WINDOW_SIZE[1] * 0.6),
                                 menu_width=int(WINDOW_SIZE[0] * 0.6),
                                 onclose=PYGAME_MENU_DISABLE_CLOSE,
                                 option_shadow=False,
                                 text_color=COLOR_BLACK,
                                 text_fontsize=16,
                                 title='Tips',
                                 window_height=WINDOW_SIZE[1],
                                 window_width=WINDOW_SIZE[0]
                                 )
tip_menu.add_line("tips will be added SOON...")
tip_menu.add_line(PYGAMEMENU_TEXT_NEWLINE)
tip_menu.add_option('Return to menu', PYGAME_MENU_BACK)

# MAIN MENU
main_menu = pygameMenu.Menu(surface,
                            bgfun=main_background,
                            color_selected=COLOR_WHITE,
                            font="gothic.ttf",
                            font_color=COLOR_BLACK,
                            font_size=30,
                            menu_alpha=100,
                            font_size_title=50,
                            menu_color=MENU_BACKGROUND_COLOR,
                            menu_color_title=COLOR_WHITE,
                            menu_height=int(WINDOW_SIZE[1] * 0.6),
                            menu_width=int(WINDOW_SIZE[0] * 0.6),
                            onclose=PYGAME_MENU_DISABLE_CLOSE,
                            option_shadow=False,
                            title='Main menu',
                            window_height=WINDOW_SIZE[1],
                            window_width=WINDOW_SIZE[0]
                            )
main_menu.add_option('Play', play_function)
main_menu.add_option('Tips', tip_menu)
main_menu.add_option('Leaderboards', board_menu)
main_menu.add_option('About', about_menu)
main_menu.add_option('Quit', PYGAME_MENU_EXIT)


# -----------------------------------------------------------------------------
# Main loop
def mainloop(namen):
    global name
    name = namen
    while True:

        # Tick
        clock.tick(60)

        # Application events
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                exit()

        # Main menu
        main_menu.mainloop(events)

        # Flip surface
        pygame.display.flip()

