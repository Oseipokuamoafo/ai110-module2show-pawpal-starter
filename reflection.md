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

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
