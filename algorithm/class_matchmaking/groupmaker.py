import math
import random

from algorithm import load_class_list


class GroupMaker:
    def __init__(self, assets_directory):
        self.assets_directory = assets_directory
        self.class_list = load_class_list(self.assets_directory)
        self.class_length = len(self.class_list)

    def groups_from_students_per_group(
        self, antall: int, minste_antall_per_gruppe=False
    ):
        random.shuffle(self.class_list)
        amount_of_groups = self.class_length / antall

        if minste_antall_per_gruppe:
            amount_of_groups = math.floor(amount_of_groups)
        else:
            amount_of_groups = math.ceil(amount_of_groups)

        groups = [[] for _ in range(amount_of_groups)]

        for i, student in enumerate(self.class_list):
            groups[i % amount_of_groups].append(student)

        return groups

    def groups_from_amounts_of_groups(self, antall: int):
        random.shuffle(self.class_list)

        groups = [[] for _ in range(antall)]

        for i, student in enumerate(self.class_list):
            groups[i % antall].append(student)

        groups = list(filter(bool, groups))
        return groups
