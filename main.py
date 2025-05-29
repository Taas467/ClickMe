import sys
import pygame
import random
from cGameObject import *
from cWave import *
from cGameGlobal import *

pygame.init()

def restart_game():
    texts.clear()
    texts.append(
       mClickMe(width // 2, height // 2, shared_font, width, height)
    )
    game_state.state = "playing"
    wave_pool.pool.clear()
    game_state.resta_score()
    game_state.Nuke_now_have=Nuke_max_have
    game_state.Ghost_now_have=Ghost_max_have


shared_font = pygame.font.SysFont(None, 68)

clock = pygame.time.Clock()
wave_pool = WavePool()
texts=[]
restart_game()

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
            
        elif event.type == pygame.KEYDOWN and game_state.state == "gameover":
            if event.key == pygame.K_SPACE:
                restart_game()

    pygame.display.set_caption(f"ClickMe! - Score: {game_state.score}")

    screen.fill((0, 0, 0))
    wave_pool.update_and_draw(screen, texts)

    if game_state.state == "playing":
        
        for text in texts:
            text.update()
            text.draw(screen)
        
        if game_state.anim_warning=="kill":
                game_state.anim_warning="stop"
                texts[:] = [obj for obj in texts if isinstance(obj, mClickMe) or isinstance(obj, mAnim_Warning)]
                game_state.Ghost_now_have=Ghost_max_have

        elif game_state.anim_warning=="kill_self":
            game_state.anim_warning="stop"
            texts[:] = [obj for obj in texts if not isinstance(obj, mAnim_Warning)]
            
            
    elif game_state.state == "gameover":
        g_over_font = pygame.font.SysFont(None, 120)
        gameover_text = g_over_font.render("Game Over", True, (255, 255, 255))
        gameover_rect = gameover_text.get_rect(center=(width // 2, height // 4))
        screen.blit(gameover_text, gameover_rect)

        score_text = shared_font.render(
            f"Your Score: {game_state.score}", True, (255, 255, 255)
        )
        score_rect = score_text.get_rect(center=(width // 2, height // 4 + 80))
        screen.blit(score_text, score_rect)

        small_font = pygame.font.SysFont(None, 36)
        retry_text = small_font.render("Press SPACE to restart", True, (200, 200, 200))
        retry_rect = retry_text.get_rect(center=(width // 2, height // 4 + 200))
        screen.blit(retry_text, retry_rect)

        small_font = pygame.font.SysFont(None, 36)
        retry_text = small_font.render("No modules", True, (200, 200, 200))
        retry_rect = retry_text.get_rect(center=(width // 2, height // 2 + 200))
        screen.blit(retry_text, retry_rect)
        
        
    pygame.display.flip()
    clock.tick(60)
