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
    """
    name: str
    available_time_minutes: int
    preferences: Dict[str, any] = field(default_factory=dict)

    def get_available_time(self) -> int:
        """Returns the available time in minutes."""
        pass

    def set_preferences(self, preferences: Dict[str, any]) -> None:
        """Updates owner preferences."""
        pass


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
        pass

    def add_special_need(self, need: str) -> None:
        """Adds a special care need for the pet."""
        pass


@dataclass
class Task:
    """
    Represents a pet care task with duration and priority.

    Attributes:
        name: Task name/description
        duration_minutes: How long the task takes
        priority: Priority level (1=lowest, 5=highest)
        task_type: Type of task (from TaskType enum)
        pet: The pet this task is for
        completed: Whether the task has been completed
    """
    name: str
    duration_minutes: int
    priority: int
    task_type: TaskType
    pet: Pet
    completed: bool = False

    def mark_complete(self) -> None:
        """Marks the task as completed."""
        pass

    def get_priority(self) -> int:
        """Returns the task priority."""
        pass

    def get_duration(self) -> int:
        """Returns the task duration in minutes."""
        pass


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
        self.pets: List[Pet] = []
        self.tasks: List[Task] = []
        self.daily_plan: List[Task] = []

    def add_task(self, task: Task) -> None:
        """Adds a task to the scheduler."""
        pass

    def remove_task(self, task: Task) -> None:
        """Removes a task from the scheduler."""
        pass

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
        pass
