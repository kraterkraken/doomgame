import pygame
from Settings import *


class Graphics:
    def __init__(self, game):
        self.game = game
        self.textures = {}
        self.sprites = {}

        # note: scaling MUST be done here, not in the game loop!  it is really slow!
        texture = pygame.image.load("resources/textures/walltile2.jpg")
        texture = texture.convert_alpha()
        self.textures['brickwall'] = pygame.transform.scale(texture, (256, 256))


    def draw_wall_chunk(self, texture_name, rect, offset, alpha_level):
        x, y, width, height = rect
        chunk = self.textures[texture_name]
        chunk.set_alpha(alpha_level)
        chunk = chunk.subsurface(offset, 0, width, TEXTURE_SIZE)
        chunk = pygame.transform.scale(chunk, (width, height))
        self.game.screen.blit(chunk, (x, y))        


    def test(self):
        h = 200
        y = 50
        for i in range(50):
            chunk = self.textures["brickwall"]
            chunk = chunk.subsurface(i*WALL_CHUNK_WIDTH, 0, WALL_CHUNK_WIDTH, TEXTURE_SIZE)
            chunk = pygame.transform.scale(chunk, (WALL_CHUNK_WIDTH, h))
            self.game.screen.blit(chunk, (i*WALL_CHUNK_WIDTH,y))
            h += 1
            y -= 2
