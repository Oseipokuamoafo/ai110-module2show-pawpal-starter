"""
PawPal+ CLI Demo Script

This script demonstrates the core functionality of the PawPal+ system
in a terminal environment without the Streamlit UI.
"""

from pawpal_system import Owner, Pet, Task, Scheduler, TaskType


def print_header(text):
    """Print a formatted section header."""
    print(f"\n{'=' * 60}")
    print(f"  {text}")
    print('=' * 60)


def print_task_list(tasks, title="Tasks"):
    """Print a formatted list of tasks."""
    print(f"\n{title}:")
    if not tasks:
        print("  (No tasks)")
        return

    for i, task in enumerate(tasks, 1):
        status = "✅" if task.completed else "⏳"
        print(f"  {i}. {status} {task.name}")
        print(f"     Pet: {task.pet.name} | Duration: {task.duration_minutes} min | "
              f"Priority: {task.priority}/5 {'⭐' * task.priority}")
        print(f"     Type: {task.task_type.value.capitalize()}")


def main():
    """Run the CLI demo."""

    print_header("🐾 PawPal+ CLI Demo")
    print("\nWelcome to PawPal+! Let's set up a pet care schedule.\n")

    # Step 1: Create an owner
    print_header("Step 1: Create Owner")
    owner = Owner(name="Jordan", available_time_minutes=180)
    print(f"✅ Owner created: {owner.name}")
    print(f"   Available time: {owner.available_time_minutes} minutes per day")

    # Step 2: Add pets
    print_header("Step 2: Add Pets")

    dog = Pet(name="Max", species="dog", age=3)
    dog.add_special_need("joint medication")
    owner.add_pet(dog)
    print(f"✅ Added pet: {dog.name} ({dog.species}, age {dog.age})")
    print(f"   Special needs: {', '.join(dog.special_needs)}")

    cat = Pet(name="Luna", species="cat", age=2)
    cat.add_special_need("indoor only")
    owner.add_pet(cat)
    print(f"✅ Added pet: {cat.name} ({cat.species}, age {cat.age})")
    print(f"   Special needs: {', '.join(cat.special_needs)}")

    # Step 3: Create scheduler
    print_header("Step 3: Initialize Scheduler")
    scheduler = Scheduler(owner)
    print(f"✅ Scheduler initialized for {owner.name}")
    print(f"   Managing {len(scheduler.pets)} pets")

    # Step 4: Add tasks (in random order to show sorting later)
    print_header("Step 4: Add Care Tasks")

    tasks_to_add = [
        Task("Evening walk", 45, 4, TaskType.WALK, dog),
        Task("Morning medication", 5, 5, TaskType.MEDICATION, dog),
        Task("Lunch feeding", 10, 5, TaskType.FEED, dog),
        Task("Morning walk", 30, 5, TaskType.WALK, dog),
        Task("Play session", 25, 3, TaskType.PLAYTIME, dog),
        Task("Cat feeding", 10, 5, TaskType.FEED, cat),
        Task("Litter box cleaning", 15, 4, TaskType.GROOMING, cat),
        Task("Cat enrichment", 20, 3, TaskType.ENRICHMENT, cat),
        Task("Dog grooming", 60, 2, TaskType.GROOMING, dog),
    ]

    for task in tasks_to_add:
        scheduler.add_task(task)
        print(f"  ➕ Added: {task.name} ({task.pet.name}) - "
              f"{task.duration_minutes} min, Priority {task.priority}/5")

    print(f"\n✅ Total tasks added: {len(scheduler.tasks)}")

    # Step 5: Show task filtering
    print_header("Step 5: Filter Tasks")

    dog_tasks = scheduler.get_tasks_by_pet(dog)
    print_task_list(dog_tasks, f"Tasks for {dog.name}")

    feed_tasks = scheduler.get_tasks_by_type(TaskType.FEED)
    print_task_list(feed_tasks, "All Feeding Tasks")

    # Step 6: Generate schedule
    print_header("Step 6: Generate Daily Schedule")

    print(f"\nGenerating optimized schedule for {owner.available_time_minutes} minutes...")
    daily_plan = scheduler.generate_daily_plan()

    print(f"\n✅ Schedule generated with {len(daily_plan)} tasks")
    print_task_list(daily_plan, "Today's Schedule")

    # Step 7: Show scheduling explanation
    print_header("Step 7: Scheduling Explanation")
    explanation = scheduler.explain_reasoning()
    print(f"\n{explanation}")

    # Step 8: Mark tasks complete
    print_header("Step 8: Complete Some Tasks")

    if daily_plan:
        # Complete the first two tasks
        daily_plan[0].mark_complete()
        print(f"✅ Completed: {daily_plan[0].name}")

        if len(daily_plan) > 1:
            daily_plan[1].mark_complete()
            print(f"✅ Completed: {daily_plan[1].name}")

        # Show incomplete tasks
        incomplete = scheduler.get_incomplete_tasks()
        print(f"\n📋 Remaining incomplete tasks: {len(incomplete)}")

        # Regenerate schedule
        print("\n🔄 Regenerating schedule with completed tasks excluded...")
        new_plan = scheduler.generate_daily_plan()
        print_task_list(new_plan, "Updated Schedule")

    # Step 9: Show statistics
    print_header("Step 9: Summary Statistics")

    total_tasks = len(scheduler.tasks)
    completed_tasks = len([t for t in scheduler.tasks if t.completed])
    incomplete_tasks = len(scheduler.get_incomplete_tasks())
    scheduled_time = scheduler.get_total_scheduled_time()
    available_time = owner.available_time_minutes
    remaining_time = available_time - scheduled_time

    print(f"""
📊 Task Statistics:
   • Total tasks: {total_tasks}
   • Completed: {completed_tasks}
   • Incomplete: {incomplete_tasks}
   • Scheduled in current plan: {len(scheduler.daily_plan)}

⏰ Time Statistics:
   • Available time: {available_time} minutes
   • Scheduled time: {scheduled_time} minutes
   • Remaining time: {remaining_time} minutes
   • Utilization: {(scheduled_time / available_time * 100):.1f}%

🐾 Pet Statistics:
   • Total pets: {len(scheduler.pets)}
   • {dog.name} tasks: {len(scheduler.get_tasks_by_pet(dog))}
   • {cat.name} tasks: {len(scheduler.get_tasks_by_pet(cat))}
    """)

    print_header("Demo Complete!")
    print("\n✨ PawPal+ successfully demonstrated all core features!")
    print("   • Owner and pet management")
    print("   • Task creation and tracking")
    print("   • Priority-based scheduling")
    print("   • Time constraint handling")
    print("   • Task filtering and completion")
    print("   • Schedule explanations\n")


if __name__ == "__main__":
    main()
