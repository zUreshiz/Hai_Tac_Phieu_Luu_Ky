from pygame import Surface
from settings import *
from math import sin, cos, radians
from random import randint
class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf = pygame.Surface((TILE_SIZE, TILE_SIZE)) , groups = None, z= Z_LAYERS['main']):
       super().__init__(groups)
       self.image = surf
       self.rect = self.image.get_frect(topleft = pos)
       self.old_rect = self.rect.copy()
       self.z = z
    """Khởi tạo một sprite.
            pos (tuple): Vị trí (x, y) của sprite.
            surf (pygame.Surface, optional): Bề mặt của sprite. Mặc định là một bề mặt trống có kích thước TILE_SIZE x TILE_SIZE.
            groups (pygame.sprite.Group, optional): Nhóm mà sprite sẽ tham gia. Mặc định là None.
            z (int, optional): Lớp Z của sprite. Mặc định là lớp 'main'.
    """

class AnimatedSprite(Sprite):
    def __init__(self, pos, frames, groups, z=Z_LAYERS['main'], animation_speed=ANIMATION_SPEED):
        """Khởi tạo một sprite có hiệu ứng chuyển động.
            pos (tuple): Vị trí (x, y) của sprite.
            frames (list): Danh sách các frame hình ảnh cho chuyển động.
            groups (pygame.sprite.Group): Nhóm mà sprite sẽ tham gia.
            z (int, optional): Lớp Z của sprite. Mặc định là lớp 'main'.
            animation_speed (int, optional): Tốc độ chuyển động. Mặc định là ANIMATION_SPEED.
        """
        self.frames, self.frame_index = frames, 0
        super().__init__(pos, self.frames[self.frame_index], groups, z)
        self.animation_speed = animation_speed

    def animate(self, dt):
        """Phương thức để chạy hoạt hình.
            dt (float): Thời gian trôi qua từ frame trước đến frame hiện tại.
        """
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]

    def update(self, dt):
        """Phương thức cập nhật sprite.
            dt (float): Thời gian trôi qua từ frame trước đến frame hiện tại.
        """
        self.animate(dt)

class MovingSprite(AnimatedSprite):
    def __init__(self, frames,  groups, start_pos, end_pos, move_dir, speed, flip = False):
        """Khởi tạo một sprite có thể di chuyển.
            frames (list): Danh sách các frame hình ảnh cho animate.
            groups (pygame.sprite.Group): Nhóm mà sprite sẽ tham gia.
            start_pos (tuple): Vị trí ban đầu (x, y) của sprite.
            end_pos (tuple): Vị trí kết thúc (x, y) của sprite.
            move_dir (str): Hướng di chuyển ('x' hoặc 'y').
            speed (int): Tốc độ di chuyển của sprite.
            flip (bool, optional): True nếu sprite cần đổi chiều khi di chuyển. Mặc định là False.
        """
        super().__init__(start_pos, frames, groups)
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

        self.flip = flip
        self.reverse = {'x': False, 'y': False}

    
    def check_border(self):
        '''Kiểm tra ranh giới di chuyển của sprite'''
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
            self.reverse['x'] = True if self.direction.x < 0 else False
        #vertical
        else:
            if self.rect.bottom >= self.end_pos[1] and self.direction.y == 1:
                self.direction.y = -1
                self.rect.bottom = self.end_pos[1]
            if self.rect.top <= self.start_pos[1] and self.direction.y == -1:
                self.direction.y = 1
                self.rect.top = self.start_pos[1]
            self.reverse['y'] = True if self.direction.y > 0 else False

    def update(self, dt):
        """Phương thức cập nhật sprite.
            dt (float): Thời gian trôi qua từ frame trước đến frame hiện tại.
        """
        self.old_rect = self.rect.copy()
        self.rect.topleft += self.direction *self.speed *dt
        self.check_border() 
        self.animate(dt) 
        if self.flip:
             self.image = pygame.transform.flip(self.image, self.reverse['x'], self.reverse['y'])

