import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to **PawPal+** — a pet care planning assistant.
Fill in the owner and pet info below, add tasks, then generate a schedule.
"""
)

st.divider()

st.subheader("Owner & Pet Info")
col_o, col_t = st.columns(2)
with col_o:
    owner_name = st.text_input("Owner name", value="Jordan")
    available_time = st.number_input(
        "Available time (minutes/day)", min_value=1, max_value=1440, value=120
    )
with col_t:
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])

st.divider()

st.subheader("Tasks")

# Session state holds Task objects
if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task description", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
with col4:
    frequency = st.selectbox("Frequency", ["daily", "weekly", "monthly"])

if st.button("Add task"):
    new_task = Task(
        description=task_title,
        duration=int(duration),
        priority=priority,
        frequency=frequency,
    )
    st.session_state.tasks.append(new_task)
    st.success(f"Task '{task_title}' added!")

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(
        [
            {
                "Description": t.description,
                "Duration (min)": t.duration,
                "Priority": t.priority,
                "Frequency": t.frequency,
                "Completed": t.completed,
            }
            for t in st.session_state.tasks
        ]
    )
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")

if st.button("Generate schedule"):
    if not st.session_state.tasks:
        st.warning("Add at least one task before generating a schedule.")
    else:
        # Build the object graph from current session state
        pet = Pet(name=pet_name, species=species)
        for task in st.session_state.tasks:
            pet.add_task(task)

        owner = Owner(name=owner_name, available_time=int(available_time))
        owner.add_pet(pet)

        scheduler = Scheduler(owner)
        scheduled = scheduler.generate_schedule()

        # ── Conflict warnings (shown first so the owner sees them immediately) ──
        conflicts = scheduler.detect_conflicts()
        if conflicts:
            st.error("⚠️ Scheduling Conflicts Detected", icon="🚨")
            for conflict in conflicts:
                # Strip the "WARNING: " prefix since the UI already signals urgency
                message = conflict.replace("WARNING: ", "")
                st.warning(message)
            st.markdown(
                "**Tip:** Assign different times to conflicting tasks so your "
                "pet's care routine runs smoothly."
            )
            st.divider()

        # ── Summary banner ──
        total = len(st.session_state.tasks)
        skipped = [t for t in st.session_state.tasks if t not in scheduled]
        if not skipped:
            st.success(
                f"All {total} tasks fit within {owner_name}'s {available_time}-minute day!"
            )
        else:
            st.success(
                f"Schedule generated for **{owner_name}** and **{pet_name}** — "
                f"{len(scheduled)} of {total} tasks scheduled."
            )

        # ── Scheduled tasks table (sorted by priority via generate_schedule) ──
        st.subheader("Today's Schedule")
        priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}
        st.table(
            [
                {
                    "Time": t.time,
                    "Task": t.description,
                    "Duration (min)": t.duration,
                    "Priority": f"{priority_emoji.get(t.priority, '')} {t.priority}",
                    "Frequency": t.frequency,
                }
                for t in scheduler.sort_by_time()
                if t in scheduled
            ]
        )

        # ── Skipped tasks ──
        if skipped:
            st.warning(
                "**Not enough time for:** "
                + ", ".join(f"*{t.description}*" for t in skipped)
                + f"  \nConsider reducing task durations or increasing available time "
                f"(currently {available_time} min)."
            )

        # ── Pending (incomplete) tasks filtered view ──
        pending = scheduler.filter_tasks(completed=False)
        if pending:
            with st.expander(f"View all pending tasks ({len(pending)})"):
                st.table(
                    [
                        {
                            "Task": t.description,
                            "Pet": t.pet_name,
                            "Duration (min)": t.duration,
                            "Priority": f"{priority_emoji.get(t.priority, '')} {t.priority}",
                            "Frequency": t.frequency,
                        }
                        for t in pending
                    ]
                )
