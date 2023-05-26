import pygame
import math

# debugging
TOPDOWN = False # set to True to for topdown 2D view of entire map; False for standard 3D gameplay

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
WALL_CHUNK_WIDTH = 2
NUM_RAYS = SCREEN_WIDTH // WALL_CHUNK_WIDTH
RAY_ANGLE = FOV / NUM_RAYS

WALL_HEIGHT = 100
VIEWER_DEPTH = (SCREEN_WIDTH / 2) / math.tan(HALF_FOV)

