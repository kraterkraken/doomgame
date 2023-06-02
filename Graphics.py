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
        texture_xoffset = int(percent * TEXTURE_SIZE)
        texture_yoffset = 0
        vert_pixels = TEXTURE_SIZE
        scale_height = height

        if (texture_xoffset + WALL_CHUNK_WIDTH > TEXTURE_SIZE):
            width = TEXTURE_SIZE - texture_xoffset

        # --------- BEGIN performance enhancement for being close to wall
        if height > SCREEN_HEIGHT:
            vert_percent = SCREEN_HEIGHT / height
            vert_pixels = int(vert_percent * TEXTURE_SIZE)
            texture_yoffset = TEXTURE_SIZE * (1 - vert_percent) / 2
            y = 0
            scale_height = SCREEN_HEIGHT
        # --------- END performance enhancement for being close to wall

        chunk = self.textures[texture_name]
        chunk.set_alpha(alpha_level)
        chunk = chunk.subsurface(texture_xoffset, texture_yoffset, width, vert_pixels)
        chunk = pygame.transform.scale(chunk, (width, scale_height))
        self.game.screen.blit(chunk, (x, y))        


