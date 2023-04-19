import pygame
from random import randint
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

        self.__rect = self.image.get_rect()

        self.__x = position.x - self.__rect.width/2
        self.__y = position.y - self.__rect.height/2

        self.max_hp = 20
        self.hp = self.max_hp

        # for having the boss move around
        self.original_position = position
        self.wander_range = 150
        self.wandering = False

        self.speed = Vector2(0,0)
        self.speed_multiplier = 2

        self.patterns = Patterns()
        self.mask = pygame.mask.from_surface(self.image)
        self._layer = 2

        self.default_shot_cooldown = 40
        self.shot_cooldown = 120

    def update(self) -> None:
        self.__tick_attack_cooldown()
        self.__wander()
    
    def __wander(self) -> None:
        if self.wandering:
            self.__x += self.speed.x
            self.__y += self.speed.y
            if self.position.distance_to(self.target) < 10:
                self.wandering = False
        else:
            target_offset = Vector2(
                randint(-self.wander_range, self.wander_range),
                randint(-self.wander_range, self.wander_range)
            )
            self.target = self.original_position + target_offset
            self.speed = self.target - self.position
            self.speed.scale_to_length(self.speed_multiplier)
            self.wandering = True

    @property
    def rect(self) -> pygame.Rect:
        self.__rect.center = self.position
        return self.__rect

    def __tick_attack_cooldown(self) -> None:
        if self.shot_cooldown > 0:
            self.shot_cooldown -= 1
        else:
            self.shot_cooldown = self.default_shot_cooldown

    def can_shoot(self) -> bool:
        return self.shot_cooldown == 0

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
        '''The coordinates of the centre of the boss.'''
        return Vector2(self.x + self.__rect.width/2, self.y + self.__rect.height/2)

    def take_damage(self, amount: int) -> None:
        self.hp = max(self.hp - 1, 0)

    def shoot(self) -> None:
        print(self.patterns.roundpattern())

