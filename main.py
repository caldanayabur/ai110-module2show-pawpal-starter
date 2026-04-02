from pawpal_system import Owner, Pet, Task, Scheduler

# Create owner
owner = Owner(name="Carolina", available_time=120)  # 120 minutes available today

# Create pets
buddy = Pet(name="Buddy", species="Dog")
whiskers = Pet(name="Whiskers", species="Cat")

# Add tasks OUT OF ORDER (mixed times across both pets)
whiskers.add_task(Task(description="Playtime",         duration=20, priority="medium", frequency="daily",   time="15:00"))
buddy.add_task(   Task(description="Evening walk",     duration=30, priority="high",   frequency="daily",   time="18:30"))
buddy.add_task(   Task(description="Feed breakfast",   duration=10, priority="high",   frequency="daily",   time="07:30"))
whiskers.add_task(Task(description="Clean litter box", duration=10, priority="high",   frequency="daily",   time="08:00"))
buddy.add_task(   Task(description="Morning walk",     duration=30, priority="high",   frequency="daily",   time="07:00"))
whiskers.add_task(Task(description="Vet check-up",     duration=60, priority="low",    frequency="monthly", time="11:00"))
buddy.add_task(   Task(description="Brush coat",       duration=15, priority="medium", frequency="weekly",  time="09:30"))

# Mark a couple of tasks complete to demo the filter
buddy.get_tasks()[2].mark_complete()      # Feed breakfast -> done (direct, no scheduler yet)
whiskers.get_tasks()[0].mark_complete()   # Playtime -> done (direct, no scheduler yet)

# Register pets with owner
owner.add_pet(buddy)
owner.add_pet(whiskers)

# Build schedule
scheduler = Scheduler(owner)
scheduler.generate_schedule()

# ── Original schedule ────────────────────────────────────────────────────────
print("=" * 45)
print("         PawPal+ - Today's Schedule")
print("=" * 45)
print(f"Owner : {owner.name}")
print(f"Pets  : {', '.join(p.name for p in owner.pets)}")
print(f"Time available : {owner.available_time} min")
print("-" * 45)
print(scheduler.explain_schedule())
print("-" * 45)
scheduled_minutes = sum(t.duration for t in scheduler.schedule)
print(f"Time remaining after schedule: {owner.available_time - scheduled_minutes} min")

# ── sort_by_time() ───────────────────────────────────────────────────────────
print("\n" + "=" * 45)
print("       All Tasks Sorted by Time")
print("=" * 45)
for task in scheduler.sort_by_time():
    status = "done" if task.completed else "todo"
    print(f"  {task.time}  [{status}]  {task.pet_name:10s}  {task.description}")

# ── filter_tasks() — pending tasks only ─────────────────────────────────────
print("\n" + "=" * 45)
print("       Pending Tasks (not completed)")
print("=" * 45)
for task in scheduler.filter_tasks(completed=False):
    print(f"  [{task.pet_name}] {task.description} @ {task.time}")

# ── filter_tasks() — completed tasks only ───────────────────────────────────
print("\n" + "=" * 45)
print("       Completed Tasks")
print("=" * 45)
for task in scheduler.filter_tasks(completed=True):
    print(f"  [{task.pet_name}] {task.description} @ {task.time}")

# ── filter_tasks() — tasks for Buddy only ────────────────────────────────────
print("\n" + "=" * 45)
print("       Tasks for Buddy")
print("=" * 45)
for task in scheduler.filter_tasks(pet_name="Buddy"):
    status = "done" if task.completed else "todo"
    print(f"  [{status}] {task.description} @ {task.time}")

# ── filter_tasks() — Whiskers's pending tasks ────────────────────────────────
print("\n" + "=" * 45)
print("       Whiskers's Pending Tasks")
print("=" * 45)
for task in scheduler.filter_tasks(completed=False, pet_name="Whiskers"):
    print(f"  {task.description} @ {task.time}")

print("=" * 45)

# ── mark_task_complete() — auto-recurring demo ───────────────────────────────
print("\n" + "=" * 45)
print("  Auto-Recurring: mark_task_complete()")
print("=" * 45)

evening_walk = buddy.get_tasks()[1]   # Evening walk (daily)
brush_coat   = buddy.get_tasks()[3]   # Brush coat   (weekly)

next_walk  = scheduler.mark_task_complete(evening_walk)
next_brush = scheduler.mark_task_complete(brush_coat)

if next_walk:
    print(f"  'Evening walk' completed. Next occurrence due: {next_walk.due_date}")
if next_brush:
    print(f"  'Brush coat' completed.   Next occurrence due: {next_brush.due_date}")

print("=" * 45)
