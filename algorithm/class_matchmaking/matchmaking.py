import os
import pickle
from typing import Any

from algorithm import load_class_list
from student import Student

# Coordinate = tuple[int, int]
Layout = list[list[bool]]
PopulatedLayout = list[list[Student]]


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

    def matchmake(self, class_list_file_name: str, layout: Layout) -> PopulatedLayout:
        class_list = load_class_list(
            os.path.join(self.assets_directory, class_list_file_name)
        )

        if sum([sum(row) for row in layout]) < len(class_list):
            return
            raise NotImplementedError

        print(class_list)
