from dataclasses import dataclass, field
from datetime import date, timedelta
from itertools import combinations
from typing import List, Optional, Tuple


PRIORITY_ORDER = {"low": 1, "medium": 2, "high": 3}
RECURRENCE_DAYS = {"daily": 1, "weekly": 7}


@dataclass
class Task:
    task_name: str
    duration: int           # in minutes
    priority: str           # "low", "medium", or "high"
    completed: bool = False
    scheduled_time: Optional[str] = None   # "HH:MM", e.g. "08:00"
    recurrence: Optional[str] = None       # None, "daily", or "weekly"
    due_date: Optional[date] = None        # date this task is due

    def get_details(self) -> str:
        """Return a readable summary of the task."""
        time_str = f" at {self.scheduled_time}" if self.scheduled_time else ""
        recur_str = f" [{self.recurrence}]" if self.recurrence else ""
        due_str = f" due {self.due_date}" if self.due_date else ""
        return f"{self.task_name}{time_str} ({self.duration} min, priority {self.priority}){recur_str}{due_str}"

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
        """Return all tasks assigned to this pet."""
        return self.tasks

    def get_pending_tasks(self) -> List[Task]:
        """Return only tasks that have not been completed."""
        return [t for t in self.tasks if not t.completed]

    def get_completed_tasks(self) -> List[Task]:
        """Return only tasks that have been completed."""
        return [t for t in self.tasks if t.completed]


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
        """Sort pending tasks by time (then priority) and return those that fit in available time."""
        pending = pet.get_pending_tasks()
        sorted_tasks = self._sort_tasks(pending)
        return self._fit_within_time(sorted_tasks, owner.get_available_time())

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Return tasks sorted chronologically by their scheduled_time field.

        Uses a lambda as the sort key, converting each "HH:MM" string to total
        minutes since midnight via _time_to_minutes(). Tasks that have no
        scheduled_time are assigned float("inf") so they sort to the end of the
        list rather than raising an error.

        Args:
            tasks: Any list of Task objects, in any order.

        Returns:
            A new sorted list — the original list is not modified.
        """
        return sorted(tasks, key=lambda t: self._time_to_minutes(t.scheduled_time) if t.scheduled_time else float("inf"))

    def _sort_tasks(self, tasks: List[Task]) -> List[Task]:
        """Sort by scheduled_time first (timed tasks before untimed), then by priority descending."""
        def sort_key(t: Task):
            time_key = self._time_to_minutes(t.scheduled_time) if t.scheduled_time else float("inf")
            priority_key = -PRIORITY_ORDER.get(t.priority, 0)  # negate so highest priority sorts first
            return (time_key, priority_key)
        return sorted(tasks, key=sort_key)

    def _sort_by_priority(self, tasks: List[Task]) -> List[Task]:
        """Return tasks sorted from highest to lowest priority."""
        return sorted(tasks, key=lambda t: PRIORITY_ORDER.get(t.priority, 0), reverse=True)

    def _fit_within_time(self, tasks: List[Task], time_available: int) -> List[Task]:
        """Select tasks that fit within the owner's available time using a greedy approach.

        Walks the pre-sorted task list in order, adding each task if its duration
        fits in the remaining time budget. Tasks that don't fit are skipped rather
        than stopping the loop — a later shorter task may still fit.

        This is O(n) and works well for small task lists, but is not guaranteed to
        find the optimal combination (see reflection.md section 2b for the tradeoff).

        Args:
            tasks:          Tasks already sorted in the desired schedule order.
            time_available: Total minutes the owner has available today.

        Returns:
            The subset of tasks that fit, in sorted order.
        """
        plan = []
        time_used = 0
        for task in tasks:
            if time_used + task.duration <= time_available:
                plan.append(task)
                time_used += task.duration
        return plan

    def detect_conflicts(self, plan: List[Task]) -> List[Tuple[Task, Task]]:
        """Detect overlapping time windows between tasks in a single pet's plan.

        Uses itertools.combinations to generate every unique pair of timed tasks
        without manual index loops, then applies the standard interval-overlap
        condition: two intervals [a_start, a_start+a.duration) and
        [b_start, b_start+b.duration) overlap when:
            a_start < b_start + b.duration  AND  b_start < a_start + a.duration

        Tasks with no scheduled_time are ignored — only timed tasks can conflict.

        Args:
            plan: The list of Task objects to check (typically the output of generate_plan).

        Returns:
            A list of (Task, Task) pairs that overlap. Empty list means no conflicts.
        """
        timed = [(t, self._time_to_minutes(t.scheduled_time)) for t in plan if t.scheduled_time]
        return [
            (a, b)
            for (a, a_start), (b, b_start) in combinations(timed, 2)
            if a_start < b_start + b.duration and b_start < a_start + a.duration
        ]

    def conflict_warnings(self, plan: List[Task], pet_name: str = "") -> List[str]:
        """Return human-readable warning strings for scheduling conflicts within one pet's plan.

        Wraps detect_conflicts() and formats each conflicting pair into a plain
        English warning string. Never raises — if there are no conflicts the
        returned list is empty and the caller can skip printing entirely.

        Args:
            plan:     The scheduled task list to check.
            pet_name: Optional pet name included in each warning for clarity.

        Returns:
            A list of warning strings, one per conflicting pair.
        """
        label = f" ({pet_name})" if pet_name else ""
        warnings = []
        for a, b in self.detect_conflicts(plan):
            warnings.append(
                f"WARNING{label}: '{a.task_name}' at {a.scheduled_time} ({a.duration} min) "
                f"overlaps with '{b.task_name}' at {b.scheduled_time} ({b.duration} min)"
            )
        return warnings

    def detect_cross_pet_conflicts(self, pet_plans: List[Tuple[str, List[Task]]]) -> List[str]:
        """Detect scheduling conflicts across multiple pets' plans.

        Accepts a list of (pet_name, plan) pairs and checks every task from one
        pet against every task from a different pet for time-window overlap.
        Returns human-readable warning strings — never raises an exception.
        """
        warnings = []
        # Flatten to (pet_name, task) pairs for timed tasks only
        entries = [
            (name, task)
            for name, plan in pet_plans
            for task in plan
            if task.scheduled_time
        ]
        for i in range(len(entries)):
            for j in range(i + 1, len(entries)):
                name_a, a = entries[i]
                name_b, b = entries[j]
                if name_a == name_b:
                    continue  # same-pet conflicts handled by conflict_warnings()
                a_start = self._time_to_minutes(a.scheduled_time)
                b_start = self._time_to_minutes(b.scheduled_time)
                if a_start < b_start + b.duration and b_start < a_start + a.duration:
                    warnings.append(
                        f"WARNING (cross-pet): {name_a}->'{a.task_name}' at {a.scheduled_time} "
                        f"({a.duration} min) overlaps with {name_b}->'{b.task_name}' at {b.scheduled_time} "
                        f"({b.duration} min)"
                    )
        return warnings

    def mark_task_complete(self, pet: Pet, task: Task) -> Optional[Task]:
        """Mark a task complete. If it recurs, add a new instance with the next due date.

        Uses timedelta to calculate the next occurrence:
          daily  -> due_date + timedelta(days=1)
          weekly -> due_date + timedelta(days=7)

        Returns the newly created Task, or None if the task does not recur.
        """
        task.mark_complete()
        if task.recurrence not in RECURRENCE_DAYS:
            return None
        days_ahead = RECURRENCE_DAYS[task.recurrence]
        base = task.due_date if task.due_date else date.today()
        next_due = base + timedelta(days=days_ahead)
        next_task = Task(
            task_name=task.task_name,
            duration=task.duration,
            priority=task.priority,
            scheduled_time=task.scheduled_time,
            recurrence=task.recurrence,
            due_date=next_due,
        )
        pet.add_task(next_task)
        return next_task

    def reset_recurring_tasks(self, pet: Pet) -> None:
        """Reset completed recurring tasks so they are included in the next day's plan."""
        for task in pet.get_tasks():
            if task.completed and task.recurrence in ("daily", "weekly"):
                task.completed = False

    def filter_by_pet(self, pets: List[Pet], pet_name: str) -> List[Task]:
        """Return all tasks belonging to the named pet (case-insensitive)."""
        for pet in pets:
            if pet.name.lower() == pet_name.lower():
                return pet.get_tasks()
        return []

    @staticmethod
    def _time_to_minutes(time_str: str) -> int:
        """Convert 'HH:MM' string to total minutes since midnight."""
        hours, minutes = map(int, time_str.split(":"))
        return hours * 60 + minutes
