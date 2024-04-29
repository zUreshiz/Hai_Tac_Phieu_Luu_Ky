from settings import *
from sprites import Sprite, AnimatedSprite
from groups import WorldSprites

class Overworld:
    def __init__(self, tmx_map , data, overworld_frames):
        self.display_surface = pygame.display.get_surface()
        self.data = data

        #groups
        self.all_sprites = WorldSprites(data)
        self.setup(tmx_map, overworld_frames)

    def setup(self, tmx_map, overworld_frames):
        #Tile
        for layer in ['main', 'top']:
            for x,y,surf in tmx_map.get_layer_by_name(layer).tiles():
                Sprite((x * TILE_SIZE,y *TILE_SIZE), surf, self.all_sprites, Z_LAYERS['bg tiles'])

        #water
        for col in range(tmx_map.width):
            for row in range(tmx_map.height):
                AnimatedSprite((col * TILE_SIZE,row *TILE_SIZE), overworld_frames['water'], self.all_sprites, Z_LAYERS['bg tiles'])


    def run(self, dt):
        self.all_sprites.update(dt)
        self.all_sprites.draw((1000,800))


