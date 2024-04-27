from settings import *
from level import Level
from pytmx.util_pygame import load_pygame
from os.path import join
from math import sin
from data import Data
from debug import debug
from ui import UI

from support import *

class Game: 
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Hải Tặc Phiêu Lưu Ký')
        self.clock = pygame.time.Clock()
        self.import_assets()


        self.ui = UI(self.font, self.ui_frames)
        self.data = Data(self.ui)
        '''tmx_map là map test '''
        self.tmx_maps = {0: load_pygame(join('data','levels','test.tmx'))}
        '''current stage là level hiện tại của người chơi'''
        self.current_stage = Level(self.tmx_maps[0], self.level_frames, self.data)

    def import_assets(self):
        self.level_frames = {
            'flag': import_folder('.', 'graphics', 'level', 'flag'),
            'saw' : import_folder('.', 'graphics', 'enemies', 'saw', 'animation'),
            'floor_spike': import_folder('.', 'graphics', 'enemies', 'floor_spikes'),
            'palms': import_sub_folders('.', 'graphics', 'level', 'palms'),
            'candle': import_folder('.', 'graphics', 'level', 'candle'),
            'window': import_folder('.', 'graphics', 'level', 'window'),
            'big_chain': import_folder('.', 'graphics', 'level', 'big_chains'),
            'small_chain': import_folder('.', 'graphics', 'level', 'small_chains'),
            'candle_light': import_folder('.', 'graphics', 'level', 'candle light'),
            'player': import_sub_folders('.', 'graphics', 'player'),
            'saw': import_folder('.', 'graphics', 'enemies', 'saw', 'animation'),
            'saw_chain': import_image('.',  'graphics', 'enemies', 'saw', 'saw_chain'),
            'helicopter': import_folder('.', 'graphics', 'level', 'helicopter'),
            'boat': import_folder('.',  'graphics', 'objects', 'boat'),
            'spike': import_image('.',  'graphics', 'enemies', 'spike_ball', 'Spiked Ball'),
            'spike_chain': import_image('.',  'graphics', 'enemies', 'spike_ball', 'spiked_chain'),
            'tooth': import_folder('.',  'graphics', 'enemies', 'tooth', 'run'),
            'shell': import_sub_folders('.', 'graphics', 'enemies', 'shell'),
            'pearl': import_image('.', 'graphics', 'enemies', 'bullets','pearl'),
            'items': import_sub_folders('.', 'graphics',  'items'),
            'particle': import_folder('.',  'graphics', 'effects', 'particle'),

        }


        self.font = pygame.font.Font(join('.', 'graphics', 'ui','runescape_uf.ttf'), 40)
        self.ui_frames = {
            'heart' : import_folder('.','graphics','ui', 'heart'),
            'coin' : import_image('.','graphics','ui', 'coin')

        }
    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.current_stage.run(dt)
            self.ui.update(dt)
            # debug(self.data.health)
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()