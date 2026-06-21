"""
Tests for PawPal+ system logic.
"""

import pytest
from pawpal_system import Task, Pet, Owner, Scheduler


class TestTask:
    """Test Task class functionality."""
    
    def test_task_completion(self):
        """Verify that mark_complete() changes task status from incomplete to complete."""
        task = Task(
            task_type="Morning Walk",
            duration=30,
            priority="high",
            description="30-minute walk"
        )
        assert task.completed is False, "Task should start as incomplete"
        task.mark_complete()
        assert task.completed is True, "Task should be marked as complete"
    
    def test_task_incomplete(self):
        """Verify that mark_incomplete() changes task status to incomplete."""
        task = Task(
            task_type="Feeding",
            duration=10,
            priority="high"
        )
        task.mark_complete()
        task.mark_incomplete()
        assert task.completed is False, "Task should be marked as incomplete"
    
    def test_task_validation_valid(self):
        """Verify that a valid task passes validation."""
        task = Task(
            task_type="Play",
            duration=15,
            priority="medium"
        )
        assert task.validate() is True, "Valid task should pass validation"
    
    def test_task_validation_invalid_priority(self):
        """Verify that invalid priority fails validation."""
        task = Task(
            task_type="Play",
            duration=15,
            priority="urgent"  # Invalid priority
        )
        assert task.validate() is False, "Invalid priority should fail validation"
    
    def test_task_validation_invalid_duration(self):
        """Verify that zero or negative duration fails validation."""
        task = Task(
            task_type="Play",
            duration=0,
            priority="medium"
        )
        assert task.validate() is False, "Zero duration should fail validation"
    
    def test_task_priority_level_high(self):
        """Verify priority level mapping for high priority."""
        task = Task(task_type="Walk", duration=30, priority="high")
        assert task.get_priority_level() == 3, "High priority should map to 3"
    
    def test_task_priority_level_medium(self):
        """Verify priority level mapping for medium priority."""
        task = Task(task_type="Walk", duration=30, priority="medium")
        assert task.get_priority_level() == 2, "Medium priority should map to 2"
    
    def test_task_priority_level_low(self):
        """Verify priority level mapping for low priority."""
        task = Task(task_type="Walk", duration=30, priority="low")
        assert task.get_priority_level() == 1, "Low priority should map to 1"


class TestPet:
    """Test Pet class functionality."""
    
    def test_pet_add_task(self):
        """Verify that adding a task to a pet increases task count."""
        pet = Pet(name="Biscuit", breed="Golden Retriever", age=3)
        initial_count = len(pet.tasks)
        assert initial_count == 0, "Pet should start with no tasks"
        
        task = Task(task_type="Walk", duration=30, priority="high")
        result = pet.add_task(task)
        
        assert result is True, "add_task should return True for valid task"
        assert len(pet.tasks) == initial_count + 1, "Task count should increase by 1"
    
    def test_pet_add_multiple_tasks(self):
        """Verify that multiple tasks are added correctly."""
        pet = Pet(name="Luna", breed="Siamese Cat", age=5)
        
        task1 = Task(task_type="Feed", duration=5, priority="high")
        task2 = Task(task_type="Play", duration=15, priority="medium")
        task3 = Task(task_type="Groom", duration=20, priority="low")
        
        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)
        
        assert len(pet.tasks) == 3, "Pet should have 3 tasks"
    
    def test_pet_add_invalid_task(self):
        """Verify that adding an invalid task returns False and doesn't add it."""
        pet = Pet(name="Biscuit", breed="Golden Retriever", age=3)
        
        invalid_task = Task(task_type="Walk", duration=-5, priority="high")
        result = pet.add_task(invalid_task)
        
        assert result is False, "add_task should return False for invalid task"
        assert len(pet.tasks) == 0, "Invalid task should not be added"
    
    def test_pet_remove_task(self):
        """Verify that removing a task decreases task count."""
        pet = Pet(name="Biscuit", breed="Golden Retriever", age=3)
        task = Task(task_type="Walk", duration=30, priority="high")
        pet.add_task(task)
        
        assert len(pet.tasks) == 1, "Pet should have 1 task"
        result = pet.remove_task(task.task_id)
        
        assert result is True, "remove_task should return True"
        assert len(pet.tasks) == 0, "Task should be removed"
    
    def test_pet_get_pending_tasks(self):
        """Verify that pending tasks (incomplete) are retrieved correctly."""
        pet = Pet(name="Biscuit", breed="Golden Retriever", age=3)
        
        task1 = Task(task_type="Walk", duration=30, priority="high")
        task2 = Task(task_type="Feed", duration=10, priority="high")
        
        pet.add_task(task1)
        pet.add_task(task2)
        task1.mark_complete()
        
        pending = pet.get_pending_tasks()
        assert len(pending) == 1, "Should have 1 pending task"
        assert pending[0] == task2, "Pending task should be the incomplete one"
    
    def test_pet_get_info(self):
        """Verify pet info string is formatted correctly."""
        pet = Pet(name="Biscuit", breed="Golden Retriever", age=3)
        info = pet.get_info()
        assert "Biscuit" in info, "Info should contain pet name"
        assert "Golden Retriever" in info, "Info should contain breed"
        assert "3" in info, "Info should contain age"


