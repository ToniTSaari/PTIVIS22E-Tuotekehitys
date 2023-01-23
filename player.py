import pygame

class Player:
    def __init__(self) -> None:
        self.sprite = pygame.image.load('assets/art/player.png')
        self.rect = self.sprite.get_rect()
        self.rect.topleft = (200, 200)