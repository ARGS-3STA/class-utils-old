import pygame

class TextField:
    def __init__(self, x, y, width, height, **kwargs):
        self.x, self.y = x,y
        self.width, self.height = width, height

        self.coordinate_position = kwargs.pop("coordinate_position", "center")

        self.font_type = kwargs.pop("font_type", "bahnschrif")
        self.max_font_size = kwargs.pop("max_font_size", 60)
        self.text_color = kwargs.pop("text_color", "black")

        self.font = None
        self.rect = None