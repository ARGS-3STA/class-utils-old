from typing import Any

import pygame
import utils
from pygame import Rect, Surface
from ui_components import Button, CheckBox, NumberField

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
            text="Lag Grupper",
            coordinate_position="center",
            button_color="white",
            text_color="black",
            button_border_width=5,
        )

        self.grupper_check_box = CheckBox(
            1 / 8,
            2.5 / 5,
            2 / 25,
            2 / 25,
            coordinate_position="topright",
            x_offset=-10,
            on_color="grey",
            off_color="white",
            border_width=3,
            hover_color=(220, 220, 220),
        )
        self.students_check_box = CheckBox(
            1 / 8,
            2.5 / 5,
            2 / 25,
            2 / 25,
            coordinate_position="topleft",
            x_offset=10,
            on_color="grey",
            off_color="white",
            border_width=3,
            hover_color=(220, 220, 220),
        )

        self.number_input_field = NumberField(0.5, 0.5, 1 / 8, 1 / 8)

    def update(self, actions, deltatime):
        self.updated = False

        mouse_pos = actions["MousePosition"]

        if actions["MouseMotion"]:
            if self.back_button.check_hover(mouse_pos):
                self.updated = True
            if self.generate_groups_button.check_hover(mouse_pos):
                self.updated = True
            if self.grupper_check_box.check_hover(mouse_pos):
                self.updated = True
            if self.students_check_box.check_hover(mouse_pos):
                self.updated = True
            if self.number_input_field.check_hover(mouse_pos):
                self.updated = True
        if actions["MouseDown"]:
            if self.back_button.is_pressed(mouse_pos):
                self.exit()
            if self.grupper_check_box.is_pressed(mouse_pos):
                self.grupper_check_box.set_state(True)
                self.students_check_box.set_state(False)
                self.updated = True
            elif self.students_check_box.is_pressed(mouse_pos):
                self.students_check_box.set_state(True)
                self.grupper_check_box.set_state(False)
                self.updated = True
            if self.number_input_field.check_buttons(mouse_pos):
                self.updated = True
        if self.number_input_field.check_key_presses(actions["KeysPressed"]):
            self.updated = True

    def draw(self, window, screen_width, screen_height):
        if not self.updated and not self.should_draw:
            return [None]

        self.should_draw = False

        return [
            window.fill((255, 255, 255)),
            self.back_button.draw(window, screen_width, screen_height),
            self.generate_groups_button.draw(window, screen_width, screen_height),
            self.grupper_check_box.draw(window, screen_width, screen_height),
            self.students_check_box.draw(window, screen_width, screen_height),
            self.number_input_field.draw(window, screen_width, screen_height),
        ]
