import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import date
from pawpal_system import Task, Pet, Owner, Scheduler


def test_mark_complete_changes_status():
    task = Task(description="Walk dog", duration=30, priority="high", frequency="daily")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Buddy", species="dog")
    assert len(pet.tasks) == 0
    task = Task(description="Feed", duration=10, priority="medium", frequency="daily")
    pet.add_task(task)
    assert len(pet.tasks) == 1


def test_sort_by_time_returns_chronological_order():
    owner = Owner(name="Alice", available_time=120)
    pet = Pet(name="Max", species="dog")
    owner.add_pet(pet)

    pet.add_task(Task(description="Evening walk", duration=30, priority="low", frequency="daily", time="18:00"))
    pet.add_task(Task(description="Morning feed", duration=10, priority="high", frequency="daily", time="07:30"))
    pet.add_task(Task(description="Noon meds", duration=5, priority="medium", frequency="daily", time="12:00"))

    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time()

    times = [t.time for t in sorted_tasks]
    assert times == sorted(times), f"Expected chronological order, got {times}"


def test_mark_complete_daily_creates_next_day_task():
    owner = Owner(name="Alice", available_time=120)
    pet = Pet(name="Max", species="dog")
    owner.add_pet(pet)

    today = date(2026, 4, 1)
    task = Task(description="Walk", duration=20, priority="high", frequency="daily", due_date=today)
    pet.add_task(task)

    scheduler = Scheduler(owner)
    next_task = scheduler.mark_task_complete(task)

    assert task.completed is True
    assert next_task is not None
    assert next_task.due_date == date(2026, 4, 2)
    assert next_task.completed is False
    assert next_task.description == task.description


def test_detect_conflicts_flags_duplicate_times():
    owner = Owner(name="Alice", available_time=120)
    pet = Pet(name="Max", species="dog")
    owner.add_pet(pet)

    pet.add_task(Task(description="Walk", duration=20, priority="high", frequency="daily", time="08:00"))
    pet.add_task(Task(description="Feed", duration=10, priority="medium", frequency="daily", time="08:00"))
    pet.add_task(Task(description="Meds", duration=5, priority="low", frequency="daily", time="12:00"))

    scheduler = Scheduler(owner)
    warnings = scheduler.detect_conflicts()

    assert len(warnings) == 1, f"Expected 1 conflict, got {len(warnings)}"
    assert "08:00" in warnings[0]
