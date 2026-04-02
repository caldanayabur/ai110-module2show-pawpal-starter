from pawpal_system import Owner, Pet, Task, Scheduler

# Create owner
owner = Owner(name="Carolina", available_time=120)  # 120 minutes available today

# Create pets
buddy = Pet(name="Buddy", species="Dog")
whiskers = Pet(name="Whiskers", species="Cat")

# Add tasks to Buddy (dog)
buddy.add_task(Task(description="Morning walk",       duration=30, priority="high",   frequency="daily"))
buddy.add_task(Task(description="Feed breakfast",     duration=10, priority="high",   frequency="daily"))
buddy.add_task(Task(description="Brush coat",         duration=15, priority="medium", frequency="weekly"))

# Add tasks to Whiskers (cat)
whiskers.add_task(Task(description="Clean litter box", duration=10, priority="high",   frequency="daily"))
whiskers.add_task(Task(description="Playtime",         duration=20, priority="medium", frequency="daily"))
whiskers.add_task(Task(description="Vet check-up",     duration=60, priority="low",    frequency="monthly"))

# Register pets with owner
owner.add_pet(buddy)
owner.add_pet(whiskers)

# Build schedule
scheduler = Scheduler(owner)
scheduler.generate_schedule()

# Print Today's Schedule
print("=" * 40)
print("       PawPal+ - Today's Schedule")
print("=" * 40)
print(f"Owner : {owner.name}")
print(f"Pets  : {', '.join(p.name for p in owner.pets)}")
print(f"Time available : {owner.available_time} min")
print("-" * 40)
print(scheduler.explain_schedule())
print("-" * 40)
scheduled_minutes = sum(t.duration for t in scheduler.schedule)
print(f"Time remaining after schedule: {owner.available_time - scheduled_minutes} min")
print("=" * 40)
