from .table import Table


class Layout:
    def __init__(self, rows: int, columns: int):
        self.rows = rows
        self.columns = columns

        self.grid: list[list[None | Table | str]] = [
            [None] * columns for _ in range(rows)
        ]
        self.table_positions: set[tuple[int, int]] = set()

    def toggle_table(self, x: int, y: int) -> None:
        if self.grid[y][x] is not None:
            self.table_positions.remove((y, x))
            self.grid[y][x] = None
        else:
            table = Table()
            self.grid[y][x] = table
            self.table_positions.add((y, x))

    def toggle_door(self, x: int, y: int) -> None:
        if self.grid[y][x] is not None:
            self.grid[y][x] = None
        else:
            self.grid[y][x] = "door"

    def toggle_teachers_desk(self, x: int, y: int) -> None:
        if self.grid[y][x] is not None:
            self.grid[y][x] = None
        else:
            self.grid[y][x] = "teachers_desk"

    def swap_tables(self, x_1: int, y_1: int, x_2: int, y_2: int) -> None:
        if self.grid[y_1][x_1] is None or self.grid[y_2][x_2] is None:
            print("Can only swap tables, not table and empty cell")
            return

        self.grid[y_1][x_1], self.grid[y_2][x_2] = (
            self.grid[y_2][x_2],
            self.grid[y_1][x_1],
        )

    def __str__(self):
        return_value = ""

        for row in self.grid:
            for value in row:
                return_value += f"{value} "

            return_value += "\n"

        return return_value[:-1]

    def __repr__(self):
        return self.__str__()


def main():
    layout = Layout(10, 10)
    layout.toggle_table(9, 0)
    print(layout)


if __name__ == "__main__":
    main()
