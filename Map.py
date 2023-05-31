import pygame
import sys
from Game import *
from Settings import *
from Utility import *

# In the map string, empty space is, unsurprisingly, represented by a space in the map string.
# Any other character represents a wall.  The character used for the wall tells the 
# class what texture to use for the wall.
#
# The "dash" at the end represents the end of the current map row.
#
# The map string should be the same aspect ratio as the screen (in the case of this 
# game, 16:9).  In other words, the screen resolution width divided by number of columns 
# must equal the screen resolution height divided by number of rows.

class Map:

    class MapSquare:
        def __init__(self, row, col, tid, is_wall):
            self.texture_id = tid
            self.row = row
            self.col = col
            self.x = col * TILE_SIZE
            self.y = row * TILE_SIZE
            self.is_wall = is_wall

    def __init__(self, game):
        self.game = game
        self.squares = {}

        self.map_string = \
            "BBBBBBBBBGBBBBBB-"\
            "B              B-"\
            "B  BBBB    BBB B-"\
            "B     G      B B-"\
            "B  BBBB      B B-"\
            "B              B-"\
            "B              S-"\
            "B  P    P      B-"\
            "BBBBPPPPBBBBGBBB"

        if self.is_good_map():
            self.generate_map();
        else:
            print("Error: Map aspect ratio does not equal screen aspect ratio. Quitting.")
            sys.exit()

    def is_good_map(self):
        map_rows = self.map_string.split('-')
        if SCREEN_HEIGHT != TILE_SIZE * len(map_rows):
            return False
        for row in map_rows:
            if SCREEN_WIDTH != TILE_SIZE * len(row):
                return False
        return True

    def is_in_wall(self, x, y):
        c, r = xy_to_cr(x, y)
        return self.squares[c, r].is_wall, c, r

    def draw(self):
        if TOPDOWN:
            for square in self.squares.values():
                color = "gray15"
                if square.is_wall:
                    color = "blue"
                pygame.draw.rect(self.game.screen, color, 
                    (square.x,          # screen x coordinate
                    square.y,           # screen y coordinate
                    TILE_SIZE,          # width of rect
                    TILE_SIZE           # height of rect
                    ), 2)

    def generate_map(self):
        rows = self.map_string.split('-')
        for row, rowstring in enumerate(rows):
            for col, tid in enumerate([ch for ch in rowstring]):
                square = self.MapSquare(row, col, tid, (tid != ' '))
                self.squares[(col, row)] = square
