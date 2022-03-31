import pygame

class CheckBox:
    def __init__(self, x, y, width, height, **kwargs):
        self.x, self.y = x,y
        self.width, self.height = width,height

        self.box_rect = None
        self.is_hovered = False

        self.state = kwargs.pop("state", False)
        self.on_color = kwargs.pop("on_color", (100,100,100))
        self.off_color = kwargs.pop("off_color", (255,0,0))
        self.hover_color = kwargs.pop("hover_color", (0,0,0))
        self.coordinate_position = kwargs.pop("coordinate_position", "center")
        self.current_color = self.off_color
        self.color = self.off_color

    def is_pressed(self, mouse_pos):
        if self.box_rect is None:
            return False

        return self.box_rect.collidepoint(mouse_pos)
    
    def toggle_state(self):
        self.state = not self.state
        if self.state:
            self.color = self.on_color
        else:
            self.color = self.off_color
        self.current_color = self.color

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
            self.current_color = self.color

        return True
    
    def draw(self, window, screen_width, screen_height):
        x,y = self.x * screen_width, self.y*screen_height
        width, height = self.width*screen_width, self.height*screen_height

        surface = pygame.Surface((width, height))

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
        
        return window.blit(surface, surface_rect)
