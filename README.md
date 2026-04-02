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

## Smarter Scheduling

PawPal+ goes beyond a simple to-do list with three algorithmic features built
into the `Scheduler` class:

### Priority-first schedule generation
`generate_schedule()` uses a **greedy algorithm** to build today's plan.
Incomplete tasks are sorted high → medium → low priority, then added to the
schedule one by one as long as they fit inside the owner's available-time
budget.  Higher-priority tasks are always considered first, so critical care
(e.g. medication) is never bumped by optional grooming.

### Chronological task sorting
`sort_by_time()` returns every task in **ascending time order** (00:00 → 23:59).
Because tasks store their time as a zero-padded `"HH:MM"` string, plain
lexicographic comparison produces the correct chronological order without
any datetime parsing overhead.

### Conflict detection
`detect_conflicts()` scans all scheduled tasks and flags any **time-slot
collisions** — two or more tasks assigned to the exact same `"HH:MM"` slot.
It returns a plain-English warning for each conflict (e.g.
`WARNING: Conflict at 08:00 — 'Morning Walk' (Max), 'Medication' (Luna) overlap.`)
so the UI can surface them to the owner before the day begins.

### Flexible filtering
`filter_tasks()` accepts optional `completed` and `pet_name` parameters,
making it easy to show only pending tasks, tasks for a specific pet, or any
combination — without touching the underlying data.

---

## Features

### Priority-Based Schedule Generation
The `Scheduler.generate_schedule()` method uses a **greedy priority-first algorithm** to build a daily schedule. It collects all incomplete tasks across every pet, sorts them by priority (`high → medium → low`) using a numeric weight map, then iterates through the sorted list and adds each task only if its duration fits within the owner's remaining time budget. Tasks that exceed the remaining time are skipped entirely — no splitting or rescheduling occurs. Time complexity: O(n log n).

### Chronological Task Sorting
`Scheduler.sort_by_time()` returns all tasks across all pets sorted in ascending order by their scheduled time. Tasks store time as `"HH:MM"` 24-hour strings, which compare correctly with Python's built-in lexicographic sort — no datetime parsing is required. Time complexity: O(n log n).

### Multi-Criteria Task Filtering
`Scheduler.filter_tasks()` supports up to two independent filters applied in sequence:
1. **Completion filter** — keep only completed or only pending tasks (or neither).
2. **Pet filter** — restrict results to a specific pet by name (case-insensitive match).

Either, both, or neither filter may be active in a single call, making the method composable for any view the UI needs.

### Scheduling Conflict Detection
`Scheduler.detect_conflicts()` finds time-slot collisions across all pets. It builds a `defaultdict` mapping each `"HH:MM"` time slot to the tasks assigned there, then iterates in chronological order and flags any slot with two or more tasks as a conflict. Each warning names every overlapping task and its pet. Returns an empty list when no conflicts exist. Time complexity: O(n log n).

### Automatic Task Recurrence
`Scheduler.mark_task_complete()` marks a task done and automatically schedules its next occurrence for recurring tasks. Internally it calls `Task.create_next_occurrence()`, which uses `timedelta` to compute the next due date — `+1 day` for daily tasks, `+1 week` for weekly tasks. The new task is appended directly to the owning pet's task list and returned. Monthly tasks (and any unknown frequency) return `None` — no next occurrence is created.

### Time-Budget Tracking
`Owner.get_available_time()` computes remaining daily time by summing the duration of all incomplete tasks across all pets and subtracting from the owner's declared available minutes. This gives the Scheduler a live budget it can check before adding each task during schedule generation.

---

## Testing PawPal+

### Run the tests

```bash
python -m pytest tests/test_pawpal.py -v
```

### What the tests cover

| Test | Description |
|---|---|
| `test_mark_complete_changes_status` | Verifies that calling `mark_complete()` on a task flips its `completed` flag from `False` to `True`. |
| `test_add_task_increases_pet_task_count` | Confirms that `Pet.add_task()` appends to the pet's task list correctly. |
| `test_sort_by_time_returns_chronological_order` | Ensures `Scheduler.sort_by_time()` returns tasks ordered earliest to latest by their `"HH:MM"` time string. |
| `test_mark_complete_daily_creates_next_day_task` | Confirms that completing a `"daily"` task auto-generates a new, incomplete copy due the following day. |
| `test_detect_conflicts_flags_duplicate_times` | Verifies that `Scheduler.detect_conflicts()` produces exactly one warning when two tasks share the same time slot, and none for unique slots. |

### Confidence Level

**4 / 5 stars**

The core scheduling behaviors — task completion, recurrence, chronological sorting, and conflict detection — are all covered and passing. The remaining gap is integration-level coverage (e.g. the Streamlit UI layer and edge cases like monthly recurrence or an empty schedule), which would round out a full 5-star confidence rating.

---

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

---

## 📸 Demo

<a href="/course_images/ai110/demo.png" target="_blank"><img src='/course_images/ai110/demo.png' width='100%'></a>
