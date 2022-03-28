from typing import Any

from pygame import Surface


class State:
    def __init__(self, app):
        self.app = app

    def update(self, actions: list[Any], deltatime: float) -> None:
        raise NotImplementedError()

    def draw(self, window: Surface) -> None:
        raise NotImplementedError()

    def enter(self) -> None:
        self.app.add_state(self)

    def exit(self) -> None:
        self.app.pop_state()
