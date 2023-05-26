import math

def sign(x):
    if x == 0: return 0
    if x > 0: return 1
    if x < 0: return -1

def depth(x0, y0, x1, y1):
    return math.sqrt((x1-x0)**2 + (y1-y0)**2)