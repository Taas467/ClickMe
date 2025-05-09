import sys
import pygame
import random
from cGameObject import *
from cWave import *

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("CLickMe!")
shared_font = pygame.font.SysFont(None, 60)

clock = pygame.time.Clock()

# 🔹 一開始只有一個文字
texts = [mClickMe(width // 2, height // 2, shared_font, width, height)]
click_me_text = texts[0]
wave_pool = WavePool()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for text in reversed(texts):
                if text.is_clicked(mouse_pos):
                    text.GetClick(texts, shared_font)
                    break
            wave_pool.get_wave(mouse_pos[0], mouse_pos[1])

    screen.fill((0, 0, 0))
    wave_pool.update_and_draw(screen, texts)

    for text in texts:
        text.update()
        text.draw(screen)

    pygame.display.flip()
    clock.tick(60)
