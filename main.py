import os

from algorithm.data_loader import load_class_list
from application import App


def main() -> None:
    # app = App(800, 600, "Test")
    # app.run()

    BASE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
    ASSETS_DIRECTORY = os.path.join(BASE_DIRECTORY, "assets")

    load_class_list(os.path.join(ASSETS_DIRECTORY, "klasseliste.txt"))


if __name__ == "__main__":
    main()
