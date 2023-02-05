import pygame
from bullet import Bullet
from patterns import Patterns

from common import Vector2


class Boss(pygame.sprite.Sprite):

    def __init__(self, position: Vector2, *groups):
        '''
        Create a boss at a given position.

        The boss will be created with its centre at `position`.
        '''
        super().__init__(groups)


        self.image = pygame.image.load('assets/art/vihapuu.png').convert_alpha()

        self.rect = self.image.get_rect()

        self.__x = position.x - self.rect.width/2
        self.__y = position.y - self.rect.height/2
        self.rect.x = self.__x
        self.rect.y = self.__y

        self.hp = 20

        self.patterns = Patterns()

        self.mask = pygame.mask.from_surface(self.image)
        self._layer = 2

    def update(self) -> None:
        pass

    @property
    def x(self) -> float:
        return self.__x

    @x.setter
    def x(self, new: float) -> None:
        self.__x = new

    @property
    def y(self) -> float:
        return self.__y

    @y.setter
    def y(self, new: float) -> None:
        self.__y = new
        
    @property
    def position(self) -> Vector2:
        return Vector2(self.x, self.y)

    def take_damage(self, amount: int) -> None:
        self.hp = max(self.hp - 1, 0)

    def shoot(self) -> None:
        print(self.patterns.roundpattern())
        
