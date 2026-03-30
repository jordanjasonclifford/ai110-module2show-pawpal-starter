from pawpal_system import Owner, Pet, Task, Scheduler

# --- Setup ---
buddy = Pet(name="Buddy", breed="Labrador", species="Dog")
whiskers = Pet(name="Whiskers", breed="Tabby", species="Cat")

# Tasks added OUT OF ORDER intentionally — to demonstrate sort_by_time()
buddy.add_task(Task(task_name="Enrichment Play", duration=20, priority="low",    scheduled_time="09:00"))
buddy.add_task(Task(task_name="Feeding",         duration=10, priority="high",   scheduled_time="07:15", recurrence="daily"))
buddy.add_task(Task(task_name="Morning Walk",    duration=30, priority="high",   scheduled_time="07:00"))

whiskers.add_task(Task(task_name="Grooming",   duration=15, priority="medium", scheduled_time="10:00"))
whiskers.add_task(Task(task_name="Feeding",    duration=5,  priority="high",   scheduled_time="07:30", recurrence="daily"))
whiskers.add_task(Task(task_name="Litter Box", duration=10, priority="medium", scheduled_time="08:00"))

pets = [buddy, whiskers]
owners = [
    Owner(name="Jordan", time_available=60, pet=buddy),
    Owner(name="Jordan", time_available=60, pet=whiskers),
]
scheduler = Scheduler()

# --- Step 2: Demonstrate sort_by_time() ---
print("=== Sorting Demo ===")
print("\nBuddy's tasks AS ADDED (out of order):")
for task in buddy.get_tasks():
    print(f"  {task.get_details()}")

print("\nBuddy's tasks SORTED BY TIME:")
for task in scheduler.sort_by_time(buddy.get_tasks()):
    print(f"  {task.get_details()}")

# --- Step 2: Demonstrate filtering by status ---
print("\n=== Filtering Demo ===")

# Mark one task complete to show the split
buddy.get_tasks()[0].mark_complete()   # Enrichment Play (was added first)

print("\nBuddy's PENDING tasks:")
for task in buddy.get_pending_tasks():
    print(f"  {task.get_details()}")

print("\nBuddy's COMPLETED tasks:")
for task in buddy.get_completed_tasks():
    print(f"  {task.get_details()}")

# --- Step 2: Demonstrate filtering by pet name ---
print("\nAll tasks for Whiskers (filtered by pet name):")
for task in scheduler.filter_by_pet(pets, "Whiskers"):
    print(f"  {task.get_details()}")

# --- Generate full schedule plans ---
print("\n=== Generated Schedules ===")
# Reset the manually completed task so it shows in the plan
buddy.get_tasks()[0].completed = False

buddy_plan = scheduler.generate_plan(owners[0], buddy)
whiskers_plan = scheduler.generate_plan(owners[1], whiskers)

for owner, plan in [(owners[0], buddy_plan), (owners[1], whiskers_plan)]:
    print(f"\n--- Today's Schedule for {owner.pet.name} ---")
    if not plan:
        print("  No tasks fit within the available time.")
    for task in plan:
        print(f"  {task.get_details()}")

    # Step 4: same-pet conflict warnings
    for warning in scheduler.conflict_warnings(plan, pet_name=owner.pet.name):
        print(f"  {warning}")

    # Mark planned tasks complete
    for task in plan:
        task.mark_complete()

# --- Step 4: Cross-pet conflict detection ---
print("\n=== Step 4: Conflict Detection ===")

# Add two tasks at the EXACT same time across different pets to trigger a cross-pet warning
buddy.add_task(Task(task_name="Vet Appointment", duration=60, priority="high", scheduled_time="09:00"))
whiskers.add_task(Task(task_name="Vet Appointment", duration=30, priority="high", scheduled_time="09:00"))

same_time_buddy = [t for t in buddy.get_tasks() if t.task_name == "Vet Appointment"]
same_time_whiskers = [t for t in whiskers.get_tasks() if t.task_name == "Vet Appointment"]

print("\nSame-pet conflict warnings (Buddy's plan):")
buddy_new_plan = same_time_buddy + [t for t in buddy_plan if not t.completed]
for w in scheduler.conflict_warnings(buddy_new_plan, pet_name="Buddy"):
    print(f"  {w}")
if not scheduler.conflict_warnings(buddy_new_plan, pet_name="Buddy"):
    print("  No same-pet conflicts.")

print("\nCross-pet conflict warnings (Buddy vs Whiskers):")
cross_warnings = scheduler.detect_cross_pet_conflicts([
    ("Buddy",    same_time_buddy),
    ("Whiskers", same_time_whiskers),
])
for w in cross_warnings:
    print(f"  {w}")
if not cross_warnings:
    print("  No cross-pet conflicts.")

# --- Step 3: mark_task_complete() auto-creates next occurrence ---
print("\n=== Recurring Task Auto-Creation Demo ===")

# Find Buddy's daily Feeding task and complete it via the scheduler
feeding = next(t for t in buddy.get_tasks() if t.task_name == "Feeding")
print(f"Completing: {feeding.get_details()}")
next_task = scheduler.mark_task_complete(buddy, feeding)
if next_task:
    print(f"Auto-created next occurrence: {next_task.get_details()}")

print("\nBuddy's full task list after completion:")
for task in buddy.get_tasks():
    status = "done" if task.completed else "pending"
    print(f"  [{status}] {task.get_details()}")
