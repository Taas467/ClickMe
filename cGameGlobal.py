import pygame

class GameState:
    def __init__(self):
        self.state = "playing"
        self.score = 0
        self.anim_warning="stop"
        self.Nuke_now_have=0
        
    def stateplay(self):
        self.state = "playing"

    def statestop(self):
        self.state = "gameover"

    def betouch(self):
        self.score += 1

    def resta_score(self):
        self.score = 0


game_state = GameState()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

Nuke_max_have=1
