import pygame
import math
from Utility import *
from Settings import *

from Game import *

class RayCaster:

    def __init__(self, game):
        self.game = game


    def ray_cast(self):
        pass

    def is_in_bounds(self, pos):
        if (pos[0] > SCREEN_WIDTH
        or pos[0] < 0
        or pos[1] > SCREEN_HEIGHT
        or pos[1] < 0):
            return False
        else:
            return True

    def find_wall(self, from_x, from_y, angle):
        # return the coordinates of the first wall we hit when we cast a ray 
        # from the given x,y at the given angle

        # this was insanely hard to come up with

        w = self.game.map.square_size # w = width of a square

        cosangle = math.cos(angle)
        sinangle = math.sin(angle)
        tanangle = math.tan(angle)
        signsin = sign(sinangle)
        signcos = sign(cosangle)

        ############ TODO: Possible division by zero errors lurking

        # figure out the increments (wx, dy) for searching "by col"
        h = abs(w / cosangle) # hypotenuse of row-bounded triangle
        dy = h * sinangle
        wx = w * sign(cosangle) # the correct sign for moving width units in x direction

        # figure out the increments (dx, wy) for searching "by row"
        h = abs(w / sinangle) # hypotenuse of column-bounded triangle
        dx = h * cosangle
        wy = w * sign(sinangle) # the correct sign for moving width units in y direction

        # x_0 is the closest column edge to the "from"" in the direction of the ray
        # y_0 is the closest row edge to the "from" in the directon of the ray
        # Math: 
        #   When sin/cos is positive we need to add 1 to the "from" row/col
        #   When sin/cos is negative we need to add ZERO to the "from" row/col
        #   To accomplish this I take the sign of each, add 0.5 and truncate to int.
        from_r = int(from_y/w)
        from_c = int(from_x/w)
        x_0 = w * (from_c + int(signcos + 0.5))
        y_0 = w * (from_r + int(signsin + 0.5))
        # pygame.draw.circle(self.game.screen, "red", (from_x, y_0), 3, 0)
        # pygame.draw.circle(self.game.screen, "orange", (x_0, from_y), 3, 0)

        # by_col is the coordinates where the ray intersects a column edge
        # by_row is the coordinates where the ray intersects a row edge
        # (again, we are starting at the edges closest to the "from" in the ray's direction)
        by_col = [x_0, from_y + (x_0 - from_x) * tanangle]
        by_row = [from_x + (y_0 - from_y) / tanangle, y_0]
        # pygame.draw.circle(self.game.screen, "purple", by_col, 9, 0)
        # pygame.draw.circle(self.game.screen, "pink", by_row, 9, 0)

        wall_hit = 0
        while self.is_in_bounds(by_col):
            # did we hit a wall "by column"?
            # pygame.draw.circle(self.game.screen, "purple", by_col, 9, 0)
            if self.game.map.is_in_wall(by_col[0] + signcos, by_col[1]):
                wall_hit += 1
                break;
            else:
                by_col[0] += wx
                by_col[1] += dy
                
        while self.is_in_bounds(by_row):
            # did we hit a wall "by column"?
            # pygame.draw.circle(self.game.screen, "pink", by_row, 9, 0)
            if self.game.map.is_in_wall(by_row[0], by_row[1] + signsin):
                wall_hit += 2
                break;
            else:
                by_row[0] += dx
                by_row[1] += wy

        # check to see what wall we hit
        if wall_hit == 1:
            # if we only hit a wall incrementing by column, return those coordinates
            return by_col
        elif wall_hit == 2:
            # if we only hit a wall incrementing by row, return those coordinates
            return by_row
        elif wall_hit == 3:
            # if we hit walls both ways, return the one that is the smallest distance away
            # (performance enhancement: distance formula normally uses square-root, but we don't 
            # need to do that in order to compare which is smaller)
            dist_by_col = (from_x - by_col[0])**2 + (from_y - by_col[1])**2
            dist_by_row = (from_x - by_row[0])**2 + (from_y - by_row[1])**2

            if dist_by_col < dist_by_row: 
                return by_col
            else:
                return by_row
        else:
            # wow this is a weird wall_hit value ...
            return (0,0)



