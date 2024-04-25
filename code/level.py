from settings import *
from sprites import Sprite, AnimatedSprite, MovingSprite, Spike
from player import Player
from groups import AllSprite

from random import uniform

class Level:
    def __init__(self, tmx_map, level_frames):
        self.display_surface = pygame.display.get_surface()

        #Groups
        self.all_sprites = AllSprite()
        self.collision_sprites = pygame.sprite.Group()
        self.semi_collision_sprites = pygame.sprite.Group()
        self.damage_sprites =  pygame.sprite.Group()


        self.setup(tmx_map, level_frames)

    def setup(self, tmx_map, level_frames):
        # tile
        for layer in ['BG', 'Terrain', 'FG', 'Platforms']:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                groups = [self.all_sprites]   
                if layer == 'Terrain' : groups.append(self.collision_sprites)
                if layer == 'Platforms' : groups.append(self.semi_collision_sprites)
                '''chuyển đổi từ grid position sang pixel position'''
                match layer:
                    case 'BG' : z = Z_LAYERS['bg tiles']
                    case 'FG' : z =  Z_LAYERS['bg tiles']
                    case _:  z =  Z_LAYERS['main']


                Sprite((x * TILE_SIZE,y * TILE_SIZE), surf, groups, z)

        
        #bg detail:
        for obj in tmx_map.get_layer_by_name('BG details'):
            if obj.name == 'static':
                Sprite((obj.x, obj.y), obj.image,self.all_sprites, z = Z_LAYERS['bg tiles'])
            else:
                AnimatedSprite((obj.x, obj.y), level_frames[obj.name], self.all_sprites, Z_LAYERS['bg tiles'])
                if obj.name == 'candle':
                    AnimatedSprite((obj.x, obj.y) + vector(-20, -20), level_frames['candle_light'], self.all_sprites, z = Z_LAYERS['bg tiles'])
        
        
        #object                    
        for obj in tmx_map.get_layer_by_name('Objects'):
            if obj.name =='player':
                self.player = Player(
                    pos = (obj.x,obj.y),
                    groups = self.all_sprites, 
                    collision_sprites = self.collision_sprites, 
                    semi_collision_sprites = self.semi_collision_sprites,
                    frames = level_frames['player'])
            else:
                if obj.name in ('barrel', 'crate'):
                    Sprite((obj.x, obj.y), obj.image ,(self.all_sprites, self.collision_sprites))
                else:
                    
                    frames = level_frames[obj.name] if not 'palm' in obj.name else level_frames['palms'][obj.name]
                    if obj.name == 'floor_spike' and obj.properties['inverted']:
                      frames = [pygame.transform.flip(frame, False, True) for frame in frames]
                    
                    groups = [self.all_sprites]
                    if obj.name in('palm_small', 'palm_large'): groups.append(self.semi_collision_sprites)
                    if obj.name in('saw', 'floor_spike'): groups.append(self.damage_sprites)

                    z = Z_LAYERS['main'] if not 'bg' in obj.name else Z_LAYERS['bg details']

                    animation_speed = ANIMATION_SPEED if not 'palm' in obj.name else ANIMATION_SPEED + uniform(-1, 1)
                    AnimatedSprite((obj.x, obj.y), frames, groups, z, animation_speed)

        #Moving Objects
        for obj in tmx_map.get_layer_by_name('Moving Objects'):
            if obj.name == 'spike':
                Spike(
                    pos = (obj.x + obj.width / 2, obj.y + obj.height / 2),
                    surf = level_frames['spike'],
                    radius = obj.properties['radius'],
                    speed = obj.properties['speed'],
                    start_angle = obj.properties['start_angle'],
                    end_angle = obj.properties['end_angle'],
                    groups = (self.all_sprites, self.damage_sprites)),
                for radius in range(0, obj.properties['radius'],20):
                    Spike(
                        pos = (obj.x + obj.width / 2, obj.y + obj.height / 2),
                        surf = level_frames['spike_chain'],
                        radius = radius,
                        speed = obj.properties['speed'],
                        start_angle = obj.properties['start_angle'],
                        end_angle = obj.properties['end_angle'],
                        groups = self.all_sprites,
                        z = Z_LAYERS['bg details'] )
            else: 
                frames = level_frames[obj.name]
                groups = (self.all_sprites, self.semi_collision_sprites ) if obj.properties['platform'] else (self.all_sprites, self.damage_sprites)
                '''xác định hướng di chuyển dựa trên chiều rộng và chiều cao của đối tượng'''
                if obj.width > obj.height:  #horizontal
                    move_dir = 'x'
                    start_pos = (obj.x, obj.y + obj.height / 2)
                    end_pos = (obj.x + obj.width, obj.y + obj.height / 2)
                else: #vertical
                    move_dir = 'y'     
                    start_pos = (obj.x + obj.width /2, obj.y)
                    end_pos = (obj.x + obj.width /2, obj.y + obj.height)     
                speed = obj.properties['speed']
                MovingSprite(frames, groups, start_pos, end_pos, move_dir, speed, obj.properties['flip'])  

                if obj.name == 'saw':
                    if move_dir == 'x':
                        y = start_pos[1] - level_frames['saw_chain'].get_height() / 2
                        left, right = int(start_pos[0]), int(end_pos[0])
                        for x in range(left, right, 20):
                            Sprite((x,y), level_frames['saw_chain'], self.all_sprites, Z_LAYERS['bg details'])
                    else:
                       x = start_pos[0] - level_frames['saw_chain'].get_width() / 2
                       top, bottom = int(start_pos[1]), int(end_pos[1])
                       for y in range(top, bottom, 20):
                           Sprite((x,y), level_frames['saw_chain'], self.all_sprites, Z_LAYERS['bg details']) 


    def run(self, dt):
        self.display_surface.fill('black')
        self.all_sprites.update(dt)
        self.all_sprites.draw(self.player.hitbox_rect.center)
