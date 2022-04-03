import copy
import math
import random

from .data_loader import DataLoader


class GroupMaker:
    def __init__(self, data_loader: DataLoader):
        self.data_loader = data_loader

    def groups_from_students_per_group(
        self,
        class_list_name: str,
        antall: int,
        missing_students: set[str],
        minste_antall_per_gruppe=True,
    ):
        class_list = copy.copy(self.data_loader.get_class_list(class_list_name))
        class_list = self.remove_missing_students(class_list, missing_students)

        random.shuffle(class_list)

        class_length = len(class_list)
        amount_of_groups = class_length / antall

        if minste_antall_per_gruppe:
            amount_of_groups = math.floor(amount_of_groups) or 1
        else:
            amount_of_groups = math.ceil(amount_of_groups)

        groups = [[] for _ in range(amount_of_groups)]

        for i, student in enumerate(class_list):
            groups[i % amount_of_groups].append(student)

        return groups

    def groups_from_amounts_of_groups(
        self, class_list_name: str, antall: int, missing_students: set[str]
    ):
        class_list = copy.copy(self.data_loader.get_class_list(class_list_name))
        class_list = self.remove_missing_students(class_list, missing_students)

        random.shuffle(class_list)

        groups = [[] for _ in range(antall)]

        for i, student in enumerate(class_list):
            groups[i % antall].append(student)

        groups = list(filter(bool, groups))
        return groups

    def remove_missing_students(
        self, class_list: list[str], missing_students: set[str]
    ):
        if not missing_students:
            return class_list

        return list(
            filter(
                lambda student_name: student_name not in missing_students, class_list
            )
        )
