import os
import pickle

from layout import Layout


class ClassMapMaker:
    def __init__(self, assets_directory: str):
        self.assets_directory = assets_directory

        self.class_lists_file_path = os.path.join(assets_directory, "class-lists.pkl")
        self.load_class_lists()

        self.layouts_file_path = os.path.join(assets_directory, "layouts.pkl")
        self.load_layouts()

    def load_class_lists(self) -> None:
        try:
            with open(self.class_lists_file_path, "rb") as class_lists_file:
                self.class_lists = pickle.load(class_lists_file)
        except FileNotFoundError:
            self.class_lists = {}
            self.save_class_lists()

    def save_class_lists(self) -> None:
        with open(self.class_lists_file_path, "wb") as class_lists_file:
            pickle.dump(self.class_lists, class_lists_file)

    def add_class_list(self, class_list: list[str], class_list_name: str) -> None:
        self.class_lists[class_list_name] = class_list
        self.save_class_lists()

    def load_layouts(self) -> None:
        try:
            with open(self.layouts_file_path, "rb") as layouts_file:
                self.layouts = pickle.load(layouts_file)
        except FileNotFoundError:
            self.layouts = {}
            self.save_layouts()

    def save_layouts(self) -> None:
        with open(self.layouts_file_path, "wb") as layouts_file:
            pickle.dump(self.layouts, layouts_file)

    def add_layout(self, layout: Layout, layout_name: str) -> None:
        self.layouts[layout_name] = layout
        self.save_layouts()

    def remove_layout(self, layout_name: str) -> None:
        if layout_name in self.layouts:
            del self.layouts[layout_name]
            self.save_layouts()

    def __str__(self):
        return f"{self.class_lists}\n{self.layouts}"


def main():
    class_map_maker = ClassMapMaker(
        "C:/Users/danie/OneDrive/Dokumenter/class-utils/assets"
    )


if __name__ == "__main__":
    main()
