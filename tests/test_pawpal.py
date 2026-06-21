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
