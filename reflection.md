# PawPal+ Project Reflection

## 1. System Design

### Core User Actions

The PawPal+ system enables users to:

1. **Add and manage pets** - Users can register their pets with basic information including name, type, and specific care needs.

2. **Create and edit care tasks** - Users can add various care tasks (walks, feeding, medications, grooming, enrichment) with attributes like duration, priority level, and frequency.

3. **Generate a daily care schedule** - The system creates an optimized daily plan that fits tasks into available time slots, respecting priorities and constraints, and explains the reasoning behind task selection and ordering.

**a. Initial design**

The initial UML design includes four main classes:

1. **Owner** (dataclass) - Holds owner information including name, available daily time in minutes, and preferences. Responsible for managing owner-specific constraints.

2. **Pet** (dataclass) - Represents a pet with attributes like name, species, age, and special needs. Maintains a reference to its owner. Responsible for storing pet-specific information.

3. **Task** (dataclass) - Represents individual care tasks with name, duration, priority (1-5), task type (walk, feed, meds, etc.), and completion status. Each task is associated with a specific pet.

4. **Scheduler** (class) - The main logic engine that manages the owner, pets, and tasks. Responsible for generating optimized daily plans, prioritizing tasks based on constraints, and explaining scheduling decisions.

**Key design decisions:**
- Used Python dataclasses for data-holding objects (Owner, Pet, Task) for cleaner, more concise code
- Separated data (Owner, Pet, Task) from logic (Scheduler) for better maintainability
- Created a TaskType enum to standardize task categories
- Established clear relationships: Owner owns Pets, Pets have Tasks, Scheduler orchestrates everything

**b. Design changes**

Yes, the design was refined based on AI review feedback. Key changes include:

1. **Added bidirectional Owner-Pet relationship**: Added a `pets` list to the `Owner` class and an `add_pet()` method that maintains consistency on both sides. This prevents the asymmetry where pets knew their owner but owners had no list of their pets. This is essential for the Scheduler to access all pets through the owner.

2. **Implemented Task validation**: Added `__post_init__()` method to the `Task` dataclass to validate that priority is between 1-5 and duration is positive. This prevents invalid data from entering the system and causing scheduling errors.

3. **Added pet management to Scheduler**: Included `add_pet()` method in the Scheduler class to manage the pet list. The Scheduler now initializes its pet list from the owner's pets, maintaining a single source of truth.

4. **Added task filtering methods**: Implemented `get_tasks_by_pet()`, `get_tasks_by_type()`, and `get_incomplete_tasks()` to support the UI and scheduling logic. These methods will be essential for displaying tasks and generating schedules.

5. **Added time tracking**: Implemented `get_total_scheduled_time()` method to track how much time has been scheduled vs. the owner's available time. This is critical for the core constraint-based scheduling.

6. **Implemented simple dataclass methods**: Converted stub methods like `mark_complete()`, `get_info()`, and `add_special_need()` into working implementations. These provide immediate utility without adding complexity.

**Rationale**: These changes address potential logic bottlenecks identified during review, improve data integrity through validation, and add essential helper methods that will be needed for scheduling and UI integration.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers three main constraints:

1. **Time Constraint** - The owner's available daily time (in minutes) is the hard constraint. No schedule can exceed this limit.

2. **Task Priority** - Each task has a priority from 1 (lowest) to 5 (highest). The scheduler sorts tasks by priority first, ensuring critical tasks like medication are scheduled before optional tasks like grooming.

3. **Task Completion Status** - Only incomplete tasks are considered for scheduling. Once a task is marked complete, it's automatically excluded from future schedules.

