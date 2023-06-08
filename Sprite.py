import pygame
import math
from Settings import *

class Sprite:
    def __init__(self, path, x, y, height):
        self.image = pygame.image.load(path).convert_alpha()
        factor = height / self.image.get_height()
        self.image = pygame.transform.scale_by(self.image, factor)
        self.x = x
        self.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.HALF_WIDTH = self.width // 2
        self.HALF_HEIGHT = self.height // 2
        self.percent_offset = 1 - (HALF_WALL_HEIGHT / self.height)

        print(self.height)

    def get_projection(self, x, y, heading):
        # Returns the apparent height and width of the sprite
        # from the vantage point of someone at the given x, y coordinates.
        # Also returns the depth (aka distance) from x,y to the sprite.
        # And also returns the screen_x and screen_y to draw the sprite.
        # I'm also going to return an indication of whether this sprite
        # should be drawn at all (for edge cases).

        if (x == self.x and y == self.y):
            # don't need to draw it if you are right on top of it
            return 0,0,0,0,0,False

        depth = math.hypot(x - self.x, y - self.y)

        if depth < self.HALF_WIDTH:
            # don't need to draw it if you are withn its radius
            return 0,0,0,0,0,False

        alpha = math.pi
        if self.x != x:
            # if we don't have to worry about division by zero (i.e., alpha isn't 90 degrees)
            alpha = math.atan((self.y - y)/(self.x - x))

        delta = alpha - heading
        pix_delta = VIEWER_DEPTH * math.tan(delta)
        screen_x = SCREEN_MID_X + pix_delta

        # un-fisheye the depth
        depth = depth * abs(math.cos(delta))

        app_height = int(self.height * VIEWER_DEPTH / depth)
        app_width = int(self.width * VIEWER_DEPTH / depth)

        if screen_x < -app_width:
            # don't need to draw it if it's off screen
            return 0,0,0,0,0,False

        screen_y = SCREEN_MID_Y - (app_height * self.percent_offset)

        return screen_x, screen_y, app_height, app_width, depth, True
