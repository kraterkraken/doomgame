import math
from Settings import *


def wrap_angle(angle):
    return angle % (2.0*math.pi)

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

def get_cr_dir(angle):
    # what direction are we going?

    angle = wrap_angle(angle)

    c_incr = 0
    r_incr = 0

    if angle == 0 or angle == TWO_PI:
        # east
        c_incr = 1
    elif angle == HALF_PI:
        # south
        r_incr = 1
    elif angle == math.pi:
        # west
        c_incr = -1
    elif angle == HALF_3PI:
        # north
        r_incr = -1
    elif 0 < angle and angle < HALF_PI:
        # south east
        c_incr = 1
        r_incr = 1
    elif HALF_PI < angle and angle < math.pi:
        # south west
        c_incr = -1
        r_incr = 1
    elif math.pi < angle and angle < HALF_3PI:
        # north west
        c_incr = -1
        r_incr = -1
    elif HALF_3PI < angle and angle < TWO_PI:
        # north east
        c_incr = 1
        r_incr = -1
    
    return c_incr, r_incr

