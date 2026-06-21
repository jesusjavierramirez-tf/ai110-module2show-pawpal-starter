# PawPal+ Project Reflection

## 1. System Design

### Core Actions
The user should be able to perform these three core actions:

1. **Add/Edit Tasks** — User can add or modify pet care tasks, specifying duration, priority (high/medium/low), and task type (e.g., walk, feeding, medication, enrichment, grooming).

2. **Generate Daily Schedule** — System creates an optimized daily plan by sorting and filtering tasks based on priority, available time, and owner preferences.

3. **View Daily Plan** — User sees the generated schedule with task times, durations, and priorities. The system should explain why tasks were prioritized or excluded.

### Building Blocks (Objects and Methods)

| Class | Attributes | Methods | Responsibility |
|-------|-----------|---------|-----------------|
| **Owner** | name, available_hours | - | Represents the pet owner with daily time availability |
| **Pet** | name, breed, age | - | Represents the pet being cared for |
| **Task** | type, duration, priority, recurring | validate(), get_duration() | Represents a single care task with attributes and validation |
| **Schedule** | tasks, owner, pet, daily_plan | add_task(), generate_plan(), get_plan() | Manages tasks and generates the daily schedule |

**a. Initial design**

The initial UML design includes four core classes:

- **Owner**: Holds owner information (name, available_hours). Responsibilities: track daily availability and provide methods to get/set availability. This encapsulates the time constraint for scheduling.

- **Pet**: Stores pet metadata (name, breed, age). Responsibilities: provide basic pet information. This allows the system to personalize schedules and explanations based on pet characteristics.

- **Task**: Represents a single care task with task_type, duration, priority, and recurring flag. Responsibilities: validate task attributes, return priority as an integer for sorting, and report duration. This is the core unit of work that needs scheduling.

- **Schedule**: Acts as the main orchestrator. Contains references to an Owner and Pet, manages a list of Tasks, and generates the daily_plan. Responsibilities: add/remove tasks, generate an optimized daily plan by sorting and filtering tasks based on available time and priority, and return the current plan.

The key design decisions:
- **Dataclass pattern** for clean, immutable data objects (Owner, Pet, Task)
- **Schedule as an orchestrator** that coordinates Owner, Pet, and Task objects
- **Priority levels** (high/medium/low) that can be converted to integers for sorting
- **Recurring flag** on Task to handle daily vs. one-time tasks

**b. Design changes**

Yes, the design was refined based on AI review of the skeleton. Key changes:

1. **Added task_id field to Task** — Tasks now have a unique UUID identifier. This fixes the logic gap where `remove_task()` expected IDs that didn't exist. Each task can now be individually identified and removed.

2. **Removed daily_plan as persistent field** — The initial design stored `daily_plan` as a separate list on Schedule, which created redundancy and confusion about the source of truth. Now `daily_plan` is generated from `tasks` by calling `generate_plan()` or `get_plan()`, making the data model cleaner.

3. **Added description field to Task** — Tasks now include an optional description field to capture more context (e.g., "30-minute walk in the park") for better explanations to the user.

4. **Clarified unit consistency** — Task duration is explicitly in **minutes** and Owner available_hours is in **hours**. The `generate_plan()` method will convert between units. This prevents subtle bugs from mixed units.

5. **Changed return types for add_task/remove_task** — These now return `bool` to indicate success/failure. `add_task()` will return False if validation fails. This allows the caller to handle errors gracefully.

