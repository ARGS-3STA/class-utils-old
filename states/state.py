from typing import Any, Protocol

from pygame import Rect, Surface
from pygame.event import Event


class App(Protocol):
    def add_state(self, state) -> None:
        raise NotImplementedError()

    def pop_state(self) -> None:
        raise NotImplementedError()

    def quit(self) -> None:
        raise NotImplementedError()

    def resize(self, new_width: int, new_height: int) -> None:
        raise NotImplementedError()


class State:
    def __init__(self, app: App):
        self.app = app
<<<<<<< HEAD
        self.should_update = True
=======
        self.should_draw = True
        self.previous_screen_size = None
>>>>>>> a2dd4f4d17feec5da9b4e771156f9b9d81b1e1b4

    def update(self, actions: dict[Any], deltatime: float) -> None:
        raise NotImplementedError()

    def draw(
        self, window: Surface, screen_width: int, screen_height: int
    ) -> list[Rect | None]:
        raise NotImplementedError()

    def force_draw(self) -> None:
        self.should_draw = True

    def enter(self) -> None:
        self.app.add_state(self)

    def exit(self) -> None:
        self.app.pop_state()
