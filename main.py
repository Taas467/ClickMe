import sys
import pygame
import random
from cGameObject import *
from cWave import *
from cGameGlobal import *
from cScreen import *

pygame.init()


def restart_game():
    texts.clear()
    texts.append(mClickMe(width // 2, height // 2, shared_font, width, height))
    wave_pool.pool.clear()
    game_state.resta_score()
    game_state.Nuke_now_have = Nuke_max_have
    game_state.Ghost_now_have = Ghost_max_have


shared_font = pygame.font.SysFont(None, 63)

start_screen = StartScreen(width, height)
end_screen = GameoverScreen(width, height)
pygame.display.set_caption("ClickMe!")

start_screen.draw(screen)
pygame.display.flip()
pygame.time.delay(1000)

clock = pygame.time.Clock()
wave_pool = WavePool()
texts = []
restart_game()
game_state.statestart()

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
            end_screen.handle_event(event)

        if game_state.state == "starting":
            start_screen.handle_event(event)

    pygame.display.set_caption(f"ClickMe! - Score: {game_state.score}")

    screen.fill((0, 0, 0))
    wave_pool.update_and_draw(screen, texts)

    if game_state.state == "starting":
        start_screen.update()
        start_screen.draw(screen)
        if start_screen.ready_to_start:
            game_state.stateplay()
            start_screen.ready_to_start = False

    elif game_state.state == "playing":

        for text in texts:
            text.update()
            text.draw(screen)

        if game_state.anim_warning == "kill":
            game_state.anim_warning = "stop"
            texts[:] = [
                obj
                for obj in texts
                if isinstance(obj, mClickMe) or isinstance(obj, mAnim_Warning)
            ]
            game_state.Ghost_now_have = Ghost_max_have

        elif game_state.anim_warning == "kill_self":
            game_state.anim_warning = "stop"
            texts[:] = [obj for obj in texts if not isinstance(obj, mAnim_Warning)]

    elif game_state.state == "gameover":
        end_screen.update()
        end_screen.draw(screen)
        if end_screen.ready_to_start:
            restart_game()
            game_state.stateplay()
            end_screen.ready_to_start = False

    pygame.display.flip()
    clock.tick(60)
