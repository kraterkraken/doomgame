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
        self.heading = PLAYER_START_HEADING # angle in CLOCKWISE radians that player is facing

    def move(self, delta_x, delta_y):
        # Moves the player in the x,y distances given (unless it makes us collide with a wall)

        x_unit = -1 if delta_x < 0 else 1
        y_unit = -1 if delta_y < 0 else 1

        # move the player if we didn't collide with a wall ...
        if not self.wall_collision_x(delta_x, x_unit):
            self.x += delta_x
        if not self.wall_collision_y(delta_y, y_unit):
            self.y += delta_y

    def rotate(self, angle):
        self.heading = self.heading + angle
        wrap_angle(self.heading)

    def wall_collision_x(self, delta_x, unit):
        mypos1 = xy_to_cr(self.x+delta_x+(unit*PLAYER_RADIUS), self.y)
        return self.game.map.squares[mypos1].is_wall

    def wall_collision_y(self, delta_y, unit):
        mypos1 = xy_to_cr(self.x, self.y+delta_y+(unit*PLAYER_RADIUS))
        return self.game.map.squares[mypos1].is_wall

    def draw(self):
        if TOPDOWN:
            pygame.draw.circle(self.game.screen, "white", (self.x, self.y), PLAYER_RADIUS, 0)
            line_end_x, line_end_y, depth, c, r = self.game.raycaster.find_wall(self.x, self.y, self.heading)
            pygame.draw.circle(self.game.screen, "green", (line_end_x, line_end_y), 7, 0)
