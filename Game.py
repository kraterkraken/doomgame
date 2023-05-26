import pygame
import sys

from Settings import *
from Map import *
from Player import *
from RayCaster import *

class Game:
    def __init__(self):
        # pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.delta_t = 1
        self.keys_pressed = {}
        pygame.key.set_repeat(1, 30)

        self.running = True
        self.map = Map(self)
        self.player = Player(self)
        self.raycaster = RayCaster(self)

    def check_events(self):

        self.keys_pressed = pygame.key.get_pressed()

        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False # pygame.QUIT event means the user clicked X to close your window

            elif event.type == pygame.MOUSEMOTION:
                delta_x = event.rel[0]
                self.player.rotate(delta_x)

    def update(self):
        self.delta_t = self.clock.tick(FRAME_RATE)  # limits FPS

        distance = PLAYER_VELOCITY * self.delta_t
        a = distance * math.cos(self.player.heading)
        b = distance * math.sin(self.player.heading)
        rot_angle = PLAYER_ANGULAR_VELOCITY * self.delta_t

        if self.keys_pressed[MOVE_LEFT]:
            self.player.move(b, -a)
        if self.keys_pressed[MOVE_RIGHT]:
            self.player.move(-b, a)
        if self.keys_pressed[MOVE_AHEAD]:
            self.player.move(a, b)
        if self.keys_pressed[MOVE_BACK]:
            self.player.move(-a, -b)
        if self.keys_pressed[ROTATE_C]:
            self.player.rotate(rot_angle)
        if self.keys_pressed[ROTATE_CC]:
            self.player.rotate(-rot_angle)



    def render(self):
        self.screen.fill("black")
        self.map.draw() # only does something in TOPDOWN mode
        self.player.draw() # only does something in TOPDOWN mode
        self.raycaster.ray_cast(self.player.x, self.player.y, self.player.heading)

        # flip() the display to put your work on screen
        pygame.display.flip()

    def run(self):
        while self.running:
            self.check_events()
            self.update()
            self.render()
        

        pygame.quit()




