from settings import *
from sprites import AnimatedSprite
from random import randint
from timer import Timer

class UI:
    def __init__(self, font, frames):
        self.display_surface = pygame.display.get_surface()
        self.sprites = pygame.sprite.Group()
        self.font = font

        #health
        self.heart_frames = frames['heart']
        self.heart_surf_width = self.heart_frames[0].get_width()
        self.heart_padding = 10

        #coin= 0
        self.coin_amount = 0
        self.coin_timer = Timer(1000)
        self.coin_surf = frames['coin']


    def display_text(self):
        text_surf = self.font.render(str(self.coin_amount), False, 'gray')
        text_rect = text_surf.get_frect(topright=(self.display_surface.get_width()-50,5))
        self.display_surface.blit(text_surf, text_rect)

        coin_rect = self.coin_surf.get_frect(centerx=text_rect.right+20, centery=text_rect.centery-3)
        self.display_surface.blit(self.coin_surf, coin_rect)


    def create_hearts(self, amount):
        for sprite in self.sprites:
            sprite.kill()
        for heart in range(amount):
            x= 10 +heart *(self.heart_surf_width + self.heart_padding)
            y= 10
            Heart((x,y), self.heart_frames, self.sprites)

    def show_coins(self, amount):
        self.coin_amount = amount


    def update(self, dt):
        self.sprites.update(dt)
        self.sprites.draw(self.display_surface)
        self.display_text()

class Heart(AnimatedSprite):
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)
        self.active = False

    def animate(self, dt):
        self.frame_index += ANIMATION_SPEED * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.active = False
            self.frame_index = 0

    def update(self, dt):
        if self.active:
            self.animate(dt)
        else:
            if randint(0,2000) ==1:
                self.active = True