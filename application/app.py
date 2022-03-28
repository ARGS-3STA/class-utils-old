from states import State


class App:
    def __init__(self):
        self.state_stack: list[State] = []

    def add_state(self, state: State):
        self.state_stack.append(state)

    def pop_state(self):
        self.state_stack.pop()
