import pygame

from common import Vector2
import settings


class Bullet(pygame.sprite.Sprite):

    def __init__(self, position: Vector2, *groups) -> None:
        '''
        Create a bullet at a given position.

        The bullet will be created with its centre at `position`.
        '''
        super().__init__(groups)

        self.image = pygame.image.load('assets/art/bullet.png')

        self.rect = self.image.get_rect()
        
        self.rect.center = position
       
    def update(self) -> None:
            self.rect.x += 10
            if self.rect.centerx >= settings.display["width"]:
                self.kill()
            