import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import date, timedelta
import pytest
from pawpal_system import Task, Pet, Owner, Scheduler


# ---------------------------------------------------------------------------
# Existing starter tests
# ---------------------------------------------------------------------------

def test_mark_complete_changes_status():
    task = Task(task_name="Walk", duration=30, priority="high")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Buddy", breed="Labrador", species="Dog")
    assert len(pet.get_tasks()) == 0
    pet.add_task(Task(task_name="Feeding", duration=10, priority="high"))
    assert len(pet.get_tasks()) == 1


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_task(name, duration, priority="medium", time=None, recurrence=None, due=None):
    return Task(
        task_name=name,
        duration=duration,
        priority=priority,
        scheduled_time=time,
        recurrence=recurrence,
        due_date=due,
    )


@pytest.fixture
def scheduler():
    return Scheduler()


# ---------------------------------------------------------------------------
# 1. Sorting Correctness
# ---------------------------------------------------------------------------

def test_sort_by_time_chronological_order(scheduler):
    """Tasks are returned earliest-first by scheduled_time."""
    tasks = [
        make_task("Evening walk", 30, time="18:00"),
        make_task("Morning feed", 10, time="07:30"),
        make_task("Noon meds",     5, time="12:00"),
    ]
    result = scheduler.sort_by_time(tasks)
    assert [t.task_name for t in result] == ["Morning feed", "Noon meds", "Evening walk"]


def test_sort_by_time_untimed_tasks_go_last(scheduler):
    """Tasks with no scheduled_time sort after all timed tasks."""
    tasks = [
        make_task("Grooming", 20),
        make_task("Morning feed", 10, time="07:30"),
    ]
    result = scheduler.sort_by_time(tasks)
    assert result[0].task_name == "Morning feed"
    assert result[1].task_name == "Grooming"


def test_sort_by_time_empty_list(scheduler):
    """Sorting an empty list returns an empty list without crashing."""
    assert scheduler.sort_by_time([]) == []


def test_sort_by_time_same_time_both_present(scheduler):
    """Two tasks at the exact same time are both returned."""
    t1 = make_task("Task A", 5, time="09:00")
    t2 = make_task("Task B", 5, time="09:00")
    result = scheduler.sort_by_time([t1, t2])
    assert len(result) == 2


# ---------------------------------------------------------------------------
# 2. Recurrence Logic
# ---------------------------------------------------------------------------

def test_daily_task_creates_next_day(scheduler):
    """Completing a daily task adds a new task due one day later."""
    today = date(2026, 3, 29)
    pet = Pet("Buddy", "Labrador", "dog")
    task = make_task("Feed", 10, recurrence="daily", due=today)
    pet.add_task(task)

    next_task = scheduler.mark_task_complete(pet, task)

    assert next_task is not None
    assert next_task.due_date == today + timedelta(days=1)
    assert next_task.task_name == "Feed"
    assert next_task.recurrence == "daily"


def test_weekly_task_creates_seven_days_later(scheduler):
    """Completing a weekly task adds a new task due seven days later."""
    today = date(2026, 3, 29)
    pet = Pet("Whiskers", "Persian", "cat")
    task = make_task("Bath", 30, recurrence="weekly", due=today)
    pet.add_task(task)

    next_task = scheduler.mark_task_complete(pet, task)

    assert next_task is not None
    assert next_task.due_date == today + timedelta(days=7)


def test_non_recurring_task_returns_none(scheduler):
    """Completing a one-off task returns None and does not add a new task."""
    pet = Pet("Goldie", "Goldfish", "fish")
    task = make_task("Tank clean", 20)
    pet.add_task(task)

    result = scheduler.mark_task_complete(pet, task)

    assert result is None
    assert len(pet.get_tasks()) == 1  # no new task added


def test_original_task_marked_complete_after_recurrence(scheduler):
    """The original task is flagged completed even when recurrence creates a new one."""
    pet = Pet("Buddy", "Labrador", "dog")
    task = make_task("Feed", 10, recurrence="daily", due=date(2026, 3, 29))
    pet.add_task(task)
    scheduler.mark_task_complete(pet, task)

    assert task.completed is True


# ---------------------------------------------------------------------------
# 3. Conflict Detection
# ---------------------------------------------------------------------------

def test_overlapping_tasks_flagged(scheduler):
    """Two tasks whose time windows overlap produce exactly one conflict."""
    t1 = make_task("Walk",  30, time="08:00")   # 08:00–08:30
    t2 = make_task("Meds",  15, time="08:15")   # 08:15–08:30  ← overlap
    conflicts = scheduler.detect_conflicts([t1, t2])
    assert len(conflicts) == 1


def test_back_to_back_tasks_no_conflict(scheduler):
    """Tasks that end exactly when the next begins do NOT conflict."""
    t1 = make_task("Walk",  30, time="08:00")   # ends 08:30
    t2 = make_task("Feed",  10, time="08:30")   # starts 08:30 — no overlap
    assert scheduler.detect_conflicts([t1, t2]) == []


def test_exact_same_time_flagged(scheduler):
    """Two tasks starting at the exact same time are detected as a conflict."""
    t1 = make_task("Task A", 10, time="09:00")
    t2 = make_task("Task B", 10, time="09:00")
    assert len(scheduler.detect_conflicts([t1, t2])) == 1


def test_no_timed_tasks_no_conflict(scheduler):
    """A plan with only untimed tasks returns no conflicts."""
    t1 = make_task("Grooming", 20)
    t2 = make_task("Play",     15)
    assert scheduler.detect_conflicts([t1, t2]) == []


def test_conflict_warnings_includes_pet_name(scheduler):
    """conflict_warnings() includes the pet name in the warning string."""
    t1 = make_task("Walk", 30, time="08:00")
    t2 = make_task("Meds", 15, time="08:15")
    warnings = scheduler.conflict_warnings([t1, t2], pet_name="Buddy")
    assert len(warnings) == 1
    assert "WARNING" in warnings[0]
    assert "Buddy" in warnings[0]


# ---------------------------------------------------------------------------
# 4. Edge Cases
# ---------------------------------------------------------------------------

def test_pet_with_no_tasks_generates_empty_plan(scheduler):
    """generate_plan for a pet with zero tasks returns an empty list."""
    pet = Pet("Empty", "Unknown", "unknown")
    owner = Owner("Jordan", 120, pet)
    assert scheduler.generate_plan(owner, pet) == []


def test_all_completed_tasks_produces_empty_plan(scheduler):
    """generate_plan skips completed tasks entirely."""
    pet = Pet("Buddy", "Labrador", "dog")
    task = make_task("Walk", 30, time="08:00")
    task.completed = True
    pet.add_task(task)
    owner = Owner("Jordan", 120, pet)
    assert scheduler.generate_plan(owner, pet) == []


def test_zero_available_time_returns_empty_plan(scheduler):
    """An owner with 0 minutes available gets an empty plan."""
    pet = Pet("Buddy", "Labrador", "dog")
    pet.add_task(make_task("Walk", 30, time="08:00"))
    owner = Owner("Jordan", 0, pet)
    assert scheduler.generate_plan(owner, pet) == []
