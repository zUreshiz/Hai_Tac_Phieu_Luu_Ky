from settings import *
from timer import Timer
from os.path import join
from math import sin

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, semi_collision_sprites, frames, data, attack_sound, jump_sound):
        """
        Khởi tạo đối tượng Player.
            pos (tuple): Vị trí ban đầu của người chơi (x, y).
            groups (pygame.sprite.Group): Nhóm sprite chứa người chơi.
            collision_sprites (pygame.sprite.Group): Nhóm sprite cho va chạm toàn phần.
            semi_collision_sprites (pygame.sprite.Group): Nhóm sprite cho va chạm bán phần.
            frames (dict): Frame của người chơi.
            data (object): Dữ liệu trò chơi.
            attack_sound (pygame.mixer.Sound): Âm thanh của hành động attack.
            jump_sound (pygame.mixer.Sound): Âm thanh của hành động nhảy.
        """
        #general setup
        super().__init__(groups)
        self.z = Z_LAYERS['main']
        self.data = data
  
        #img
        self.frames, self.frame_index = frames, 0
        self.state, self.facing_right = 'idle', True
        self.image = self.frames[self.state][self.frame_index]

        #rects
        self.rect = self.image.get_frect(topleft = pos)
        self.hitbox_rect = self.rect.inflate(-76, -36)
        self.old_rect = self.hitbox_rect.copy()

        #movement
        self.direction = vector()
        self.speed = 500
        self.gravity = 1000
        self.jump = False
        self.jump_height = 700
        self.attacking = False

        #collision: va chạm
        self.collision_sprites = collision_sprites
        self.semi_collision_sprites = semi_collision_sprites
        self.on_surface = {'floor': False, 'left': False, 'right': False}
        self.platform = None

        #Timer
        self.timers = {
            'wall jump': Timer(400),
            'wall slide block': Timer(250),
            'platform skip' : Timer(100),
            'attack block' : Timer(100),
            'hit': Timer(400)
        }

        #audio
        self.attack_sound = attack_sound
        self.attack_sound.set_volume(0.1)
        self.jump_sound = jump_sound
        self.jump_sound.set_volume(0.1)

    def input(self):
        """
        Xử lý sự kiện nhập từ bàn phím để điều khiển người chơi.
        """
        keys = pygame.key.get_pressed()
        # Tạo biến input_vector nếu right +1, left -1
        input_vector = vector(0,0)
        if not self.timers['wall jump'].active:
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]: 
                input_vector.x += 1
                self.facing_right = True
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                input_vector.x -= 1
                self.facing_right = False
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.timers['platform skip'].activate()
            # normalize để độ dài vector luôn là 1 

            if keys[pygame.K_x]:
                self.attack()

            self.direction .x= input_vector.normalize().x if input_vector else input_vector.x
        

        if keys[pygame.K_SPACE]:
            self.jump = True

    def attack(self):
        """
        Xử lý hành động tấn công của người chơi.
        """
        if not self.timers['attack block'].activate():
            self.attacking = True 
            self.frame_index = 0
            self.timers['attack block'].activate()
            self.attack_sound.play()
        

    def move(self, dt):
        """
        Xử lý việc di chuyển của người chơi.
        """
        #horizontal: hoành
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')

        #vertical: tung
        if not self.on_surface['floor'] and any((self.on_surface['left'], self.on_surface['right'])) and not self.timers['wall slide block'].active:
            self.direction.y = 0
            self.hitbox_rect.y += self.gravity / 10 * dt
        else:
            self.direction.y += self.gravity / 2 * dt
            self.hitbox_rect.y += self.direction.y * dt
            self.direction.y += self.gravity / 2 * dt

        if self.jump:
            if self.on_surface['floor']:
                self.direction.y = -self.jump_height
                self.timers['wall slide block'].activate()
                self.hitbox_rect.bottom -=1
                self.jump_sound.play()
            elif any((self.on_surface['left'], self.on_surface['right'])) and not self.timers['wall slide block'].active:
                self.timers['wall jump'].activate()
                self.direction.y = -self.jump_height
                self.direction.x = 1 if self.on_surface['left'] else -1
                self.jump_sound.play()
            self.jump = False

        self.collision('vertical')
        self.semi_collision()
        self.rect.center = self.hitbox_rect.center

    def platform_move(self, dt):
        '''Hàm xử lý việc di chuyển trên platform'''
        if self.platform:
            self.hitbox_rect.topleft += self.platform.direction * self.platform.speed * dt


    def check_contact(self):
        """
        Kiểm tra va chạm với các sprite khác.
        """
        floor_rect = pygame.Rect(self.hitbox_rect.bottomleft,(self.hitbox_rect.width,2))
        right_rect = pygame.Rect(self.hitbox_rect.topright+ vector(0,self.hitbox_rect.height / 4),(2, self.hitbox_rect.height / 2))
        left_rect = pygame.Rect(self.hitbox_rect.topleft + vector(-2, self.hitbox_rect.height / 4), (2, self.hitbox_rect.height / 2))
        collide_rects = [sprite.rect for sprite in self.collision_sprites]
        semi_collide_rect = [sprite.rect for sprite in self.semi_collision_sprites]

        #collision
        self.on_surface['floor'] = True if floor_rect.collidelist(collide_rects) >= 0 or floor_rect.collidelist(semi_collide_rect) >= 0 and self.direction.y >= 0 else False
        self.on_surface['right'] = True if right_rect.collidelist(collide_rects) >= 0 else False
        self.on_surface['left'] = True if left_rect.collidelist(collide_rects) >= 0 else False

        self.platform = None
        sprites = self.collision_sprites.sprites() + self.semi_collision_sprites.sprites()
        for sprite in [sprite for sprite in sprites if hasattr(sprite, 'moving')]:
            if sprite.rect.colliderect(floor_rect):
                self.platform = sprite

    def collision(self, axis):
        """
        Xử lý va chạm với sprite theo chiều ngang hoặc dọc.
        """
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if axis == 'horizontal':
                    '''check giữa hai phía player và sprite'''
                    #left
                    if self.hitbox_rect.left <= sprite.rect.right and int(self.old_rect.left) >= int(sprite.old_rect.right):
                        self.hitbox_rect.left = sprite.rect.right
                    #right
                    if self.hitbox_rect.right >= sprite.rect.left and int(self.old_rect.right) <= int(sprite.old_rect.left):
                        self.hitbox_rect.right = sprite.rect.left
                else:
                    '''check phía trên dưới của player và sprite'''
                    #Top
                    if self.hitbox_rect.top <= sprite.rect.bottom and int(self.old_rect.top) >= int(sprite.old_rect.bottom):
                        self.hitbox_rect.top = sprite.rect.bottom
                        if hasattr(sprite, 'moving'):
                            self.hitbox_rect.top +=6
                    #bottom
                    if self.hitbox_rect.bottom >= sprite.rect.top and int(self.old_rect.bottom) <= int(sprite.old_rect.top):
                        self.hitbox_rect.bottom = sprite.rect.top
                    self.direction.y = 0


    def semi_collision(self):
        """
        Kiểm tra va chạm bán phần với các sprite khác.
        """
        if not self.timers['platform skip'].active:
            for sprite in self.semi_collision_sprites:
                if sprite.rect.colliderect(self.hitbox_rect):
                    if self.hitbox_rect.bottom >= sprite.rect.top and int(self.old_rect.bottom) <= sprite.old_rect.top:
                        self.hitbox_rect.bottom = sprite.rect.top
                        if self.direction.y > 0:
                            self.direction.y = 0

    def update_timers(self):
        """
        Cập nhật các bộ đếm thời gian.
        """
        for timer in self.timers.values():
            timer.update()

    def animate(self, dt):
        """
        Chạy hoạt ảnh cho người chơi.
        """
        self.frame_index += ANIMATION_SPEED * dt
        if self.state == 'attack' and self.frame_index >= len(self.frames[self.state]):
            self.state = 'idle'
        self.image = self.frames[self.state][int(self.frame_index % len(self.frames[self.state]))]
        self.image = self.image if self.facing_right else pygame.transform.flip(self.image, True, False)
        
        if self.attacking and self.frame_index > len(self.frames[self.state]):
            self.attacking = False

    def get_state(self):
        """
        Xác định trạng thái hiện tại của người chơi.
        """
        if self.on_surface['floor']:
            if self.attacking:
                self.state = 'attack'
            else:
                self.state = 'idle' if self.direction.x == 0 else 'run'
        else:
            if self.attacking:
                self.state = 'air_attack'
            else:
                if any((self.on_surface['left'], self.on_surface['right'])):
                    self.state = 'wall'
                else:
                    self.state = 'jump' if self.direction.y < 0 else 'fall'
    
    def get_damage(self):
        """
        Giảm health của người chơi.
        """
        if not self.timers['hit'].active:
            self.data.health -=1
            self.timers['hit'].activate()

    def flicker(self):
        """
        Hiệu ứng nhấp nháy khi bị tấn công.
        """
        if self.timers['hit'].active :
            white_mask = pygame.mask.from_surface(self.image)
            white_surf = white_mask.to_surface()
            white_surf.set_colorkey('black')
            self.image = white_surf

    def update(self, dt):
        """
        Cập nhật trạng thái của người chơi.
        """
        self.old_rect = self.hitbox_rect.copy()
        self.update_timers()
        self.input()
        self.move(dt)
        self.platform_move(dt)
        self.check_contact()
        self.get_state()
        self.animate(dt)
        self.flicker()
