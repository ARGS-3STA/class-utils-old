import pygame
import utils

from .button import Button


class NumberField:
    def __init__(self, x, y, width, height, **kwargs):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.font = None

        self.value = kwargs.pop("value", 0)
        self.color = kwargs.pop("color", (0, 0, 0))

        self.font_type = kwargs.pop("font_type", "bahnschrif")
        self.max_font_size = kwargs.pop("max_font_size", 60)
        self.text_color = kwargs.pop("text_color", (0, 0, 0))

        self.coordinate_position = kwargs.pop("coordinate_position", "center")
        self.border_radius = kwargs.pop("border_radius", 0.01)
        self.border_width = kwargs.pop("border_width", 3)

        self.increase_button = Button(
            0.8,
            0.32,
            0.2,
            0.3,
            text="^",
            coordinate_position="center",
            button_color="white",
            text_color="black",
            button_border_width=3,
        )

        self.decrease_button = Button(
            0.8,
            0.63,
            0.2,
            0.3,
            text="v",
            coordinate_position="center",
            button_color="white",
            text_color="black",
            button_border_width=3,
        )

        self.rect = None

    def draw(self, window, screen_width, screen_height):
        x, y = self.x * screen_width, self.y * screen_height
        width, height = self.width * screen_width, self.height * screen_height

        surface = pygame.Surface((width, height))
        surface.fill((255, 255, 255))

        match self.coordinate_position:
            case "center":
                self.rect = surface.get_rect(center=(x, y))
            case "topright":
                self.rect = surface.get_rect(topright=(x, y))
            case "topleft":
                self.rect = surface.get_rect(topleft=(x, y))
            case "bottomright":
                self.rect = surface.get_rect(bottomright=(x, y))
            case "bottomleft":
                self.rect = surface.get_rect(bottomleft=(x, y))

        self.decrease_button.draw(surface, width, height)
        self.increase_button.draw(surface, width, height)

        update_area = window.blit(surface, self.rect)

        update_area = pygame.draw.rect(
            window,
            self.color,
            self.rect,
            self.border_width,
            border_radius=int(screen_width * self.border_radius),
        )

        if self.font is None:
            font = utils.get_dynamic_font(
                width * 0.8 - self.border_width * 2,
                height * 0.6 - self.border_width * 2,
                str(self.value),
                self.font_type,
                self.max_font_size,
            )
        else:
            font = self.font

        text_surf = font.render(str(self.value), True, self.text_color)
        text_rect = text_surf.get_rect(
            center=pygame.Rect(
                self.rect.x, self.rect.y, self.rect.width * 0.8, self.rect.height
            ).center
        )

        window.blit(text_surf, text_rect)

        return update_area
