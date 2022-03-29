from .state import App, State


class Settings(State):
    def __init__(self, app: App):
        super().__init__(app)

    def update(self, actions, deltatime):
        pass

    def draw(self, window, screen_width, screen_height):
        pass
