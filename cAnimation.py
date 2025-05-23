import pygame

class NukeAnimation:
    def __init__(self, screen, font, width, height):
        self.screen = screen
        self.font = font
        self.width = width
        self.height = height
        
        self.state = "I_in"  # 動畫階段
        self.timer = 0
        
        # 文字與初始位置
        self.i_pos = [-50, height // 2]  # 左側外
        self.am_pos = [width + 50, height // 2]  # 右側外
        self.nb_scale = 0.1  # 縮放比例
        self.nb_alpha = 255
        
        # 文字表面
        self.i_surf = self.font.render("I", True, (255,255,255))
        self.am_surf = self.font.render("AM", True, (255,255,255))
        self.nb_text = "N-Bomb"

    def update(self):
        speed = 10
        self.timer += 1
        
        if self.state == "I_in":
            # I 從左邊移動到 x=100
            if self.i_pos[0] < 100:
                self.i_pos[0] += speed
            else:
                if self.timer > 30:
                    self.state = "I_out"
                    self.timer = 0

        elif self.state == "I_out":
            # I 跑回左邊外面
            if self.i_pos[0] > -50:
                self.i_pos[0] -= speed
            else:
                self.state = "AM_in"
                self.timer = 0

        elif self.state == "AM_in":
            # AM 從右邊移動到 x = width - 150
            if self.am_pos[0] > self.width - 150:
                self.am_pos[0] -= speed
            else:
                if self.timer > 30:
                    self.state = "AM_out"
                    self.timer = 0

        elif self.state == "AM_out":
            # AM 跑回右邊外面
            if self.am_pos[0] < self.width + 50:
                self.am_pos[0] += speed
            else:
                self.state = "NB_grow"
                self.timer = 0

        elif self.state == "NB_grow":
            # N-Bomb 從小放大到覆蓋整個螢幕
            if self.nb_scale < 10:
                self.nb_scale += 0.2
            else:
                self.state = "NB_fade"
                self.timer = 0

        elif self.state == "NB_fade":
            # N-Bomb 淡出
            if self.nb_alpha > 0:
                self.nb_alpha -= 5
            else:
                self.state = "done"  # 動畫結束

    def draw(self):
        if self.state in ["I_in", "I_out"]:
            self.screen.blit(self.i_surf, self.i_pos)
        elif self.state in ["AM_in", "AM_out"]:
            self.screen.blit(self.am_surf, self.am_pos)
        elif self.state in ["NB_grow", "NB_fade"]:
            # 繪製放大字
            scaled_font_size = int(self.font.get_height() * self.nb_scale)
            if scaled_font_size < 1:
                scaled_font_size = 1
            scaled_font = pygame.font.SysFont(None, scaled_font_size)
            nb_surf = scaled_font.render(self.nb_text, True, (255, 255, 255))
            nb_surf.set_alpha(self.nb_alpha)
            rect = nb_surf.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(nb_surf, rect)

    def is_done(self):
        return self.state == "done"