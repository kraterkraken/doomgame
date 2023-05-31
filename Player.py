import math
import pygame

from Settings import *
from Game import *
from Utility import *

class Player:
    def __init__(self, game):
        self.game = game
        self.x = PLAYER_START_X
        self.y = PLAYER_START_Y
        self.heading = 5 * math.pi / 180 # angle in CLOCKWISE radians that player is facing

    def move(self, delta_x, delta_y):
        # Moves the player in the x,y distances given (unless it makes us collide with a wall)
        self.x += delta_x
        self.y += delta_y

        if (self.wall_collision()):
            # undo the previous movement if it puts us inside a wall
            self.x -= delta_x
            self.y -= delta_y

    def rotate(self, angle):
        self.heading = self.heading + angle
        wrap_angle(self.heading)

    def wall_collision(self):
        mypos = xy_to_cr(self.x, self.y)
        return self.game.map.squares[mypos].is_wall

    def draw(self):
        if TOPDOWN:
            pygame.draw.circle(self.game.screen, "white", (self.x, self.y), 7, 0)
            line_end_x, line_end_y, depth, c, r = self.game.raycaster.find_wall(self.x, self.y, self.heading)
            pygame.draw.circle(self.game.screen, "green", (line_end_x, line_end_y), 7, 0)
