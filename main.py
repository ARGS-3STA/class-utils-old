import os

from algorithm.class_matchmaking import GroupMaker, SeatingPlanGenerator
from algorithm.class_matchmaking.layout import Layout
from algorithm.data_loader import load_class_list
from application import App


def main() -> None:
    BASE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
    ASSETS_DIRECTORY = os.path.join(BASE_DIRECTORY, "assets")

    if not os.path.isdir(ASSETS_DIRECTORY):
        os.mkdir(ASSETS_DIRECTORY)

    # seating_plan_generator = SeatingPlanGenerator(ASSETS_DIRECTORY)

    # print(seating_plan_generator.generate("1stn", "Rom 205"))
    # print(seating_plan_generator.generate("1stn", "Rom 205"))

    # groups = GroupMaker(os.path.join(ASSETS_DIRECTORY, "klasseliste.txt"))
    # print(groups.groups_from_students_per_group(3, {"Viktor", "Stine"}, True))

    app = App(800, 600, "Klasseverktøy")
    app.run()


if __name__ == "__main__":
    main()