**Decision rationale**: I prioritized these constraints because they directly impact pet health and owner feasibility. Time is non-negotiable (you can't add more hours to a day), priority ensures critical care isn't missed, and completion status prevents redundant work.

**b. Tradeoffs**

The scheduler makes a key tradeoff: **maximizing high-priority tasks vs. maximizing total tasks scheduled**.

The current implementation uses a **greedy priority-first algorithm** that:
- First sorts by priority (highest to lowest)
- Then sorts by duration (shortest to longest) for tasks with equal priority
- Fills the schedule until time runs out

**Tradeoff example**: If you have:
- Task A: 60 minutes, priority 5
- Task B: 30 minutes, priority 4
- Task C: 30 minutes, priority 4
- Available time: 90 minutes

The scheduler will choose A + B (or A + C), not B + C, even though B + C would fit perfectly and give you 2 completed tasks instead of just filling leftover time.

**Why this is reasonable**: Pet care priorities matter more than quantity. A critical medication (priority 5) should never be skipped just to fit in two play sessions (priority 3). The secondary sort by duration helps fit more tasks when priorities are equal, balancing both concerns.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI tools (Claude Code) throughout multiple phases:

1. **Design Phase** - Asked AI to create a Mermaid UML class diagram from my class descriptions. This helped visualize relationships and spot missing connections (like the bidirectional Owner-Pet relationship).

2. **Implementation Phase** - Used AI to generate class skeleton code from the UML, ensuring consistent structure with Python dataclasses. Also asked for help implementing the scheduling algorithms, particularly the sorting logic in `prioritize_tasks()`.

3. **Testing Phase** - AI helped generate comprehensive pytest test cases covering edge cases I hadn't considered (zero available time, tasks exceeding time limits, completed tasks being excluded).

4. **UI Integration** - AI assisted with Streamlit session state management and created the full app.py with proper widget callbacks.

5. **Code Review** - Asked AI to review my initial design for potential issues, which led to adding validation in `Task.__post_init__()` and helper methods in the Scheduler.

**Most helpful prompts**:
- "Review this design for potential logic bottlenecks" - uncovered the missing Owner-to-Pet reference
- "Generate pytest tests for edge cases in scheduling" - created scenarios I hadn't thought about
- "Explain the tradeoffs in this greedy algorithm" - helped me articulate design decisions

**b. Judgment and verification**

**Moment of disagreement**: When implementing the `explain_reasoning()` method, AI initially suggested a verbose explanation that included technical details about the algorithm ("greedy knapsack approach", "O(n log n) sorting complexity").

**Why I modified it**: The target audience is pet owners, not computer scientists. They don't care about algorithm names—they want to know *why* their specific tasks were or weren't scheduled.

**How I verified**: I rewrote the explanation to focus on:
- Clear summary metrics (tasks scheduled, time used)
- Plain language strategy description ("highest priority first, shorter tasks break ties")
- Specific reasons for each task (duration, priority, pet name)
- Empathetic messaging for skipped tasks ("could not fit in available time")

**Verification method**: I ran the app with various scenarios and read the explanations as if I were a user. The revised version was immediately understandable without technical knowledge, confirming the change was correct.

---

## 4. Testing and Verification

**a. What you tested**

I created 23 comprehensive tests covering four main categories:

1. **Data Model Tests** (10 tests)
   - Object creation for Owner, Pet, Task
   - Validation logic (priority bounds, positive duration)
   - Bidirectional relationships (Owner ↔ Pet)
   - Special behaviors (adding special needs, marking tasks complete)

   **Why important**: These ensure data integrity at the foundation. Invalid data (like priority = 10) could break scheduling logic later.

2. **Scheduling Logic Tests** (8 tests)
   - Task prioritization algorithm
   - Schedule generation within time limits
   - Schedule generation when time is exceeded
   - Completed task exclusion
   - Empty schedule handling
   - Zero available time edge case

   **Why important**: This is the core functionality. These tests verify the scheduler makes correct decisions under various constraints.

3. **Query/Filter Tests** (3 tests)
   - Filtering tasks by pet
   - Filtering tasks by type
   - Getting incomplete tasks

   **Why important**: The UI relies on these methods to display relevant subsets of tasks. Bugs here would confuse users.

4. **Integration Tests** (1 test)
   - Complete end-to-end workflow from owner creation to schedule explanation

   **Why important**: Unit tests can pass while the system fails in realistic scenarios. This test ensures all components work together correctly.

5. **Explanation Tests** (1 test)
   - Verifying the explanation includes key information

   **Why important**: The explanation is a critical feature for user trust. Users need to understand *why* the schedule looks the way it does.

**b. Confidence**

**Confidence level**: 85% confident the scheduler works correctly for the defined scope.

**What gives me confidence**:
- All 23 tests pass
- Edge cases are covered (no tasks, no time, excessive tasks)
- Manual testing in the Streamlit UI with various scenarios
- Code review caught design issues early

**What limits my confidence**:
- Haven't tested with extremely large numbers of tasks (100+)
- No testing of concurrent modifications (what if user adds task while schedule is generating?)
- Limited testing of owner preferences (they're stored but not used in scheduling yet)

**Edge cases I'd test next with more time**:

1. **Task Dependencies** - "Must walk dog before feeding" type constraints
2. **Recurring Tasks** - Daily tasks that repeat and accumulate if not completed
3. **Time Windows** - "Medication must be given between 8am-9am"
4. **Multi-Owner Scenarios** - Shared pet care between multiple people
5. **Task Conflicts** - Can't walk two dogs simultaneously
6. **Dynamic Time Changes** - What if owner's available time changes mid-schedule?
7. **Priority Ties with Multiple Factors** - Equal priority *and* duration, how to break tie?
8. **Negative/Boundary Values** - Very large durations (1000 minutes), fractional ages
9. **Special Characters in Names** - Pets named "🐶" or tasks with quotes/apostrophes
10. **Persistence** - Saving/loading schedules across sessions

---

## 5. Reflection

**a. What went well**

I'm most satisfied with **the separation of concerns in the architecture**.

By keeping data models (Owner, Pet, Task) separate from business logic (Scheduler), the code is:
- Easy to understand - each class has a clear, single responsibility
- Easy to test - can test scheduling logic without worrying about data validation
- Easy to extend - could swap scheduling algorithms without touching data models

The use of Python dataclasses was particularly effective—they reduced boilerplate while providing automatic `__init__`, `__repr__`, and type hints. The validation in `Task.__post_init__()` catches bad data immediately rather than failing silently later.

The comprehensive test suite (23 tests) gives confidence that changes won't break existing functionality. Having these tests from the start made refactoring the scheduling algorithm stress-free.

**b. What you would improve**

If I had another iteration, I would improve:

1. **Smarter Scheduling Algorithm**
   - Current greedy approach is fast but not optimal
   - Could use dynamic programming (0/1 knapsack) to find the *best* combination of tasks that maximizes total value (priority × completion) within time constraints
   - Would better handle the "two medium-priority tasks vs. one high-priority" tradeoff

2. **Owner Preferences Integration**
   - Currently stored but not used in scheduling
   - Could add: preferred task times, disliked task types, minimum/maximum task durations per day
   - Example: "morning_person: True" could boost priority of early tasks

3. **Task Scheduling Details**
   - Add specific time slots (9:00 AM - 9:30 AM) instead of just a list
   - Consider travel time between tasks
   - Handle task dependencies and conflicts

4. **Persistence Layer**
   - Save/load schedules to a database or JSON file
   - Track completion history over time
   - Generate insights ("You've completed 95% of medication tasks this month!")

5. **UI Enhancements**
   - Drag-and-drop task reordering
   - Calendar view showing schedules over multiple days
   - Mobile-responsive design
   - Export schedule to Google Calendar or as PDF

6. **Performance Optimization**
   - Current O(n log n) algorithm works fine for small n (< 50 tasks)
   - For large pet care businesses with hundreds of tasks, would need caching and incremental updates

**c. Key takeaway**

**Key learning**: **AI is most valuable in the design phase, not just the implementation phase.**

Initially, I thought AI would be most helpful for writing code faster. But the most impactful moment was when I asked AI to review my initial UML design.

The AI spotted the missing bidirectional Owner ↔ Pet relationship that I'd overlooked. This would have caused major problems later—the Scheduler wouldn't have been able to access all of an owner's pets! Fixing this in the design phase took 5 minutes. Discovering it after implementing the UI would have required restructuring multiple files and rewriting tests.

**Broader insight**: Design-time mistakes compound exponentially. A class missing a critical method requires adding the method, updating all call sites, adding tests, and potentially restructuring related classes. A well-designed system absorbs changes easily.

This changed my workflow: Now I use AI to critique designs *before* writing implementation code. The prompt "Review this for potential issues" before starting to code has saved hours of refactoring.

**Working with AI effectively means**:
1. Use AI to explore design space and spot issues early
2. Verify AI suggestions against real user needs (like the explanation text)
3. Treat AI as a collaborator, not an oracle—question and adapt suggestions
4. Use AI to generate boilerplate, but apply human judgment to architecture

This project reinforced that system design is harder than coding. Once you have a good design, implementation is straightforward. The real skill is thinking through the problem space, identifying constraints, and making explicit tradeoffs—which AI can help with, but can't replace human judgment on.
