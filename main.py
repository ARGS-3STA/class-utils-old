import os

from algorithm.class_matchmaking import GroupMaker
from algorithm.data_loader import load_class_list
from application import App


def main() -> None:
    # main 2
    BASE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
    ASSETS_DIRECTORY = os.path.join(BASE_DIRECTORY, "assets")

    # groups = GroupMaker(os.path.join(ASSETS_DIRECTORY, "klasseliste.txt"))
    # print(groups.groups_from_amounts_of_groups(10))

    app = App(800, 600, "Klasseverktøy")
    app.run()


if __name__ == "__main__":
    main()
