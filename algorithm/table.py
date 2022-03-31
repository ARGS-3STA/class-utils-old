from dataclasses import dataclass


@dataclass(slots=True)
class Table:
    student_name: str = ""

    def set_student(self, student_name: str) -> None:
        self.student_name = student_name
