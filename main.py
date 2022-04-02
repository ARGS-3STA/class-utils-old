from algorithm import DataLoader, GroupMaker, Layout, SeatingPlanGenerator
from application import App


def main() -> None:
    import os

    BASE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
    ASSETS_DIRECTORY = os.path.join(BASE_DIRECTORY, "assets")

    if not os.path.isdir(ASSETS_DIRECTORY):
        os.mkdir(ASSETS_DIRECTORY)

    data_loader = DataLoader(ASSETS_DIRECTORY)

    # seating_plan_generator = SeatingPlanGenerator(data_loader)

    # print(seating_plan_generator.generate("1stn", "Rom 205"))
    # print(seating_plan_generator.generate("1stn", "Rom 205"))

    # groups = GroupMaker(data_loader)
    # print(groups.groups_from_students_per_group("1stn", 3, {"Viktor", "Stine"}, True))

    app = App(800, 600, "Klasseverktøy", data_loader)
    app.run()


if __name__ == "__main__":
    main()
