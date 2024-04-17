from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.Surface((48,56))
        self.image.fill('red')

        #rects
        self.rect = self.image.get_frect(topleft = pos)
        self.old_rect = self.rect.copy()

        #movement
        self.direction = vector()
        self.speed = 200
        self.gravity = 1000

        #collision: va chạm
        self.collision_sprites = collision_sprites

    def input(self):
        '''Hàm xử lý sự kiện nhập từ bàn phím để điều khiển đối tượng di chuyển'''
        '''Biến keys lấy tất cả thông tin của các phím người dùng đang nhấn'''
        keys = pygame.key.get_pressed()
        # Tạo biến input_vector nếu right +1, left -1
        input_vector = vector(0,0)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: 
            input_vector.x += 1
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            input_vector.x -= 1
        # normalize để độ dài vector luôn là 1 
        self.direction .x= input_vector.normalize().x if input_vector else input_vector.x

    def move(self, dt):
        '''tốc độ player khi di chuyển tung và hoành'''
        #horizontal: hoành
        self.rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')

        #vertical: tung
        self.direction.y += self.gravity / 2 * dt
        self.rect.y += self.direction.y * dt
        self.direction.y += self.gravity / 2 * dt
        self.collision('vertical')




    def collision(self, axis):
        '''Hàm để xử lý collision giữa player và sprite'''
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if axis == 'horizontal':
                    '''check giữa hai phía player và sprite'''
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                else:
                    '''check phía trên dưới của player và sprite'''
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                    self.direction.y = 0

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.input()
        self.move(dt)
