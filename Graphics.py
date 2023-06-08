import pygame
from Settings import *
from Sprite import *


class Graphics:
    class Drawable:
        def __init__(self, screen_x, screen_y, depth, surface, type):
            self.screen_x = screen_x
            self.screen_y = screen_y
            self.depth = depth
            self.surface = surface
            self.type = type

    def __init__(self, game):
        self.game = game
        self.draw_list = []
        self.textures = {}
        self.sprites = []
        self.texture_ids = {}
        self.sky = self.load_image("resources/textures/sunset.png", (SCREEN_WIDTH, SCREEN_MID_Y))

        self.store_texture("brickwall",      "B", self.load_image("resources/textures/walltile2.jpg"))
        self.store_texture("grate",          "G", self.load_image("resources/textures/rustygrate.jpg"))
        self.store_texture("paintedbrick",   "P", self.load_image("resources/textures/wall_1.jpg"))
        self.store_texture("screampainting", "S", self.load_image("resources/textures/scream.jpg"))

        self.load_sprite("purplecolumn", "resources/sprites/HUPPB0.png", 1200, 350, 90)

    def prepare_sprite_rendering(self, x, y, heading):
        for sprite in self.sprites:
            screen_x, screen_y, height, width, depth, draw = sprite.get_projection(x, y, heading)
            if not draw: return

            scaled_image = pygame.transform.scale(sprite.image, (width, height))
            self.draw_list.append(self.Drawable(screen_x, screen_y, depth, scaled_image, "sprite"))

    def reset_draw_list(self):
        self.draw_list = []

    def draw(self):
        # draw all of the Drawables we've collected in the draw_list,
        # starting with the ones farthest away
        self.draw_list.sort(key=lambda x : x.depth, reverse=True)
        for obj in self.draw_list:
            self.game.screen.blit(obj.surface, (obj.screen_x, obj.screen_y))        
 
    def load_sprite(self, name, path, x, y, height):
        self.sprites.append(Sprite(path, x, y, height))

    def store_texture(self, name, tid, texture):
        if (name != "" and tid != ""):
            self.textures[name] = texture
            self.texture_ids[tid] = name

    def load_image(self, path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pygame.image.load(path)
        texture = texture.convert_alpha()
        texture = pygame.transform.scale(texture, res)
        return texture

    def draw_sprite(self, name):
        pass

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

    def store_wall_chunk(self, texture_name, rect, tile_offset, alpha_level, depth):

        if len(texture_name) == 1:
            texture_name = self.texture_ids[texture_name]

        x, y, width, height = rect

        # first figure out the dimensions of the subportion of full wall texture
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

        # temp below is a correctly-sized surface containing a portion of the texture
        temp = self.textures[texture_name]
        temp.set_alpha(alpha_level)
        temp = temp.subsurface(texture_xoffset, texture_yoffset, width, vert_pixels)
        temp = pygame.transform.scale(temp, (width, scale_height))

        # Now we make a new surface for the wallchunk.  Using the Surface constructor
        # here gives a black background onto which we blit the temp texture, and that
        # enables the depth shading that I want.
        chunk = pygame.Surface((width, scale_height))
        chunk.blit(temp, (0, 0))

        # store the wall chunk for drawing later on
        self.draw_list.append(self.Drawable(x, y, depth, chunk, "wallchunk"))


