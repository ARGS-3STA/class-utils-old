import copy
import random

from .data_loader import DataLoader
from .layout import Layout


class SeatingPlanGenerator:
    def __init__(self, data_loader: DataLoader):
        self.data_loader = data_loader

    def generate(self, class_list_name: str, layout_name: str) -> Layout | None:
        class_list = copy.copy(self.data_loader.get_class_list(class_list_name))
        class_size = len(class_list)

        random.shuffle(class_list)

        layout = copy.deepcopy(self.data_loader.get_layout(layout_name))

        while class_list:
            if not layout.table_positions:
                print("Not enough seats for class of size:", class_size)
                return

            table_y, table_x = layout.table_positions.pop()
            table = layout.grid[table_y][table_x]
            table.set_student(class_list.pop())

        return layout


def main():
    pass


if __name__ == "__main__":
    main()
