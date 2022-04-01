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
        self.hover_color = kwargs.pop("hover_color", "grey")

        self.font_type = kwargs.pop("font_type", "bahnschrift")
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
        self.is_selected = False
        self.is_hovered = False

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

        if self.is_hovered:
            pygame.draw.rect(
                surface,
                self.hover_color,
                (0, 0, width, height),
                border_radius=int(screen_width * self.border_radius),
            )

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

    def check_buttons(self, mouse_pos):
        self.is_selected = False

        if self.increase_button.is_pressed(
            mouse_pos, x_offset=self.rect.x, y_offset=self.rect.y
        ):
            if self.value < 99:
                self.value += 1
                return True
        elif self.decrease_button.is_pressed(
            mouse_pos, x_offset=self.rect.x, y_offset=self.rect.y
        ):
            if self.value > 0:
                self.value -= 1
                return True
        elif self.rect.collidepoint(mouse_pos):
            self.is_selected = True
            self.is_hovered = not self.is_hovered
            return True

        return False

    def check_key_presses(self, keys):
        if not self.is_selected:
            return False

        previous_value = self.value

        str_value = str(self.value)

        for key in keys:
            match key:
                case pygame.K_BACKSPACE:
                    str_value = str_value[:-1]
                case pygame.K_ESCAPE:
                    str_value = ""
                case _:
                    key = pygame.key.name(key)
                    if key.isdigit():
                        str_value += key

        self.value = min(int(str_value), 99) if str_value else 0

        return self.value != previous_value

    def check_hover(self, mouse_pos):
        if self.rect is None:
            return False

        changed = False

        if self.increase_button.check_hover(
            mouse_pos, x_offset=self.rect.x, y_offset=self.rect.y
        ):
            changed = True
        if self.decrease_button.check_hover(
            mouse_pos, x_offset=self.rect.x, y_offset=self.rect.y
        ):
            changed = True

        if (
            changed
            or self.increase_button.is_hovered
            or self.decrease_button.is_hovered
        ):
            self.is_hovered = False
            return True

        was_hovered = self.is_hovered
        self.is_hovered = self.rect.collidepoint(mouse_pos)

        return self.is_hovered != was_hovered
