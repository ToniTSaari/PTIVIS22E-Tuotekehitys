# USED FOR CAMERA TESTING TREE ECT SOME STUFF
import pygame

from common import Vector2


class Object(pygame.sprite.Sprite):

    def __init__(self):
        """
        super().__init__()
        

        super() lets you avoid referring to the base class explicitly,
        which can be nice. But the main advantage comes with multiple
        inheritance, where all sorts of fun stuff can happen. 
        See the standard docs on super if you haven't already.
        
        """
        pygame.sprite.Sprite.__init__(self) 
        self.__x = 10
        self.__y = 10
        self._layer = 2

        self.__width = 32
        self.__height = 32

        self.image = pygame.Surface([self.__width, self.__height])
        self.image.fill((100,200,100))

        # TODO delete if not needed
        self.rect = self.image.get_rect()
        self.rect.x = self.__x
        self.rect.x = self.__y

        self.mask = pygame.mask.from_surface(self.image)

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