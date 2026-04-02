from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Literal


@dataclass
class Task:
    description: str
    duration: int                               # in minutes
    priority: Literal["high", "medium", "low"]
    frequency: str                              # e.g. "daily", "weekly"
    time: str = "00:00"                         # scheduled time, "HH:MM" (24-hour)
    pet_name: str = ""                          # name of the pet this task belongs to
    completed: bool = False
    due_date: date = field(default_factory=date.today)

    def is_high_priority(self) -> bool:
        """Return True if the task's priority is 'high'."""
        return self.priority == "high"

    def mark_complete(self) -> None:
        """Mark the task as completed by setting completed to True."""
        self.completed = True

    def create_next_occurrence(self) -> "Task | None":
        """Return a fresh, incomplete copy of this task due at the next occurrence.

        Uses timedelta to calculate the next due_date:
          - "daily"  → due_date + timedelta(days=1)
          - "weekly" → due_date + timedelta(weeks=1)
        Returns None for any other frequency (e.g. "monthly").
        """
        if self.frequency == "daily":
            next_due = self.due_date + timedelta(days=1)
        elif self.frequency == "weekly":
            next_due = self.due_date + timedelta(weeks=1)
        else:
            return None

        return Task(
            description=self.description,
            duration=self.duration,
            priority=self.priority,
            frequency=self.frequency,
            time=self.time,
            pet_name=self.pet_name,
            completed=False,
            due_date=next_due,
        )


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Append a Task to this pet's task list, tagging it with this pet's name."""
        task.pet_name = self.name
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
        """Return remaining minutes after accounting for scheduled (incomplete) tasks."""
        used = sum(task.duration for task in self.get_all_tasks() if not task.completed)
        return self.available_time - used


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner: Owner = owner
        self.schedule: list[Task] = []

    def mark_task_complete(self, task: Task) -> "Task | None":
        """Mark *task* complete and, if it is daily/weekly, auto-schedule the next occurrence.

        Finds the Pet that owns the task, marks it done, then calls
        create_next_occurrence().  If a next occurrence is produced it is
        appended to the same pet's task list and returned; otherwise None is
        returned.
        """
        task.mark_complete()

        next_task = task.create_next_occurrence()
        if next_task is None:
            return None

        # Find the pet that owns this task and add the new occurrence to it.
        for pet in self.owner.pets:
            if pet.name == task.pet_name:
                pet.add_task(next_task)
                break

        return next_task

    def generate_schedule(self) -> list[Task]:
        """Build and store a schedule using a greedy priority-first algorithm.

        Algorithm:
            1. Collect all incomplete tasks from every pet owned by the owner.
            2. Sort them by priority: high (0) → medium (1) → low (2).
            3. Greedily iterate through the sorted list and add each task to the
               schedule only if its duration fits within the remaining available
               time budget.  Tasks that do not fit are skipped entirely (no
               splitting or rescheduling).
            4. The resulting schedule is stored in ``self.schedule`` and returned.

        Returns:
            list[Task]: Tasks selected for today's schedule, ordered by priority.
                        The list may be empty if no tasks fit the time budget.
        """
        all_tasks = self.owner.get_all_tasks()
        priority_order = {"high": 0, "medium": 1, "low": 2}
        sorted_tasks = sorted(
            (t for t in all_tasks if not t.completed),
            key=lambda t: priority_order[t.priority],
        )

        self.schedule = []
        time_remaining = self.owner.available_time
        for task in sorted_tasks:
            if task.duration <= time_remaining:
                self.schedule.append(task)
                time_remaining -= task.duration
        return self.schedule

    def sort_by_time(self) -> list[Task]:
        """Return all owner tasks sorted chronologically by their scheduled time.

        Algorithm:
            Retrieves all tasks across every pet and applies Python's built-in
            ``sorted()`` using each task's ``time`` string (``"HH:MM"`` 24-hour
            format) as the sort key.  Because ``"HH:MM"`` strings compare
            lexicographically in the same order as their numeric values, no
            datetime parsing is required — string comparison is both correct and
            efficient (O(n log n)).

        Returns:
            list[Task]: All tasks in ascending chronological order (midnight first,
                        23:59 last).  The original task list is not modified.
        """
        all_tasks = self.owner.get_all_tasks()
        return sorted(all_tasks, key=lambda t: t.time)

    def filter_tasks(
        self,
        completed: bool | None = None,
        pet_name: str | None = None,
    ) -> list[Task]:
        """Return tasks filtered by completion status and/or pet name.

        Algorithm:
            Starts with the full flat task list from ``owner.get_all_tasks()``,
            then applies up to two independent list-comprehension passes:

            1. **Completion filter** (applied first if ``completed`` is not None):
               keeps only tasks whose ``task.completed`` matches the given boolean.
            2. **Pet filter** (applied second if ``pet_name`` is not None):
               keeps only tasks whose ``task.pet_name`` matches case-insensitively.

            Either, both, or neither filter may be active in a single call.

        Args:
            completed (bool | None): ``True`` → finished tasks only,
                ``False`` → pending tasks only, ``None`` → no status filter.
            pet_name (str | None): Restrict results to this pet's tasks
                (case-insensitive match).  ``None`` includes all pets.

        Returns:
            list[Task]: Tasks that pass all active filters.  May be empty.
        """
        tasks = self.owner.get_all_tasks()
        if completed is not None:
            tasks = [t for t in tasks if t.completed == completed]
        if pet_name is not None:
            tasks = [t for t in tasks if t.pet_name.lower() == pet_name.lower()]
        return tasks

    def detect_conflicts(self) -> list[str]:
        """Detect scheduling conflicts and return human-readable warning messages.

        Algorithm:
            1. Build a ``defaultdict(list)`` that maps each ``"HH:MM"`` time slot
               to every task scheduled at that time.
            2. Iterate over the slots in sorted (chronological) order.
            3. Any slot with two or more tasks is a conflict — generate one warning
               string listing all conflicting task descriptions and their pet names.
            4. Return the collected warnings; an empty list means no conflicts.

            Time complexity: O(n log n) where n is the total number of tasks
            (dominated by the sort over time slots).

        Returns:
            list[str]: One warning string per conflicting time slot, in
                       chronological order.  Empty list if there are no conflicts.
        """
        from collections import defaultdict

        by_time: dict[str, list[Task]] = defaultdict(list)
        for task in self.owner.get_all_tasks():
            by_time[task.time].append(task)

        warnings: list[str] = []
        for time_slot, tasks in sorted(by_time.items()):
            if len(tasks) > 1:
                names = ", ".join(
                    f"'{t.description}' ({t.pet_name})" for t in tasks
                )
                warnings.append(
                    f"WARNING: Conflict at {time_slot} — {names} overlap."
                )
        return warnings

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
