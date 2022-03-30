import os
import pickle
import random
from typing import Any

import utils
from algorithm import load_class_list

from .student import Student

# Coordinate = tuple[int, int]
Layout = list[list[bool]]
PopulatedLayout = list[list[Student | None]]


class Matchmaking:
    def __init__(self, assets_directory: str):
        self.assets_directory = assets_directory

        self.layouts_file_path = os.path.join(self.assets_directory, "layouts.pkl")

        self.load_layouts()

    def load_layouts(self) -> None:
        try:
            with open(self.layouts_file_path, "rb") as layouts_file:
                self.layouts = pickle.load(layouts_file)
        except FileNotFoundError:
            self.layouts = {}

    def save_layouts(self) -> None:
        with open(self.layouts_file_path, "wb") as layouts_file:
            pickle.dump(self.layouts, layouts_file)

    def add_layout(self, layout_name: str, layout: Layout) -> None:
        self.layouts[layout_name] = layout
        self.save_layouts(layout)

    def matchmake(
        self, class_list_file_name: str, layout_name: str = "default"
    ) -> PopulatedLayout | None:
        class_list = load_class_list(
            os.path.join(self.assets_directory, class_list_file_name)
        )

        layout = self.layouts[layout_name]

        if utils.amount_of_valid_seats(layout) < len(class_list):
            print("Not enough seats")
            return

        random.shuffle(class_list)

        populated_layout = []

        for row in layout:
            populated_layout.append([])
            for val in row:
                if not val:
                    populated_layout[-1].append(None)
                else:
                    populated_layout[-1].append(class_list.pop())
