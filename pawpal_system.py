"""
PawPal+ System Logic
A pet care task scheduler for busy pet owners.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
from uuid import uuid4


@dataclass
class Task:
    """Represents a single pet care task."""
    task_type: str
    duration: float  # in minutes
    priority: str  # "high", "medium", "low"
    description: str = ""
    recurring: bool = False
    time_slot: Optional[str] = None
    task_id: str = field(default_factory=lambda: str(uuid4()))
    completed: bool = False
    
    def validate(self) -> bool:
        """Validate task attributes (priority, duration, type)."""
        if self.priority not in ["high", "medium", "low"]:
            return False
        if self.duration <= 0:
            return False
        if self.task_type.strip() == "":
            return False
        return True
    
    def get_duration(self) -> float:
        """Return the duration of the task in minutes."""
        return self.duration
    
    def get_priority_level(self) -> int:
        """Return priority as an integer (3=high, 2=medium, 1=low) for sorting."""
        priority_map = {"high": 3, "medium": 2, "low": 1}
        return priority_map.get(self.priority, 0)
    
    def mark_complete(self) -> None:
        """Mark task as completed."""
        self.completed = True
    
    def mark_incomplete(self) -> None:
        """Mark task as incomplete."""
        self.completed = False


@dataclass
class Pet:
    """Represents a pet that needs care."""
    name: str
    breed: str
    age: int
    tasks: List[Task] = field(default_factory=list)
    
    def get_info(self) -> str:
        """Return a string description of the pet."""
        return f"{self.name} ({self.breed}, {self.age} years old)"
    
    def add_task(self, task: Task) -> bool:
        """Add a task to the pet's list if valid."""
        if not task.validate():
            return False
        self.tasks.append(task)
        return True
    
    def remove_task(self, task_id: str) -> bool:
        """Remove a task by ID."""
        original_length = len(self.tasks)
        self.tasks = [t for t in self.tasks if t.task_id != task_id]
        return len(self.tasks) < original_length
    
    def get_tasks(self) -> List[Task]:
        """Return all tasks for this pet."""
        return self.tasks
    
    def get_pending_tasks(self) -> List[Task]:
        """Return all incomplete tasks for the pet."""
        return [t for t in self.tasks if not t.completed]


@dataclass
class Owner:
    """Represents a pet owner with multiple pets."""
    name: str
    available_hours: float  # in hours
    pets: List[Pet] = field(default_factory=list)
    
    def set_availability(self, hours: float) -> None:
        """Set the owner's available hours for the day."""
        self.available_hours = hours
    
    def get_availability(self) -> float:
        """Get the owner's available hours for the day."""
        return self.available_hours
    
    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's pet list."""
        self.pets.append(pet)
    
    def remove_pet(self, pet_name: str) -> bool:
        """Remove a pet by name."""
        original_length = len(self.pets)
        self.pets = [p for p in self.pets if p.name != pet_name]
        return len(self.pets) < original_length
    
    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks from all owner's pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks
    
    def get_all_pending_tasks(self) -> List[Task]:
        """Retrieve all incomplete tasks from all owner's pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_pending_tasks())
        return all_tasks


@dataclass
class Scheduler:
    """The 'Brain' that retrieves, organizes, and schedules tasks."""
    owner: Owner
    
    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks for the owner."""
        return self.owner.get_all_tasks()
    
    def get_pending_tasks(self) -> List[Task]:
        """Retrieve all incomplete tasks for the owner."""
        return self.owner.get_all_pending_tasks()
    
    def sort_by_priority(self, tasks: Optional[List[Task]] = None) -> List[Task]:
        """Sort tasks by priority (descending) then duration (ascending)."""
        if tasks is None:
            tasks = self.get_pending_tasks()
        return sorted(tasks, key=lambda t: (-t.get_priority_level(), t.duration))
    
    def generate_plan(self, available_minutes: Optional[float] = None) -> List[Task]:
        """Generate daily plan by fitting high-priority tasks within available time."""
        if available_minutes is None:
            available_minutes = self.owner.get_availability() * 60
        
        pending_tasks = self.get_pending_tasks()
        sorted_tasks = self.sort_by_priority(pending_tasks)
        
        planned_tasks = []
        time_used = 0
        
        for task in sorted_tasks:
            if time_used + task.duration <= available_minutes:
                planned_tasks.append(task)
                time_used += task.duration
        
        return planned_tasks
    
    def get_daily_plan(self) -> List[Task]:
        """Get today's schedule."""
        return self.generate_plan()

