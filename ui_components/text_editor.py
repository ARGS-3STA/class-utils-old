import pygame
import math
from utils import lowest_font
from .scroll_bar import ScrollBar


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
        self.new_groups = False

        self.update = False
        self.update_scroll_bar = False

        self.surface = None

        self.groups = []
        self.text_surfaces = []

    def draw(self, window, screen_width, screen_height):

        x, y = self.x * screen_width, self.y * screen_height
        width, height = self.width * screen_width, self.height * screen_height

        self.update_scroll_bar = False

        if self.update:
            self.surface = pygame.Surface((width, height))

        if self.surface == None:
            self.surface = pygame.Surface((width, height))
            self.surface.fill((255, 255, 255))

        if self.new_groups:
            self.new_groups = False
            self.text_surfaces = []
            self.create_text_surfaces(screen_width, screen_height)
            self.update_scroll_bar = True

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
            for x, line in enumerate(
                self.text_surfaces[self.start_index : self.stop_index + 1]
            ):
                for j, text_surf in enumerate(line):
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
        if self.stop_index < math.ceil(len(self.groups) / self.groups_per_row) * len(
            self.groups[0]
        ) + 3 * math.ceil(len(self.groups) / self.groups_per_row):
            self.start_index += 1
            self.stop_index += 1
            self.update = True
            return True
        return False

    def scroll_up(self):
        if self.start_index > 0:
            self.start_index -= 1
            self.stop_index -= 1
            self.update = True
            return True
        return False

    def number_of_students(self, groups):
        ret_val = 0
        for group in groups:
            ret_val += len(group)
        return ret_val

    def create_text_surfaces(self, screen_width, screen_height):
        width, height = self.width * screen_width, self.height * screen_height
        if not self.groups:
            return

        length = len(self.groups[0])
        lines = [""] * (
            (
                math.ceil(len(self.groups) / self.groups_per_row) * length
                + 3 * math.ceil(len(self.groups) / self.groups_per_row)
            )
        )
        print(len(lines))
        last_group = 0
        for x, group in enumerate(self.groups):

            index = x % self.groups_per_row

            lines[last_group] += f"Gruppe {x+1}:{'|' if not (x%3 == 2) else ''}"
            for y, student in enumerate(group):
                lines[last_group + y + 1] += f"{student}{'|' if not (x%3 == 2) else ''}"

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

        for x, line in enumerate(lines):
            self.text_surfaces.append([])
            for word in line.split("|"):
                text_surf = font.render(word, True, self.text_color)

                self.text_surfaces[x].append(text_surf)

    def update_groups(self, new_groups):
        self.groups = new_groups
        if self.groups:
            self.has_values = True
            self.update = True
            self.new_groups = True
            self.start_index = 0
            self.stop_index = self.max_viewed_elements - 1
            return True
        return False
