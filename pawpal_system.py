from dataclasses import dataclass, field
from typing import List


PRIORITY_ORDER = {"low": 1, "medium": 2, "high": 3}

@dataclass
class Task:
    task_name: str
    duration: int       # in minutes
    priority: str       # "low", "medium", or "high"
    completed: bool = False

    def get_details(self) -> str:
        """Return a readable summary of the task's name, duration, and priority."""
        return f"{self.task_name} ({self.duration} min, priority {self.priority})"

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True


@dataclass
class Pet:
    name: str
    breed: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet's task list."""
        self.tasks.remove(task)

    def get_tasks(self) -> List[Task]:
        """Return the full list of tasks assigned to this pet."""
        return self.tasks


class Owner:
    def __init__(self, name: str, time_available: int, pet: "Pet" = None):
        self.name = name
        self.time_available = time_available  # in minutes
        self.pet = pet

    def get_available_time(self) -> int:
        """Return the owner's total available time in minutes."""
        return self.time_available


class Scheduler:
    def generate_plan(self, owner: Owner, pet: Pet) -> List[Task]:
        """Sort pet tasks by priority and return those that fit within the owner's available time."""
        sorted_tasks = self._sort_by_priority(pet.get_tasks())
        return self._fit_within_time(sorted_tasks, owner.get_available_time())

    def _sort_by_priority(self, tasks: List[Task]) -> List[Task]:
        """Return tasks sorted from highest to lowest priority."""
        return sorted(tasks, key=lambda t: PRIORITY_ORDER.get(t.priority, 0), reverse=True)

    def _fit_within_time(self, tasks: List[Task], time_available: int) -> List[Task]:
        """Greedily add tasks until the time budget is exhausted; skip tasks that don't fit."""
        plan = []
        time_used = 0
        for task in tasks:
            if time_used + task.duration <= time_available:
                plan.append(task)
                time_used += task.duration
        return plan
