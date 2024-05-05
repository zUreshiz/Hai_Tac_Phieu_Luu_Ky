from pygame.time import get_ticks

class Timer:
    def __init__(self, duration, func = None, repeat = False):
        """Khởi tạo một đối tượng hẹn giờ.
            duration (int): Thời gian kéo dài của hẹn giờ (đơn vị: milliseconds).
            func (function, optional): Hàm sẽ được gọi khi hẹn giờ kết thúc. Mặc định là None.
            repeat (bool, optional): Xác định liệu hẹn giờ sẽ lặp lại sau khi kết thúc hay không. Mặc định là False.
        """
        self.duration = duration
        self.func = func
        self.start_time = 0
        self.active = False
        self.repeat = repeat
    
    def activate(self):
        """Kích hoạt hẹn giờ."""
        self.active = True
        self.start_time = get_ticks()

    def deactivate(self):
        """Ngưng kích hoạt hẹn giờ."""
        self.active = False
        self.start_time = 0
        if self.repeat:
            self.activate()

    def update(self):
        """Cập nhật trạng thái của hẹn giờ."""
        current_time = get_ticks()
        if current_time - self.start_time >= self.duration:
            if self.func and self.start_time != 0:
                self.func()
            self.deactivate()