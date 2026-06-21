import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

# Configure page
st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")
st.title("🐾 PawPal+")

st.markdown(
    """
A pet care planning assistant that helps you schedule tasks for your pet(s) 
based on time availability and priorities.
"""
)

# ============================================================================
# STEP 2: Initialize Session State (Application "Memory")
# ============================================================================
# Streamlit reruns the entire script on every interaction, so we use 
# st.session_state as a persistent "vault" to keep our Owner object alive

def init_session_state():
    """Initialize session state with Owner object if not already present."""
    if "owner" not in st.session_state:
        st.session_state.owner = Owner(name="Pet Owner", available_hours=3.0)
    if "scheduler" not in st.session_state:
        st.session_state.scheduler = Scheduler(owner=st.session_state.owner)

init_session_state()

# ============================================================================
# UI LAYOUT: Owner & Pet Setup
# ============================================================================

st.divider()
st.subheader("1️⃣ Owner Setup")

col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Owner name", value=st.session_state.owner.name, key="owner_name_input")
    if owner_name != st.session_state.owner.name:
        st.session_state.owner.name = owner_name

with col2:
    available_hours = st.number_input(
        "Available hours per day",
        min_value=0.5,
        max_value=24.0,
        value=st.session_state.owner.get_availability(),
        step=0.5,
        key="available_hours_input"
    )
    if available_hours != st.session_state.owner.get_availability():
        st.session_state.owner.set_availability(available_hours)

# ============================================================================
# UI LAYOUT: Pet Management
# ============================================================================

st.divider()
st.subheader("2️⃣ Pet Management")

# Display current pets
if st.session_state.owner.pets:
    st.write(f"**Pets ({len(st.session_state.owner.pets)}):**")
    for pet in st.session_state.owner.pets:
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.write(f"  • {pet.get_info()}")
        with col2:
            st.caption(f"{len(pet.tasks)} tasks")
        with col3:
            if st.button(f"Remove", key=f"remove_pet_{pet.name}"):
                st.session_state.owner.remove_pet(pet.name)
                st.rerun()
else:
    st.info("No pets yet. Add one below.")

# Add new pet
st.markdown("**Add a new pet:**")
col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet name", value="", key="pet_name_input", placeholder="e.g., Biscuit")
with col2:
    breed = st.text_input("Breed", value="", key="breed_input", placeholder="e.g., Golden Retriever")
with col3:
    age = st.number_input("Age (years)", min_value=0, max_value=50, value=1, key="age_input")

if st.button("Add Pet", key="add_pet_btn"):
    if pet_name.strip() == "":
        st.error("Please enter a pet name.")
    else:
        new_pet = Pet(name=pet_name, breed=breed, age=age)
        st.session_state.owner.add_pet(new_pet)
        st.success(f"✓ Added {pet_name}!")
        st.rerun()

# ============================================================================
# UI LAYOUT: Task Management
# ============================================================================

st.divider()
st.subheader("3️⃣ Task Management")

if not st.session_state.owner.pets:
    st.warning("Add a pet first before creating tasks.")
