from pawpal_system import Owner, Pet, Task, Scheduler

# --- Setup ---
buddy = Pet(name="Buddy", breed="Labrador", species="Dog")
whiskers = Pet(name="Whiskers", breed="Tabby", species="Cat")

buddy.add_task(Task(task_name="Morning Walk", duration=30, priority=3))
buddy.add_task(Task(task_name="Feeding", duration=10, priority=5))
buddy.add_task(Task(task_name="Enrichment Play", duration=20, priority=2))

whiskers.add_task(Task(task_name="Feeding", duration=5, priority=5))
whiskers.add_task(Task(task_name="Grooming", duration=15, priority=3))
whiskers.add_task(Task(task_name="Litter Box", duration=10, priority=4))

owners = [
    Owner(name="Jordan", time_available=60, pet=buddy),
    Owner(name="Jordan", time_available=60, pet=whiskers),
]
scheduler = Scheduler()

# --- Run Plans ---
for owner in owners:
    plan = scheduler.generate_plan(owner, owner.pet)
    print(f"\n--- Today's Schedule for {owner.pet.name} ---")
    if not plan:
        print("  No tasks fit within the available time.")
    for task in plan:
        print(f"  {task.get_details()}")
