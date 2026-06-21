"""
Demo script for PawPal+ system logic.
Creates sample owner, pets, and tasks, then generates a daily schedule.
"""

from pawpal_system import Owner, Pet, Task, Scheduler


def print_schedule(scheduler: Scheduler, title: str = "Today's Schedule"):
    """Print a formatted schedule to the terminal."""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    
    plan = scheduler.get_daily_plan()
    
    if not plan:
        print("No tasks scheduled for today.")
        return
    
    total_time = 0
    for idx, task in enumerate(plan, 1):
        pet_name = "Unknown"
        for pet in scheduler.owner.pets:
            if task in pet.tasks:
                pet_name = pet.name
                break
        
        status = "✓ DONE" if task.completed else "○ TODO"
        print(f"\n{idx}. [{status}] {task.task_type.upper()}")
        print(f"   Pet: {pet_name}")
        print(f"   Duration: {task.duration} min | Priority: {task.priority}")
        if task.description:
            print(f"   Details: {task.description}")
        total_time += task.duration
    
    print(f"\n{'-'*60}")
    print(f"Total time needed: {total_time} minutes ({total_time/60:.1f} hours)")
    available = scheduler.owner.get_availability() * 60
    print(f"Available time: {available} minutes ({available/60:.1f} hours)")
    if total_time <= available:
        print("✓ All scheduled tasks fit within available time!")
    else:
        print(f"⚠ Tasks exceed available time by {total_time - available} minutes")
    print(f"{'='*60}\n")


def main():
    """Run the demo script."""
    
    # Create an owner
    owner = Owner(name="Alice", available_hours=3.0)
    print(f"Owner: {owner.name} (available: {owner.get_availability()} hours)")
    
    # Create pets
    biscuit = Pet(name="Biscuit", breed="Golden Retriever", age=3)
    luna = Pet(name="Luna", breed="Siamese Cat", age=5)
    owner.add_pet(biscuit)
    owner.add_pet(luna)
    print(f"\nPets: {biscuit.get_info()}, {luna.get_info()}")
    
    # Create and add tasks to Biscuit
    task1 = Task(
        task_type="Morning Walk",
        duration=30,
        priority="high",
        description="Brisk walk in the park"
    )
    task2 = Task(
        task_type="Feeding",
        duration=10,
        priority="high",
        description="Breakfast meal"
    )
    task3 = Task(
        task_type="Play Session",
        duration=20,
        priority="medium",
        description="Fetch with tennis ball"
    )
    
    # Create and add tasks to Luna
    task4 = Task(
        task_type="Feeding",
        duration=5,
        priority="high",
        description="Breakfast kibble"
    )
    task5 = Task(
        task_type="Litter Box Cleaning",
        duration=10,
        priority="high",
        description="Clean and refill litter box"
    )
    task6 = Task(
        task_type="Play with Toy",
        duration=15,
        priority="medium",
        description="Interactive wand toy"
    )
    
    # Add tasks to pets
    biscuit.add_task(task1)
    biscuit.add_task(task2)
    biscuit.add_task(task3)
    luna.add_task(task4)
    luna.add_task(task5)
    luna.add_task(task6)
    
    print(f"\nAdded {len(biscuit.tasks)} tasks to {biscuit.name}")
    print(f"Added {len(luna.tasks)} tasks to {luna.name}")
    
    # Create scheduler and generate plan
    scheduler = Scheduler(owner=owner)
    
    # Print all tasks
    all_tasks = scheduler.get_all_tasks()
    print(f"\nTotal tasks in system: {len(all_tasks)}")
    
    # Print sorted by priority
    print("\nTasks sorted by priority:")
    sorted_tasks = scheduler.sort_by_priority()
    for task in sorted_tasks:
        print(f"  - {task.task_type} ({task.priority}, {task.duration} min)")
    
    # Print the daily schedule
    print_schedule(scheduler, f"Daily Plan for {owner.name}")
    
    # Mark a task complete and reprint
    print("Marking 'Morning Walk' as complete...")
    task1.mark_complete()
    print_schedule(scheduler, f"Daily Plan for {owner.name} (Updated)")


if __name__ == "__main__":
    main()
