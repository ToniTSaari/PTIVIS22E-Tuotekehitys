import pygame

from common import Vector2


class Boss:

    def __init__(self):
        self.sprite = pygame.image.load('assets/art/vihapuu.png')

        self.__width = self.sprite.get_width()
        self.__height = self.sprite.get_height()

        self.__x = 400 - self.__width / 2
        self.__y = 0

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
