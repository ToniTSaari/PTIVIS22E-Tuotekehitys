import pygame

from common import Vector2


class Player:
    def __init__(self) -> None:
        self.sprite = pygame.image.load('assets/art/player.png')

        self.__x = 200
        self.__y = 200

        self.__width = self.sprite.get_width()
        self.__height = self.sprite.get_height()

        self.speed = Vector2(0,0)
        self.speed_multiplier = 1

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
    def pos(self) -> Vector2:
        return Vector2(self.x, self.y)


    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height


    @property
    def left(self) -> float:
        return self.x

    @left.setter
    def left(self, new: float) -> None:
        self.x = new

    @property
    def right(self) -> float:
        return self.x + self.width

    @right.setter
    def right(self, new: float) -> None:
        self.x = new - self.width

    @property
    def top(self) -> float:
        return self.y

    @top.setter
    def top(self, new: float) -> None:
        self.y = new

    @property
    def bottom(self) -> float:
        return self.y + self.height

    @bottom.setter
    def bottom(self, new: float) -> None:
        self.y = new - self.height


    def move(self, speed: Vector2) -> None:
        """Move the player by a given amount in two dimensions."""
        self.__x += speed.x
        self.__y += speed.y
