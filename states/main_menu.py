import pygame
from pygame import Rect, Surface
from pygame.event import Event
from ui_components import Button

from .state import App, State


class MainMenu(State):
    def __init__(self, app: App):
        super().__init__(app)

        self.updated = False
        self.colors = [(0, 0, 0), (255, 255, 255)]
        self.current_color = 0

        self.class_list_button = Button(
            0.5,
            1 / 4,
            1 / 4,
            1 / 10,
            text="Klassekart",
            x_offset=-10,
            coordinate_position="topright",
        )

        self.groups_button = Button(
            0.5,
            1 / 4,
            1 / 4,
            1 / 10,
            text="Grupper",
            x_offset=10,
            coordinate_position="topleft",
        )

    def update(self, events: list[Event], deltatime: float) -> None:
        self.updated = False

        for event in events:
            match event.type:
                case pygame.QUIT:
                    self.app.quit()
                case pygame.KEYDOWN if event.key == pygame.K_f:
                    self.updated = True
                    self.current_color = (self.current_color + 1) % 2

    def draw(
        self, window: Surface, screen_width: int, screen_height: int
    ) -> list[Rect | None]:
        if not self.updated:
            return [None]

        return [
            window.fill(self.colors[self.current_color]),
            self.class_list_button.draw(window, screen_width, screen_height),
            self.groups_button.draw(window, screen_width, screen_height),
        ]
