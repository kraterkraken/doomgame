import pygame
import sys

from Settings import *
from Map import *
from Player import *

TOPDOWN = True

class Game:
    def __init__(self):
        # pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.delta_t = 1
        pygame.key.set_repeat(1, 30)

        self.running = True
        self.map = Map(self)
        self.player = Player(self)

    def check_events(self):
        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False # pygame.QUIT event means the user clicked X to close your window

            elif event.type == pygame.MOUSEMOTION:
                delta_x = event.rel[0]
                self.player.rotate(delta_x)

    def update(self):
        self.delta_t = self.clock.tick(FRAME_RATE)  # limits FPS
        self.player.update()

    def render(self):
        self.screen.fill("black")

        if TOPDOWN:
            # topdown view is primarily for debugging and testing
            self.map.draw_topdown()
            self.player.draw_topdown()

        else:
            # this draws the game the way a player will see it
            pass



        # flip() the display to put your work on screen
        pygame.display.flip()

    def run(self):
        while self.running:
            self.check_events()
            self.update()
            self.render()
        

        pygame.quit()




