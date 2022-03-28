import os

from algorithm.data_loader import load_class_list
from application import App


def main() -> None:
    # main 2
    BASE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
    ASSETS_DIRECTORY = os.path.join(BASE_DIRECTORY, "assets")

    app = App(800, 600, "Test")
    app.run()


if __name__ == "__main__":
    main()
