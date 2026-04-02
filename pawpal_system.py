from dataclasses import dataclass


@dataclass
class Pet:
    name: str
    species: str


@dataclass
class Task:
    description: str
    duration: int       # in minutes
    priority: str       # e.g. "high", "medium", "low"

    def is_high_priority(self) -> bool:
        pass


class Owner:
    def __init__(self, name: str, available_time: int):
        self.name: str = name
        self.available_time: int = available_time   # in minutes
        self.pets: list[Pet] = []
        self.tasks: list[Task] = []

    def add_pet(self, pet: Pet) -> None:
        pass

    def add_task(self, task: Task) -> None:
        pass

    def get_available_time(self) -> int:
        pass


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner: Owner = owner
        self.tasks: list[Task] = []

    def generate_schedule(self) -> list[Task]:
        pass

    def explain_schedule(self) -> str:
        pass
