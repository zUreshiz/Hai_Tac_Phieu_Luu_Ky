from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf = pygame.Surface((TILE_SIZE, TILE_SIZE)) , groups = None, z= Z_LAYERS['main']):
       super().__init__(groups)
       self.image = surf
       self.rect = self.image.get_frect(topleft = pos)
       self.old_rect = self.rect.copy()
       self.z = z

class AnimatedSprite(Sprite):
	def __init__(self, pos, frames, groups, z = Z_LAYERS['main'], animation_speed = ANIMATION_SPEED):
		self.frames, self.frame_index = frames, 0
		super().__init__(pos, self.frames[self.frame_index], groups, z)
		self.animation_speed = animation_speed

	def animate(self, dt):
		self.frame_index += self.animation_speed * dt
		self.image = self.frames[int(self.frame_index % len(self.frames))]

	def update(self, dt):
		self.animate(dt) 

class MovingSprite(Sprite):
    def __init__(self, groups, start_pos, end_pos, move_dir, speed):
        surf = pygame.Surface((200,50))
        super().__init__(start_pos, surf, groups)
        self.image.fill('white')
        '''Thiết lập điểm neo cho sprite chuyển động'''
        if move_dir == 'x':
            self.rect.midleft = start_pos
        else:
            self.rect.midtop = start_pos
        self.start_pos = start_pos
        self.end_pos = end_pos

        '''Thiết lập thuộc tính chuyển động'''
        self.moving = True
        self.speed = speed
        self.direction = vector(1,0) if move_dir == 'x' else vector(0,1)
        self.move_dir = move_dir
    
    '''Kiểm tra ranh giới di chuyển của sprite'''
    def check_border(self):
        #horizontal
        if self.move_dir == 'x':
            '''Kiểm tra cạnh phải của sprite đã đạt đến vị trí kết thúc chưa'''
            if self.rect.right >= self.end_pos[0] and self.direction.x == 1:
                '''Thay đổi hướng sang trái'''
                self.direction.x = -1
                '''Cập nhật lại vị trí của sprite'''
                self.rect.right = self.end_pos[0]
            if self.rect.left <= self.start_pos[0] and self.direction.x == -1:
                self.direction.x = 1
                self.rect.left = self.start_pos[0]
        #vertical
        else:
            if self.rect.bottom >= self.end_pos[1] and self.direction.y == 1:
                self.direction.y = -1
                self.rect.bottom = self.end_pos[1]
            if self.rect.top <= self.start_pos[1] and self.direction.y == -1:
                self.direction.y = 1
                self.rect.top = self.start_pos[1]

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.rect.topleft += self.direction *self.speed *dt
        self.check_border()
