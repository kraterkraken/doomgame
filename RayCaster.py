import pygame
import math
from Utility import *
from Settings import *

from Game import *

class RayCaster:                                               

    class WallChunk:
        def __init__(self, x, y, height, width, depth):
            self.x = x
            self.y = y
            self.height = height
            self.width = width
            self.depth = depth

    def __init__(self, game):
        self.game = game

    def find_wall2(self, x, y, angle):

        s = TILE_SIZE
        tanangle = math.tan(angle)
        cotangle = 1 / tanangle
        x_div_s = x / s # real col coord, i.e. 4.35 is 35% of the way across col #4
        y_div_s = y / s # real row coord, i.e. 3.22 is 22% of the way across row #3
        pix = 1 / s  # the pct of a col or row that equals 1 pixel

        # what tile are we in?
        c, r = xy_to_cr(x, y)

        # what direction are we going?
        c_incr, r_incr = get_cr_dir(angle)

        # get starting coords
        c1 = c + c_incr if c_incr > 0 else c - pix
        r1 = y_div_s + (c1 - x_div_s) * tanangle

        r2 = r + r_incr if r_incr > 0 else r - pix
        c2 = x_div_s + (r2 - y_div_s) / tanangle # TODO: DIV BY ZERO CHECK!!

        # get deltas
        dc = abs(cotangle) * c_incr
        dr = abs(tanangle) * r_incr

        # find wall by column
        while self.is_in_bounds_cr(c1, r1):
            # did we hit a wall
            if self.game.map.squares[(int(c1), int(r1))].is_wall:
                break;
            else:
                c1 += c_incr
                r1 += dr

        # find wall by row
        while self.is_in_bounds_cr(c2, r2):
            # did we hit a wall
            if self.game.map.squares[(int(c2), int(r2))].is_wall:
                break;
            else:
                c2 += dc
                r2 += r_incr

        # pick the wall coords that are the smallest distance away
        dist1 = depth(x_div_s, y_div_s, c1, r1)
        dist2 = depth(x_div_s, y_div_s, c2, r2)
        answer = (c1, r1)
        dist = dist1
        if dist2 < dist1:
            answer = (c2, r2)
            dist = dist2

        # return the x,y and c,r coords where we hit wall, and the depth to wall
        return (answer[0]*s, answer[1]*s, int(answer[0]), int(answer[1]), dist*s)  


    def ray_cast(self, x, y, heading):

        angle = heading - HALF_FOV - RAY_ANGLE
        ray_count = -1

        while ray_count < NUM_RAYS:

            angle += RAY_ANGLE
            ray_count += 1

            endx, endy, c, r, depth = self.find_wall2(x, y, angle)

            # the closer away the wall, the brighter it will appear
            brightness = 255 - int(255 * depth/SCREEN_WIDTH)

            # un-fisheye the depth
            depth = depth * math.cos(angle - heading)

            # find the height of the projected the wall chunk on the viewscreen
            wall_height = int(WALL_HEIGHT * VIEWER_DEPTH / depth)

            # here are the coordinates of the wall chunk
            screen_x = int(ray_count * WALL_CHUNK_WIDTH)
            screen_y = int((SCREEN_HEIGHT - wall_height)/2)


            # ----------------- Debugging Modes ------------ -------------------------
            if TOPDOWN:
                pygame.draw.line(self.game.screen, "yellow", (x, y), (endx, endy), 2)
                continue
            if PLAINWALL: # or not (c == 6 and r == 0):
                # Draw a very narrow vertical rectangle to represent the portion
                # of the wall ("wall chunk") that the current ray hit.  The 
                # farther away it is the shorter the wall chunk will be, which  
                # will give the illusion of the entire wall receding if it is at  
                # an angle to the player.  Assumption: player is ALWAYS looking  
                # at the vertical center of any portion of any wall.

                pygame.draw.rect(
                    self.game.screen, 
                    pygame.Color(brightness, brightness, brightness), 
                    (screen_x, screen_y, WALL_CHUNK_WIDTH, wall_height),2)
                continue
            # ----------------- End: Debugging Modes ---------------------------------


            # We need to find how far (offset) across the edge of the 
            # tile that the ray hit.  There are 4 cases: (1) ray hit the left
            # of the tile, (2) ray hit the bottom of the tile, (3) ray hit
            # the right of the tile, and (4) ray hit the top of the tile.
            # Rays always scan from left to right from the perspective of the 
            # player, so for the 4 cases the rays scan (1) down, (2) right,
            # (3) up, and (4) left.  

            # Starting in the upper left of the tile and going counter-clockwise,
            # I'm going to label the corners A, B, C, D:

            w = TILE_SIZE
            Ax, Ay = (w*c, w*r)
            Bx, By = (Ax, Ay+w-1)
            Cx, Cy = (Ax+w-1, By)
            Dx, Dy = (Cx, Ay)

            offset = 0
            if (int(endx) == Ax):
                # CASE 1 - left side of 2D tile
                offset = endy - Ay
            elif (int(endy) == By):
                # CASE 2 - bottom side of 2D tile
                offset = endx - Bx
            elif (int(endx) == Cx):
                # CASE 3 - right side of 2D tile
                offset = Cy - endy
            elif (int(endy) == Dy):
                # CASE 4 - top side of 2D tile
                offset = Dx - endx
            else:
                print("HUUUGE ERROR: Could not determine whihc side of tile a ray hit!!")
                pass

            texture_id = "B" #self.game.map.squares[c,r].texture_id
            self.game.graphics.draw_wall_chunk(
                texture_id, 
                (screen_x, screen_y, WALL_CHUNK_WIDTH, wall_height), 
                offset,
                brightness)
 
    def is_in_bounds_cr(self, c, r):
        return (int(c), int(r)) in self.game.map.squares

    def is_in_bounds(self, pos):
        if (pos[0] > SCREEN_WIDTH
        or pos[0] < 0
        or pos[1] > SCREEN_HEIGHT
        or pos[1] < 0):
            return False
        else:
            return True

    def find_wall(self, from_x, from_y, angle):
        # This function finds the nearest wall hit by a ray
        # cast from (from_x,from_y) and returns the following:
        #
        #   x :     horiz map coordinate where the ray hit the wall
        #   y :     vert map coordinate where the way hit the wall
        #   depth:  distance from (from_x,fomr_y) to the wall
        #   col :   the map column where the ray hit the wall
        #   row :   the map row where the ray hit the wall

        # this was insanely hard to come up with

        w = TILE_SIZE

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
        from_c, from_r = xy_to_cr(from_x, from_y)
        x_0 = w * (from_c + int(signcos + 0.5))
        y_0 = w * (from_r + int(signsin + 0.5))

        # by_col is the coordinates where the ray intersects a column edge
        # by_row is the coordinates where the ray intersects a row edge
        # (again, we are starting at the edges closest to the "from" in the ray's direction)
        temp = from_y + (x_0 - from_x) * tanangle
        by_col = [x_0, temp]
        temp = 1 if cosangle == 0 else from_x + (y_0 - from_y) / tanangle # this prevents division by zero
        by_row = [temp, y_0]

        c, r = 0, 0
        while go_col and self.is_in_bounds(by_col):
            # did we hit a wall "by column"?
            is_in_wall, c, r = self.game.map.is_in_wall(by_col[0] + signcos, by_col[1])
            if is_in_wall:
                break;
            else:
                by_col[0] += wx
                by_col[1] += dy
                
        while go_row and self.is_in_bounds(by_row):
            # did we hit a wall "by row"?
            is_in_wall, c, r = self.game.map.is_in_wall(by_row[0], by_row[1] + signsin)
            if is_in_wall:
                break;
            else:
                by_row[0] += dx
                by_row[1] += wy

        dist_by_col = depth(from_x, from_y, by_col[0], by_col[1])
        dist_by_row = depth(from_x, from_y, by_row[0], by_row[1])

        wallpos = by_row
        dist = dist_by_row
        if dist_by_col < dist_by_row:
            wallpos = by_col
            dist = dist_by_col

        c, r = xy_to_cr(wallpos[0], wallpos[1])

        return wallpos[0], wallpos[1], c, r, dist