class TestOwner:
    """Test Owner class functionality."""
    
    def test_owner_add_pet(self):
        """Verify that adding a pet to owner increases pet count."""
        owner = Owner(name="Alice", available_hours=3.0)
        initial_count = len(owner.pets)
        
        pet = Pet(name="Biscuit", breed="Golden Retriever", age=3)
        owner.add_pet(pet)
        
        assert len(owner.pets) == initial_count + 1, "Pet count should increase"
    
    def test_owner_get_all_tasks(self):
        """Verify that all tasks from all pets are retrieved."""
        owner = Owner(name="Alice", available_hours=3.0)
        
        pet1 = Pet(name="Biscuit", breed="Dog", age=3)
        pet2 = Pet(name="Luna", breed="Cat", age=5)
        
        task1 = Task(task_type="Walk", duration=30, priority="high")
        task2 = Task(task_type="Feed", duration=10, priority="high")
        task3 = Task(task_type="Play", duration=15, priority="medium")
        
        pet1.add_task(task1)
        pet1.add_task(task2)
        pet2.add_task(task3)
        
        owner.add_pet(pet1)
        owner.add_pet(pet2)
        
        all_tasks = owner.get_all_tasks()
        assert len(all_tasks) == 3, "Should retrieve all 3 tasks"
    
    def test_owner_availability(self):
        """Verify owner availability can be set and retrieved."""
        owner = Owner(name="Alice", available_hours=3.0)
        assert owner.get_availability() == 3.0, "Initial availability should be 3.0"
        
        owner.set_availability(5.0)
        assert owner.get_availability() == 5.0, "Availability should update"


class TestScheduler:
    """Test Scheduler class functionality."""
    
    def test_scheduler_sort_by_priority(self):
        """Verify tasks are sorted by priority (high to low), then by duration."""
        owner = Owner(name="Alice", available_hours=3.0)
        scheduler = Scheduler(owner=owner)
        
        task1 = Task(task_type="Play", duration=20, priority="medium")
        task2 = Task(task_type="Walk", duration=30, priority="high")
        task3 = Task(task_type="Feed", duration=5, priority="high")
        
        pet = Pet(name="Biscuit", breed="Dog", age=3)
        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)
        owner.add_pet(pet)
        
        sorted_tasks = scheduler.sort_by_priority()
        
        # Should be: Feed (high, 5), Walk (high, 30), Play (medium, 20)
        assert sorted_tasks[0] == task3, "Feed should be first (high priority, shortest)"
        assert sorted_tasks[1] == task2, "Walk should be second (high priority, longer)"
        assert sorted_tasks[2] == task1, "Play should be last (medium priority)"
    
    def test_scheduler_generate_plan_respects_time(self):
        """Verify that generated plan respects available time constraints."""
        owner = Owner(name="Alice", available_hours=1.0)  # 60 minutes
        scheduler = Scheduler(owner=owner)
        
        pet = Pet(name="Biscuit", breed="Dog", age=3)
        task1 = Task(task_type="Walk", duration=30, priority="high")
        task2 = Task(task_type="Feed", duration=10, priority="high")
        task3 = Task(task_type="Play", duration=20, priority="high")
        task4 = Task(task_type="Nap", duration=15, priority="low")
        
        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)
        pet.add_task(task4)
        owner.add_pet(pet)
        
        plan = scheduler.generate_plan()
        
        # Total time = 30 + 10 + 20 = 60 minutes (fits exactly)
        total_time = sum(t.duration for t in plan)
        assert total_time <= 60, "Plan should not exceed available time"
        assert len(plan) == 3, "Should include first 3 high-priority tasks"
    
    def test_scheduler_pending_tasks_only(self):
        """Verify that scheduler only includes pending (incomplete) tasks."""
        owner = Owner(name="Alice", available_hours=3.0)
        scheduler = Scheduler(owner=owner)
        
        pet = Pet(name="Biscuit", breed="Dog", age=3)
        task1 = Task(task_type="Walk", duration=30, priority="high")
        task2 = Task(task_type="Feed", duration=10, priority="high")
        
        pet.add_task(task1)
        pet.add_task(task2)
        task1.mark_complete()
        
        owner.add_pet(pet)
        
        pending = scheduler.get_pending_tasks()
        assert len(pending) == 1, "Should have 1 pending task"
        assert task2 in pending, "Pending task should be the incomplete one"


