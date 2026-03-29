from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    task_name: str
    duration: int       # in minutes
    priority: int       # higher = more important

    def get_details(self) -> str:
        pass


@dataclass
class Pet:
    name: str
    breed: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task: Task) -> None:
        pass

    def get_tasks(self) -> List[Task]:
        pass


class Owner:
    def __init__(self, name: str, time_available: int):
        self.name = name
        self.time_available = time_available  # in minutes

    def get_available_time(self) -> int:
        pass


class Scheduler:
    def generate_plan(self, owner: Owner, pet: Pet) -> List[Task]:
        pass

    def sort_by_priority(self, tasks: List[Task]) -> List[Task]:
        pass

    def fit_within_time(self, tasks: List[Task], time_available: int) -> List[Task]:
        pass
