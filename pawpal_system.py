"""
PawPal+ System - Core Logic Layer

This module contains the main classes for the PawPal+ pet care scheduling system.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum


class TaskType(Enum):
    """Enum for different types of pet care tasks."""
    WALK = "walk"
    FEED = "feed"
    MEDICATION = "medication"
    GROOMING = "grooming"
    ENRICHMENT = "enrichment"
    PLAYTIME = "playtime"
    TRAINING = "training"


@dataclass
class Owner:
    """
    Represents a pet owner with time constraints and preferences.

    Attributes:
        name: Owner's name
        available_time_minutes: Total daily time available for pet care
        preferences: Dictionary of owner preferences (e.g., preferred task times)
        pets: List of pets owned by this owner
    """
    name: str
    available_time_minutes: int
    preferences: Dict[str, any] = field(default_factory=dict)
    pets: List['Pet'] = field(default_factory=list)

    def get_available_time(self) -> int:
        """Returns the available time in minutes."""
        return self.available_time_minutes

    def set_preferences(self, preferences: Dict[str, any]) -> None:
        """Updates owner preferences."""
        self.preferences.update(preferences)

    def add_pet(self, pet: 'Pet') -> None:
        """Adds a pet to this owner's pet list."""
        if pet not in self.pets:
            self.pets.append(pet)
            pet.owner = self


@dataclass
class Pet:
    """
    Represents a pet with basic information and care needs.

    Attributes:
        name: Pet's name
        species: Type of pet (dog, cat, etc.)
        age: Pet's age in years
        special_needs: List of special care requirements
        owner: Reference to the pet's owner
    """
    name: str
    species: str
    age: int
    special_needs: List[str] = field(default_factory=list)
    owner: Optional[Owner] = None

    def get_info(self) -> Dict[str, any]:
        """Returns a dictionary of pet information."""
        return {
            "name": self.name,
            "species": self.species,
            "age": self.age,
            "special_needs": self.special_needs,
            "owner": self.owner.name if self.owner else None
        }

    def add_special_need(self, need: str) -> None:
        """Adds a special care need for the pet."""
        if need and need not in self.special_needs:
            self.special_needs.append(need)


@dataclass
class Task:
    """
    Represents a pet care task with duration and priority.

    Attributes:
        name: Task name/description
        duration_minutes: How long the task takes
        priority: Priority level (1=lowest, 5=highest)
        task_type: Type of task (from TaskType enum)
        pet: Pet
        completed: Whether the task has been completed
    """
    name: str
    duration_minutes: int
    priority: int
    task_type: TaskType
    pet: Pet
    completed: bool = False

    def __post_init__(self):
        """Validates task attributes after initialization."""
        if not 1 <= self.priority <= 5:
            raise ValueError("Priority must be between 1 and 5")
        if self.duration_minutes <= 0:
            raise ValueError("Duration must be positive")

    def mark_complete(self) -> None:
        """Marks the task as completed."""
        self.completed = True

    def get_priority(self) -> int:
        """Returns the task priority."""
        return self.priority

    def get_duration(self) -> int:
        """Returns the task duration in minutes."""
        return self.duration_minutes


class Scheduler:
    """
    Main scheduling engine that generates daily care plans.

    The Scheduler takes owner constraints, pet needs, and task priorities
    to create an optimized daily schedule.

    Attributes:
        owner: The pet owner
        pets: List of pets to schedule care for
        tasks: List of all care tasks
        daily_plan: The generated schedule
    """

    def __init__(self, owner: Owner):
        """Initialize the scheduler with an owner."""
        self.owner = owner
        self.pets: List[Pet] = owner.pets
        self.tasks: List[Task] = []
        self.daily_plan: List[Task] = []

    def add_pet(self, pet: Pet) -> None:
        """Adds a pet to the scheduler."""
        if pet not in self.pets:
            self.pets.append(pet)
            self.owner.add_pet(pet)

    def add_task(self, task: Task) -> None:
        """Adds a task to the scheduler."""
        if task not in self.tasks:
            self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Removes a task from the scheduler."""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks_by_pet(self, pet: Pet) -> List[Task]:
        """Returns all tasks for a specific pet."""
        return [task for task in self.tasks if task.pet == pet]

    def get_tasks_by_type(self, task_type: TaskType) -> List[Task]:
        """Returns all tasks of a specific type."""
        return [task for task in self.tasks if task.task_type == task_type]

    def get_incomplete_tasks(self) -> List[Task]:
        """Returns all incomplete tasks."""
        return [task for task in self.tasks if not task.completed]

    def get_total_scheduled_time(self) -> int:
        """Returns total time of all scheduled tasks in minutes."""
        return sum(task.duration_minutes for task in self.daily_plan)

    def generate_daily_plan(self) -> List[Task]:
        """
        Generates an optimized daily schedule based on constraints.

        Returns:
            List of tasks in scheduled order
        """
        pass

    def prioritize_tasks(self) -> List[Task]:
        """
        Sorts tasks by priority and other criteria.

        Returns:
            List of tasks in priority order
        """
        pass

    def explain_reasoning(self) -> str:
        """
        Provides explanation for scheduling decisions.

        Returns:
            String explaining why tasks were scheduled in this order
        """
        pass

    def get_schedule(self) -> List[Task]:
        """Returns the current daily plan."""
        return self.daily_plan
