from settings import *
from sprites import Sprite
from player import Player


class Level:
    def __init__(self, tmx_map):
        self.display_surface = pygame.display.get_surface()

        #Groups
        self.all_sprites = pygame.sprite.Group()

        self.setup(tmx_map)

    def setup(self, tmx_map):
        for x, y, surf in tmx_map.get_layer_by_name('Terrain').tiles():
            '''chuyển đổi từ grid position sang pixel position'''
            Sprite((x * TILE_SIZE,y * TILE_SIZE), surf, self.all_sprites)

        for obj in tmx_map.get_layer_by_name('Objects'):
            if obj.name =='player':
                Player((obj.x,obj.y), self.all_sprites)
                print(x)
                print(y)



    def run(self):
        self.display_surface.fill('black')
        self.all_sprites.draw(self.display_surface)