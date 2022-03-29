from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Gender(Enum):
    MALE = "based"
    FEMALE = "not based"


Coordinate = tuple[int, int]


@dataclass(slots=True)
class Student:
    name: str
    gender: Gender
    seat: Coordinate = field(default=None)
