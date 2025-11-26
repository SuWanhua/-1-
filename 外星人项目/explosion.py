import pygame
from pygame.sprite import Sprite

class Explosion(Sprite):
    def __init__(self, ai_game, center):
        super().__init__()
        self.screen      = ai_game.screen
        self.alpha       = 255       
        self.max_scale   = 2.5          
        self.scale_step  = 0.08         
        self.fade_speed  = 8           

        try:
            self.orig_image = pygame.image.load('images/explosion0.bmp')
        except FileNotFoundError:
            self.orig_image = pygame.Surface((60, 60)).convert()
            self.orig_image.fill((255, 220, 0))   

        self.orig_image.set_colorkey((0, 0, 0)) 
        self.image  = self.orig_image.copy()
        self.rect   = self.image.get_rect(center=center)

        self.scale = 1.0

    def update(self):

        self.scale += self.scale_step
        if self.scale >= self.max_scale:
            self.scale = self.max_scale
        w, h = self.orig_image.get_size()
        new_size = int(w * self.scale), int(h * self.scale)
        self.image = pygame.transform.scale(self.orig_image, new_size)
        self.rect  = self.image.get_rect(center=self.rect.center)
        self.alpha = max(0, self.alpha - self.fade_speed)
        self.image.set_alpha(self.alpha)
        if self.alpha <= 0:
            self.kill()

    def draw(self, surface=None):
        surface = surface or self.screen
        surface.blit(self.image, self.rect)