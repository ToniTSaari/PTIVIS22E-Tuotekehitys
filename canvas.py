import pygame
from pygame import Color, Rect, Surface
from pygame.sprite import Sprite, Group

import settings


class Canvas:
    """
    A canvas to draw things on before drawing them on the screen.
    
    `draw()`: Draw sprites onto the canvas.

    `camera_view()`: Return the part of the canvas to be drawn on the screen.
    """

    def __init__(
        self,
        dimensions: tuple[int, int],
        background: Surface | Color,
        camera: Sprite
    ) -> None:
        """
        `dimensions`: The size of the canvas in pixels.

        `background`: The image or color to use as the background of the canvas.
        Will be used to reset the canvas on every draw. Can be a pygame Surface
        or Color or any value that can be used to construct a Color.

        `camera`: The game object the screen should follow.
        """
        self.__canvas = Surface(dimensions)

        if isinstance(background, Surface):
            self.__background_color = None
            self.__background_image = background
            self.__canvas = self.__background_image.copy()
        else:
            self.__background_color = Color(background)
            self.__background_image = None
            self.__canvas.fill(self.__background_color)

        self.__camera = camera

    @property
    def inner(self) -> Surface:
        """The surface representing the canvas."""
        return self.__canvas

    def draw(
        self,
        sprites: Group,
        reset: bool = True
    ) -> None:
        """
        Draw all sprites in a given group onto the canvas.
        
        `sprites`: A list of sprites to draw. Must implement a `draw()` method
        similar to `pygame.Group.draw()`.

        `reset`: Whether the canvas should be reset to its default background.
        Should be `True` on the first `draw()` of every frame.
        """
        if reset:
            self.__reset()
        sprites.draw(self.__canvas)

    def __reset(self) -> None:
        """Reset the canvas to its default background image or color."""
        if self.__background_image is not None:
            self.__canvas = self.__background_image.copy()
        else:
            self.__canvas.fill(self.__background_color)

    def camera_view(self) -> Surface:
        """
        Get the portion of the canvas that should be drawn on the screen.
        
        Returns a Rect matching the size of the screen, centered on the camera
        given in the constructor of the canvas.
        """
        view_width = settings.display["width"]
        view_height = settings.display["height"]

        view_rect = Rect(0, 0, view_width, view_height)
        view_rect.center = self.__camera.rect.center

        return view_rect


def from_image(
    image: Surface,
    camera: Sprite
) -> Canvas:
    """
    Create a canvas from an image.
    
    `image`: Defines the size and background image of the canvas.
    
    `camera`: The game object the screen should follow.
    """
    dimensions = (image.get_width(), image.get_height())
    return Canvas(dimensions, image, camera)
