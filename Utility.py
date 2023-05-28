import math
from Settings import *

def sign(x):
    if x == 0: return 0
    if x > 0: return 1
    if x < 0: return -1

def depth(x0, y0, x1, y1):
    # pythagorean theorem
    return math.sqrt((x1-x0)**2 + (y1-y0)**2)

def xy_to_cr(x, y):
    # convert a map x-y coordinate into the 
    # row and column of the tile that coordinate is inside of
    return x//TILE_SIZE, y//TILE_SIZE

