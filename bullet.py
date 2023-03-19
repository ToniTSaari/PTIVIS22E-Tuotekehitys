import pygame

from common import Vector2
import settings
import math

class Bullet(pygame.sprite.Sprite):

    def __init__(self,shootpos: Vector2, position: Vector2, *groups) -> None:
        '''
        Create a bullet at a given position.

        The bullet will be created with its centre at `position`.
        '''
        super().__init__(groups)

       # self.directionvector = direction

        self.image = pygame.image.load('assets/art/bullet.png')

        self.rect = self.image.get_rect()
        
        self.rect.center = position

        distance_x = shootpos.x - self.rect.centerx
        distance_y = shootpos.y - self.rect.centery

        angle = math.atan2(distance_y, distance_x)

        self.speed_x = 10 * math.cos(angle)
        self.speed_y = 10 * math.sin(angle)
       
    def update(self) -> None:
            #self.rect.x += 10
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y

            if self.rect.centerx > 5000 \
            or self.rect.centerx < 0 \
            or self.rect.centery > 5000 \
            or self.rect.centery < 0:
                self.kill()
