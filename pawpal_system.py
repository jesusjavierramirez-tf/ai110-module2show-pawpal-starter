"""
PawPal+ System Logic
A pet care task scheduler for busy pet owners.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple
from datetime import datetime, timedelta
from uuid import uuid4


@dataclass
class Task:
    """Represents a single pet care task."""
    task_type: str
    duration: float  # in minutes
    priority: str  # "high", "medium", "low"
    description: str = ""
    frequency: str = "once"  # "once", "daily", "weekly"
    time_slot: Optional[str] = None  # "HH:MM" format
    task_id: str = field(default_factory=lambda: str(uuid4()))
    completed: bool = False
    due_date: Optional[datetime] = None
    
    def validate(self) -> bool:
        """Validate task attributes (priority, duration, type)."""
        if self.priority not in ["high", "medium", "low"]:
            return False
        if self.duration <= 0:
            return False
        if self.task_type.strip() == "":
            return False
        if self.frequency not in ["once", "daily", "weekly"]:
            return False
        if self.time_slot is not None:
            # Validate HH:MM format
            try:
                h, m = self.time_slot.split(":")
                h, m = int(h), int(m)
                if not (0 <= h < 24 and 0 <= m < 60):
                    return False
            except (ValueError, AttributeError):
                return False
        return True
    
    def get_duration(self) -> float:
        """Return the duration of the task in minutes."""
        return self.duration
    
    def get_priority_level(self) -> int:
        """Return priority as an integer (3=high, 2=medium, 1=low) for sorting."""
        priority_map = {"high": 3, "medium": 2, "low": 1}
        return priority_map.get(self.priority, 0)
    
    def get_time_slot_minutes(self) -> int:
        """Convert HH:MM time slot to minutes since midnight for sorting."""
        if self.time_slot is None:
            return 0
        try:
            h, m = map(int, self.time_slot.split(":"))
            return h * 60 + m
        except (ValueError, AttributeError):
            return 0
    
    def mark_complete(self) -> Optional["Task"]:
        """Mark task as completed and return recurring instance if applicable."""
        self.completed = True
        # Generate next recurring task if applicable
        if self.frequency in ["daily", "weekly"]:
            return self._generate_next_occurrence()
        return None
    
    def _generate_next_occurrence(self) -> "Task":
        """Create a new task for the next occurrence (daily or weekly)."""
        next_due = self.due_date or datetime.now()
        if self.frequency == "daily":
            next_due = next_due + timedelta(days=1)
        elif self.frequency == "weekly":
            next_due = next_due + timedelta(weeks=1)
        
        return Task(
            task_type=self.task_type,
            duration=self.duration,
            priority=self.priority,
            description=self.description,
            frequency=self.frequency,
            time_slot=self.time_slot,
            completed=False,
            due_date=next_due
        )
    
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
    
    def mark_task_complete(self, task_id: str) -> Optional[Task]:
        """
        Mark a task as complete and auto-schedule next occurrence if recurring.
        Returns the new recurring task if one was created, otherwise None.
        """
        for task in self.tasks:
            if task.task_id == task_id:
                next_task = task.mark_complete()
                if next_task:
                    self.tasks.append(next_task)
                return next_task
        return None


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
    
    def sort_by_time(self, tasks: Optional[List[Task]] = None) -> List[Task]:
        """Sort tasks by scheduled time slot (HH:MM format, earliest first)."""
        if tasks is None:
            tasks = self.get_pending_tasks()
        # Tasks without time slots appear first, then sorted by time
        return sorted(tasks, key=lambda t: (t.get_time_slot_minutes(),))
    
    def filter_by_pet(self, pet_name: str) -> List[Task]:
        """Filter tasks belonging to a specific pet."""
        for pet in self.owner.pets:
            if pet.name == pet_name:
                return pet.get_pending_tasks()
        return []
    
    def filter_by_status(self, completed: bool = False) -> List[Task]:
        """Filter tasks by completion status (True for completed, False for pending)."""
        all_tasks = self.owner.get_all_tasks()
        return [t for t in all_tasks if t.completed == completed]
    
    def detect_conflicts(self) -> List[Dict]:
        """
        Detect tasks scheduled at the same time.
        Returns list of conflict dictionaries with task pairs and suggested solutions.
        """
        conflicts = []
        tasks_with_times = [t for t in self.get_pending_tasks() if t.time_slot]
        
        # Group tasks by time slot
        time_groups: Dict[str, List[Task]] = {}
        for task in tasks_with_times:
            if task.time_slot not in time_groups:
                time_groups[task.time_slot] = []
            time_groups[task.time_slot].append(task)
        
        # Find conflicts (multiple tasks at same time)
        for time_slot, tasks in time_groups.items():
            if len(tasks) > 1:
                pet_names = []
                for task in tasks:
                    for pet in self.owner.pets:
                        if task in pet.tasks:
                            pet_names.append(pet.name)
                            break
                
                conflicts.append({
                    "time_slot": time_slot,
                    "task_count": len(tasks),
                    "tasks": [t.task_type for t in tasks],
                    "pets": pet_names,
                    "warning": f"⚠️  {len(tasks)} tasks scheduled at {time_slot}: {', '.join([t.task_type for t in tasks])}"
                })
        
        return conflicts
    
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
    
    def assign_time_slots(self, tasks: List[Task], start_time: str = "08:00") -> List[Task]:
        """
        Assign time slots to tasks based on their order and durations.
        Returns tasks with updated time_slot fields.
        """
        try:
            start_h, start_m = map(int, start_time.split(":"))
            current_minutes = start_h * 60 + start_m
            
            for task in tasks:
                hours = current_minutes // 60
                minutes = current_minutes % 60
                task.time_slot = f"{hours:02d}:{minutes:02d}"
                current_minutes += int(task.duration)
            
            return tasks
        except (ValueError, AttributeError):
            # If start_time format is invalid, return unchanged tasks
            return tasks

