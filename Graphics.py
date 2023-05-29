import pygame
from Settings import *


class Graphics:
    def __init__(self, game):
        self.game = game
        self.textures = {}
        self.sprites = {}

        self.load_texture("brickwall", "resources/textures/walltile2.jpg")
        self.load_texture("test", "resources/textures/test.png")

    def load_texture(self, name, path):
        texture = pygame.image.load(path)
        texture = texture.convert_alpha()
        self.textures[name] = pygame.transform.scale(texture, (256, 256))

    def draw_wall_chunk(self, texture_name, rect, tile_offset, alpha_level):
        x, y, width, height = rect

        percent = tile_offset / TILE_SIZE
        texture_offset = int(percent * TEXTURE_SIZE)

        if (texture_offset + WALL_CHUNK_WIDTH > TEXTURE_SIZE):
            width = TEXTURE_SIZE - texture_offset

        chunk = self.textures[texture_name]
        chunk.set_alpha(alpha_level)
        chunk = chunk.subsurface(texture_offset, 0, width, TEXTURE_SIZE)
        chunk = pygame.transform.scale(chunk, (width, height))
        self.game.screen.blit(chunk, (x, y))        


