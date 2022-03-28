import sys
from typing import Protocol

import pygame
from pygame import Rect, Surface
from pygame.event import Event
from states import MainMenu


class State(Protocol):
    def update(self, events: list[Event], deltatime: float) -> None:
        raise NotImplementedError()

    def draw(self, window: Surface) -> list[Rect | None]:
        raise NotImplementedError()

    def enter(self) -> None:
        raise NotImplementedError()

    def exit(self) -> None:
        raise NotImplementedError()


class App:
    def __init__(self, screen_width: int, screen_height: int, title: str, **kwargs):
        self.screen_width = screen_width
        self.screen_height = screen_height

        pygame.init()
        pygame.font.init()

        self.window = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption(title)

        self.state_stack: list[State] = []
        main_menu = MainMenu(self)
        main_menu.enter()

        self.clock = pygame.time.Clock()
        self.fps = kwargs.pop("fps", 60)

    def add_state(self, state: State) -> None:
        self.state_stack.append(state)

    def pop_state(self) -> None:
        self.state_stack.pop()

    def quit(self) -> None:
        pygame.quit()
        sys.exit()

    def run(self) -> None:
        while True:
            if not self.state_stack:
                self.quit()

            current_state = self.state_stack[-1]

            events = pygame.event.get()
            deltatime = self.clock.tick(self.fps)
            current_state.update(events, deltatime)

            update_area = current_state.draw(self.window)
            pygame.display.update(update_area)
