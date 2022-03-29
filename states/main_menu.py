from typing import Any

import pygame
import utils
from pygame import Rect, Surface
from ui_components import Button

from .groups_state import Groups
from .state import App, State


class MainMenu(State):
    def __init__(self, app: App):
        super().__init__(app)

        self.updated = False

        self.class_list_button = Button(
            0.5,
            1 / 4,
            1 / 4,
            1 / 10,
            text="Klassekart",
            x_offset=-20,
            coordinate_position="topright",
            button_color="#E66A35",
            button_hover_color="#b81c14",
            text_color="#dbf4e6",
        )

        self.groups_button = Button(
            0.5,
            1 / 4,
            1 / 4,
            1 / 10,
            text="Grupper",
            x_offset=20,
            coordinate_position="topleft",
            button_color="#E66A35",
            button_hover_color="#b81c14",
            text_color="#dbf4e6",
        )

        self.quit_button = Button(
            2 / 4,
            3 / 4,
            1 / 4,
            1 / 10,
            text="Avslutt",
            button_color="#E66A35",
            button_hover_color="#b81c14",
            text_color="#dbf4e6",
        )

        self.gradient_colors = [
            (41, 220, 148),
            (41, 220, 220),
            (41, 140, 180),
            (41, 100, 180),
            (41, 140, 180),
            (41, 220, 220),
            (41, 220, 148),
        ]
        self.gradient = None
        self.gradient_enabled = True
        self.gradient_offset = 0
        self.gradient_width = 0

    def update(self, actions: dict[str, Any], deltatime: float) -> None:
        self.updated = False
        mouse_pos = actions["MousePosition"]

        if actions["MouseDown"]:
            if self.class_list_button.is_pressed(mouse_pos):
                print("Clicked class list button")
            elif self.groups_button.is_pressed(mouse_pos):
                group_state = Groups(self.app)
                group_state.enter()
            elif self.quit_button.is_pressed(mouse_pos):
                self.app.quit()

        if actions["MouseMotion"]:
            mouse_pos = pygame.mouse.get_pos()
            if self.class_list_button.check_hover(mouse_pos):
                self.updated = True
            if self.groups_button.check_hover(mouse_pos):
                self.updated = True
            if self.quit_button.check_hover(mouse_pos):
                self.updated = True

        if self.gradient_enabled and self.gradient is not None:
            self.gradient_offset += 200 * deltatime
            self.app._window.blit(self.gradient, (self.gradient_offset, 0))

            self.app._window.blit(
                self.gradient,
                (
                    -(self.gradient_width * (len(self.gradient_colors) - 1))
                    + self.gradient_offset,
                    0,
                ),
            )

            if self.gradient_offset > (
                self.gradient_width * (len(self.gradient_colors) - 1)
            ):
                self.gradient_offset = 0

    def draw(
        self, window: Surface, screen_width: int, screen_height: int
    ) -> list[Rect | None]:

        if self.should_draw:
            self.gradient, self.gradient_width = utils.create_gradient(
                self.gradient_colors, screen_width, screen_height
            )
            self.should_draw = False

        current_screen_size = (screen_width, screen_height)

        if current_screen_size != self.previous_screen_size:
            text_data = [
                self.class_list_button.get_text_data(screen_width, screen_height),
                self.groups_button.get_text_data(screen_width, screen_height),
                self.quit_button.get_text_data(screen_width, screen_height),
            ]

            font = utils.lowest_font(text_data)
            self.class_list_button.set_font(font)
            self.groups_button.set_font(font)
            self.quit_button.set_font(font)

            self.previous_screen_size = current_screen_size

        return [
            self.class_list_button.draw(window, screen_width, screen_height),
            self.groups_button.draw(window, screen_width, screen_height),
            self.quit_button.draw(window, screen_width, screen_height),
        ]
