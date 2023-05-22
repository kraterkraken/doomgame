import math
import pygame

from Settings import *
from Game import *

class Player:
    def __init__(self, game):
        self.game = game
        self.x = PLAYER_START_X
        self.y = PLAYER_START_Y
        self.heading = 5 * math.pi / 180 # angle in CLOCKWISE radians that player is facing


    def update(self):
        distance = PLAYER_VELOCITY * self.game.delta_t
        a = distance * math.cos(self.heading)
        b = distance * math.sin(self.heading)

        keys = pygame.key.get_pressed()
        if keys[MOVE_LEFT]:
            self.move(b, -a)
        if keys[MOVE_RIGHT]:
            self.move(-b, a)
        if keys[MOVE_AHEAD]:
            self.move(a, b)
        if keys[MOVE_BACK]:
            self.move(-a, -b)


    def move(self, delta_x, delta_y):
        # Moves the player in the x,y distances given
        self.x += delta_x
        self.y += delta_y


    def rotate(self, mouse_delta_x):
        angle = mouse_delta_x * math.pi/180
        self.heading = self.heading + angle

    def draw_topdown(self):
        line_d = SCREEN_WIDTH
        line_end_x = max(0, self.x + line_d * math.cos(self.heading))
        line_end_y = max(0, self.y + line_d * math.sin(self.heading))
        pygame.draw.circle(self.game.screen, "white", (self.x, self.y), 7, 0)
        pygame.draw.line(self.game.screen, "green", 
            (self.x, self.y), 
            (line_end_x, line_end_y), 2)