class TestSmartAlgorithms:
    """Test new smart algorithms: sorting, filtering, conflicts, recurring tasks."""
    
    def test_sort_by_time(self):
        """Verify tasks are sorted by time slot (HH:MM format)."""
        owner = Owner(name="Alice", available_hours=3.0)
        scheduler = Scheduler(owner=owner)
        
        pet = Pet(name="Biscuit", breed="Dog", age=3)
        task1 = Task(task_type="Walk", duration=30, priority="high", time_slot="14:00")
        task2 = Task(task_type="Feed", duration=10, priority="high", time_slot="08:00")
        task3 = Task(task_type="Play", duration=20, priority="medium", time_slot="10:00")
        
        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)
        owner.add_pet(pet)
        
        sorted_tasks = scheduler.sort_by_time()
        
        # Should be: Feed (08:00), Play (10:00), Walk (14:00)
        assert sorted_tasks[0] == task2, "Feed should be first (08:00)"
        assert sorted_tasks[1] == task3, "Play should be second (10:00)"
        assert sorted_tasks[2] == task1, "Walk should be third (14:00)"
    
    def test_filter_by_pet(self):
        """Verify filtering tasks by pet name."""
        owner = Owner(name="Alice", available_hours=3.0)
        scheduler = Scheduler(owner=owner)
        
        dog = Pet(name="Biscuit", breed="Dog", age=3)
        cat = Pet(name="Luna", breed="Cat", age=5)
        
        dog_task = Task(task_type="Walk", duration=30, priority="high")
        cat_task = Task(task_type="Play", duration=15, priority="medium")
        
        dog.add_task(dog_task)
        cat.add_task(cat_task)
        owner.add_pet(dog)
        owner.add_pet(cat)
        
        biscuit_tasks = scheduler.filter_by_pet("Biscuit")
        assert len(biscuit_tasks) == 1, "Should have 1 Biscuit task"
        assert dog_task in biscuit_tasks, "Should contain dog task"
        
        luna_tasks = scheduler.filter_by_pet("Luna")
        assert len(luna_tasks) == 1, "Should have 1 Luna task"
        assert cat_task in luna_tasks, "Should contain cat task"
    
    def test_filter_by_status(self):
        """Verify filtering tasks by completion status."""
        owner = Owner(name="Alice", available_hours=3.0)
        scheduler = Scheduler(owner=owner)
        
        pet = Pet(name="Biscuit", breed="Dog", age=3)
        task1 = Task(task_type="Walk", duration=30, priority="high")
        task2 = Task(task_type="Feed", duration=10, priority="high")
        
        pet.add_task(task1)
        pet.add_task(task2)
        task1.mark_complete()
        owner.add_pet(pet)
        
        completed = scheduler.filter_by_status(completed=True)
        assert len(completed) == 1, "Should have 1 completed task"
        assert task1 in completed, "Should contain completed task"
        
        pending = scheduler.filter_by_status(completed=False)
        assert len(pending) == 1, "Should have 1 pending task"
        assert task2 in pending, "Should contain pending task"
    
    def test_detect_conflicts(self):
        """Verify conflict detection identifies tasks at same time."""
        owner = Owner(name="Alice", available_hours=3.0)
        scheduler = Scheduler(owner=owner)
        
        pet = Pet(name="Biscuit", breed="Dog", age=3)
        task1 = Task(task_type="Walk", duration=30, priority="high", time_slot="08:00")
        task2 = Task(task_type="Feed", duration=10, priority="high", time_slot="08:00")  # Conflict
        task3 = Task(task_type="Play", duration=20, priority="medium", time_slot="08:30")
        
        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)
        owner.add_pet(pet)
        
        conflicts = scheduler.detect_conflicts()
        assert len(conflicts) == 1, "Should detect 1 conflict"
        assert conflicts[0]["time_slot"] == "08:00", "Conflict should be at 08:00"
        assert conflicts[0]["task_count"] == 2, "Should have 2 tasks in conflict"
    
    def test_no_conflicts(self):
        """Verify no false conflicts when times don't overlap."""
        owner = Owner(name="Alice", available_hours=3.0)
        scheduler = Scheduler(owner=owner)
        
        pet = Pet(name="Biscuit", breed="Dog", age=3)
        task1 = Task(task_type="Walk", duration=30, priority="high", time_slot="08:00")
        task2 = Task(task_type="Feed", duration=10, priority="high", time_slot="08:30")
        task3 = Task(task_type="Play", duration=20, priority="medium", time_slot="08:40")
        
        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)
        owner.add_pet(pet)
        
        conflicts = scheduler.detect_conflicts()
        assert len(conflicts) == 0, "Should not detect any conflicts"
    
    def test_recurring_task_generation(self):
        """Verify recurring tasks auto-generate next occurrence."""
        task = Task(
            task_type="Daily Walk",
            duration=30,
            priority="high",
            frequency="daily"
        )
        
        assert task.completed is False, "Task should start incomplete"
        next_task = task.mark_complete()
        
        assert task.completed is True, "Task should be marked complete"
        assert next_task is not None, "Should generate next occurrence"
        assert next_task.task_type == task.task_type, "New task should have same type"
        assert next_task.completed is False, "New task should be incomplete"
        assert next_task.due_date is not None, "New task should have due date"
    
    def test_recurring_weekly_task(self):
        """Verify weekly recurring tasks calculate correct next date."""
        from datetime import datetime, timedelta
        
        today = datetime.now()
        task = Task(
            task_type="Weekly Bath",
            duration=45,
            priority="medium",
            frequency="weekly",
            due_date=today
        )
        
        next_task = task.mark_complete()
        
        assert next_task is not None, "Should generate weekly task"
        expected_date = today + timedelta(weeks=1)
        # Check that next task is approximately a week away (within 1 day tolerance)
        assert abs((next_task.due_date - expected_date).days) <= 1
    
    def test_one_time_task_no_recurrence(self):
        """Verify one-time tasks don't auto-generate."""
        task = Task(
            task_type="Vet Appointment",
            duration=60,
            priority="high",
            frequency="once"
        )
        
        next_task = task.mark_complete()
        
        assert next_task is None, "One-time task should not generate next occurrence"
        assert task.completed is True, "Task should be marked complete"
    
    def test_assign_time_slots(self):
        """Verify time slot assignment calculates correct start times."""
        owner = Owner(name="Alice", available_hours=3.0)
        scheduler = Scheduler(owner=owner)
        
        tasks = [
            Task(task_type="Walk", duration=30, priority="high"),
            Task(task_type="Feed", duration=10, priority="high"),
            Task(task_type="Play", duration=20, priority="medium"),
        ]
        
        assigned = scheduler.assign_time_slots(tasks, start_time="08:00")
        
        assert assigned[0].time_slot == "08:00", "First task should start at 08:00"
        assert assigned[1].time_slot == "08:30", "Second task should start at 08:30"
        assert assigned[2].time_slot == "08:40", "Third task should start at 08:40"
    
    def test_pet_mark_task_complete_with_recurrence(self):
        """Verify pet's mark_task_complete auto-adds next occurrence."""
        pet = Pet(name="Biscuit", breed="Dog", age=3)
        
        task = Task(
            task_type="Daily Feeding",
            duration=10,
            priority="high",
            frequency="daily"
        )
        pet.add_task(task)
        
        assert len(pet.tasks) == 1, "Should have 1 task initially"
        next_task = pet.mark_task_complete(task.task_id)
        
        assert next_task is not None, "Should return next task"
        assert len(pet.tasks) == 2, "Should have 2 tasks after recurrence"
        assert pet.tasks[1].completed is False, "New task should be incomplete"
