import pygame
import math
from utils import lowest_font


class GroupText:
    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        *,
        text: str = "",
        **kwargs,
    ):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.text = text

        self.rect = None

        self.coordinate_position = kwargs.pop("coordinate_position", "center")

        self.font_type = kwargs.pop("font_type", "bahnschrif")
        self.max_font_size = kwargs.pop("max_font_size", 50)
        self.text_color = kwargs.pop("text_color", "black")
        self.font = None

        self.color = kwargs.pop("color", "white")
        self.border_radius = kwargs.pop("border_radius", 0.01)
        self.border_width = kwargs.pop("border_width", 3)
        self.border_color = kwargs.pop("border_color", "black")
        self.is_transparent = kwargs.pop("is_transparent", False)

        self.max_viewed_elements = kwargs.pop("max_viewed_elements", 14)
        self.start_index = 0
        self.stop_index = self.max_viewed_elements - 1

        self.groups_per_row = kwargs.pop("groups_per_row", 3)

        self.x_offset = kwargs.pop("x_offset", 0)
        self.y_offset = kwargs.pop("y_offset", 0)

        self.has_values = False

        self.update = False

        self.surface = None

        self.groups = []

    def draw(self, window, screen_width, screen_height):

        x, y = self.x * screen_width, self.y * screen_height
        width, height = self.width * screen_width, self.height * screen_height

        if self.update:
            self.surface = pygame.Surface((width, height))

        if self.surface == None:
            self.surface = pygame.Surface((width, height))
            self.surface.fill((255, 255, 255))

        match self.coordinate_position:
            case "center":
                self.rect = self.surface.get_rect(center=(x, y))
            case "topright":
                self.rect = self.surface.get_rect(topright=(x, y))
            case "topleft":
                self.rect = self.surface.get_rect(topleft=(x, y))
            case "bottomright":
                self.rect = self.surface.get_rect(bottomright=(x, y))
            case "bottomleft":
                self.rect = self.surface.get_rect(bottomleft=(x, y))

        if not self.update:
            window.blit(self.surface, self.rect)

            update_area = pygame.draw.rect(
                window,
                self.border_color,
                self.rect,
                self.border_width,
                border_radius=int(screen_width * self.border_radius),
            )
            return update_area
        self.update = False

        self.surface.fill((255, 255, 255))

        if self.groups:
            lines = [""] * (
                len(self.groups)
                * (
                    math.ceil(
                        len(self.groups[0]) / min(len(self.groups), self.groups_per_row)
                    )
                    + 2
                )
            )
            length = len(self.groups[0])
            last_group = 0
            for x, group in enumerate(self.groups):

                index = x % self.groups_per_row

                lines[last_group] += f"gruppe: {x+1}{'|' if not (x%3 == 2) else ''}"
                for y, student in enumerate(group):
                    lines[
                        last_group + y + 1
                    ] += f"{student}{'|' if not (x%3 == 2) else ''}"

                if index == 2:
                    last_group += length + 2

            font = lowest_font(
                [
                    (
                        width * 0.6 - self.border_width * 2,
                        height * 0.6 - self.border_width * 2,
                        i,
                        self.font_type,
                        self.max_font_size,
                    )
                    for i in lines
                ]
            )

            for x, line in enumerate(lines[self.start_index : self.stop_index + 1]):

                for j, word in enumerate(line.split("|")):
                    text_surf = font.render(word, True, self.text_color)
                    # text_rect = text_surf.get_rect(center=self.rect.center)

                    self.surface.blit(
                        text_surf,
                        (
                            20 + j * (width * 0.9 // self.groups_per_row) + j * 20,
                            20 + (x) * height // (self.max_viewed_elements),
                        ),
                    )

        update_area = window.blit(self.surface, self.rect)

        update_area = pygame.draw.rect(
            window,
            self.border_color,
            self.rect,
            self.border_width,
            border_radius=int(screen_width * self.border_radius),
        )

        return update_area

    def scroll_down(self):
        if self.stop_index < (
            len(self.groups)
            * (
                math.ceil(
                    len(self.groups[0]) / min(len(self.groups), self.groups_per_row)
                )
                + 2
            )
        ):
            self.start_index += 1
            self.stop_index += 1
            self.update = True

    def scroll_up(self):
        if self.start_index > 0:
            self.start_index -= 1
            self.stop_index -= 1
            self.update = True

    def update_groups(self, new_groups):
        self.groups = new_groups
        if self.groups:
            self.has_values = True
            self.update = True
