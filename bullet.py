import pygame
from pygame.locals import *



class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y) -> None:
        super().__init__()

        self.image = pygame.image.load('assets/art/bullet.png')

        self.rect = self.image.get_rect()
        
        self.rect.center = [x, y]
       
    def update(self) -> None:
            self.rect.x += 10
            if self.rect.centerx >= 800:
                self.kill()
            