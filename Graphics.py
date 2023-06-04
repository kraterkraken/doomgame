import pygame
from Settings import *


class Graphics:
    def __init__(self, game):
        self.game = game
        self.textures = {}
        self.sprites = {}
        self.texture_ids = {}
        self.sky = self.load_texture("", "", "resources/textures/sunset.png", (SCREEN_WIDTH, SCREEN_MID_Y))

        self.load_texture("brickwall", "B", "resources/textures/walltile2.jpg")
        self.load_texture("grate", "G", "resources/textures/rustygrate.jpg")
        self.load_texture("paintedbrick", "P", "resources/textures/wall_1.jpg")
        self.load_texture("screampainting", "S", "resources/textures/scream.jpg")

        self.load_texture("test", "$", "resources/textures/test.png")

    def load_texture(self, name, tid, path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pygame.image.load(path)
        texture = texture.convert_alpha()
        texture = pygame.transform.scale(texture, res)
        if (name != "" and tid != ""):
            self.textures[name] = texture
            self.texture_ids[tid] = name
        return texture

    def draw_sky(self, player_heading):
        # The heading tells which part of the sky we are looking at.

        # how far in radians have we changed direction since the start?
        angle_delta = player_heading - PLAYER_START_HEADING

        # how far in pixels have we changed direction since the start?
        pix_delta = SKY_PIX_PER_RADIAN * angle_delta

        # wrap the pixels delta so that we never have areas of blank sky
        pix_delta_wrapped = pix_delta % SCREEN_WIDTH

        # draw two skys ... one starting far to the left and ending where
        # we are looking, and one starting where we are looking and ending
        # far to the right (gives illusion of continuous sky)
        self.game.screen.blit(self.sky, (-pix_delta_wrapped, 0))
        self.game.screen.blit(self.sky, (SCREEN_WIDTH-pix_delta_wrapped, 0))

    def draw_floor(self):
        pygame.draw.rect(self.game.screen, FLOOR_COLOR, 
            (0,          # screen x coordinate
            SCREEN_MID_Y,   # screen y coordinate
            SCREEN_WIDTH,   # width of rect
            SCREEN_MID_Y    # height of rect
            ), 0)

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

        # make a black rectangle underneath the wall texture to help with depth shading
        pygame.draw.rect(self.game.screen, "black", 
            (x, y, width, scale_height), 0)

        self.game.screen.blit(chunk, (x, y))        


