# PawPal+ (Module 2 Project)

> An intelligent pet care scheduling assistant that helps busy pet owners plan and manage daily care tasks.

## 🎯 Overview

**PawPal+** is a comprehensive pet care planning system that helps pet owners:
- Track care tasks (walks, feeding, medication, enrichment, grooming, etc.)
- Consider constraints (time available, priority, recurring schedules)
- Produce optimized daily plans with clear explanations
- Detect scheduling conflicts and manage recurring tasks

## ✨ Features

### Core Features
- ✅ **Multi-Pet Management** - Track multiple pets with unique care needs
- ✅ **Task Prioritization** - 5-level priority system (1-5 stars)
- ✅ **Smart Scheduling** - Priority-first algorithm with time constraints
- ✅ **Task Tracking** - Mark tasks complete and regenerate schedules
- ✅ **Transparent Reasoning** - Clear explanations of scheduling decisions

### Smarter Scheduling (Advanced Features)
- ⏰ **Time-Based Scheduling** - Schedule tasks at specific times (HH:MM format)
- 🔄 **Recurring Tasks** - Automatic creation of daily, weekly, and monthly tasks
- ⚠️ **Conflict Detection** - Identify and warn about overlapping tasks
- 📊 **Task Filtering** - Filter by pet, type, completion status, or time
- 📈 **Usage Statistics** - Track time utilization and task completion

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Oseipokuamoafo/ai110-module2show-pawpal-starter.git
   cd ai110-module2show-pawpal-starter
   ```

2. **Create and activate a virtual environment** (recommended)
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 📖 Usage

### Running the Streamlit Web App

Launch the interactive web interface:

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Running the CLI Demo

Try the command-line demo to see all features in action:

```bash
python main.py
```

This demonstrates:
- Owner and pet creation
- Task management
- Schedule generation
- Task filtering
- Conflict detection
- Recurring task handling

## 🧪 Testing PawPal+

### Run All Tests

```bash
python -m pytest
```

### Run Tests with Verbose Output

```bash
python -m pytest -v
```

### Run Tests with Coverage

```bash
python -m pytest --cov=pawpal_system --cov-report=html
```

### Test Coverage

The test suite includes **41 comprehensive tests** covering:

1. **Data Model Tests** (10 tests)
   - Object creation and validation
   - Bidirectional relationships
   - Special behaviors

2. **Scheduling Logic Tests** (8 tests)
   - Task prioritization
   - Time constraint handling
   - Completion status tracking

3. **Query/Filter Tests** (3 tests)
   - Pet-based filtering
   - Type-based filtering
   - Status-based filtering

4. **Time-Based Features** (12 tests)
   - Scheduled time validation
   - End time calculation
   - Time-based sorting
   - Conflict detection (exact, partial, adjacent)
   - Conflict warnings

5. **Recurring Tasks** (7 tests)
   - Daily/weekly/monthly recurrence
   - Automatic instance creation
   - One-time task handling

6. **Integration Tests** (1 test)
   - End-to-end workflow verification

**Confidence Level**: ⭐⭐⭐⭐⭐ (5/5) - All critical paths tested with edge cases covered

## 📊 Architecture

### System Design

PawPal+ follows a clean separation of concerns:

- **Data Layer** (`Owner`, `Pet`, `Task`) - Immutable data objects using Python dataclasses
- **Business Logic** (`Scheduler`) - Handles scheduling algorithms and task management
- **UI Layer** (`app.py`) - Streamlit interface for user interaction
- **CLI Layer** (`main.py`) - Command-line demonstration tool

### Core Classes

#### `Owner`
Represents a pet owner with:
- Name and available daily time
- List of pets
- Preferences for scheduling

#### `Pet`
Represents a pet with:
- Basic info (name, species, age)
- Special needs tracking
- Owner reference

#### `Task`
Represents a care task with:
- Name, duration, and priority (1-5)
- Task type (walk, feed, medication, etc.)
- Optional scheduled time and end time calculation
- Recurring frequency (once, daily, weekly, monthly)
- Completion status

#### `Scheduler`
The "brain" of the system that:
- Manages pets and tasks
- Generates optimized daily plans
- Prioritizes tasks by importance and duration
- Detects time conflicts
- Explains scheduling decisions
- Handles recurring task automation

### Scheduling Algorithm

**Algorithm**: Greedy priority-first with time constraints

**How it works**:
1. Filter to incomplete tasks only
2. Sort by priority (highest → lowest)
3. For equal priority, sort by duration (shortest → longest)
4. Greedily add tasks until time runs out

**Time Complexity**: O(n log n) for sorting, O(n) for scheduling = **O(n log n)** overall

**Trade-offs**:
- ✅ **Pros**: Fast, simple, prioritizes critical tasks, maximizes task count for equal priorities
- ⚠️ **Cons**: Not globally optimal (a perfect-fit combination might be missed)
- 🎯 **Rationale**: Pet care priorities matter more than quantity. A critical medication should never be skipped to fit in play sessions.

## 🎨 UI Features

The Streamlit web app includes:

1. **Owner Setup** - Configure name and available time
2. **Pet Management** - Add pets with special needs
3. **Task Creation** - Create tasks with priority levels
4. **Schedule Generation** - One-click optimized planning
5. **Visual Schedule** - Color-coded priority indicators
6. **Task Completion** - Mark tasks done and regenerate
7. **Explanations** - Clear reasoning for each decision
8. **Statistics Dashboard** - Time utilization and task metrics

## 📁 Project Structure

```
pawpal-starter/
├── pawpal_system.py       # Core logic (Owner, Pet, Task, Scheduler)
├── test_pawpal_system.py  # 41 comprehensive tests
├── app.py                 # Streamlit web interface
├── main.py                # CLI demo script
├── reflection.md          # Detailed project documentation
├── README.md              # This file
└── requirements.txt       # Python dependencies
```

## 🔧 API Reference

### Creating Tasks with Time Scheduling

```python
from pawpal_system import Task, TaskType, Frequency
from datetime import datetime

