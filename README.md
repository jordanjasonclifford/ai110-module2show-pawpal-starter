# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Smarter Scheduling

For module 2 the scheduler got a few upgrades to make it actually useful.

Tasks can now have a scheduled time in HH:MM format, and `sort_by_time()` will put them in order for you. It uses a lambda as the key so tasks without a time just get pushed to the end instead of breaking anything.

Filtering was also added. You can call `get_pending_tasks()` or `get_completed_tasks()` on any pet to get just what you need, and `filter_by_pet()` on the scheduler if you want to pull tasks for a specific pet out of a bigger list.

Recurring tasks were the big one. Tasks can be set to daily or weekly, and when you mark one complete through `mark_task_complete()` it automatically queues up the next one with the right due date using timedelta. So you don't have to re-add feeding or walks every day yourself.

Conflict detection was also added in. The scheduler checks for overlapping time windows and prints a warning instead of just silently letting two things be scheduled at the same time. It works for a single pet's plan and across multiple pets too.

---

## Testing PawPal+

To run the full test suite:

```bash
python -m pytest tests/test_pawpal.py -v
```

I wrote 18 tests across four areas:

- **Sorting correctness** — verifies that `sort_by_time()` returns tasks in chronological order, pushes untimed tasks to the end, and handles empty lists without crashing.
- **Recurrence logic** — confirms that marking a daily task complete automatically creates a new task due the next day, weekly tasks land seven days out, and one-off tasks don't spawn duplicates.
- **Conflict detection** — checks that overlapping time windows get flagged, back-to-back tasks (no actual overlap) stay clean, and the warning strings include the pet name.
- **Edge cases** — covers a pet with no tasks, a plan where everything is already completed, and an owner with zero available time.

All 18 tests pass.

**Confidence Level: ★★★★☆**

The core scheduling logic — sorting, recurrence, and conflict detection — is solid and well-covered. I'd bump it to five stars once the Streamlit UI layer and any user-input validation gets test coverage too.

---

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.




