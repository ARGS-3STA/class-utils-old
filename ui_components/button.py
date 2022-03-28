import utils
from pygame import Rect, Surface


class Button:
    def __init__(
        self, x: int, y: int, width: int, height: int, *, text: str = "", **kwargs
    ):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.text = text

        self.coordinate_position = kwargs.get("coordinate_position", "center")
        self.font_type = kwargs.get("font_type", "Microsoft Sans Serif")
        self.max_font_size = kwargs.get("max_font_size", 60)
        self.text_color = kwargs.get("text_color", "black")
        self.button_color = kwargs.get("button_color", "white")

    def draw(self, window: Surface, screen_width: int, screen_height: int) -> Rect:
        x, y = self.x * screen_width, self.y * screen_height
        width, height = self.width * screen_width, self.height * screen_height

        button_surf = Surface((width, height))
        button_surf.fill(self.button_color)

        match self.coordinate_position:
            case "center":
                button_rect = button_surf.get_rect(center=(x, y))
            case "topright":
                button_rect = button_surf.get_rect(topright=(x, y))
            case "topleft":
                button_rect = button_surf.get_rect(topleft=(x, y))
            case "bottomright":
                button_rect = button_surf.get_rect(bottomright=(x, y))
            case "bottomleft":
                button_rect = button_surf.get_rect(bottomleft=(x, y))

        if self.text:
            font = utils.get_dynamic_font(
                width * 0.9, height * 0.9, self.text, self.font_type, self.max_font_size
            )

            text_surf = font.render(self.text, True, self.text_color)
            text_rect = text_surf.get_rect(center=button_rect.center)

            button_surf.blit(text_surf, text_rect)

        return window.blit(button_surf, button_rect)
