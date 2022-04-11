import pygame


class ScrollBar:
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

        self.max_value = kwargs.pop("max_value", 10)
        self.start_value = kwargs.pop("start_value", 0)
        self.stop_value = kwargs.pop("stop_value", 0)

    def update_values(self, start, stop, max_values):
        self.start_value = start
        self.stop_value = stop
        self.max_value = max_values

    def draw(self, window, screen_width, screen_height):

        x, y = self.x * screen_width, self.y * screen_height
        width, height = self.width * screen_width, self.height * screen_height
        square_size = height // self.max_value

        surface = pygame.Surface((width, height))
        surface.fill((255, 255, 255))

        match self.coordinate_position:
            case "center":
                self.rect = surface.get_rect(center=(x, y))
            case "topright":
                self.rect = surface.get_rect(topright=(x, y))
            case "topleft":
                self.rect = surface.get_rect(topleft=(x, y))
            case "bottomright":
                self.rect = surface.get_rect(bottomright=(x, y))
            case "bottomleft":
                self.rect = surface.get_rect(bottomleft=(x, y))

        for i in range(self.max_value + 1):
            if i >= self.start_value and i <= self.stop_value:
                pygame.draw.rect(
                    surface, (0, 0, 0), (0, i * square_size, width, square_size)
                )

        update_area = window.blit(surface, self.rect)

        update_area = pygame.draw.rect(
            window,
            self.border_color,
            self.rect,
            self.border_width,
        )

        return update_area
