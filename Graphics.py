import pygame
from Settings import *


class Graphics:
    def __init__(self, game):
        self.game = game
        self.textures = {}
        self.sprites = {}
        self.texture_ids = {}

        self.load_texture("brickwall", "B", "resources/textures/walltile2.jpg")
        self.load_texture("grate", "G", "resources/textures/rustygrate.jpg")
        self.load_texture("paintedbrick", "P", "resources/textures/wall_1.jpg")
        self.load_texture("screampainting", "S", "resources/textures/scream.jpg")

        self.load_texture("test", "$", "resources/textures/test.png")

    def load_texture(self, name, tid, path):
        texture = pygame.image.load(path)
        texture = texture.convert_alpha()
        self.textures[name] = pygame.transform.scale(texture, (TEXTURE_SIZE, TEXTURE_SIZE))
        self.texture_ids[tid] = name

    def draw_wall_chunk(self, texture_name, rect, tile_offset, alpha_level):

        if len(texture_name) == 1:
            texture_name = self.texture_ids[texture_name]

        x, y, width, height = rect

        percent = int(tile_offset) / TILE_SIZE
        texture_offset = int(percent * TEXTURE_SIZE)

        if (texture_offset + WALL_CHUNK_WIDTH > TEXTURE_SIZE):
            width = TEXTURE_SIZE - texture_offset

        chunk = self.textures[texture_name]
        chunk.set_alpha(alpha_level)
        chunk = chunk.subsurface(texture_offset, 0, width, TEXTURE_SIZE)
        chunk = pygame.transform.scale(chunk, (width, height))
        self.game.screen.blit(chunk, (x, y))        


