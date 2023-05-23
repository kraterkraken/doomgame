import pygame
import math

# basic settings
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
FRAME_RATE = 60
PLAYER_START_X = 200
PLAYER_START_Y = 200
PLAYER_VELOCITY = 0.4
PLAYER_ANGULAR_VELOCITY = 0.005
FOV = math.pi / 3

# control settings
MOVE_LEFT = pygame.K_a
MOVE_RIGHT = pygame.K_d
MOVE_AHEAD = pygame.K_w
MOVE_BACK = pygame.K_s
ROTATE_CC = pygame.K_LEFT
ROTATE_C = pygame.K_RIGHT


# constants ... don't change
HALF_FOV = FOV / 2 # performance enhancement (less divisions)
NUM_RAYS = SCREEN_WIDTH # each ray needs to hit a pixel
RAY_ANGLE = FOV / NUM_RAYS

