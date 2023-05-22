import pygame
from Game import *
from Settings import *

# In the map, empty space is, unsurprisingly, represented by a space in the map string.
# Any other character represents a wall.  The character used for the wall tells the 
# class what texture to use for the wall.
#
# The "dash" at the end represents the end of the current map row.
#
# The map string should be the same aspect ratio as the screen (in the case of this 
# game, 16:9).  In other words, the screen resolution width divided by number of columns 
# should equal the screen resolution height divided by number of rows.  There are zero
# checks for this, so be careful designing maps.

class Map:

    class MapSquare:
        def __init__(self, row, col, kind, size, is_wall):
            self.kind = kind
            self.row = row
            self.col = col
            self.x = col * size
            self.y = row * size
            self.is_wall = is_wall

    def __init__(self, game):
        self.game = game
        self.squares = {}
        self.square_size = SCREEN_WIDTH / 16

        self.map_string = \
            "1111111111111111-"\
            "1              1-"\
            "1  1111    111 1-"\
            "1     1      1 1-"\
            "1  1111      1 1-"\
            "1              1-"\
            "1              1-"\
            "1  1    1      1-"\
            "1111111111111111-"

        self.generate_map();


    def draw_topdown(self):
        for square in self.squares.values():
            if square.is_wall:
                pygame.draw.rect(self.game.screen, "blue", 
                    (square.x,          # screen x coordinate
                    square.y,           # screen y coordinate
                    self.square_size,   # width of rect
                    self.square_size    # height of rect
                    ), 2)

    def xy_to_rc(self, x, y):
        # convert a screen x-y coordinate into the 
        # row and column of the square that coordinate is inside of
        return int(y/self.square_size), int(x/self.square_size)


    def generate_map(self):

        # We need to keep track of the numeric coordinates of each "square" on the map.
        rows = self.map_string.split('-')

        for row, rowstring in enumerate(rows):
            for col, kind in enumerate([ch for ch in rowstring]):
                square = self.MapSquare(row, col, kind, self.square_size, (kind != ' '))
                self.squares[(row,col)] = square
