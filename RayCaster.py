import pygame
import math
from Utility import *
from Settings import *

from Game import *

class RayCaster:

    def __init__(self, game):
        self.game = game


    def ray_cast(self, x, y, heading):

        angle = heading - HALF_FOV
        ray_count = 0
        while ray_count < NUM_RAYS:
            endx, endy, depth = self.find_wall(x, y, angle)
            if TOPDOWN:
                pygame.draw.line(self.game.screen, "yellow", (x, y), (endx, endy), 2)
            else:
                # Draw a very narrow vertical rectangle to represent the portion
                # of the wall that the current ray hit.  The farther away it is
                # the shorter the portion will be, which will give the illusion 
                # of the entire wall receding if it is at an angle to the player.
                # Assumption: player is ALWAYS looking at the vertical center of
                # any portion of any wall.

                # project the wall onto the viewscreen
                wall_height = WALL_HEIGHT * VIEWER_DEPTH / depth

                # the farther away the wall, the dimmer the color
                color = 255 - int(255 * depth/SCREEN_WIDTH)

                pygame.draw.rect(
                    self.game.screen, 
                    pygame.Color(color, color, color), 
                    (int(ray_count * WALL_CHUNK_WIDTH),     # screen x coordinate
                    int((SCREEN_HEIGHT - wall_height)/2),   # screen y coordinate
                    WALL_CHUNK_WIDTH,                       # width of rect
                    int(wall_height)),                      # height of rect
                    2)

            angle += RAY_ANGLE
            ray_count += 1

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

        go_col = cosangle != 0 # if we aren't going straight up / down, we can check "by col"
        go_row = sinangle != 0 # if we aren't going straight left / right, we can check "by row"

        # figure out the increments (wx, dy) for searching "by col"
        h = w if cosangle == 0 else abs(w / cosangle)
        dy = h * sinangle
        wx = w * sign(cosangle) # the correct sign for moving width units in x direction

        # figure out the increments (dx, wy) for searching "by row"
        h = w if sinangle == 0 else abs(w / sinangle)
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

        # by_col is the coordinates where the ray intersects a column edge
        # by_row is the coordinates where the ray intersects a row edge
        # (again, we are starting at the edges closest to the "from" in the ray's direction)
        temp = from_y + (x_0 - from_x) * tanangle
        by_col = [x_0, temp]
        temp = 1 if cosangle == 0 else from_x + (y_0 - from_y) / tanangle # this prevents division by zero
        by_row = [temp, y_0]

        wall_hit = 0
        while go_col and self.is_in_bounds(by_col):
            # did we hit a wall "by column"?
            if self.game.map.is_in_wall(by_col[0] + signcos, by_col[1]):
                wall_hit += 1
                break;
            else:
                by_col[0] += wx
                by_col[1] += dy
                
        while go_row and self.is_in_bounds(by_row):
            # did we hit a wall "by column"?
            if self.game.map.is_in_wall(by_row[0], by_row[1] + signsin):
                wall_hit += 2
                break;
            else:
                by_row[0] += dx
                by_row[1] += wy

        dist_by_col = depth(from_x, from_y, by_col[0], by_col[1])
        dist_by_row = depth(from_x, from_y, by_row[0], by_row[1])

        # check to see what wall we hit
        if wall_hit == 1:
            # if we only hit a wall incrementing by column, return those coordinates
            return by_col[0], by_col[1], dist_by_col
        elif wall_hit == 2:
            # if we only hit a wall incrementing by row, return those coordinates
            return by_row[0], by_row[1], dist_by_row
        elif wall_hit == 3:
            # if we hit walls both ways, return the one that is the smallest distance away
            if dist_by_col < dist_by_row: 
                return by_col[0], by_col[1], dist_by_col
            else:
                return by_row[0], by_row[1], dist_by_row

        else:
            # wow this is a weird wall_hit value ...
            return (0,0,0)



