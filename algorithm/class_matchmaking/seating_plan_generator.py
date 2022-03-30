import copy
import os
import pickle
import random

from .layout import Layout


class SeatingPlanGenerator:
    def __init__(self, assets_directory: str):
        self.assets_directory = assets_directory

        self.class_lists_file_path = os.path.join(assets_directory, "class-lists.pkl")
        self.class_lists: dict[str, list[str]] = self.load_class_lists()

        self.layouts_file_path = os.path.join(assets_directory, "layouts.pkl")
        self.layouts: dict[str, Layout] = self.load_layouts()

        self.seating_plans_file_path = os.path.join(
            assets_directory, "seating-plans.pkl"
        )
        self.seating_plans: dict[str, Layout] = self.load_seating_plans()

    def load_class_lists(self) -> None:
        try:
            with open(self.class_lists_file_path, "rb") as class_lists_file:
                return pickle.load(class_lists_file)
        except FileNotFoundError:
            return {}

    def save_class_lists(self) -> None:
        with open(self.class_lists_file_path, "wb") as class_lists_file:
            pickle.dump(self.class_lists, class_lists_file)

    def add_class_list(self, class_list: list[str], class_list_name: str) -> None:
        self.class_lists[class_list_name] = class_list
        self.save_class_lists()

    def load_layouts(self) -> None:
        try:
            with open(self.layouts_file_path, "rb") as layouts_file:
                return pickle.load(layouts_file)
        except FileNotFoundError:
            return {}

    def save_layouts(self) -> None:
        with open(self.layouts_file_path, "wb") as layouts_file:
            pickle.dump(self.layouts, layouts_file)

    def add_layout(self, layout: Layout, layout_name: str) -> None:
        self.layouts[layout_name] = layout
        self.save_layouts()

    def rename_layout(self, layout_name: str, new_layout_name: str) -> None:
        if layout_name not in self.layouts:
            print(f"No layout with name {layout_name} found to rename")
            return

        if new_layout_name in self.layouts:
            print(f"A layout with the name {new_layout_name} already exists")
            return

        self.layouts[new_layout_name] = self.layouts[layout_name]
        del self.layouts[layout_name]

        self.save_layouts()

    def remove_layout(self, layout_name: str) -> None:
        if layout_name in self.layouts:
            del self.layouts[layout_name]
            self.save_layouts()

    def load_seating_plans(self) -> None:
        try:
            with open(self.seating_plans_file_path, "rb") as seating_plans_file:
                return pickle.load(seating_plans_file)
        except FileNotFoundError:
            return {}

    def save_seating_plans(self) -> None:
        with open(self.seating_plans_file_path, "wb") as seating_plans_file:
            pickle.dump(self.seating_plans, seating_plans_file)

    def add_seating_plan(self, seating_plan: Layout, seating_plan_name: str) -> None:
        self.seating_plans[seating_plan_name] = seating_plan
        self.save_seating_plans()

    def __str__(self):
        return f"{self.class_lists}\n{self.layouts}"

    def get_class_list_names(self) -> list[str]:
        return self.class_lists.keys()

    def get_class_list(self, class_list_name: str) -> list[str] | None:
        return self.class_lists.get(class_list_name, None)

    def get_layout_names(self) -> list[str]:
        return self.layouts.keys()

    def get_layout(self, layout_name: str) -> Layout | None:
        return self.layouts.get(layout_name, None)

    def get_seating_plan_names(self) -> list[str]:
        return self.seating_plans.keys()

    def get_seating_plan(self, seating_plan_name: str) -> Layout | None:
        return self.seating_plans.get(seating_plan_name, None)

    def generate(self, class_list_name: str, layout_name: str) -> Layout | None:
        if class_list_name not in self.class_lists:
            print("Invalid class-list name")
            return
        elif layout_name not in self.layouts:
            print("Invalid layout name")
            return

        class_list = copy.deepcopy(self.class_lists[class_list_name])
        random.shuffle(class_list)

        class_size = len(class_list)

        layout = copy.deepcopy(self.layouts[layout_name])

        while class_list:
            if not layout.table_positions:
                print("Not enough seats for class of size:", class_size)
                return

            table_y, table_x = layout.table_positions.pop()
            table = layout.grid[table_y][table_x]
            table.set_student(class_list.pop())

        return layout


def main():
    seating_plan_generator = SeatingPlanGenerator(
        "C:/Users/danie/OneDrive/Dokumenter/class-utils/assets"
    )


if __name__ == "__main__":
    main()