else:
    # Select which pet to add a task to
    pet_options = {pet.name: pet for pet in st.session_state.owner.pets}
    selected_pet_name = st.selectbox("Select pet", list(pet_options.keys()), key="pet_select")
    selected_pet = pet_options[selected_pet_name]
    
    # Display current tasks for this pet
    if selected_pet.tasks:
        st.write(f"**Tasks for {selected_pet.name}:**")
        for task in selected_pet.tasks:
            col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
            with col1:
                status = "✓" if task.completed else "○"
                st.write(f"  {status} {task.task_type}")
            with col2:
                st.caption(f"{int(task.duration)} min")
            with col3:
                st.caption(f"{task.priority}")
            with col4:
                if st.button("Done" if not task.completed else "Undo", key=f"toggle_task_{task.task_id}"):
                    if task.completed:
                        task.mark_incomplete()
                    else:
                        task.mark_complete()
                    st.rerun()
            with col5:
                if st.button("Delete", key=f"delete_task_{task.task_id}"):
                    selected_pet.remove_task(task.task_id)
                    st.rerun()
    else:
        st.info(f"No tasks for {selected_pet.name} yet.")
    
    # Add new task
    st.markdown(f"**Add a task for {selected_pet.name}:**")
    col1, col2, col3 = st.columns(3)
    with col1:
        task_type = st.text_input("Task", value="", key="task_type_input", placeholder="e.g., Morning Walk")
    with col2:
        duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=15, key="duration_input")
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=1, key="priority_select")
    
    description = st.text_input("Description (optional)", value="", key="description_input", placeholder="e.g., Brisk walk in the park")
    
    if st.button("Add Task", key="add_task_btn"):
        if task_type.strip() == "":
            st.error("Please enter a task name.")
        else:
            new_task = Task(
                task_type=task_type,
                duration=duration,
                priority=priority,
                description=description
            )
            if selected_pet.add_task(new_task):
                st.success(f"✓ Added task '{task_type}'!")
                st.rerun()
            else:
                st.error("Invalid task. Please check inputs.")

# ============================================================================
# UI LAYOUT: Schedule Generation
# ============================================================================

st.divider()
st.subheader("4️⃣ Generate Daily Schedule")

available_tasks = st.session_state.owner.get_all_pending_tasks()

if not available_tasks:
    st.info("All tasks completed! Add more tasks or mark some incomplete to generate a schedule.")
else:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(f"**Available pending tasks: {len(available_tasks)}**")
    with col2:
        if st.button("Generate Schedule", key="generate_schedule_btn"):
            st.session_state.generated_plan = st.session_state.scheduler.generate_plan()

# Display the generated plan
if "generated_plan" in st.session_state:
    plan = st.session_state.generated_plan
    
    if not plan:
        st.warning("⚠️ No tasks could fit in the available time.")
    else:
        st.markdown("### 📋 Today's Schedule")
        
        # Calculate totals
        total_time = sum(t.duration for t in plan)
        available_mins = st.session_state.owner.get_availability() * 60
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Tasks Scheduled", len(plan))
        with col2:
            st.metric("Time Used", f"{int(total_time)} min")
        with col3:
            st.metric("Time Available", f"{int(available_mins)} min")
        with col4:
            st.metric("Time Remaining", f"{int(available_mins - total_time)} min")
        
        st.divider()
        
        # Display schedule table
        schedule_data = []
        cumulative_time = 0
        for idx, task in enumerate(plan, 1):
            # Find which pet this task belongs to
            pet_name = "Unknown"
            for pet in st.session_state.owner.pets:
                if task in pet.tasks:
                    pet_name = pet.name
                    break
            
            start_mins = int(cumulative_time)
            start_hours = start_mins // 60
            start_mins_remainder = start_mins % 60
            
            schedule_data.append({
                "Order": idx,
                "Pet": pet_name,
                "Task": task.task_type,
                "Priority": task.priority.upper(),
                "Duration (min)": int(task.duration),
                "Start Time": f"{start_hours:02d}:{start_mins_remainder:02d}",
                "Details": task.description or "-"
            })
            cumulative_time += task.duration
        
        st.dataframe(schedule_data, use_container_width=True)
        
        # Show notes
        st.markdown("### 📝 Notes")
        high_priority = [t for t in plan if t.priority == "high"]
        medium_priority = [t for t in plan if t.priority == "medium"]
        low_priority = [t for t in plan if t.priority == "low"]
        
        notes = [
            f"✓ All {len(high_priority)} high-priority tasks are included.",
            f"✓ {len(medium_priority)} medium-priority tasks fit in the schedule.",
        ]
        if low_priority:
            notes.append(f"✓ {len(low_priority)} low-priority tasks are included.")
        else:
            skipped_low = len([t for t in available_tasks if t.priority == "low" and t not in plan])
            if skipped_low > 0:
                notes.append(f"⚠️ {skipped_low} low-priority tasks were skipped to fit in available time.")
        
        for note in notes:
            st.write(note)

st.divider()
st.caption("PawPal+ v1.0 — Built with Python, Streamlit, and 🐾")
