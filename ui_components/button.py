import utils
from pygame import Rect, Surface


class Button:
    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        *,
        text: str = "",
        **kwargs
    ):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.text = text

        self.button_rect = None

        self.coordinate_position = kwargs.pop("coordinate_position", "center")

        self.font_type = kwargs.pop("font_type", "Microsoft Sans Serif")
        self.max_font_size = kwargs.pop("max_font_size", 60)
        self.text_color = kwargs.pop("text_color", "black")

        self.button_color = kwargs.pop("button_color", "white")
        self.button_hover_color = kwargs.pop("button_hover_color", "grey")

        self.current_button_color = self.button_color

        self.x_offset = kwargs.pop("x_offset", 0)
        self.y_offset = kwargs.pop("y_offset", 0)

        self.is_hovered = False

    def draw(self, window: Surface, screen_width: int, screen_height: int) -> Rect:
        x, y = (
            self.x * screen_width + self.x_offset,
            self.y * screen_height + self.y_offset,
        )
        width, height = self.width * screen_width, self.height * screen_height

        button_surf = Surface((width, height))
        button_surf.fill(self.current_button_color)

        match self.coordinate_position:
            case "center":
                self.button_rect = button_surf.get_rect(center=(x, y))
            case "topright":
                self.button_rect = button_surf.get_rect(topright=(x, y))
            case "topleft":
                self.button_rect = button_surf.get_rect(topleft=(x, y))
            case "bottomright":
                self.button_rect = button_surf.get_rect(bottomright=(x, y))
            case "bottomleft":
                self.button_rect = button_surf.get_rect(bottomleft=(x, y))

        if self.text:
            font = utils.get_dynamic_font(
                width * 0.9, height * 0.9, self.text, self.font_type, self.max_font_size
            )

            text_surf = font.render(self.text, True, self.text_color)
            text_rect = text_surf.get_rect(
                center=(self.button_rect.width / 2, self.button_rect.height / 2)
            )

            button_surf.blit(text_surf, text_rect)

        return window.blit(button_surf, self.button_rect)
    
    def check_hover(self, mouse_pos) -> bool:
        if self.button_rect is None:
            return False

        was_hovered = self.is_hovered

        self.is_hovered = self.button_rect.collidepoint(mouse_pos)

        if self.is_hovered == was_hovered:
            return False
        
        if self.is_hovered:
            self.current_button_color = self.button_hover_color
        else:
            self.current_button_color = self.button_color
        
        return True

    def is_pressed(self, mouse_pos) -> bool:
        if self.button_rect is None:
            return False

        return self.button_rect.collidepoint(mouse_pos)
