import math
from Settings import *


def wrap_angle(angle):
    # force angle to be between 0 and 360 degrees
    angle = angle % DEG_360
    if angle < 0:
        angle += DEG_360
    return angle

def wrap_angle_180(angle):
    # force angle to be between -180 and 180
    angle = wrap_angle(angle)
    if angle > DEG_180:
        angle -= DEG_360
    return angle

def to_degrees(x):
    return 360 * x / DEG_360

def xy_to_cr(x, y):
    # convert a map x-y coordinate into the 
    # row and column of the tile that coordinate is inside of
    return x//TILE_SIZE, y//TILE_SIZE

def get_cr_dir(angle):
    # what direction are we going?

    angle = wrap_angle(angle)

    c_incr = 0
    r_incr = 0

    if angle == 0 or angle == DEG_360:
        # east
        c_incr = 1
    elif angle == DEG_90:
        # south
        r_incr = 1
    elif angle == DEG_180:
        # west
        c_incr = -1
    elif angle == DEG_270:
        # north
        r_incr = -1
    elif 0 < angle and angle < DEG_90:
        # south east
        c_incr = 1
        r_incr = 1
    elif DEG_90 < angle and angle < DEG_180:
        # south west
        c_incr = -1
        r_incr = 1
    elif DEG_180 < angle and angle < DEG_270:
        # north west
        c_incr = -1
        r_incr = -1
    elif DEG_270 < angle and angle < DEG_360:
        # north east
        c_incr = 1
        r_incr = -1
    
    return c_incr, r_incr

