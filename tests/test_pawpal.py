from pawpal_system import Task, Pet


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
