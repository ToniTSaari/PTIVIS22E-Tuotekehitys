import pygame

from common import Vector2
from enum import Enum


class Player(pygame.sprite.Sprite):

    def __init__(self, position: Vector2, *groups) -> None:
        '''
        Create a player at a given position.

        The player will be created with its centre at `position`.
        '''
        super().__init__(groups)

        self.player_images=[pygame.image.load('assets/art/player_l0.png').convert_alpha(),
                            pygame.image.load('assets/art/player_u0.png').convert_alpha(),
                            pygame.image.load('assets/art/player_r0.png').convert_alpha(),
                            pygame.image.load('assets/art/player_d0.png').convert_alpha()]
        self.image = self.player_images[3]
        self.playerstate = Enum ("State",['A','W','D','S','AW','WD','SD','AS',"STILL"])

        self._layer = 3

        self.__width = self.image.get_width()
        self.__height = self.image.get_height()

        self.__hitbox = pygame.Rect(0,0,32,76)

        # the location of the player sprite's top left corner
        self.__x = position.x - self.__width/2
        self.__y = position.y - self.__height/2

        self.speed = Vector2(0,0)
        self.speed_multiplier = 5

        self.hp = 3

        self.mask = pygame.mask.from_surface(self.image)

        self.default_shot_cooldown = 15
        self.shot_cooldown = 0

    @property
    def x(self) -> float:
        '''The x coordinate of the player's top left corner.'''
        return self.__x

    @x.setter
    def x(self, new: float) -> None:
        self.__x = new

    @property
    def y(self) -> float:
        '''The y coordinate of the player's top left corner.'''
        return self.__y

    @y.setter
    def y(self, new: float) -> None:
        self.__y = new

    @property
    def position(self) -> Vector2:
        '''The coordinates of the centre of the player.'''
        return Vector2(self.x + self.width/2, self.y + self.height/2)

    @property
    def angle(self) -> float:
        return Vector2(1,0).angle_to(self.speed)


    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    @property
    def rect(self) -> pygame.Rect:
        '''
        A Rect that shows where the player sprite is.
        
        This should only be used by Pygame's built-in functions or 
        display-related code.
        '''
        r = self.mask.get_rect()
        (r.left, r.top) = (round(self.x), round(self.y))
        return r

    @property
    def hitbox(self) -> pygame.Rect:
        '''
        The player's hitbox.
        
        Should be used for collision detection with things that
        damage the player.
        '''
        self.__hitbox.center = (self.position.x, self.position.y - 7)
        return self.__hitbox

    # The collider properties have magic numbers that just let the player
    # get close enough to the edges of the map to look natural.
    # This is janky but we can live with it.
    # They're different from the hitbox because they're only used for
    # visual purposes while the hitbox is used for mechanics.
    @property
    def collider_left(self) -> float:
        """The x coordinate of the left side of the player's collider box."""
        return self.x + 84

    @collider_left.setter
    def collider_left(self, new: float) -> None:
        self.x = new - 84

    @property
    def collider_right(self) -> float:
        """The x coordinate of the right side of the player's collider box."""
        return self.x + self.width - 84

    @collider_right.setter
    def collider_right(self, new: float) -> None:
        self.x = new - self.width + 84

    @property
    def collider_top(self) -> float:
        """The y coordinate of the top of the player's collider box."""
        return self.y - 6

    @collider_top.setter
    def collider_top(self, new: float) -> None:
        self.y = new - 6

    @property
    def collider_bottom(self) -> float:
        """The y coordinate of the bottom of the player's collider box."""
        return self.y + self.height

    @collider_bottom.setter
    def collider_bottom(self, new: float) -> None:
        self.y = new - self.height

    def take_damage(self, amount: int) -> None:
        self.hp = max(self.hp - 1, 0)

    def update(self) -> None:
        self.move(self.speed)
        self.__tick_shot_cooldown()
    
    def move(self, speed: Vector2) -> None:
        """Move the player by a given amount in two dimensions."""
        self.__x += speed.x
        self.__y += speed.y
        self.setmovestate(self.angle)

    def __tick_shot_cooldown(self) -> None:
        if self.shot_cooldown > 0:
            self.shot_cooldown -= 1

    def can_shoot(self) -> bool:
        return self.shot_cooldown == 0

    def setmovestate(self,angle: float,)-> None:
        if self.speed == [0,0]:
            self.playerstate=8
        elif -157.5 >= angle or 157.5 <= angle <= 180:
            self.playerstate=0
        elif -112.5 <= angle <= -67.5:
            self.playerstate=1
        elif -22.5 <= angle <=0 or 0 < angle <= 22.5:
            self.playerstate=2
        elif 67.5 <= angle <= 112.5:
            self.playerstate=3
        elif -157.5 < angle < -112.5:
            self.playerstate=4
        elif -67.5 < angle < -22.5:
            self.playerstate=5
        elif 22.5 < angle < 67.5:
            self.playerstate=6
        elif 112.5 < angle < 157.5:
            self.playerstate=7

        match self.playerstate:
            case 0:
                self.image = self.player_images[0]
            case 1:
                self.image = self.player_images[1]
            case 2:
                self.image = self.player_images[2]
            case 3:
                self.image = self.player_images[3]
            case 4:
                self.image = self.player_images[0]
            case 5:
                self.image = self.player_images[1]
            case 6:
                self.image = self.player_images[2]
            case 7:
                self.image = self.player_images[3]
            case 8:
                self.image = self.player_images[3]

        

    

        


