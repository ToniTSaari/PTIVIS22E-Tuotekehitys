from pygame.locals import *
from typing import Sequence

from common import Vector2


def movement_direction(pressed_keys: Sequence[bool]) -> Vector2:
    direction = Vector2(0,0)
    
    if pressed_keys[K_w]:
        direction.y -= 1
    if pressed_keys[K_s]:
        direction.y += 1
    if pressed_keys[K_d]:
        direction.x += 1
    if pressed_keys[K_a]:
        direction.x -= 1


    if direction.length() != 0:
        direction.normalize_ip()
        
    return direction
