from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        self.image = pygame.Surface((48,56))
        self.rect = self.image.get_frect(topleft = pos)