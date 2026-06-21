"""
PawPal+ System Logic
A pet care task scheduler for busy pet owners.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class Owner:
    """Represents a pet owner with their availability."""
    name: str
    available_hours: float
    
    def set_availability(self, hours: float) -> None:
        """Set the owner's available hours for the day."""
        pass
    
    def get_availability(self) -> float:
        """Get the owner's available hours for the day."""
        pass


@dataclass
class Pet:
    """Represents a pet that needs care."""
    name: str
    breed: str
    age: int
    
    def get_info(self) -> str:
        """Return a string description of the pet."""
        pass


@dataclass
class Task:
    """Represents a single pet care task."""
    task_type: str
    duration: float
    priority: str  # "high", "medium", "low"
    recurring: bool = False
    time_slot: Optional[str] = None
    
    def validate(self) -> bool:
        """Validate that task attributes are valid."""
        pass
    
    def get_duration(self) -> float:
        """Return the duration of the task in minutes."""
        pass
    
    def get_priority_level(self) -> int:
        """Return priority as an integer (3=high, 2=medium, 1=low) for sorting."""
        pass


@dataclass
class Schedule:
    """Manages tasks and generates a daily schedule."""
    owner: Owner
    pet: Pet
    tasks: List[Task] = field(default_factory=list)
    daily_plan: List[Task] = field(default_factory=list)
    
    def add_task(self, task: Task) -> None:
        """Add a task to the schedule."""
        pass
    
    def remove_task(self, task_id: str) -> None:
        """Remove a task from the schedule by its ID."""
        pass
    
    def generate_plan(self, date: str) -> List[Task]:
        """Generate an optimized daily plan based on available time and priorities."""
        pass
    
    def get_plan(self) -> List[Task]:
        """Return the current daily plan."""
        pass
    
    def sort_by_priority(self) -> List[Task]:
        """Sort tasks by priority (high to low), then by duration."""
        pass
