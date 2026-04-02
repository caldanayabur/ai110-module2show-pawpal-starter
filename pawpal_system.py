from dataclasses import dataclass, field
from typing import Literal


@dataclass
class Task:
    description: str
    duration: int                               # in minutes
    priority: Literal["high", "medium", "low"]
    frequency: str                              # e.g. "daily", "weekly"
    completed: bool = False

    def is_high_priority(self) -> bool:
        """Return True if the task's priority is 'high'."""
        return self.priority == "high"

    def mark_complete(self) -> None:
        """Mark the task as completed by setting completed to True."""
        self.completed = True


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Append a Task to this pet's task list."""
        self.tasks.append(task)

    def get_tasks(self) -> list[Task]:
        """Return the list of tasks assigned to this pet."""
        return self.tasks


class Owner:
    def __init__(self, name: str, available_time: int):
        self.name: str = name
        self.available_time: int = available_time   # total minutes available per day
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a Pet to this owner's pet list."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        """Return all tasks across all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks

    def get_available_time(self) -> int:
        """Return remaining minutes after accounting for all scheduled tasks."""
        used = sum(task.duration for task in self.get_all_tasks())
        return self.available_time - used


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner: Owner = owner
        self.schedule: list[Task] = []

    def generate_schedule(self) -> list[Task]:
        """Build and store a schedule from the owner's tasks within available time."""
        all_tasks = self.owner.get_all_tasks()
        priority_order = {"high": 0, "medium": 1, "low": 2}
        sorted_tasks = sorted(all_tasks, key=lambda t: priority_order[t.priority])

        self.schedule = []
        time_remaining = self.owner.available_time
        for task in sorted_tasks:
            if task.duration <= time_remaining:
                self.schedule.append(task)
                time_remaining -= task.duration
        return self.schedule

    def explain_schedule(self) -> str:
        """Return a human-readable explanation of self.schedule."""
        if not self.schedule:
            return "No tasks scheduled."
        lines = []
        for task in self.schedule:
            status = "x" if task.completed else " "
            lines.append(
                f"  [{status}] {task.description} - {task.duration} min "
                f"({task.priority} priority, {task.frequency})"
            )
        return "\n".join(lines)
