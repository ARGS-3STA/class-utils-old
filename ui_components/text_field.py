import pygame
import utils


class TextField:
    def __init__(self, x, y, width, height, **kwargs):
        self.x, self.y = x, y
        self.width, self.height = width, height

        self.coordinate_position = kwargs.pop("coordinate_position", "center")

        self.font_type = kwargs.pop("font_type", "bahnschrif")
        self.max_font_size = kwargs.pop("max_font_size", 60)
        self.text_color = kwargs.pop("text_color", "black")

        self.text = kwargs.pop("text", "None")

        self.font = None
        self.rect = None

    def draw(self, window, screen_width, screen_height):
        x, y = (
            self.x * screen_width,
            self.y * screen_height,
        )
        width, height = self.width * screen_width, self.height * screen_height

        text_surf = pygame.Surface((width, height))

        match self.coordinate_position:
            case "center":
                self.rect = text_surf.get_rect(center=(x, y))
            case "topright":
                self.rect = text_surf.get_rect(topright=(x, y))
            case "topleft":
                self.rect = text_surf.get_rect(topleft=(x, y))
            case "bottomright":
                self.rect = text_surf.get_rect(bottomright=(x, y))
            case "bottomleft":
                self.rect = text_surf.get_rect(bottomleft=(x, y))

        if self.font is None:
            font = utils.get_dynamic_font(
                width * 0.9,
                height * 0.9,
                self.text,
                self.font_type,
                self.max_font_size,
            )
        else:
            font = self.font

        text_surf = font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)

        update_area = window.blit(text_surf, text_rect)
