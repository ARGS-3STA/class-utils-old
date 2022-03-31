import pygame
import utils
from pygame import Rect, Surface
from pygame.font import Font


class Button:
    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        *,
        text: str = "",
        **kwargs
    ):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.text = text

        self.button_rect = None

        self.coordinate_position = kwargs.pop("coordinate_position", "center")

        self.font_type = kwargs.pop("font_type", "bahnschrif")
        self.max_font_size = kwargs.pop("max_font_size", 60)
        self.text_color = kwargs.pop("text_color", "black")
        self.font = None

        self.button_color = kwargs.pop("button_color", "white")
        self.button_hover_color = kwargs.pop("button_hover_color", "grey")
        self.button_border_radius = kwargs.pop("button_border_radius", 0.01)
        self.button_border_width = kwargs.pop("button_border_width", 0)
        self.button_border_color = kwargs.pop("button_border_color", "black")

        self.current_button_color = self.button_color

        self.x_offset = kwargs.pop("x_offset", 0)
        self.y_offset = kwargs.pop("y_offset", 0)

        self.is_hovered = False

    def draw(self, window: Surface, screen_width: int, screen_height: int) -> Rect:
        x, y = (
            self.x * screen_width + self.x_offset,
            self.y * screen_height + self.y_offset,
        )
        width, height = self.width * screen_width, self.height * screen_height

        button_surf = Surface((width, height))

        match self.coordinate_position:
            case "center":
                self.button_rect = button_surf.get_rect(center=(x, y))
            case "topright":
                self.button_rect = button_surf.get_rect(topright=(x, y))
            case "topleft":
                self.button_rect = button_surf.get_rect(topleft=(x, y))
            case "bottomright":
                self.button_rect = button_surf.get_rect(bottomright=(x, y))
            case "bottomleft":
                self.button_rect = button_surf.get_rect(bottomleft=(x, y))

        update_area = pygame.draw.rect(
            window,
            self.current_button_color,
            self.button_rect,
            border_radius=int(screen_width * self.button_border_radius),
        )

        if self.button_border_width > 0:
            pygame.draw.rect(window, self.button_border_color, self.button_rect, self.button_border_width, border_radius=int(screen_width * self.button_border_radius))

        if self.text:
            if self.font is None:
                font = utils.get_dynamic_font(
                    width * 0.9 - self.button_border_width * 2,
                    height * 0.9 - self.button_border_width * 2,
                    self.text,
                    self.font_type,
                    self.max_font_size,
                )
            else:
                font = self.font

            text_surf = font.render(self.text, True, self.text_color)
            text_rect = text_surf.get_rect(center=self.button_rect.center)

            window.blit(text_surf, text_rect)

        return update_area

    def check_hover(self, mouse_pos) -> bool:
        if self.button_rect is None:
            return False

        was_hovered = self.is_hovered

        self.is_hovered = self.button_rect.collidepoint(mouse_pos)

        if self.is_hovered == was_hovered:
            return False

        if self.is_hovered:
            self.current_button_color = self.button_hover_color
        else:
            self.current_button_color = self.button_color

        return True

    def is_pressed(self, mouse_pos) -> bool:
        if self.button_rect is None:
            return False

        return self.button_rect.collidepoint(mouse_pos)

    def set_font(self, font: Font) -> None:
        self.font = font

    def get_text_data(self, screen_width: int, screen_height: int):
        return (
            screen_width * self.width * 0.9,
            screen_height * self.height * 0.9,
            self.text,
            self.font_type,
            self.max_font_size,
        )
