import pygame
import sys

from Settings import *
from Map import *

TOPDOWN = True

class Game:
    def __init__(self):
        # pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((RES_WIDTH, RES_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.map = Map(self)


    def check_events(self):
        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # pygame.QUIT event means the user clicked X to close your window
                self.running = False

    def update(self):
        pass

    def render(self):
        self.screen.fill("black")

        if TOPDOWN:
            # topdown view is primarily for debugging and testing
            self.map.draw_topdown()

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
        
            self.clock.tick(FRAME_RATE)  # limits FPS

        pygame.quit()




