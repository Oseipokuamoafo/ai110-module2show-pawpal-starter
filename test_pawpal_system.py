"""
Tests for PawPal+ System

This module contains comprehensive tests for the scheduling logic.
"""

import pytest
from pawpal_system import Owner, Pet, Task, Scheduler, TaskType


class TestOwner:
    """Tests for Owner class."""

    def test_owner_creation(self):
        """Test creating an owner with basic attributes."""
        owner = Owner(name="Alice", available_time_minutes=180)
        assert owner.name == "Alice"
        assert owner.available_time_minutes == 180
        assert len(owner.pets) == 0

    def test_owner_add_pet(self):
        """Test adding pets to an owner."""
        owner = Owner(name="Bob", available_time_minutes=240)
        pet = Pet(name="Max", species="dog", age=3)
        owner.add_pet(pet)

        assert len(owner.pets) == 1
        assert pet in owner.pets
        assert pet.owner == owner

    def test_owner_preferences(self):
        """Test setting and updating owner preferences."""
        owner = Owner(name="Carol", available_time_minutes=120)
        owner.set_preferences({"morning_person": True, "prefers_walks": True})

        assert owner.preferences["morning_person"] is True
        assert owner.preferences["prefers_walks"] is True


class TestPet:
    """Tests for Pet class."""

    def test_pet_creation(self):
        """Test creating a pet with basic attributes."""
        pet = Pet(name="Luna", species="cat", age=2)
        assert pet.name == "Luna"
        assert pet.species == "cat"
        assert pet.age == 2
        assert len(pet.special_needs) == 0

    def test_pet_special_needs(self):
        """Test adding special needs to a pet."""
        pet = Pet(name="Charlie", species="dog", age=5)
        pet.add_special_need("medication")
        pet.add_special_need("gentle exercise")

        assert len(pet.special_needs) == 2
        assert "medication" in pet.special_needs

        # Test no duplicates
        pet.add_special_need("medication")
        assert len(pet.special_needs) == 2

    def test_pet_get_info(self):
        """Test getting pet information."""
        owner = Owner(name="Dave", available_time_minutes=200)
        pet = Pet(name="Buddy", species="dog", age=4, owner=owner)

        info = pet.get_info()
        assert info["name"] == "Buddy"
        assert info["species"] == "dog"
        assert info["age"] == 4
        assert info["owner"] == "Dave"


class TestTask:
    """Tests for Task class."""

    def test_task_creation(self):
        """Test creating a task with valid attributes."""
        pet = Pet(name="Mochi", species="cat", age=1)
        task = Task(
            name="Morning feed",
            duration_minutes=10,
            priority=5,
            task_type=TaskType.FEED,
            pet=pet
        )

        assert task.name == "Morning feed"
        assert task.duration_minutes == 10
        assert task.priority == 5
        assert task.completed is False

    def test_task_validation_priority(self):
        """Test that invalid priority raises an error."""
        pet = Pet(name="Rex", species="dog", age=3)

        with pytest.raises(ValueError, match="Priority must be between 1 and 5"):
            Task(
                name="Walk",
                duration_minutes=30,
                priority=6,
                task_type=TaskType.WALK,
                pet=pet
            )

    def test_task_validation_duration(self):
        """Test that invalid duration raises an error."""
        pet = Pet(name="Whiskers", species="cat", age=2)

        with pytest.raises(ValueError, match="Duration must be positive"):
            Task(
                name="Play",
                duration_minutes=0,
                priority=3,
                task_type=TaskType.PLAYTIME,
                pet=pet
            )

    def test_task_mark_complete(self):
        """Test marking a task as complete."""
        pet = Pet(name="Bella", species="dog", age=5)
        task = Task(
            name="Medication",
            duration_minutes=5,
            priority=5,
            task_type=TaskType.MEDICATION,
            pet=pet
        )

        assert task.completed is False
        task.mark_complete()
        assert task.completed is True


