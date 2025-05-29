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
        self.rect.y += self.vy
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

# --------------------------------------------------------
class mClickMe(GameRule):
    def __init__(self, x, y, font, Width, Height):
        super().__init__(
            "ClickMe", x, y, font, Width, Height, color=(0, 255, 0)
        )  # 設定為綠色

    def GetClick(self, texts, font):
        global Nuke_now_have 
        game_state.betouch()
        random_temp = random.randint(0, 1000)
        if random_temp < 60:
            if game_state.Nuke_now_have==0:
                new_enemy = mEnemy(self.rect.x, self.rect.y, font, self.width, self.height)
            else:
                new_enemy = mN_Clear(self.rect.x, self.rect.y, font, self.width, self.height)
                game_state.Nuke_now_have=max(game_state.Nuke_now_have-1,-1)
                
        elif random_temp < 200:
            if game_state.Ghost_now_have==0:
                new_enemy = mSli(self.rect.x, self.rect.y, font, self.width, self.height)
            else:
                new_enemy = mGhost(self.rect.x, self.rect.y, font, self.width, self.height)
                game_state.Ghost_now_have=max(game_state.Ghost_now_have-1,-1)
                
        elif random_temp < 400:
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
            if random_temp > 35:
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
        
class mN_Clear(GameRule):
    def __init__(self, x, y, font, Width, Height):
        self.frame_count = 0  # 用於顏色變化的時間基準
        self.font = font
        self.text = "N-Clear"
        super().__init__(self.text, x, y, font, Width, Height, color=(255, 0, 0))

    def update(self):
        # RGB 動態色彩循環
        self.frame_count += 1
        r = int(127 * math.sin(0.05 * self.frame_count) + 128)
        g = int(127 * math.sin(0.05 * self.frame_count + 2) + 128)
        b = int(127 * math.sin(0.05 * self.frame_count + 4) + 128)
        self.surface = self.font.render(self.text, True, (r, g, b))
        super().update()

    def GetClick(self, texts, font):
        if game_state.anim_warning=="stop":
            game_state.anim_warning="run"
            new_enemy = mAnim_Warning()
            texts.append(new_enemy)
        

        

class mGhost(GameRule):
    def __init__(self, x, y, font, Width, Height):
        super().__init__("Ghost", x, y, font, Width, Height, color=(173, 173, 173))
        self.vx=random.randint(-1, 1)
        self.vy=random.randint(-1, 1)

    def update(self):
        
        self.rect.y += self.vy
        self.rect.x += self.vx
        # 飄動
        target_x, target_y = pygame.mouse.get_pos()
        
        dx = target_x - self.rect.centerx
        dy = target_y - self.rect.centery
        
        distance = math.hypot(dx, dy)  # 計算距離（避免除以 0）
        if distance > 0:
            dx /= distance
            dy /= distance

            add_speed =0.3   # 你可以調整速度
            self.vx =max(-10, min((self.vx+(dx * add_speed)),10))
            self.vy =max(-10, min((self.vy+(dy * add_speed)),10))

        if self.rect.top < 0:
            self.rect.top = 0
            self.vy = -self.vy * 0.9

        # 底部
        if self.rect.bottom >= self.height:
            self.rect.bottom = self.height
            self.vy = -self.vy * 0.9

        # 左右邊界
        if self.rect.left <= 0:
            self.rect.left  =0
            self.vx = -self.vx * 0.9
        
        if self.rect.right >= self.width:
            self.rect.right = self.width
            self.vx = -self.vx * 0.9
    
    def GetClick(self, texts, font):
        game_state.statestop()



class mAnim_Warning:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 320) 
        self.text = "WARNING"
        self.color = (225, 252, 136)
        self.rect_x=width*2
        self.rect_y=height // 2
        self.surface = self.font.render(self.text, True, self.color)
        self.rect = self.surface.get_rect(center=(self.rect_x,  self.rect_y))
       
        self.vx=0
        self.vy=0
        

    def update(self):
        self.rect_x-=20
        self.rect.center = (self.rect_x, self.rect_y)
        self.surface = self.font.render(self.text, True, self.color)
        self.vx=0
        self.vy=0
        if self.rect.left <=-80 and game_state.anim_warning =="run":
            game_state.anim_warning="kill"

    def draw(self, screen):
        if not self.is_done():
            screen.blit(self.surface, self.surface.get_rect(center=(self.rect_x, self.rect_y)))
        else:
            game_state.anim_warning="kill_self"
             

    def is_done(self):
        return self.rect.right<=0
    
    def is_clicked(self, pos):
        return False
    
    def GetClick(self, texts, font):
        pass