import pygame
from pygame.sprite import Sprite

class ScoreFloat(Sprite):
    """积分飞升：从外星人位置飘到右上角"""
    def __init__(self, ai_game, pos, value):
        super().__init__()
        self.screen   = ai_game.screen
        self.value    = value
        self.font     = pygame.font.SysFont(None, 28)
        self.image    = self.font.render(f"+{value}", True, (250, 250, 0))
        self.rect     = self.image.get_rect(center=pos)
        self.speed_y  = -3
        self.alpha    = 255
        self.fade_sp  = 6

    def update(self):
        self.rect.y += self.speed_y
        self.alpha = max(0, self.alpha - self.fade_sp)
        self.image.set_alpha(self.alpha)
        if self.alpha <= 0 or self.rect.y <= 0:
            self.kill()

    def draw(self, surface=None):
        surface = surface or self.screen
        surface.blit(self.image, self.rect)