class Spike(Sprite):
    def __init__(self, pos, surf, groups, radius, speed, start_angle, end_angle,z = Z_LAYERS['main']):
        """Khởi tạo một spike.
            pos (tuple): Vị trí (x, y) của spike.
            surf (pygame.Surface): Bề mặt của spike.
            groups (pygame.sprite.Group): Nhóm mà spike sẽ tham gia.
            radius (int): Bán kính của spike.
            speed (int): Tốc độ quay của spike.
            start_angle (int): Góc bắt đầu quay (đơn vị: độ).
            end_angle (int): Góc kết thúc quay (đơn vị: độ).
            z (int, optional): Lớp Z của sprite. Mặc định là lớp 'main'.
        """
        self.center = pos
        self.radius = radius
        self.speed = speed
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.angle = self.start_angle
        self.direction = 1
        self.full_circle = True if self.end_angle == -1 else False

        #trigonometry
        y = self.center[1] + sin(radians(self.angle)) * self.radius 
        x = self.center[0] + cos(radians(self.angle)) * self.radius 
        super().__init__((x,y), surf, groups, z)
        
    def update(self,dt):
        """Cập nhật vị trí của spike sau mỗi frame.
            dt (float): Thời gian trôi qua từ frame trước đến frame hiện tại.
        """
        self.angle += self.direction * self.speed * dt

        if not self.full_circle:
            if self.angle >= self.end_angle:
                self.direction = -1
            if self.angle < self.start_angle:
                 self.direction = 1
            

        y = self.center[1] + sin(radians(self.angle)) * self.radius 
        x = self.center[0] + cos(radians(self.angle)) * self.radius 
        self.rect.center = (x , y)

class Item(AnimatedSprite):
    def __init__(self, item_type, pos, frames, groups, data):
        """Khởi tạo một item.
            item_type (str): Loại item ('gold', 'silver', 'diamond', 'skull', 'potion').
            pos (tuple): Vị trí (x, y) của item.
            frames (list): Các frame của animation của item.
            groups (pygame.sprite.Group): Nhóm mà item sẽ tham gia.
            data: Dữ liệu của trò chơi.
        """
        super().__init__(pos, frames, groups)
        self.rect.center = pos
        self.item_type = item_type
        self.data = data

    def activate(self):
        """Kích hoạt item để tương tác với dữ liệu trò chơi."""
        if self.item_type == 'gold':
            self.data.coins += 5
        if self.item_type == 'silver':
            self.data.coins += 1
        if self.item_type == 'diamond':
            self.data.coins += 10
        if self.item_type == 'skull':
            self.data.coins += 15
        if self.item_type == 'potion':
            self.data.health += 1
class ParticleEffectSprite(AnimatedSprite):
    def __init__(self, pos, frames, groups):
        """Khởi tạo một particle effect.
            pos (tuple): Vị trí (x, y) của particle effect.
            frames (list): Các frame của animation của particle effect.
            groups (pygame.sprite.Group): Nhóm mà particle effect sẽ tham gia.
        """
        super().__init__(pos, frames, groups)
        self.rect.center = pos  
        self.z = Z_LAYERS['fg']

    def animate(self, dt):
        """Chạy animation của particle effect.
            dt (float): Thời gian trôi qua từ frame trước đến frame hiện tại.
        """
        self.frame_index += self.animation_speed * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else: 
            self.kill()

class Cloud(Sprite):
    def __init__(self, pos , surf, groups,z = Z_LAYERS['clouds'] ):
        """Khởi tạo một đám mây.
            pos (tuple): Vị trí (x, y) của đám mây.
            surf (pygame.Surface): Bề mặt của đám mây.
            groups (pygame.sprite.Group): Nhóm mà đám mây sẽ tham gia.
            z (int, optional): Lớp Z của sprite. Mặc định là lớp 'clouds'.
        """
        super().__init__(pos, surf, groups, z)
        self.speed = randint(50, 120)
        self.direction = -1
        self.rect.midbottom = pos

    def update(self,dt):
        """Cập nhật vị trí của đám mây sau mỗi frame.
            dt (float): Thời gian trôi qua từ frame trước đến frame hiện tại.
        """
        self.rect.x += self.direction * self.speed * dt

        if self.rect.right <= 0:
            self.kill()
    
