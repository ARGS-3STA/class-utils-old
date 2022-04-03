import pygame
import utils

from .button import Button
from .text_field import TextField


class DropDown:
    def __init__(self, x, y, width, height, app, **kwargs):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.app = app

        self.coordinate_position = kwargs.pop("coordinate_position", "center")
        self.border_radius = kwargs.pop("border_radius", 0.01)
        self.border_width = kwargs.pop("border_width", 3)

        self.color = kwargs.pop("color", (0, 0, 0))
        self.hover_color = kwargs.pop("hover_color", "grey")

        self.font_type = kwargs.pop("font_type", "bahnschrif")
        self.max_font_size = kwargs.pop("max_font_size", 60)
        self.text_color = kwargs.pop("text_color", "black")

        self.text = kwargs.pop("text", "None")

        self.last_element_text: str = kwargs.pop("last_element_text", "")

        self.element_stack = list(self.app.data_loader.get_class_list_names()) + [
            self.last_element_text
        ]
        self.max_viewed_elements = kwargs.pop("max_viewed_elements", 4)
        self.start_index = 0
        self.stop_index = self.max_viewed_elements - 1
        self.buttons = [
            Button(
                self.x,
                self.y + self.height * (i + 1),
                self.width,
                self.height,
                button_border_width=3,
                button_border_color="black",
                button_color="white",
            )
            for i in range(self.max_viewed_elements)
        ]

        self.font = None
        self.rect = None

        self.is_hovered = False
        self.is_expanded = True

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
                height * 0.8 - self.border_width * 2,
                self.text,
                self.font_type,
                self.max_font_size,
            )
        else:
            font = self.font

        text_surf = font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(
            center=pygame.Rect(
                self.rect.x, self.rect.y, self.rect.width, self.rect.height
            ).center
        )

        window.blit(text_surf, text_rect)

        if self.is_expanded:
            idx = 0
            for name in self.element_stack[self.start_index : self.stop_index + 1]:
                self.buttons[idx].text = name
                self.buttons[idx].draw(window, screen_width, screen_height)
                idx += 1

        return update_area

    def check_buttons(self, mouse_pos):
        for button in self.buttons:
            if button.is_pressed(mouse_pos):
                text = button.text

                if text == self.last_element_text:
                    return True
                else:
                    self.text = text
        return False

    def check_button_hovers(self, mouse_pos):
        changed = False
        for button in self.buttons:
            if button.check_hover(mouse_pos):
                changed = True

        return changed

    def check_press(self, mouse_pos) -> bool:
        if self.rect is None:
            return False

        if self.rect.collidepoint(mouse_pos):
            self.is_expanded = not self.is_expanded
            return True

        self.is_expanded = False
        return False

    def check_hover(self, mouse_pos):
        if self.rect is None:
            return False

        was_hovered = self.is_hovered
        self.is_hovered = self.rect.collidepoint(mouse_pos)

        return self.is_hovered != was_hovered

    def scroll_down(self):
        if self.stop_index < len(self.element_stack) - 1:
            self.start_index += 1
            self.stop_index += 1

    def scroll_up(self):
        if self.start_index > 0:
            self.start_index -= 1
            self.stop_index -= 1