class TestScheduler:
    """Tests for Scheduler class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.owner = Owner(name="Jordan", available_time_minutes=120)
        self.pet1 = Pet(name="Max", species="dog", age=3)
        self.pet2 = Pet(name="Luna", species="cat", age=2)
        self.owner.add_pet(self.pet1)
        self.owner.add_pet(self.pet2)
        self.scheduler = Scheduler(self.owner)

    def test_scheduler_creation(self):
        """Test creating a scheduler."""
        assert self.scheduler.owner == self.owner
        assert len(self.scheduler.pets) == 2
        assert len(self.scheduler.tasks) == 0

    def test_add_task(self):
        """Test adding tasks to the scheduler."""
        task = Task(
            name="Morning walk",
            duration_minutes=30,
            priority=4,
            task_type=TaskType.WALK,
            pet=self.pet1
        )
        self.scheduler.add_task(task)

        assert len(self.scheduler.tasks) == 1
        assert task in self.scheduler.tasks

    def test_prioritize_tasks(self):
        """Test that tasks are prioritized correctly."""
        # Create tasks with different priorities
        task1 = Task("Low priority", 20, 1, TaskType.PLAYTIME, self.pet1)
        task2 = Task("High priority", 15, 5, TaskType.MEDICATION, self.pet1)
        task3 = Task("Medium priority", 25, 3, TaskType.WALK, self.pet1)
        task4 = Task("High priority short", 10, 5, TaskType.FEED, self.pet1)

        self.scheduler.add_task(task1)
        self.scheduler.add_task(task2)
        self.scheduler.add_task(task3)
        self.scheduler.add_task(task4)

        prioritized = self.scheduler.prioritize_tasks()

        # Check order: highest priority first, shorter duration for equal priorities
        assert prioritized[0].priority == 5
        assert prioritized[1].priority == 5
        assert prioritized[0].duration_minutes < prioritized[1].duration_minutes
        assert prioritized[2].priority == 3
        assert prioritized[3].priority == 1

    def test_generate_daily_plan_within_time(self):
        """Test schedule generation with sufficient time."""
        task1 = Task("Walk", 30, 5, TaskType.WALK, self.pet1)
        task2 = Task("Feed", 10, 5, TaskType.FEED, self.pet1)
        task3 = Task("Play", 20, 3, TaskType.PLAYTIME, self.pet1)

        self.scheduler.add_task(task1)
        self.scheduler.add_task(task2)
        self.scheduler.add_task(task3)

        plan = self.scheduler.generate_daily_plan()

        # All tasks should fit (total 60 minutes, available 120)
        assert len(plan) == 3
        assert self.scheduler.get_total_scheduled_time() == 60

    def test_generate_daily_plan_exceeds_time(self):
        """Test schedule generation when tasks exceed available time."""
        # Total tasks: 150 minutes, available: 120 minutes
        task1 = Task("Long walk", 60, 5, TaskType.WALK, self.pet1)
        task2 = Task("Feed", 10, 4, TaskType.FEED, self.pet1)
        task3 = Task("Play", 40, 3, TaskType.PLAYTIME, self.pet1)
        task4 = Task("Grooming", 40, 2, TaskType.GROOMING, self.pet1)

        self.scheduler.add_task(task1)
        self.scheduler.add_task(task2)
        self.scheduler.add_task(task3)
        self.scheduler.add_task(task4)

        plan = self.scheduler.generate_daily_plan()

        # Should prioritize and fit within time
        assert self.scheduler.get_total_scheduled_time() <= 120
        assert len(plan) < 4  # Not all tasks will fit

        # Highest priority tasks should be included
        assert task1 in plan  # priority 5
        assert task2 in plan  # priority 4

    def test_generate_daily_plan_completed_tasks_excluded(self):
        """Test that completed tasks are excluded from scheduling."""
        task1 = Task("Walk", 30, 5, TaskType.WALK, self.pet1)
        task2 = Task("Feed", 10, 5, TaskType.FEED, self.pet1)
        task1.mark_complete()

        self.scheduler.add_task(task1)
        self.scheduler.add_task(task2)

        plan = self.scheduler.generate_daily_plan()

        # Only incomplete task should be scheduled
        assert len(plan) == 1
        assert task2 in plan
        assert task1 not in plan

    def test_get_tasks_by_pet(self):
        """Test filtering tasks by pet."""
        task1 = Task("Walk dog", 30, 4, TaskType.WALK, self.pet1)
        task2 = Task("Feed cat", 10, 5, TaskType.FEED, self.pet2)
        task3 = Task("Play with dog", 20, 3, TaskType.PLAYTIME, self.pet1)

        self.scheduler.add_task(task1)
        self.scheduler.add_task(task2)
        self.scheduler.add_task(task3)

        dog_tasks = self.scheduler.get_tasks_by_pet(self.pet1)
        cat_tasks = self.scheduler.get_tasks_by_pet(self.pet2)

        assert len(dog_tasks) == 2
        assert len(cat_tasks) == 1
        assert task1 in dog_tasks
        assert task3 in dog_tasks
        assert task2 in cat_tasks

    def test_get_tasks_by_type(self):
        """Test filtering tasks by type."""
        task1 = Task("Walk", 30, 4, TaskType.WALK, self.pet1)
        task2 = Task("Feed cat", 10, 5, TaskType.FEED, self.pet2)
        task3 = Task("Feed dog", 10, 5, TaskType.FEED, self.pet1)

        self.scheduler.add_task(task1)
        self.scheduler.add_task(task2)
        self.scheduler.add_task(task3)

        feed_tasks = self.scheduler.get_tasks_by_type(TaskType.FEED)
        walk_tasks = self.scheduler.get_tasks_by_type(TaskType.WALK)

        assert len(feed_tasks) == 2
        assert len(walk_tasks) == 1

    def test_explain_reasoning_no_plan(self):
        """Test explanation when no plan exists."""
        explanation = self.scheduler.explain_reasoning()
        assert "No tasks have been scheduled" in explanation

    def test_explain_reasoning_with_plan(self):
        """Test explanation after generating a plan."""
        task1 = Task("Walk", 30, 5, TaskType.WALK, self.pet1)
        task2 = Task("Feed", 10, 4, TaskType.FEED, self.pet1)

        self.scheduler.add_task(task1)
        self.scheduler.add_task(task2)
        self.scheduler.generate_daily_plan()

        explanation = self.scheduler.explain_reasoning()

        assert "Jordan" in explanation
        assert "Scheduled 2" in explanation
        assert "Walk" in explanation
        assert "Feed" in explanation
        assert "Priority" in explanation

    def test_empty_schedule(self):
        """Test behavior with no tasks."""
        plan = self.scheduler.generate_daily_plan()
        assert len(plan) == 0
        assert self.scheduler.get_total_scheduled_time() == 0

    def test_zero_available_time(self):
        """Test schedule generation with zero available time."""
        owner = Owner(name="Busy Person", available_time_minutes=0)
        scheduler = Scheduler(owner)
        pet = Pet(name="Spot", species="dog", age=2)
        owner.add_pet(pet)

        task = Task("Walk", 30, 5, TaskType.WALK, pet)
        scheduler.add_task(task)

        plan = scheduler.generate_daily_plan()
        assert len(plan) == 0


class TestIntegration:
    """Integration tests for complete workflows."""

    def test_complete_workflow(self):
        """Test a complete workflow from owner creation to scheduling."""
        # Create owner
        owner = Owner(name="Sarah", available_time_minutes=180)
        owner.set_preferences({"morning_person": True})

        # Create pets
        dog = Pet(name="Rex", species="dog", age=4)
        cat = Pet(name="Mittens", species="cat", age=2)
        dog.add_special_need("joint medication")

        owner.add_pet(dog)
        owner.add_pet(cat)

        # Create scheduler
        scheduler = Scheduler(owner)

        # Add tasks
        tasks = [
            Task("Morning walk", 45, 5, TaskType.WALK, dog),
            Task("Dog medication", 5, 5, TaskType.MEDICATION, dog),
            Task("Feed dog", 10, 5, TaskType.FEED, dog),
            Task("Feed cat", 10, 5, TaskType.FEED, cat),
            Task("Play with dog", 30, 3, TaskType.PLAYTIME, dog),
            Task("Cat enrichment", 20, 3, TaskType.ENRICHMENT, cat),
            Task("Evening walk", 45, 4, TaskType.WALK, dog),
            Task("Grooming", 60, 2, TaskType.GROOMING, dog),
        ]

        for task in tasks:
            scheduler.add_task(task)

        # Generate plan
        plan = scheduler.generate_daily_plan()

        # Verify results
        assert len(plan) > 0
        assert scheduler.get_total_scheduled_time() <= 180

        # High priority tasks should be in plan
        task_names = [task.name for task in plan]
        assert "Dog medication" in task_names  # Critical priority 5

        # Get explanation
        explanation = scheduler.explain_reasoning()
        assert len(explanation) > 0
        assert "Sarah" in explanation

        # Complete a task
        plan[0].mark_complete()
        assert plan[0].completed is True

        # Generate new plan should exclude completed task
        new_plan = scheduler.generate_daily_plan()
        assert plan[0] not in new_plan
