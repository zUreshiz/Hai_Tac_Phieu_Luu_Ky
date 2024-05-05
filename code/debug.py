import pygame
pygame.init()
font = pygame.font.Font(None, 30)

def debug(info, y = 10, x= 10):
    """
    Hiển thị thông tin debug lên màn hình.
        info (any): Thông tin cần hiển thị, có thể là bất kỳ kiểu dữ liệu nào có thể chuyển đổi thành chuỗi.
        y (int): Vị trí theo trục y để hiển thị thông tin debug. Mặc định là 10.
        x (int): Vị trí theo trục x để hiển thị thông tin debug. Mặc định là 10.
    """
    display_surface = pygame.display.get_surface()
    debug_surf = font.render(str(info), True, 'White')
    debug_rect = debug_surf.get_rect(topleft = (x,y))
    pygame.draw.rect(display_surface, 'Black', debug_rect)
    display_surface.blit(debug_surf, debug_rect)