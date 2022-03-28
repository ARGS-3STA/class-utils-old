import pygame
from pygame import Rect, Surface
from pygame.event import Event

from .state import App, State


class MainMenu(State):
    def __init__(self, app: App):
        super().__init__(app)

        self.updated = False
        self.colors = [(0, 0, 0), (255, 255, 255)]
        self.current_color = 0

    def update(self, events: list[Event], deltatime: float) -> None:
        self.updated = False

        for event in events:
            match event.type:
                case pygame.QUIT:
                    self.app.quit()
                case pygame.KEYDOWN if event.key == pygame.K_f:
                    self.updated = True
                    self.current_color = (self.current_color + 1) % 2

    def draw(self, window: Surface) -> list[Rect | None]:
        if not self.updated:
            return [None]

        return [window.fill(self.colors[self.current_color])]