# Basic task (no specific time)
task1 = Task("Walk dog", 30, 5, TaskType.WALK, my_pet)

# Task with scheduled time
task2 = Task(
    "Morning medication",
    5,
    5,
    TaskType.MEDICATION,
    my_pet,
    scheduled_time="08:00"  # HH:MM format
)

# Recurring daily task
task3 = Task(
    "Daily walk",
    30,
    5,
    TaskType.WALK,
    my_pet,
    frequency=Frequency.DAILY,
    due_date=datetime.now()
)
```

### Detecting Conflicts

```python
scheduler = Scheduler(owner)
scheduler.add_task(task1)
scheduler.add_task(task2)

# Get conflict list
conflicts = scheduler.detect_conflicts()

# Get human-readable warning
warning = scheduler.get_conflict_warnings()
if warning:
    print(warning)
```

### Sorting by Time

```python
# Sort all tasks by scheduled time
sorted_tasks = scheduler.sort_by_time()
# Tasks with scheduled_time come first in chronological order
# Tasks without scheduled_time come last
```

### Handling Recurring Tasks

```python
# Mark task complete and auto-create next instance
new_task = scheduler.mark_task_complete(daily_task)
if new_task:
    print(f"Created next occurrence: {new_task.name} on {new_task.due_date}")
```

## 🎓 Learning Outcomes

This project demonstrates:

1. **System Design** - UML diagrams, class relationships, separation of concerns
2. **Algorithm Design** - Greedy algorithms, sorting, constraint satisfaction
3. **Testing** - Unit tests, integration tests, edge case handling
4. **AI Collaboration** - Using AI for design, implementation, and refinement
5. **Python Best Practices** - Dataclasses, type hints, documentation

## 🤝 Contributing

This is an educational project for AI110 Module 2. While not accepting external contributions, feel free to:
- Fork the repository for your own learning
- Use as a template for similar projects
- Reference in your coursework (with proper attribution)

## 📝 License

This project is created for educational purposes as part of AI110 coursework.

## 🙏 Acknowledgments

- Built with AI assistance (Claude Sonnet 4.5)
- Course: AI110 - AI-Assisted Software Engineering
- Streamlit framework for rapid UI development
- pytest for comprehensive testing

## 📞 Support

For questions or issues:
- Review the [reflection.md](reflection.md) for detailed implementation insights
- Check the test suite for usage examples
- Run `python main.py` for a working demonstration

---

**Built with ❤️ using AI-assisted development | PawPal+ © 2024**
