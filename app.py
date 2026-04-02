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

        st.success(f"Schedule generated for **{owner_name}** and **{pet_name}**!")
        st.markdown(f"**Available time:** {available_time} min")
        st.markdown(f"**Tasks scheduled:** {len(scheduled)} / {len(st.session_state.tasks)}")

        st.text(scheduler.explain_schedule())

        skipped = [t for t in st.session_state.tasks if t not in scheduled]
        if skipped:
            st.warning(
                "The following tasks were skipped (not enough time): "
                + ", ".join(t.description for t in skipped)
            )
