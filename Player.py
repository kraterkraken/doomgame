import math
from Settings import *
from Game import *

class Player:
    def __init__(self, game):
        self.game = game
        self.x = PLAYER_START_X
        self.y = PLAYER_START_Y
        self.heading = 5 * math.pi / 180 # angle in CLOCKWISE radians that player is facing

    def move(self, rel_angle):
        # Moves the player in the direction given by the 
        # relative angle (rel_angle). Heading remains unchanged.

        distance = PLAYER_VELOCITY * self.game.delta_t
        angle = self.heading + rel_angle
        self.x = self.x + distance * math.cos(angle)
        self.y = self.y + distance * math.sin(angle)

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