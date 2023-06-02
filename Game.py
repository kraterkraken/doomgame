import pygame
import sys

from Settings import *
from Map import *
from Player import *
from RayCaster import *
from Graphics import *

class Game:
    def __init__(self):
        # pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.mouse.set_visible(False)

        # initialize the class
        self.delta_t = 1
        self.keys_pressed = {}
        self.mouse_rel_x = 0
        self.running = True
        self.map = Map(self)
        self.player = Player(self)
        self.raycaster = RayCaster(self)
        self.graphics = Graphics(self)

    def check_events(self):

        self.keys_pressed = pygame.key.get_pressed()

        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False # pygame.QUIT event means the user clicked X to close your window

            elif event.type == pygame.MOUSEMOTION:
                mouse_x = event.pos[0]
                self.mouse_rel_x  = event.rel[0]

                # keep the mouse from going off the window (center it when it goes out of bounds)
                if mouse_x < MOUSE_MIN_X or mouse_x > MOUSE_MAX_X:
                    pygame.mouse.set_pos([SCREEN_WIDTH//2, SCREEN_HEIGHT//2])

    def update(self):
        self.delta_t = self.clock.tick(FRAME_RATE)  # limits FPS

        # cap the rel(ative) mouse movement at MOUSE_MAX_REL
        self.mouse_rel_x = min(self.mouse_rel_x, MOUSE_MAX_REL)
        self.mouse_rel_x = max(self.mouse_rel_x, -MOUSE_MAX_REL)

        # prevent the strange drifting I saw when holding the mouse still
        if abs(self.mouse_rel_x) <= 3:
            self.mouse_rel_x = 0

        # rotate the player based on the rel(ative) mouse movement
        delta_x = self.mouse_rel_x * MOUSE_SENSITIVITY * self.delta_t
        self.player.rotate(delta_x)

        # for the motion keys, figure out how for and in what direction to move the player
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

        # draw the aiming reticle
        pygame.draw.circle(self.screen, "red", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), 6, 2)

        # flip() the display to put your work on screen
        pygame.display.flip()

    def run(self):
        while self.running:
            self.check_events()
            self.update()
            self.render()
        

        pygame.quit()




