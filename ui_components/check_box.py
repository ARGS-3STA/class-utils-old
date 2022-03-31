import pygame


class CheckBox:
    def __init__(self, x, y, width, height, **kwargs):
        self.x, self.y = x, y
        self.width, self.height = width, height

        self.box_rect = None
        self.is_hovered = False

        self.state = kwargs.pop("state", False)
        self.on_color = kwargs.pop("on_color", (100, 100, 100))

        self.off_color = kwargs.pop("off_color", (255, 0, 0))
        self.hover_color = kwargs.pop("hover_color", (0, 0, 0))

        self.coordinate_position = kwargs.pop("coordinate_position", "center")
        self.x_offset = kwargs.pop("x_offset", 0)

        self.border_width = kwargs.pop("border_width", 0)
        self.border_color = kwargs.pop("border_color", "black")

        self.current_color = None
        self.set_color()

    def set_color(self):
        if self.state:
            self.current_color = self.on_color
        else:
            self.current_color = self.off_color

    def is_pressed(self, mouse_pos):
        if self.box_rect is None:
            return False

        return self.box_rect.collidepoint(mouse_pos)

    def set_state(self, state: bool):
        self.state = state
        self.set_color()

    def check_hover(self, mouse_pos) -> bool:
        if self.box_rect is None:
            return False

        was_hovered = self.is_hovered

        self.is_hovered = self.box_rect.collidepoint(mouse_pos)

        if self.is_hovered == was_hovered:
            return False

        if self.is_hovered:
            self.current_color = self.hover_color
        else:
            self.set_color()

        return True

    def draw(self, window, screen_width, screen_height):
        x, y = self.x * screen_width + self.x_offset, self.y * screen_height
        width, height = self.width * screen_width, self.height * screen_height

        size = min(width, height)

        surface = pygame.Surface((size, size))

        match self.coordinate_position:
            case "center":
                self.box_rect = surface.get_rect(center=(x, y))
            case "topright":
                self.box_rect = surface.get_rect(topright=(x, y))
            case "topleft":
                self.box_rect = surface.get_rect(topleft=(x, y))
            case "bottomright":
                self.box_rect = surface.get_rect(bottomright=(x, y))
            case "bottomleft":
                self.box_rect = surface.get_rect(bottomleft=(x, y))

        surface_rect = surface.get_rect(center=self.box_rect.center)

        surface.fill(self.current_color)

        if self.border_width:
            pygame.draw.rect(
                surface, self.border_color, (0, 0, size, size), self.border_width
            )

        return window.blit(surface, surface_rect)
