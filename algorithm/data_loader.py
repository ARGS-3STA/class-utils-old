def load_class_list(file_path: str):
    try:
        with open(file_path, encoding="latin-1") as class_list:
            return class_list.read().splitlines()
    except FileNotFoundError:
        print("Can't find file with path:", file_path)
