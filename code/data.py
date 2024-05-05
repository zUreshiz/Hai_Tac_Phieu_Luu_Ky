class Data:
    """Lớp Data lưu trữ dữ liệu của trò chơi như số vàng, máu, và trạng thái của giao diện người dùng."""
    def __init__(self, ui):
        """
        Khởi tạo một đối tượng Data mới.
            ui (UI): Đối tượng UI để tương tác với giao diện người dùng.
        """
        self.ui =ui
        self._coins = 0
        self._health = 6
        self.ui.create_hearts(self._health)

        self.unlocked_level = 0
        self.current_level = 0
    

    #Coins
    @property
    def coins(self):
        """Trả về số vàng hiện tại."""
        return self._coins
    
    @coins.setter
    def coins(self, value):
        """
        Thiết lập số vàng mới và cập nhật giao diện người dùng.
            value (int): Số vàng mới.
        """
        self._coins = value
        self.ui.show_coins(value)

    #Health
    @property
    def health(self):
        """Trả về số máu hiện tại."""
        return self._health
    
    @health.setter
    def health(self, value):
        """
        Thiết lập số máu mới và cập nhật giao diện người dùng.
            value (int): Số máu mới.
        """
        self._health = value
        self.ui.create_hearts(value)