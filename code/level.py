from settings import *
from sprites import Sprite, AnimatedSprite, MovingSprite, Spike, Item, ParticleEffectSprite
from player import Player
from groups import AllSprite
from enemies import Tooth, Shell, Pearl

from random import uniform

class Level:
    def __init__(self, tmx_map, level_frames, audio_files, data, switch_stage):
        """
        Khởi tạo một level mới.
            tmx_map (tmx): Bản đồ TMX của level.
            level_frames (dict): Frames của level.
            audio_files (dict): Tệp âm thanh của level.
            data (Data): Dữ liệu trò chơi.
            switch_stage (function): Hàm chuyển level.
        """
        self.display_surface = pygame.display.get_surface()
        self.data = data
        self.switch_stage = switch_stage

        self.level_width = tmx_map.width * TILE_SIZE
        self.level_bottom = tmx_map.height * TILE_SIZE
        tmx_level_properties = tmx_map.get_layer_by_name('Data')[0].properties

        self.level_unlock = tmx_level_properties['level_unlock']
        if tmx_level_properties['bg']:
            bg_tile = level_frames['bg_tiles'][tmx_level_properties['bg']]
        else:
            bg_tile = None

        #Groups
        self.all_sprites = AllSprite(
            width = tmx_map.width, 
            height = tmx_map.height,
            bg_tile=bg_tile,
            top_limit = tmx_level_properties['top_limit'],
            clouds = {'large': level_frames['cloud_large'], 'small' : level_frames['cloud_small']},
            horizon_line = tmx_level_properties['horizon_line']     )
        self.collision_sprites = pygame.sprite.Group()
        self.semi_collision_sprites = pygame.sprite.Group()
        self.damage_sprites =  pygame.sprite.Group()
        self.tooth_sprites = pygame.sprite.Group()
        self.pearl_sprites = pygame.sprite.Group()
        self.item_sprites = pygame.sprite.Group()



        self.setup(tmx_map, level_frames, audio_files)

        #frames
        self.pearl_surf = level_frames['pearl']
        self.particle_frames = level_frames['particle']

        #audio
        self.coin_sound = audio_files['coin']
        self.coin_sound.set_volume(0.1)
        self.damage_sound = audio_files['damage']
        self.damage_sound.set_volume(0.8)
        self.pearl_sound = audio_files['pearl']

        

    def setup(self, tmx_map, level_frames, audio_files):
        """
        Thiết lập các yếu tố trong level.
            tmx_map (tmx): Bản đồ TMX của level.
            level_frames (dict): Frame của level.
            audio_files (dict): Tệp âm thanh của level.
        """
        #tile
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
                    frames = level_frames['player'],
                    data = self.data,
                    attack_sound = audio_files['attack'],
                    jump_sound = audio_files['jump'],)
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

                if obj.name == 'flag':
                    self.level_finish_rect =pygame. FRect((obj.x,obj.y),(obj.width, obj.height))

        #moving Objects
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

        #enemies
        for obj in tmx_map.get_layer_by_name('Enemies'):
            if obj.name == 'tooth':
                Tooth((obj.x, obj.y), level_frames['tooth'], (self.all_sprites, self.damage_sprites, self.tooth_sprites), self.collision_sprites)
            if obj.name == 'shell':
                Shell(
                    pos=(obj.x, obj.y), 
                    frames=level_frames['shell'], 
                    groups=(self.all_sprites, self.collision_sprites), 
                    reverse=obj.properties['reverse'], 
                    player=self.player, 
                    create_pearl =self.create_pearl)

        #items
        for obj in tmx_map.get_layer_by_name('Items'):
            Item(obj.name, (obj.x + TILE_SIZE/2, obj.y + TILE_SIZE/2), level_frames['items'][obj.name], (self.all_sprites,self.item_sprites), self.data )

        #water
        for obj in tmx_map.get_layer_by_name('Water'):
            rows = int(obj.height/ TILE_SIZE)
            cols = int(obj.width / TILE_SIZE)
            for row in range(rows):
                for col in range(cols):
                    x = obj.x + col * TILE_SIZE
                    y = obj.y + row * TILE_SIZE
                    if row == 0:
                        AnimatedSprite((x,y), level_frames['water_top'],self.all_sprites, Z_LAYERS['water'])
                    else:
                        Sprite((x,y),  level_frames['water_body'],self.all_sprites, Z_LAYERS['water'])


    def create_pearl(self, pos, direction):
        """
        Tạo pearl.
            pos (tuple): Vị trí của pearl.
            direction (int): Hướng của pearl.
        """
        Pearl(pos, (self.all_sprites, self.damage_sprites, self.pearl_sprites), self.pearl_surf , direction, 150)
        self.pearl_sound.play()

    def pearl_collision(self):
        """Xử lý va chạm giữa pearl và các sprite khác."""
        for sprite in self.collision_sprites:
            sprite = pygame.sprite.spritecollide(sprite, self.pearl_sprites, True)
            if sprite:
                ParticleEffectSprite((sprite[0].rect.center),self.particle_frames, self.all_sprites)


    def hit_collision(self):
        """Xử lý va chạm với các sprite gây sát thương."""
        for sprite in self.damage_sprites:
            if sprite.rect.colliderect(self.player.hitbox_rect):
                self.player.get_damage()
                self.damage_sound.play()
                if hasattr(sprite, 'pearl'):
                    sprite.kill()
                    ParticleEffectSprite((sprite.rect.center),self.particle_frames, self.all_sprites)


    def item_collision(self):
        """Xử lý va chạm với các vật phẩm."""
        if self.item_sprites:
            item_sprites = pygame.sprite.spritecollide(self.player, self.item_sprites, True) 
            if item_sprites:
                item_sprites[0].activate()
                ParticleEffectSprite((item_sprites[0].rect.center),self.particle_frames, self.all_sprites)
                self.coin_sound.play()
    
    def attack_collision(self):
        """Xử lý va chạm với các sprite khi tấn công."""
        for target in self.pearl_sprites.sprites() + self.tooth_sprites.sprites():
            facing_target = self.player.rect.centerx < target.rect.centerx and self.player.facing_right or\
                            self.player.rect.centerx > target.rect.centerx and not self.player.facing_right
            if target.rect.colliderect(self.player.rect) and self.player.attacking and facing_target:
                target.reverse()

    def check_constraint(self):
        """Kiểm tra ràng buộc vị trí của người chơi."""
        #left/right
        if self.player.hitbox_rect.left <=0:
            self.player.hitbox_rect.left = 0
        if self.player.hitbox_rect.right >=  self.level_width:
            self.player.hitbox_rect.right =  self.level_width

        #bottom
        if self.player.hitbox_rect.bottom > self.level_bottom:
            self.switch_stage('overworld', -1)
        
        #success
        if self.player.hitbox_rect.colliderect(self.level_finish_rect):
            self.switch_stage('overworld', self.level_unlock)

    def run(self, dt):
        """
        Thực hiện vòng lặp chính của level.
            dt (float): Thời gian chênh lệch giữa các khung hình.
        """
        self.display_surface.fill('black')
        self.all_sprites.update(dt)
        self.pearl_collision()
        self.hit_collision()
        self.item_collision()
        self.attack_collision()
        self.check_constraint()
        self.all_sprites.draw(self.player.hitbox_rect.center, dt)
