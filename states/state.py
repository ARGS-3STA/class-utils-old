from typing import Protocol

from pygame import Surface
from pygame.event import Event


class App(Protocol):
    def add_state(self, state) -> None:
        raise NotImplementedError()

    def pop_state(self) -> None:
        raise NotImplementedError()

    def quit(self) -> None:
        raise NotImplementedError()


class State:
    def __init__(self, app: App):
        self.app = app

    def update(self, events: list[Event], deltatime: float) -> None:
        raise NotImplementedError()

    def draw(self, window: Surface) -> None:
        raise NotImplementedError()

    def enter(self) -> None:
        self.app.add_state(self)

    def exit(self) -> None:
        self.app.pop_state()
