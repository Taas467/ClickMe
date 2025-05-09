import pygame


class WavePool:
    def __init__(self, initial_size=10):
        self.pool = [WaveEffect() for _ in range(initial_size)]

    def get_wave(self, x, y):
        for wave in self.pool:
            if not wave.active:
                wave.reset(x, y)
                return wave
        # 若無可用波，新增一個
        new_wave = WaveEffect()
        new_wave.reset(x, y)
        self.pool.append(new_wave)
        return new_wave

    def update_and_draw(self, surface, texts):
        for wave in self.pool:
            if wave.active:
                wave.apply_to(texts)  # ✅ 確保推動只做一次
                wave.update()
                wave.draw(surface)
                if not wave.is_alive():
                    wave.deactivate()


class WaveEffect:
    def __init__(self):
        self.active = False

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.radius = 0
        self.max_radius = 250
        self.alpha = 255
        self.affected = set()
        self.active = True
        self.pushed = False  # ✅ 加入已推動標記

    def update(self):
        if not self.active:
            return
        self.radius += 8
        self.alpha -= 16
        if self.alpha < 0:
            self.alpha = 0

    def draw(self, surface):
        if not self.active or self.alpha <= 0:
            return
        temp_surf = pygame.Surface(
            (self.max_radius * 2, self.max_radius * 2), pygame.SRCALPHA
        )
        pygame.draw.circle(
            temp_surf,
            (255, 255, 255, self.alpha),
            (self.max_radius, self.max_radius),
            self.radius,
            3,
        )
        surface.blit(temp_surf, (self.x - self.max_radius, self.y - self.max_radius))

    def is_alive(self):
        return self.radius < self.max_radius and self.active

    def apply_to(self, text_list):
        if not self.active or self.pushed:
            return
        for text in text_list:
            dx = text.rect.centerx - self.x
            dy = text.rect.centery - self.y
            dist = (dx**2 + dy**2) ** 0.5
            if dist <= 150:
                power = min(max(3, 400 / (dist + 1)), 10)  # ✅ 強化推力
                text.vx += (dx / (dist + 1)) * power
                text.vy += (dy / (dist + 1)) * power
        self.pushed = True  # ✅ 確保只推動一次

    def deactivate(self):
        self.active = False
