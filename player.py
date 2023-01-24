import pygame

from common import Vector2


class Player:
    def __init__(self) -> None:
        self.sprite = pygame.image.load('assets/art/player.png')

        self.rect = self.sprite.get_rect()
        self.rect.topleft = (200, 200)

        self.speed = Vector2(0,0)
        self.speed_multiplier = 1
