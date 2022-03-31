from typing import Any

import pygame
import utils
from pygame import Rect, Surface
from ui_components import Button, CheckBox

from .state import App, State


class Groups(State):
    def __init__(self, app: App):
        super().__init__(app)
        self.updated = False

        self.background = None

        self.back_button = Button(
            1 - 0.1 / 10,
            0.1 / 10,
            0.1 / 10 * 8,
            0.1,
            text="Tilbake",
            coordinate_position="topright",
            button_color="#000000",
            text_color="white",
        )

        self.generate_groups_button = Button(
            1 / 8,
            5 / 6,
            4 / 20,
            4 / 25,
            text="LAG GRUPPER!",
            coordinate_position="center",
            button_color="white",
            text_color="black",
            button_border_width=5,
        )

        self.check_box = CheckBox(0.5, 0.5, 0.1, 0.1)

    def update(self, actions, deltatime):
        self.updated = False

        mouse_pos = actions["MousePosition"]

        if actions["MouseMotion"]:
            if self.back_button.check_hover(mouse_pos):
                self.updated = True
            if self.generate_groups_button.check_hover(mouse_pos):
                self.updated = True
            if self.check_box.check_hover(mouse_pos):
                self.updated = True
        if actions["MouseDown"]:
            if self.back_button.is_pressed(mouse_pos):
                self.exit()
            if self.check_box.is_pressed(mouse_pos):
                self.check_box.toggle_state()
                self.updated = True

    def draw(self, window, screen_width, screen_height):
        if not self.updated and not self.should_draw:
            return [None]

        self.should_draw = False

        return [
            window.fill((255, 255, 255)),
            self.back_button.draw(window, screen_width, screen_height),
            self.generate_groups_button.draw(window, screen_width, screen_height),
            self.check_box.draw(window, screen_width, screen_height),
        ]
