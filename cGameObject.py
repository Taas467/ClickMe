import random
from cGameGlobal import *


class GameRule:
    def __init__(self, text, x, y, font, Width, Height, color):
        self.surface = font.render(text, True, color)
        self.rect = self.surface.get_rect(center=(x, y))
        self.orginv_x = 5
        self.vx = random.choice([-5, 5])
        self.orginv_y = -20
        self.vy = -10  # 初始向上跳
        self.gravity = 0.4
        self.height = Height
        self.width = Width

    def update(self):
        # 模擬跳動
        self.vy += self.gravity
        self.rect.y += int(self.vy)
        self.rect.x += self.vx

        if self.rect.top < 0:
            self.rect.top = 0
            self.vy = -self.vy * 0.9

        # 碰到底部就彈起
        if self.rect.bottom >= self.height:
            self.rect.bottom = self.height
            if abs(abs(self.vy) - abs(self.orginv_y)) < 0.7:
                self.vy = self.orginv_y
            elif abs(self.vy) < 5:
                self.vy = -abs(self.vy) * 2.5
            elif abs(self.vy) < abs(self.orginv_y):
                self.vy = -abs(self.vy) * 1.1
            else:
                self.vy = -abs(self.vy) * 0.9
            if abs(self.vx) < 2:
                self.vx = 3 if self.vx > 0 else -3

        # 左右邊界反彈
        if self.rect.left < 0 or self.rect.right > self.width:
            if self.rect.left < 0:
                self.rect.left = 0
            else:
                self.rect.right = self.width
            if abs(self.vx) == self.orginv_x:
                self.vx *= random.uniform(0.6, 1.4)
                self.vx *= -1
            elif abs(abs(self.vx) - self.orginv_x) < 0.2:
                self.vx = self.orginv_x * (1 if self.vx > 0 else -1)
            elif abs(self.vx) < self.orginv_x:
                self.vx = -self.vx * 1.1
            else:
                self.vx = -self.vx * 0.9
            if abs(self.vx) > 15:
                self.vx = 15 * (1 if self.vx > 0 else -1)

    def draw(self, surface):
        surface.blit(self.surface, self.rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class mClickMe(GameRule):
    def __init__(self, x, y, font, width, height):
        super().__init__(
            "ClickMe", x, y, font, width, height, color=(0, 255, 0)
        )  # 設定為綠色

    def GetClick(self, texts, font):
        game_state.betouch()
        new_emeny = mEnemy(self.rect.x, self.rect.y, font, self.width, self.height)
        while True:
            temp_x = random.randint(0, self.width)
            temp_y = random.randint(0, self.height)
            if (temp_x - self.rect.x) ** 2 + (temp_y - self.rect.y) ** 2 > 10000:
                self.rect.x, self.rect.y = temp_x, temp_y
                self.vy = -10
                break
        texts.append(new_emeny)


class mEnemy(GameRule):
    def __init__(self, x, y, font, width, height):
        super().__init__("Enemy", x, y, font, width, height, color=(255, 0, 0))

    def GetClick(self, texts, font):
        game_state.statestop()
