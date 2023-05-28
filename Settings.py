import pygame
import math

# debugging
TOPDOWN = False # set to True to for topdown 2D view of entire map; False for standard 3D gameplay
PLAINWALL = True # set to true to eliminate wall textures; False for standard 3D gameplay

# basic settings
ASPECT_RATIO = (16,9)
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
FRAME_RATE = 60
PLAYER_START_X = 200
PLAYER_START_Y = 200
PLAYER_VELOCITY = 0.4
PLAYER_ANGULAR_VELOCITY = 0.003
FOV = math.pi / 3
TEXTURE_SIZE = 256

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
TILE_SIZE = SCREEN_WIDTH // ASPECT_RATIO[0]
WALL_HEIGHT = TILE_SIZE
VIEWER_DEPTH = (SCREEN_WIDTH / 2) / math.tan(HALF_FOV)

# sanity checks
if TILE_SIZE*ASPECT_RATIO[1] != SCREEN_HEIGHT:
    print("Error: Aspect ratio doesn't match screen width and height.  Quitting.")
    pygame.quit()
