import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# --- Session state init ---
if "owner" not in st.session_state:
    st.session_state.owner = None
if "pet" not in st.session_state:
    st.session_state.pet = None

# --- Owner + Pet setup ---
st.subheader("Owner & Pet Info")
col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Owner name", value="Jordan")
    time_available = st.number_input("Time available today (minutes)", min_value=10, max_value=480, value=60)
with col2:
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    breed = st.text_input("Breed", value="Mixed")

if st.button("Save owner & pet"):
    pet = Pet(name=pet_name, breed=breed, species=species)
    st.session_state.owner = Owner(name=owner_name, time_available=int(time_available), pet=pet)
    st.session_state.pet = pet
    st.success(f"Saved! {owner_name} owns {pet_name} the {species}.")

st.divider()

# --- Add tasks ---
st.subheader("Tasks")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

col4, col5 = st.columns(2)
with col4:
    scheduled_time = st.text_input("Scheduled time (HH:MM, optional)", value="", placeholder="e.g. 08:00")
with col5:
    recurrence = st.selectbox("Recurrence", ["none", "daily", "weekly"])

if st.button("Add task"):
    if st.session_state.pet is None:
        st.warning("Save your owner & pet info first.")
    else:
        # Validate time format if provided
        time_val = scheduled_time.strip() or None
        if time_val:
            try:
                h, m = time_val.split(":")
                assert 0 <= int(h) <= 23 and 0 <= int(m) <= 59
            except (ValueError, AssertionError):
                st.error("Invalid time format. Use HH:MM (e.g. 08:30).")
                st.stop()

        recur_val = None if recurrence == "none" else recurrence
        st.session_state.pet.add_task(Task(
            task_name=task_title,
            duration=int(duration),
            priority=priority,
            scheduled_time=time_val,
            recurrence=recur_val,
        ))
        st.success(f"Added: {task_title}")

# --- Task list with pending/completed split and mark-complete buttons ---
if st.session_state.pet and st.session_state.pet.get_tasks():
    pending = st.session_state.pet.get_pending_tasks()
    completed = st.session_state.pet.get_completed_tasks()

    if pending:
        st.write("**Pending tasks:**")
        for i, task in enumerate(st.session_state.pet.get_tasks()):
            if task.completed:
                continue
            cols = st.columns([3, 1, 1, 1, 1])
            cols[0].write(task.task_name)
            cols[1].write(f"{task.duration} min")
            cols[2].write(task.priority)
            cols[3].write(task.scheduled_time or "—")
            cols[4].write(task.recurrence or "—")
            if st.button("Done", key=f"done_{i}"):
                task.mark_complete()
                st.rerun()

    if completed:
        st.write("**Completed tasks:**")
        st.table([
            {"Task": t.task_name, "Duration": t.duration, "Priority": t.priority,
             "Time": t.scheduled_time or "—", "Recurrence": t.recurrence or "—"}
            for t in completed
        ])

    # Recurring reset button
    if completed and any(t.recurrence for t in completed):
        if st.button("Reset recurring tasks (next day)"):
            scheduler = Scheduler()
            scheduler.reset_recurring_tasks(st.session_state.pet)
            st.success("Recurring tasks reset for the next day.")
            st.rerun()
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# --- Generate schedule ---
st.subheader("Build Schedule")

if st.button("Generate schedule"):
    if st.session_state.owner is None or st.session_state.pet is None:
        st.warning("Save your owner & pet info first.")
    elif not st.session_state.pet.get_pending_tasks():
        st.warning("No pending tasks to schedule.")
    else:
        scheduler = Scheduler()
        plan = scheduler.generate_plan(st.session_state.owner, st.session_state.pet)
        if not plan:
            st.error("No tasks fit within the available time.")
        else:
            st.success(f"Today's plan for {st.session_state.pet.name}:")
            for task in plan:
                time_str = f" at {task.scheduled_time}" if task.scheduled_time else ""
                recur_str = f" [{task.recurrence}]" if task.recurrence else ""
                st.markdown(f"- **{task.task_name}**{time_str} — {task.duration} min ({task.priority} priority){recur_str}")

            # Conflict detection
            conflicts = scheduler.detect_conflicts(plan)
            if conflicts:
                st.warning("Scheduling conflicts detected:")
                for a, b in conflicts:
                    st.write(f"- **{a.task_name}** ({a.scheduled_time}, {a.duration} min) overlaps with **{b.task_name}** ({b.scheduled_time}, {b.duration} min)")

            skipped = [t for t in st.session_state.pet.get_pending_tasks() if t not in plan]
            if skipped:
                st.caption("Skipped (didn't fit in time): " + ", ".join(t.task_name for t in skipped))
