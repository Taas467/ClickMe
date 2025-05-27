import random
import math
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
    def __init__(self, x, y, font, Width, Height):
        super().__init__(
            "ClickMe", x, y, font, Width, Height, color=(0, 255, 0)
        )  # 設定為綠色

    def GetClick(self, texts, font):
        game_state.betouch()
        random_temp = random.randint(0, 1000)
        if random_temp < 200:
            new_enemy = mSlime(self.rect.x, self.rect.y, font, self.width, self.height)
        else:
            new_enemy = mEnemy(self.rect.x, self.rect.y, font, self.width, self.height)
        while True:
            temp_x = random.randint(0, self.width)
            temp_y = random.randint(0, self.height)
            if (temp_x - self.rect.x) ** 2 + (temp_y - self.rect.y) ** 2 > 10000:
                self.rect.x, self.rect.y = temp_x, temp_y
                self.vy = -10
                break
        texts.append(new_enemy)


class mEnemy(GameRule):
    def __init__(self, x, y, font, Width, Height):
        super().__init__("Enemy", x, y, font, Width, Height, color=(255, 0, 0))

    def GetClick(self, texts, font):
        game_state.statestop()


class mSlime(GameRule):
    def __init__(self, x, y, font, Width, Height):
        super().__init__("Slime", x, y, font, Width, Height, color=(60, 226, 218))

    def GetClick(self, texts, font):
        texts.remove(self)
        val_random = random.randint(0, 100)
        val = 3 if val_random < 10 else 2
        for i in range(0, val):
            random_temp = random.randint(0, 100)
            if random_temp < 38:
                new_enemy = mSli(
                    self.rect.x, self.rect.y, font, self.width, self.height
                )
            else:
                new_enemy = mMe(self.rect.x, self.rect.y, font, self.width, self.height)

            angle = math.radians(random.randint(0, 360))
            speed = random.uniform(3, 6)  # 可以調整速度範圍
            new_enemy.vx = math.cos(angle) * speed
            new_enemy.vy = math.sin(angle) * speed

            texts.append(new_enemy)


class mSli(GameRule):
    def __init__(self, x, y, font, Width, Height):
        super().__init__("Sli", x, y, font, Width, Height, color=(44, 146, 242))

    def GetClick(self, texts, font):
        game_state.statestop()


class mMe(GameRule):
    def __init__(self, x, y, font, Width, Height):
        super().__init__("Me", x, y, font, Width, Height, color=(60, 226, 140))

    def GetClick(self, texts, font):
        game_state.betouch()
        texts.remove(self)
