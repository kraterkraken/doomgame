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

    def find_wall(self, x, y, angle):

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

            endx, endy, c, r, depth = self.find_wall(x, y, angle)

            # the closer the wall, the brighter it will appear
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
                print("HUUUGE ERROR: Could not determine which side of tile a ray hit!!")
                pass

            texture_id = self.game.map.squares[c,r].texture_id
            self.game.graphics.draw_wall_chunk(
                texture_id, 
                (screen_x, screen_y, WALL_CHUNK_WIDTH, wall_height), 
                offset,
                brightness)
 
    def is_in_bounds_cr(self, c, r):
        return (int(c), int(r)) in self.game.map.squares


