import os
import pickle
from dataclasses import dataclass

from .class_matchmaking import Layout


def load_class_list(file_path: str):
    try:
        with open(file_path, encoding="latin-1") as class_list:
            return class_list.read().splitlines()
    except FileNotFoundError:
        print("Can't find file with path:", file_path)


@dataclass(slots=True)
class DataLoader:
    assets_directory: str

    def __post_init__(self):
        self.class_lists_file_path = os.path.join(
            self.assets_directory, "class-lists.pkl"
        )
        self.class_lists = self.load_class_lists()

        self.layouts_file_path = os.path.join(self.assets_directory, "layouts.pkl")
        self.layouts = self.load_layouts()

        self.seating_plans_file_path = os.path.join(
            self.assets_directory, "seating-plans.pkl"
        )
        self.seating_plans = self.load_seating_plans()

    def load_class_lists(self) -> dict[str, list[str]]:
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

    def remove_class_list(self, class_list_name: str) -> None:
        del self.class_lists[class_list_name]

    def rename_class_list(self, class_list_name: str, new_class_list_name: str) -> None:
        self.class_lists[new_class_list_name] = self.class_lists[class_list_name]
        self.remove_class_list(class_list_name)

    def load_layouts(self) -> dict[str, Layout]:
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

    def remove_layout(self, layout_name: str) -> None:
        del self.layouts[layout_name]

    def rename_layout(self, layout_name: str, new_layout_name: str) -> None:
        self.layouts[new_layout_name] = self.layouts[layout_name]
        self.remove_layout(layout_name)

    def load_seating_plans(self) -> dict[str, Layout]:
        try:
            with open(self.seating_plans_file_path, "rb") as seating_plans_file:
                return pickle.load(seating_plans_file)
        except FileNotFoundError:
            return {}

    def save_seating_plans(self) -> None:
        with open(self.seating_plans_file_path, "wb") as seating_plans_file:
            pickle.dump(self.seating_plans, seating_plans_file)

    def add_seating_plan(self, seating_plan: Layout, seating_plan_name: str) -> None:
        self.layouts[seating_plan_name] = seating_plan
        self.save_seating_plans()

    def remove_seating_plan(self, seating_plan_name: str) -> None:
        del self.seating_plans[seating_plan_name]

    def rename_seating_plan(
        self, seating_plan_name: str, new_seating_plan_name: str
    ) -> None:
        self.seating_plans[new_seating_plan_name] = self.seating_plans[
            seating_plan_name
        ]
        self.remove_seating_plan(seating_plan_name)
