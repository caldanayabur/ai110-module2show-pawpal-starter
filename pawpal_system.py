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
        pass

    def mark_complete(self) -> None:
        pass


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def get_tasks(self) -> list[Task]:
        pass


class Owner:
    def __init__(self, name: str, available_time: int):
        self.name: str = name
        self.available_time: int = available_time   # total minutes available per day
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        pass

    def get_all_tasks(self) -> list[Task]:
        """Return all tasks across all pets."""
        pass

    def get_available_time(self) -> int:
        """Return remaining minutes after accounting for all scheduled tasks."""
        pass


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner: Owner = owner
        self.schedule: list[Task] = []

    def generate_schedule(self) -> list[Task]:
        """Build and store a schedule from the owner's tasks within available time."""
        pass

    def explain_schedule(self) -> str:
        """Return a human-readable explanation of self.schedule."""
        pass
