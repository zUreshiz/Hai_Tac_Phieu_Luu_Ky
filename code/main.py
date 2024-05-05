from settings import *
from level import Level
from pytmx.util_pygame import load_pygame
from os.path import join
from math import sin
from data import Data
from debug import debug
from ui import UI
from overworld import Overworld

from support import *

class Game: 
    """Lớp Game điều khiển trò chơi Hải Tặc Phiêu Lưu Ký."""
    def __init__(self):
        """Khởi tạo trò chơi."""
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Hải Tặc Phiêu Lưu Ký')
        self.clock = pygame.time.Clock()
        self.import_assets()


        self.ui = UI(self.font, self.ui_frames)
        self.data = Data(self.ui)
        '''tmx_map là map test '''
        self.tmx_maps = {
            0: load_pygame(join('.','data','levels','test.tmx')),
            1: load_pygame(join('.','data','levels','1.tmx')),
            2: load_pygame(join('.','data','levels','2.tmx')),
            3: load_pygame(join('.','data','levels','3.tmx')),
            4: load_pygame(join('.','data','levels','4.tmx')),
            5: load_pygame(join('.','data','levels','5.tmx')),



            }
        self.tmx_overworld = load_pygame(join('.','data','overworld','overworld.tmx'))
        '''current stage là level hiện tại của người chơi'''
        self.current_stage = Level(self.tmx_maps[self.data.current_level], self.level_frames, self.audio_files, self.data, self.switch_stage)
        self.bg_music.play(-1)
        
    def switch_stage(self, target, unlock = 0):
        """Chuyển đổi giữa các giai đoạn trong trò chơi.
            target (str): Mục tiêu chuyển đổi (level hoặc overworld).
            unlock (int): Cấp độ mới được mở khi chuyển đổi. Mặc định là 0.
        """
        if target == 'level':
            self.current_stage = Level(self.tmx_maps[self.data.current_level], self.level_frames, self.audio_files, self.data, self.switch_stage)
        else:
            if unlock > 0:
                self.data.unlocked_level = unlock
            else:
                self.data.health -= 1
            self.current_stage = Overworld(self.tmx_overworld, self.data, self.overworld_frames, self.switch_stage)

    def import_assets(self):
        """Nhập các tài nguyên cần thiết cho trò chơi nhưu tileset, audio, map..."""
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
            'water_top': import_folder('.',  'graphics', 'level', 'water', 'top'),
            'water_body': import_image('.',  'graphics', 'level', 'water', 'body'),
            'bg_tiles': import_folder_dict('.',  'graphics', 'level', 'bg', 'tiles'),
            'cloud_small': import_folder('.',  'graphics', 'level', 'clouds', 'small'),
            'cloud_large': import_image('.',  'graphics', 'level', 'clouds', 'large_cloud'),


            



        }


        self.font = pygame.font.Font(join('.', 'graphics', 'ui','runescape_uf.ttf'), 40)
        self.ui_frames = {
            'heart' : import_folder('.','graphics','ui', 'heart'),
            'coin' : import_image('.','graphics','ui', 'coin')

        }

        self.overworld_frames = {
            'palms' : import_folder('.','graphics','overworld','palm'),
            'water' : import_folder('.','graphics','overworld','water'),
            'path' : import_folder_dict('.','graphics','overworld','path'),
            'icon' : import_sub_folders('.','graphics','overworld','icon'),


        }

        self.audio_files = {
            'coin': pygame.mixer.Sound(join('.', 'audio', 'coin.wav')),
            'attack': pygame.mixer.Sound(join('.', 'audio', 'attack.wav')),
            'damage': pygame.mixer.Sound(join('.', 'audio', 'damage.wav')),
            'hit': pygame.mixer.Sound(join('.', 'audio', 'hit.wav')),
            'jump': pygame.mixer.Sound(join('.', 'audio', 'jump.wav')),
            'pearl': pygame.mixer.Sound(join('.', 'audio', 'pearl.wav')),
        }
        self.bg_music = pygame.mixer.Sound(join('.', 'audio', 'starlight_city.mp3'))
        self.bg_music.set_volume(0.2)


    def game_over_screen(self):
        """Hiển thị màn hình kết thúc game khi người chơi thua."""
        while True:
            self.display_surface.fill('#0A6847')

            gold_font = pygame.font.Font(join('.', 'graphics', 'ui', 'runescape_uf.ttf'), 40)
            gold_text = gold_font.render("Coins: {}".format(self.data.coins), True, (255, 255, 0))  # Màu vàng
            gold_rect = gold_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40))  # Đặt văn bản ở giữa màn hình
            self.display_surface.blit(gold_text, gold_rect)

            # Hiển thị văn bản "Game Over"
            game_over_font = pygame.font.Font(join('.', 'graphics', 'ui', 'runescape_uf.ttf'), 60)
            game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
            game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100))
            self.display_surface.blit(game_over_text, game_over_rect)

            # Vẽ nút "Retry"
            retry_font = pygame.font.Font(join('.', 'graphics', 'ui', 'runescape_uf.ttf'), 40)
            retry_text = retry_font.render("Retry", True, ('#7ABA78'))
            retry_rect = retry_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 15))
            self.display_surface.blit(retry_text, retry_rect)

            # Vẽ nút "Exit"
            exit_font = pygame.font.Font(join('.', 'graphics', 'ui', 'runescape_uf.ttf'), 40)
            exit_text = exit_font.render("Exit", True, ('#7ABA78'), )
            exit_rect = exit_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 70))
            self.display_surface.blit(exit_text, exit_rect)

            pygame.display.flip()

            # Lắng nghe sự kiện
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if retry_rect.collidepoint(mouse_pos):
                        self.restart_game()  
                        return  
                    elif exit_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()


    def check_game_over(self):
        """Kiểm tra máu người chơi để kết thúc game."""
        if self.data.health <= 0:
            self.game_over_screen()  


    # def check_game_over(self):
    #     if self.data.health <= 0:
    #         pygame.quit()
    #         sys.exit()

    def restart_game(self):
        """Khởi động lại trò chơi khi người chơi muốn chơi lại."""
        self.data.health = 6  # Đặt lại máu
        self.data.coins = 0  
        self.current_stage = Level(self.tmx_maps[self.data.current_level], self.level_frames, self.audio_files, self.data, self.switch_stage)


    def start_screen(self):
        """Hiển thị màn hình bắt đầu game."""
        while True:
            self.display_surface.fill('#0A6847')

            # Sử dụng font 'runescape_uf.ttf' với kích thước 50 cho tiêu đề trò chơi
            game_title_font = pygame.font.Font(join('.', 'graphics', 'ui', 'runescape_uf.ttf'), 75)
            game_title_text = game_title_font.render("ADVENTURES OF THE PIRATE", True, ('#F6E9B2'))
            game_title_rect = game_title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 -75))
            self.display_surface.blit(game_title_text, game_title_rect)

            # Sử dụng font 'runescape_uf.ttf' với kích thước 36 cho văn bản "Start" và "Exit"
            start_font = pygame.font.Font(join('.', 'graphics', 'ui', 'runescape_uf.ttf'), 40)
            start_text = start_font.render("Start", True, ('#7ABA78'))
            start_rect = start_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 15))
            self.display_surface.blit(start_text, start_rect)

            exit_text = start_font.render("Exit", True, ('#7ABA78'), )
            exit_rect = exit_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 70))
            self.display_surface.blit(exit_text, exit_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if start_rect.collidepoint(mouse_pos):
                        return
                    elif exit_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()

    def pause_screen(self):
        """Hiển thị màn hình tạm dừng trò chơi."""
        while True:
            self.display_surface.fill('#0A6847')

            # Hiển thị văn bản "Pause"
            pause_font = pygame.font.Font(join('.', 'graphics', 'ui', 'runescape_uf.ttf'), 60)
            pause_text = pause_font.render("PAUSE", True, (255, 255, 255))
            pause_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100))
            self.display_surface.blit(pause_text, pause_rect)

            # Vẽ nút "Tiếp tục"
            continue_font = pygame.font.Font(join('.', 'graphics', 'ui', 'runescape_uf.ttf'), 40)
            continue_text = continue_font.render("Continue", True, ('#7ABA78'))
            continue_rect = continue_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.display_surface.blit(continue_text, continue_rect)

            # Vẽ nút "Thoát ra menu"
            exit_menu_text = continue_font.render("Exit to menu", True, ('#7ABA78'))
            exit_menu_rect = exit_menu_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
            self.display_surface.blit(exit_menu_text, exit_menu_rect)

            # Vẽ nút "Thoát"
            exit_text = continue_font.render("Exit", True, ('#7ABA78'))
            exit_rect = exit_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100))
            self.display_surface.blit(exit_text, exit_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if continue_rect.collidepoint(mouse_pos):
                        return  # Tiếp tục chơi
                    elif exit_menu_rect.collidepoint(mouse_pos):
                        # Trở về màn hình menu
                        self.start_screen()
                        return
                    elif exit_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()



    def run(self):
        """khởi chạy trò chơi."""
        self.start_screen()
        while True:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause_screen()  # Hiển thị màn hình tạm dừng khi nhấn Esc
            self.check_game_over()
            self.current_stage.run(dt)
            self.ui.update(dt)
            pygame.display.update()



if __name__ == '__main__':
    game = Game()
    game.run()