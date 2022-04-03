import sys
from typing import Any, Protocol

import pygame
from pygame import Rect, Surface
from pygame.event import Event
from states import MainMenu


class State(Protocol):
    def update(self, actions: dict[str, Any], deltatime: float) -> None:
        raise NotImplementedError()

    def draw(self, window: Surface) -> list[Rect | None]:
        raise NotImplementedError()

    def force_draw(self) -> None:
        raise NotImplementedError()

    def enter(self) -> None:
        raise NotImplementedError()

    def exit(self) -> None:
        raise NotImplementedError()


class App:
    def __init__(
        self, screen_width: int, screen_height: int, title: str, data_loader, **kwargs
    ):
        self._screen_width = screen_width
        self._screen_height = screen_height
        self.data_loader = data_loader

        pygame.init()
        pygame.font.init()

        self._window = pygame.display.set_mode(
            (screen_width, screen_height), pygame.RESIZABLE
        )
        pygame.display.set_caption(title)

        self.actions = {
            "MouseDown": False,
            "MouseUp": False,
            "MouseMotion": False,
            "Resized": False,
            "ShiftHeld": False,
            "ScrolledDown": False,
            "ScrolledUp": False,
            "MousePosition": (0, 0),
            "KeysPressed": [],
        }

        self._state_stack: list[State] = []
        main_menu = MainMenu(self)
        main_menu.enter()

        self._clock = pygame.time.Clock()
        self._fps = kwargs.pop("fps", 60)

    def add_state(self, state: State) -> None:
        self._state_stack.append(state)

    def pop_state(self) -> None:
        self._state_stack.pop()

    def quit(self) -> None:
        pygame.quit()
        sys.exit()

    def resize(self, new_width: int, new_height: int) -> None:
        self._screen_width = new_width
        self._screen_height = new_height

        self._window = pygame.display.set_mode(
            (new_width, new_height), pygame.RESIZABLE
        )

        for state in self._state_stack:
            state.force_draw()

    def reset_actions(self) -> None:
        self.actions = {
            "MouseDown": False,
            "MouseUp": False,
            "MouseMotion": False,
            "Resized": False,
            "ScrolledDown": False,
            "ScrolledUp": False,
            "ShiftHeld": self.actions["ShiftHeld"],
            "MousePosition": (0, 0),
            "KeysPressed": [],
        }

    def run(self) -> None:
        while True:
            if not self._state_stack:
                self.quit()

            current_state = self._state_stack[-1]

            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        self.quit()
                    case pygame.VIDEORESIZE:
                        self.resize(event.w, event.h)
                        self.actions["Resized"] = True
                    case pygame.KEYDOWN if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                        self.actions["ShiftHeld"] = True
                    case pygame.KEYUP if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                        self.actions["ShiftHeld"] = False
                    case pygame.KEYDOWN:
                        self.actions["KeysPressed"].append(event.key)
                    case pygame.MOUSEBUTTONDOWN if event.button == 1:
                        self.actions["MouseDown"] = True
                    case pygame.MOUSEBUTTONUP if event.button == 1:
                        self.actions["MouseUp"] = True
                    case pygame.MOUSEMOTION:
                        self.actions["MouseMotion"] = True
                    case pygame.MOUSEBUTTONDOWN if event.button == 4:
                        self.actions["ScrolledUp"] = True
                    case pygame.MOUSEBUTTONUP if event.button == 5:
                        self.actions["ScrolledDown"] = True

            self.actions["MousePosition"] = pygame.mouse.get_pos()

            deltatime = self._clock.tick(self._fps) / 1000
            current_state.update(self.actions, deltatime)

            self.reset_actions()

            update_area = current_state.draw(
                self._window, self._screen_width, self._screen_height
            )
            pygame.display.update()
