from typing import Any

import pygame
from algorithm import DataLoader, GroupMaker
from pygame import Rect, Surface
from ui_components import (
    Button,
    CheckBox,
    DropDown,
    NumberField,
    TextField,
    GroupText,
    ScrollBar,
)
from utils import *

from .state import App, State


class Groups(State):
    def __init__(self, app: App):
        super().__init__(app)
        self.updated = False

        self.background = None

        self.group_maker = GroupMaker(app.data_loader)

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
            5 / 6 - 1 / 8,
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
            2.5 / 5 - 1 / 8,
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
            2.5 / 5 - 1 / 8,
            2 / 25,
            2 / 25,
            coordinate_position="topleft",
            x_offset=10,
            on_color="grey",
            off_color="white",
            border_width=3,
            hover_color=(220, 220, 220),
            state=True,
        )

        self.number_input_field = NumberField(1 / 8, 4 / 6 - 1 / 8, 1 / 8, 1 / 8)

        self.method_text_field = TextField(
            1 / 8, 2 / 4 - 1 / 16 - 1 / 8, 0.2, 0.1, text="Grupperingsmetode"
        )
        self.student_text_field = TextField(
            1 / 8 - 1 / 25,
            2 / 4 - 1 / 30 - 1 / 8,
            2 / 25,
            0.05,
            text="Antall grupper",
        )
        self.groups_text_field = TextField(
            1 / 8 + 1 / 25, 2 / 4 - 1 / 30 - 1 / 8, 2 / 25, 0.05, text="Antall personer"
        )

        self.drop_down_menu = DropDown(
            1 / 8,
            2 / 6 - 1 / 8,
            1 / 5,
            0.1,
            self.app,
            text="Velg Klasseliste",
            last_element_text="Legg til klasseliste +",
        )

        self.group_display = GroupText(
            4 / 8 + 1 / 16, 0.5, 0.5, 0.9, max_viewed_elements=20
        )

        self.scroll_bar = ScrollBar(
            3 / 8 + 0.5 - 0.048, 0.5, 0.025, 0.9
        )  # 0.002 % spacing

    def update(self, actions, deltatime):
        self.updated = False

        mouse_pos = actions["MousePosition"]

        if actions["Resized"]:
            self.group_display.update = True
            self.group_display.new_groups = True

        if actions["MouseMotion"]:
            if self.back_button.check_hover(mouse_pos):
                self.updated = True
            if self.drop_down_menu.check_hover(mouse_pos):
                self.updated = True

            if not self.drop_down_menu.is_expanded:
                if self.generate_groups_button.check_hover(mouse_pos):
                    self.updated = True
                if self.grupper_check_box.check_hover(mouse_pos):
                    self.updated = True
                if self.students_check_box.check_hover(mouse_pos):
                    self.updated = True
                if self.number_input_field.check_hover(mouse_pos):
                    self.updated = True
            else:
                if self.drop_down_menu.check_button_hovers(mouse_pos):
                    self.updated = True

        if actions["MouseDown"]:
            self.updated = True
            if self.back_button.is_pressed(mouse_pos):
                self.exit()

            if not self.drop_down_menu.is_expanded:
                if self.grupper_check_box.is_pressed(mouse_pos):
                    self.grupper_check_box.set_state(True)
                    self.students_check_box.set_state(False)
                elif self.students_check_box.is_pressed(mouse_pos):
                    self.students_check_box.set_state(True)
                    self.grupper_check_box.set_state(False)

                elif self.generate_groups_button.is_pressed(mouse_pos):
                    if self.students_check_box.state:
                        groups = self.group_maker.groups_from_students_per_group(
                            self.drop_down_menu.text,
                            self.number_input_field.value,
                            [],
                        )
                    else:
                        groups = self.group_maker.groups_from_amounts_of_groups(
                            self.drop_down_menu.text,
                            self.number_input_field.value,
                            [],
                        )
                    self.group_display.update_groups(groups)

                if self.number_input_field.check_buttons(mouse_pos):
                    pass

            else:
                if self.drop_down_menu.check_buttons(mouse_pos):
                    print("add klasseliste")

            self.drop_down_menu.check_press(mouse_pos)

        if self.drop_down_menu.is_expanded:
            if actions["ScrolledDown"]:
                self.drop_down_menu.scroll_down()
                self.updated = True
            if actions["ScrolledUp"]:
                self.drop_down_menu.scroll_up()
                self.updated = True

        if self.group_display.has_values:
            if actions["ScrolledDown"]:
                if self.group_display.scroll_down():
                    self.scroll_bar.update_values(
                        self.group_display.start_index,
                        self.group_display.stop_index,
                        len(self.group_display.text_surfaces),
                    )
                self.updated = True
            if actions["ScrolledUp"]:
                if self.group_display.scroll_up():
                    self.scroll_bar.update_values(
                        self.group_display.start_index,
                        self.group_display.stop_index,
                        len(self.group_display.text_surfaces),
                    )
                self.updated = True

        if not self.drop_down_menu.is_expanded:
            if self.number_input_field.check_key_presses(actions["KeysPressed"]):
                self.updated = True

        if self.group_display.update_scroll_bar:
            self.scroll_bar.update_values(
                self.group_display.start_index,
                self.group_display.stop_index,
                len(self.group_display.text_surfaces),
            )
            self.updated = True

    def draw(self, window, screen_width, screen_height):
        if not self.updated and not self.should_draw:
            return [None]

        self.should_draw = False

        window.fill((255, 255, 255))

        if not self.drop_down_menu.is_expanded:
            self.generate_groups_button.draw(window, screen_width, screen_height),
            self.grupper_check_box.draw(window, screen_width, screen_height),
            self.students_check_box.draw(window, screen_width, screen_height),
            self.number_input_field.draw(window, screen_width, screen_height),
            self.method_text_field.draw(window, screen_width, screen_height),
            self.student_text_field.draw(window, screen_width, screen_height),
            self.groups_text_field.draw(window, screen_width, screen_height),

        return [
            self.back_button.draw(window, screen_width, screen_height),
            self.drop_down_menu.draw(window, screen_width, screen_height),
            self.group_display.draw(window, screen_width, screen_height),
            self.scroll_bar.draw(window, screen_width, screen_height),
        ]
