import pygame


class Graphics:
    def __init__(self, game):
        self.game = game
        self.textures = {}
        self.sprites = {}

        # note: scaling MUST be done here, not in the game loop!  it is really slow!
        texture = pygame.image.load("resources/textures/walltile2.jpg")
        texture = texture.convert_alpha()
        self.textures['brickwall'] = texture #pygame.transform.scale(texture,(200, 200))