class Node(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, level, data, paths):
        """Khởi tạo một node trong overworld.
            pos (tuple): Vị trí (x, y) của node.
            surf (pygame.Surface): Bề mặt của node.
            groups (pygame.sprite.Group): Nhóm mà node sẽ tham gia.
            level (int): Cấp độ của node.
            data: Dữ liệu của trò chơi.
            paths (dict): Danh sách các đường đi từ node này đến các node khác.
        """
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (pos[0] + TILE_SIZE/2, pos[1] + TILE_SIZE/2))
        self.z = Z_LAYERS['path']
        self.level = level
        self.data = data
        self.paths = paths
        self.grid_pos = (int(pos[0] / TILE_SIZE), int(pos[1] / TILE_SIZE))
    
    def can_move(self, direction):
        """Kiểm tra xem có thể di chuyển theo hướng đã cho không.
            direction (str): Hướng di chuyển ('left', 'right', 'up', 'down').
            bool: True nếu có thể di chuyển, False nếu không thể.
        """
        if direction in list(self.paths.keys()) and int(self.paths[direction][0][0]) <= self.data.unlocked_level:
            return True

class Icon(pygame.sprite.Sprite):
    def __init__(self, pos, groups, frames):
        """Khởi tạo một biểu tượng.
            pos (tuple): Vị trí (x, y) của biểu tượng.
            groups (pygame.sprite.Group): Nhóm mà biểu tượng sẽ tham gia.
            frames (list): Các frame của animation của biểu tượng.
        """
        super().__init__(groups)
        self.icon =True
        self.path = None
        self.direction = vector()
        self.speed = 400

        #image
        self.frames, self.frame_index = frames, 0
        self.state = 'idle'
        self.image = self.frames[self.state][self.frame_index]
        self.z = Z_LAYERS['main']


        self.rect = self.image.get_frect(center = pos)

    # def can_move(self, path):
    #     self.rect.center = path[0]
    #     self.path = path[1:]
    #     self.find_path()

    def start_move(self, path):
        """Bắt đầu di chuyển theo một đường đã cho.
            path (list): Danh sách các điểm trên đường đi.
        """
        self.rect.center = path[0]
        self.path = path[1:]
        self.find_path()

    def find_path(self):
        """Tìm đường đi tiếp theo trên đường đã chọn."""
        if self.path:
            if self.rect.centerx == self.path[0][0]: #vertical
                self.direction = vector(0, 1 if self.path[0][1] > self.rect.centery else -1)
            else: #horizontal 
                self.direction = vector(1 if self.path[0][0] > self.rect.centerx else -1, 0)
        else:
            self.direction = vector()

    def point_collision(self):
        """Xử lý va chạm với điểm trên đường đã chọn."""
        if self.direction.y == 1 and self.rect.centery >= self.path[0][1] or \
            self.direction.y == -1 and self.rect.centery <= self.path[0][1]:
            self.rect.centery = self.path[0][1]
            del self.path[0]
            self.find_path()

        if self.direction.x == 1 and self.rect.centerx >= self.path[0][0] or \
            self.direction.x == -1 and self.rect.centerx <= self.path[0][0]:
            self.rect.centerx = self.path[0][0]
            del self.path[0]
            self.find_path()

    def animate(self, dt):
        """Chạy animation của player.
            dt (float): Thời gian trôi qua từ frame trước đến frame hiện tại.
        """
        self.frame_index += ANIMATION_SPEED *dt
        self.image = self.frames[self.state][int(self.frame_index % len(self.frames[self.state]))]
         
    def get_state(self):
        """Xác định trạng thái di chuyển của player."""
        self.state = 'idle'
        if self.direction == vector(1, 0): 
            self.state = 'right'        
        if self.direction == vector(-1, 0): 
            self.state = 'left'        
        if self.direction == vector(0, 1): 
            self.state = 'down'       
        if self.direction == vector(0, -1): 
            self.state = 'up'
       
    def update(self, dt):
        """Cập nhật vị trí và trạng thái của player sau mỗi frame.
            dt (float): Thời gian trôi qua từ frame trước đến frame hiện tại.
        """
        if self.path:
            self.point_collision()
            self.rect.center += self.direction * self.speed * dt
        self.get_state()
        self.animate(dt)

class PathSprite(Sprite):
    def __init__(self, pos, surf, groups, level):
        """Khởi tạo một sprite đường đi.
            pos (tuple): Vị trí (x, y) của sprite.
            surf (pygame.Surface): Bề mặt của sprite.
            groups (pygame.sprite.Group): Nhóm mà sprite sẽ tham gia.
            level (int): Cấp độ của sprite.
        """
        super().__init__(pos, surf, groups, Z_LAYERS['path'])
        self.level = level