6. **Improved generate_plan signature** — Now accepts an optional `available_minutes` parameter (defaults to owner's hours converted to minutes). This allows flexibility for testing different time scenarios.

**Why these changes matter:**
- Task IDs enable proper tracking and removal
- Computed daily_plan eliminates data consistency issues
- Unit clarity prevents runtime errors
- Return values enable proper error handling
- Better method signatures improve testability

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

The test suite covers 20 test cases across four classes:

- **Task (8 tests)**: Validation logic, priority mapping, completion status, and duration retrieval
- **Pet (6 tests)**: Task addition/removal, task count, pending task filtering, and pet info formatting
- **Owner (3 tests)**: Pet management, retrieving all tasks across pets, and availability management
- **Scheduler (3 tests)**: Priority-based sorting, time constraint enforcement, and pending-task filtering

Key behaviors tested:
- Task validation prevents invalid priorities, zero/negative durations, and empty task types
- Task completion status is correctly tracked and retrieved
- Pet task lists grow and shrink appropriately
- Scheduler respects available time and filters completed tasks
- Priority sorting places high→medium→low tasks, with ties broken by duration (short first)

**b. Confidence**

Confidence level: **High** (20/20 tests passing, 100% pass rate)

The scheduler correctly:
- Prioritizes high-priority tasks over lower ones
- Respects time constraints (doesn't overschedule)
- Filters out completed tasks
- Sorts by duration as a tiebreaker

**Edge cases tested:**
- Empty task lists
- Invalid task properties
- Multiple pets with overlapping task types
- Exact time fit scenarios
- Task completion state transitions

**Remaining test opportunities:**
- Recurring task handling (daily/weekly patterns)
- Multiple schedule generation across different days
- Conflict resolution for overlapping time slots
- Persistence/storage layer tests

---

## 5. Reflection

**a. What went well**

- **Comprehensive test coverage**: 20 tests with 100% pass rate covering all core classes and behaviors. Tests were easy to write and caught design issues early.
- **Clean class hierarchy**: Task, Pet, Owner, and Scheduler form a logical, composable structure. Each class has a single clear responsibility.
- **Practical demo**: The `main.py` demo proves the system works end-to-end with realistic pet care scenarios (dogs and cats with multiple task types).
- **Data consistency**: Using task IDs and proper filtering prevents data corruption. The scheduler reliably respects time constraints.

**b. What you would improve**

- **Scheduling algorithm**: Current greedy approach could be replaced with a more sophisticated algorithm (e.g., bin packing, constraint satisfaction) to better handle complex scenarios.
- **Persistent storage**: No database integration yet. Should add SQLite or file-based persistence for tasks to survive app restarts.
- **Time slot assignment**: Tasks don't yet have specific start times (only durations). Next phase should assign exact time slots (e.g., "Walk: 08:00-08:30").
- **Recurring task logic**: The `recurring` flag exists but isn't used. Should implement logic to generate recurring instances (daily at 8am, etc.).
- **Error handling**: Method docstrings could include `Raises:` sections documenting edge cases.

**c. Key takeaway**

The most valuable lesson: **Start with a solid UML design, then iterate ruthlessly**. The initial design had redundancy and missing IDs that were caught during code review before implementation. Tests drove confidence that the final system actually works. AI assistance was most helpful for generating boilerplate and catching overlooked requirements—not for making architectural decisions.

---

## Commit Message

```
feat: implement PawPal+ system logic layer with tests

Implement four core classes for pet care scheduling:
- Task: represents individual care activities with priority and duration
- Pet: manages tasks for a single pet with validation
- Owner: manages multiple pets and aggregates their tasks
- Scheduler: generates optimized daily plans respecting time constraints

Features:
- Priority-based task sorting (high → low, with duration tiebreaker)
- Time-aware scheduling that respects owner availability
- Task completion tracking and filtering
- Full input validation on task creation

Tests:
- 20 comprehensive unit tests (100% pass rate)
- Covers validation, completion, priority sorting, and time constraints
- Tests task/pet/owner/scheduler interactions

Demo:
- main.py demonstrates real-world usage with 2 pets and 6 tasks
- Outputs formatted daily schedule with time accounting
- Shows all tasks fit within 3-hour availability window

Updated:
- pawpal_system.py: full implementation with 1-line docstrings
- tests/test_pawpal.py: comprehensive test suite
- main.py: demo script and usage example
- README.md: sample output and test results
- reflection.md: design decisions and testing details
```
