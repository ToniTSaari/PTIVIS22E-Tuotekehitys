import pygame
import time
from common import Vector2
from player import Player
from typing import Sequence
from pygame.locals import *



class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y) -> None:

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('assets/art/bullet.png')

        self.rect = self.image.get_rect()
        
        self.rect.center = [x, y]


        
    def prepare_bullet(self, x, y) -> None:
        self.rect.center = [x, y]
       
    def update(self) -> None:
            self.rect.x += 10
            if self.rect.centerx >= 800:
                self.kill()
            