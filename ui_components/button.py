import pygame
from pygame import Surface


class Button:
    def __init__(
        self, x: int, y: int, width: int, height: int, *, text: str = "", **kwargs
    ):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.text = text

        self.coordinate_position = kwargs.get("coordinate_position", "center")

    def draw(self, window: Surface, screen_width: int, screen_height: int) -> None:
        x, y = self.x * screen_width, self.y * screen_height
        width, height = self.width * screen_width, self.height * screen_height

        match self.coordinate_position:
            case "center":
                pass
