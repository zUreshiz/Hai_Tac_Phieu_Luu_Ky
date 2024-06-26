from settings import *
from sprites import Sprite, Cloud
from random import choice, randint
from timer import Timer

class AllSprite(pygame.sprite.Group):
    def __init__(self, width, height, clouds,horizon_line, bg_tile = None, top_limit = 0):
        """
        Khởi tạo tất cả các sprite trong trò chơi.
            width (int): Chiều rộng của màn hình.
            height (int): Chiều cao của màn hình.
            clouds (dict): Danh sách các hình ảnh đám mây.
            horizon_line (int): Đường chân trời.
            bg_tile (pygame.Surface, optional): Hình ảnh nền. Mặc định là None.
            top_limit (int, optional): Giới hạn trên của màn hình. Mặc định là 0.
        """
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = vector()
        self.width = width * TILE_SIZE
        self.height = height *TILE_SIZE
        self.borders = {
            'left' : 0,
            'right': -self.width + WINDOW_WIDTH,
            'top':top_limit,
            'bottom': -self.height + WINDOW_HEIGHT
        }
        self.sky = not bg_tile
        self.horizon_line = horizon_line

        if bg_tile:
            for col in range(width):
                for row in range(-int(top_limit/ TILE_SIZE)-1, height):
                    x= col * TILE_SIZE
                    y = row * TILE_SIZE
                    Sprite((x,y) , bg_tile, self, -1  )

        else:
            #sky
            self.large_cloud = clouds['large']
            self.small_clouds = clouds['small']
            self.cloud_direction = -1
            

            #large cloud
            self.large_cloud_speed = 50
            self.large_cloud_x = 0
            self.large_cloud_tiles = int(self.width / self.large_cloud.get_width()) +2  
            self.large_cloud_width, self.large_cloud_height = self.large_cloud.get_size()

            #small cloud
            self.cloud_timer= Timer(2500, self.create_cloud, True)
            self.cloud_timer.activate()
            for cloud in range(20):
                pos =(randint(0, self.width),randint(self.borders['top'], self.horizon_line))
                surf = choice(self.small_clouds)
                Cloud(pos, surf, self)


    def draw_large_cloud(self,dt):
        """
        Vẽ đám mây lớn.
            dt (float): Thời gian giữa các khung hình.
        """
        self.large_cloud_x += self.cloud_direction* self.large_cloud_speed * dt
        if self.large_cloud_x <= -self.large_cloud_width:
            self.large_cloud_x = 0
        for cloud in range(self.large_cloud_tiles):
            top = self.horizon_line - self.large_cloud_height + self.offset.y
            #cloud move
            left = self.large_cloud_x + self.large_cloud_width * cloud + self.offset.x
            self.display_surface.blit(self.large_cloud, (left,top))

    def camera_constraint(self):
        """Xác định ràng buộc của camera."""
        self.offset.x = self.offset.x if self.offset.x < self.borders['left'] else self.borders['left']
        self.offset.x = self.offset.x if self.offset.x > self.borders['right'] else self.borders['right']
        self.offset.y =  self.offset.y if self.offset.y > self.borders['bottom'] else  self.borders['bottom']
        self.offset.y =  self.offset.y if self.offset.y < self.borders['top'] else  self.borders['top']


    def draw_sky(self):
        """Vẽ bầu trời."""
        self.display_surface.fill('#ddc6a9')
        horizon_pos = self.horizon_line+ self.offset.y

        #sea rect
        sea_rect = pygame.FRect(0, horizon_pos, WINDOW_WIDTH, WINDOW_HEIGHT -horizon_pos)
        pygame.draw.rect(self.display_surface, '#2faee0', sea_rect)


        #horizon line
        pygame.draw.line(self.display_surface, '#f5f1de', (0, horizon_pos), (WINDOW_WIDTH, horizon_pos), 5)

    def create_cloud(self):
        """Tạo đám mây."""
        pos =(randint(self.width, self.width + 700),randint(self.borders['top'], self.horizon_line))
        surf = choice(self.small_clouds)
        Cloud(pos, surf, self)

    def draw(self, target_pos, dt):
        """
        Vẽ tất cả các sprite.
            target_pos (tuple): Vị trí mục tiêu của camera.
            dt (float): Thời gian giữa các khung hình.
        """
        self.offset.x = -(target_pos[0] - WINDOW_WIDTH /2)
        self.offset.y = -(target_pos[1] - WINDOW_HEIGHT /2)
        self.camera_constraint()

        if self.sky:
            self.cloud_timer.update()
            self.draw_sky() 
            self.draw_large_cloud(dt)

        for sprite in sorted(self, key = lambda sprite: sprite.z ):
            offset_pos = sprite.rect.topleft + self.offset
            self.display_surface.blit(sprite.image, offset_pos)



class WorldSprites(pygame.sprite.Group):
    def __init__(self, data):
        """
        Khởi tạo tất cả các sprite trong overworld.
            data (Data): Dữ liệu trò chơi.
        """
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.data = data
        self.offset = vector()

    def draw(self, target_pos):
        """
        Vẽ tất cả các sprite trong thế giới của trò chơi.
            target_pos (tuple): Vị trí mục tiêu của camera.
        """
        self.offset.x = -(target_pos[0] - WINDOW_WIDTH /2)
        self.offset.y = -(target_pos[1] - WINDOW_HEIGHT /2)

        #background
        for sprite in sorted(self, key = lambda sprite: sprite.z):
            if sprite.z < Z_LAYERS['main']:
                if sprite.z == Z_LAYERS['path']:
                    if sprite.level <= self.data.unlocked_level:
                        self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)
                else:
                    self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)

        #main 
        for sprite in sorted(self, key = lambda sprite: sprite.rect.centery):
            if sprite.z ==Z_LAYERS['main']:
                if hasattr(sprite, 'icon'):
                    self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset + vector(0, -23))
                else:
                    self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)

        