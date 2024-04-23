from settings import *
from level import Level
from pytmx.util_pygame import load_pygame
from os.path import join

from support import *

class Game: 
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Hải Tặc Phiêu Lưu Ký')
        self.clock = pygame.time.Clock()
        self.import_assets()

        '''tmx_map là map test '''
        self.tmx_maps = {0: load_pygame(join('data','levels','test.tmx'))}
        '''current stage là level hiện tại của người chơi'''
        self.current_stage = Level(self.tmx_maps[0], self.level_frames)

    def import_assets(self):
        self.level_frames = {
            'flag': import_folder('.', 'graphics', 'level', 'flag'),
            'saw' : import_folder('.', 'graphics', 'enemies', 'saw', 'animation'),
            'floor_spike': import_folder('.', 'graphics', 'enemies', 'floor_spikes'),
            'palms': import_sub_folders('.', 'graphics', 'level', 'palms'),
            'candle': import_folder('.', 'graphics', 'level', 'candle'),
            'window': import_folder('.', 'graphics', 'level', 'window'),
            'big_chain': import_folder('.', 'graphics', 'level', 'big_chain'),
            'small_chain': import_folder('.', 'graphics', 'level', 'small_chain'),
            'candle_light': import_folder('.', 'graphics', 'level', 'candle light'),
            'player': import_sub_folders('.', 'graphics', 'player'),
            'saw': import_folder('..', 'graphics', 'enemies', 'saw', 'animation'),
            'saw_chain': import_image('..',  'graphics', 'enemies', 'saw', 'saw_chain'),
            'helicopter': import_folder('..', 'graphics', 'level', 'helicopter'),
            'boat': import_folder('..',  'graphics', 'objects', 'boat'),
            
        }
        print(self.level_frames['candle_light'])
    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.current_stage.run(dt)

            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()