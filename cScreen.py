import pygame
from cGameGlobal import *


class StartScreen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font_100 = pygame.font.SysFont(None, 100)
        self.font_40 = pygame.font.SysFont(None, 40)

        self.title_text = self.font_100.render("ClickMe!", True, (0, 255, 0))
        self.prompt_text = self.font_40.render(
            "Press SPACE to start the game", True, (200, 200, 200)
        )

        self.title_rect = self.title_text.get_rect(center=(width // 2, height // 3))
        self.prompt_rect = self.prompt_text.get_rect(center=(width // 2, height // 1.5))

        self.ready_to_start = False  # 狀態旗標，供 main 判斷是否開始遊戲

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.ready_to_start = True

    def update(self):
        pass  # 可加上閃爍提示文字或其他效果

    def draw(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.title_text, self.title_rect)
        screen.blit(self.prompt_text, self.prompt_rect)


class GameoverScreen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font_40 = pygame.font.SysFont(None, 40)
        self.font_60 = pygame.font.SysFont(None, 60)
        self.font_120 = pygame.font.SysFont(None, 120)
        self.ready_to_start = False

        self.gameover_text = self.font_120.render("Game Over", True, (255, 255, 255))
        self.gameover_rect = self.gameover_text.get_rect(
            center=(width // 2, height // 4)
        )

        self.retry_text = self.font_40.render(
            "Press SPACE to restart", True, (200, 200, 200)
        )
        self.retry_rect = self.retry_text.get_rect(
            center=(width // 2, height // 4 + 200)
        )

        self.mod_text = self.font_40.render("No modules", True, (200, 200, 200))
        self.mod_rect = self.mod_text.get_rect(center=(width // 2, height // 2 + 200))

        self.ready_to_start = False  # 狀態旗標，供 main 判斷是否開始遊戲

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.ready_to_start = True

    def update(self):
        self.score_text = self.font_60.render(
            f"Your Score: {game_state.score}", True, (255, 255, 255)
        )
        self.score_rect = self.score_text.get_rect(
            center=(width // 2, height // 4 + 80)
        )

    def draw(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.gameover_text, self.gameover_rect)
        screen.blit(self.retry_text, self.retry_rect)
        screen.blit(self.mod_text, self.mod_rect)
        screen.blit(self.score_text, self.score_rect)
