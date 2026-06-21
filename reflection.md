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

The scheduler considers the following constraints and priorities:

1. **Time Constraint** — Tasks must fit within owner's available hours per day. The greedy algorithm prioritizes high-priority tasks first, then medium, then low, stopping when available time runs out.

2. **Priority Levels** — Tasks are ranked: high (3) > medium (2) > low (1). Within the same priority, shorter tasks are scheduled first (duration tiebreaker).

3. **Task Frequency** — Recurring tasks (daily, weekly, one-time) are tracked with `due_date`. When marked complete, recurring tasks auto-generate the next occurrence.

4. **Time Slots** — Tasks can have specific start times (HH:MM). The scheduler can detect conflicts (multiple tasks at same time) and suggest reassignments.

5. **Pet Assignment** — Tasks belong to specific pets. The scheduler can filter by pet name to show pet-specific workload.

**Decision Process:**
- Time constraint matters most (can't schedule more than available)
- Priority matters second (complete high-value tasks first)
- Task duration matters third (fit more tasks by doing short ones early)
- Specific time slots matter least (auto-assigned if not specified)

**b. Tradeoffs**

**Tradeoff 1: Greedy Algorithm vs. Optimal Packing**
- **Current approach (Greedy)**: Sort by priority, fit tasks sequentially until time runs out. Simple, predictable, O(n log n).
- **Cost**: May leave gaps in the schedule. Example: with 3 hours available, if high-priority tasks total 2.5 hours, a 0.5-hour low-priority task won't fit even though it fills the gap perfectly.
- **Tradeoff decision**: Greedy is more readable and predictable for a pet owner. The time cost (gaps) is acceptable because schedules are usually not packed tightly anyway.

**Tradeoff 2: Exact Time Conflicts vs. Duration Overlaps**
- **Current approach (Exact)**: Only detect conflicts if multiple tasks have the exact same `time_slot` (e.g., "08:00").
- **Cost**: Misses overlaps. Example: Walk (08:00-08:30) and Feeding (08:15-08:25) aren't flagged as conflicting.
- **Tradeoff decision**: Exact conflicts are sufficient for a first pass. Duration-based conflict detection would require more complex logic and isn't critical for MVP.

**Tradeoff 3: Automatic Recurrence vs. Manual Re-creation**
- **Current approach (Automatic)**: When a recurring task is marked complete, a new instance is auto-generated for tomorrow/next week.
- **Cost**: Creates unlimited tasks over time. Database grows indefinitely without archival/cleanup.
- **Tradeoff decision**: Automatic recurrence is more user-friendly. Archive strategy (clean up completed tasks older than 30 days) can address growth later.

**Tradeoff 4: In-Memory Session State vs. Persistent Database**
- **Current approach (Session State)**: All data lives in `st.session_state`, lost when browser closes.
- **Cost**: No data persistence. User loses schedules on refresh.
- **Tradeoff decision**: Session state is fast and simple for MVP. Production should add SQLite/Firestore.

These tradeoffs prioritize **usability** and **simplicity** over **optimality** and **completeness**.

---

## 3. AI Collaboration

**a. How you used AI**

AI was instrumental in:
1. **UML Design** — Generated initial class structure with proper relationships and suggested dataclasses pattern
2. **Testing** — Created comprehensive test templates and edge case suggestions
3. **UI Integration** — Suggested session_state pattern for state persistence and wiring patterns for connecting UI to logic
4. **Code Review** — Identified missing fields (task_id, description) and redundant storage patterns before implementation

Most helpful prompt types:
- "Based on my skeleton, how should the Scheduler retrieve tasks from the Owner?"
- "What's the best way to persist data in Streamlit between button clicks?"
- "How do I wire a form submission to call a Python class method and update the UI?"

**b. Judgment and verification**

One moment where I rejected AI suggestions:
- **Initial suggestion**: Store tasks in multiple places (both `tasks` and `daily_plan` on Schedule). 
- **My verification**: I recognized this created a data consistency problem. Tested by asking: "If I modify a task, do I need to update it in two places?" Yes → rejected the suggestion.
- **Resolution**: Implemented computed plans where `daily_plan` is derived from `tasks` on-demand. One source of truth = fewer bugs.

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

---

## 7. Smart Algorithms (Phase 4)

### New Features Implemented

**1. Sorting Enhancements:**
- `sort_by_priority()` — Existing method (high→medium→low, duration tiebreaker)
- `sort_by_time()` — NEW: Sort by HH:MM time slots, unscheduled tasks first

**2. Filtering:**
- `filter_by_pet(pet_name)` — NEW: Show only tasks for a specific pet
- `filter_by_status(completed)` — NEW: Show only pending or completed tasks

**3. Conflict Detection:**
- `detect_conflicts()` — NEW: Identifies tasks at same time, returns warnings with task names and pet names
- Helps user manually resolve scheduling conflicts

**4. Recurring Tasks:**
- Changed `Task.recurring` (boolean) to `Task.frequency` (string: "once", "daily", "weekly")
- `Task.mark_complete()` — Now returns next recurring instance (if applicable)
- `Task._generate_next_occurrence()` — NEW: Creates next task with updated due_date
- `Pet.mark_task_complete(task_id)` — NEW: Marks task complete AND auto-adds next occurrence

**5. Time Slot Assignment:**
- `assign_time_slots(tasks, start_time)` — NEW: Auto-calculates start times for unscheduled tasks
- Handles cumulative duration calculations (08:00, 08:30, 08:40, etc.)

### Algorithm Comparisons

**Time-based Sorting: Simple vs. Complex Implementation**
- **Simple (chosen)**: `sorted(tasks, key=lambda t: (t.get_time_slot_minutes(),))`
  - Uses `get_time_slot_minutes()` helper to convert "HH:MM" to integer minutes
  - Readable, 1-line sort key
  
- **Complex alternative**: Manual parsing of time slots in the lambda
  - Would be harder to read and debug
  - **Decision**: Simple version is more Pythonic and maintainable

**Conflict Detection: Exact vs. Duration-based**
- **Current (Exact)**: Check if multiple tasks have identical `time_slot` value
  - Fast: O(n) with dict grouping
  - Limitation: Misses overlaps (08:00-08:30 walk + 08:15-08:25 feeding)
  
- **Alternative (Overlaps)**: Check if time ranges intersect
  - Would require start/end time calculation for each task
  - More complex: O(n²) naive comparison or O(n log n) with sweep-line algorithm
  - **Decision**: Exact matching is sufficient for MVP. Overlap detection can be Phase 5

**Recurring Task Auto-generation: Approach**
- **Chosen**: Call `task.mark_complete()` which returns new Task instance
  - Clean separation: Task handles logic, Pet handles storage
  - `Pet.mark_task_complete()` adds returned task to pet.tasks
  - Testable: Can verify new task properties independently
  
- **Alternative**: Have Pet poll task completion and auto-create
  - Tighter coupling between Pet and Task
  - Less clear responsibility boundary
  - **Decision**: Current approach is cleaner

### Testing Strategy

Added 10 new tests in `TestSmartAlgorithms` class covering:
- Time sorting (ordering tasks by HH:MM)
- Pet filtering (single pet returns only its tasks)
- Status filtering (pending vs completed)
- Conflict detection (same time) and no-conflict scenarios
- Recurring tasks (daily, weekly, one-time)
- Time slot assignment (cumulative duration calculation)
- Pet auto-recurrence integration

**Coverage**: 30/30 tests passing (20 original + 10 new)

---

## 3. AI Strategy and Collaboration

### 3a. Most Effective AI Coding Assistant Features

**1. Code Generation from Specifications** ⭐⭐⭐⭐⭐
- **What worked**: Providing detailed prompts with class names, method signatures, and expected behavior
- **Example**: "Generate a `sort_by_time()` method that sorts tasks by their HH:MM time_slot. Tasks without time slots should appear first. Return a sorted list."
- **Why effective**: AI produced clean, working code immediately. Required minimal edits.
- **Lesson**: Specificity in prompts dramatically improves output quality.

**2. Skeleton Generation from UML** ⭐⭐⭐⭐⭐
- **What worked**: Showing the AI a UML diagram and asking for Python class stubs
- **Example**: "Here's my UML. Convert this to Python dataclasses with stub methods (just `pass`)"
- **Why effective**: AI understood relationships and generated logical method names and parameters
- **Lesson**: Visual references (UML) help AI maintain architectural consistency

**3. Test Suite Generation** ⭐⭐⭐⭐
- **What worked**: Asking for specific test cases with happy paths and edge cases
- **Example**: "Generate tests for Task.mark_complete() covering: 1) task becomes completed, 2) one-time tasks don't create recurrence, 3) daily tasks create next-day instance"
- **Why effective**: AI generated well-organized test classes with clear docstrings
- **Limitation**: AI sometimes created redundant tests; required filtering
- **Lesson**: Test generation needs human review to avoid bloat

**4. Refactoring and Code Cleanup** ⭐⭐⭐⭐
- **What worked**: Asking AI to simplify or improve existing code without changing behavior
- **Example**: "My sort_by_time() method has inline time parsing. Can you extract a helper function to make it more readable?"
- **Why effective**: AI understood the intent and produced cleaner code
- **Limitation**: Sometimes over-engineered; simpler original was better
- **Lesson**: Not all AI suggestions improve code; trust your judgment on complexity vs. clarity

**5. Documentation and Docstrings** ⭐⭐⭐
- **What worked**: Asking AI to add 1-line docstrings to existing methods
- **Why effective**: Quick and consistent across the codebase
- **Limitation**: Sometimes docstrings were obvious or slightly inaccurate
- **Lesson**: AI documentation is a good starting point but needs review

### 3b. Example: AI Suggestion Rejected/Modified

**Scenario: Conflict Detection Algorithm**

**AI Suggestion (Initial):**
```python
def detect_conflicts(self) -> List[Dict]:
    """Complex duration-based overlap detection."""
    conflicts = []
    for i, task1 in enumerate(self.get_pending_tasks()):
        for j, task2 in enumerate(self.get_pending_tasks()):
            if i < j and task1.time_slot and task2.time_slot:
                # Parse HH:MM and check if durations overlap
                start1 = task1.get_time_slot_minutes()
                end1 = start1 + int(task1.duration)
                start2 = task2.get_time_slot_minutes()
                end2 = start2 + int(task2.duration)
                
                if start1 < end2 and start2 < end1:  # Overlap
                    conflicts.append({...})
    return conflicts
```

**Why I Rejected It:**
- ❌ Overly complex for MVP
- ❌ Requires task duration to be set for conflict detection (not always true)
- ❌ O(n²) performance with nested loops
- ❌ Harder to test with many edge cases
- ❌ User's workflow doesn't require exact overlap detection

**My Modified Decision:**
```python
def detect_conflicts(self) -> List[Dict]:
    """Simple exact-time conflict detection."""
    time_groups: Dict[str, List[Task]] = {}
    for task in self.get_pending_tasks():
        if task.time_slot:
            if task.time_slot not in time_groups:
                time_groups[task.time_slot] = []
            time_groups[task.time_slot].append(task)
    
    conflicts = []
    for time_slot, tasks in time_groups.items():
        if len(tasks) > 1:
            conflicts.append({...})
    return conflicts
```

**Why This Was Better:**
- ✅ O(n) with single pass
- ✅ Clear intent: "multiple tasks at exact same time"
- ✅ Works with or without duration
- ✅ Easy to test and debug
- ✅ Sufficient for a pet owner's schedule
- ✅ Can be enhanced later (duration overlap) if needed

**Key Lesson:** AI suggests feature-complete solutions; as the architect, you choose MVP simplicity over premature optimization. "Simple enough to explain" > "As powerful as possible."

### 3c. Separate Chat Sessions for Organization

**How I Used Multiple Sessions:**

1. **Session 1: Design** — "Here's the scenario, what classes do I need?"
   - Brainstormed Owner, Pet, Task, Scheduler
   - Created initial UML
   
2. **Session 2: Implementation** — "Convert this UML to Python dataclasses"
   - Generated pawpal_system.py skeleton
   - Added full method implementations
   
3. **Session 3: Algorithms** — "How do I sort tasks by time? Filter by pet?"
   - Developed sorting/filtering/conflict logic
   - Refined tradeoffs
   
4. **Session 4: Testing** — "Generate comprehensive tests for all my classes"
   - Created 30 test cases
   - Debugged failing tests
   
5. **Session 5: UI** — "How do I integrate Streamlit with my logic layer?"
   - Wired up app.py with session_state
   - Added smart algorithm display
   
6. **Session 6: Finalization** — "Polish README and finish reflection"
   - Refined documentation
   - Added this AI strategy section

**Why Separate Sessions Were Helpful:**
- ✅ **Focus**: Each session had one clear goal (no context switching)
- ✅ **Organization**: Easy to find prior context when implementing (Session 2 → "remember the classes from Session 1?")
- ✅ **Token efficiency**: Kept chat history manageable (~5-10 exchanges per session)
- ✅ **Problem isolation**: Algorithm bugs isolated to Session 3, not affecting design decisions
- ✅ **Mental model**: Different phase = different vocabulary (design → architecture → algorithms → tests)

**Downside:** Had to re-explain architecture in later sessions, but the benefit of clarity outweighed redundancy.

### 3d. Lessons: Being the Lead Architect with AI

**Key Insights:**

1. **You Are the Decider, AI Is the Suggester**
   - AI is excellent at generating code and explaining options
   - YOU decide whether the suggestion aligns with your vision
   - Example: Rejected complex conflict detection for simple approach

2. **Specificity Saves Iteration**
   - Vague prompts ("make the scheduler smarter") → Vague results
   - Specific prompts ("Sort by priority first, then duration") → Exact results
   - Time investment: 2 minutes writing a good prompt saves 10 minutes of editing

3. **AI Excels at Boilerplate, Struggles with Design**
   - ✅ Excellent: "Generate docstrings," "Write tests," "Refactor this method"
   - ⚠️ Risky: "Design a scheduling algorithm" (too many options, no context)
   - ✅ Better: "I want a greedy algorithm that fits high-priority first. Generate that."

4. **Human Review Is Essential**
   - AI generated 30 test cases; I filtered to 20 core behaviors
   - AI suggested O(n²) algorithm; I chose O(n) simplicity
   - AI wrote docstrings; I corrected 2-3 that were vague
   - Lesson: AI is a multiplier of your judgment, not a replacement

5. **Separation of Concerns Stays Boundaries**
   - Task handles validation and recurrence logic
   - Pet manages task storage
   - Scheduler handles algorithms
   - Owner manages metadata
   - AI suggested violating these boundaries; you maintained them
   - Lesson: Your UML is your contract; enforce it with AI

6. **Test-Driven Refinement**
   - Wrote tests in Session 4
   - Found bugs in implementation
   - Used AI to fix bugs while preserving tests
   - Result: Confidence in reliability
   - Lesson: Tests + AI collaboration = high-quality code

**Overall AI Collaboration Score: 9/10**
- What worked: Code generation, test suite, documentation, refactoring
- What didn't: Design decisions, architectural tradeoffs, simplicity vs. completeness
- Bottom line: AI is a force multiplier when you're the clear architect

### Evaluation: Simplicity vs. Performance

**Example: sort_by_time()**

Original AI suggestion:
```python
# Complex with inline parsing
sorted_tasks = sorted(tasks, key=lambda t: tuple(map(int, t.time_slot.split(":") or (999, 999))))
```

**Chosen (simpler):**
```python
def get_time_slot_minutes(self) -> int:
    """Convert HH:MM to minutes since midnight."""
    if self.time_slot is None:
        return 0
    try:
        h, m = map(int, self.time_slot.split(":"))
        return h * 60 + m
    except (ValueError, AttributeError):
        return 0

sorted_tasks = sorted(tasks, key=lambda t: (t.get_time_slot_minutes(),))
```

**Why chosen version is better:**
- Readable: Clear helper method with docstring
- Reusable: Used in conflict detection and time assignment
- Debuggable: Can inspect `get_time_slot_minutes()` independently
- Error-safe: Handles None and format errors gracefully

**Performance trade-off:** Helper method is negligible (microseconds). Readability wins.

### Connection Architecture

The app.py now bridges logic and UI through three key mechanisms:

**1. Imports (Lines 2-3):**
```python
from pawpal_system import Owner, Pet, Task, Scheduler
```
Makes all classes available in the Streamlit app.

**2. Session State Initialization (Lines 26-31):**
```python
def init_session_state():
    if "owner" not in st.session_state:
        st.session_state.owner = Owner(...)
        st.session_state.scheduler = Scheduler(...)
```
Solves Streamlit's stateless problem by persisting the Owner object across reruns.

**3. UI-to-Logic Wiring:**
- **Add Pet** → `owner.add_pet(Pet(...))` → `st.rerun()` to refresh UI
- **Add Task** → `pet.add_task(Task(...))` → `st.rerun()`
- **Toggle Task** → `task.mark_complete()` / `mark_incomplete()` → `st.rerun()`
- **Generate Plan** → `scheduler.generate_plan()` → Display results with time accounting

### Data Flow

```
User clicks "Add Pet" button
    ↓
Streamlit captures form inputs (name, breed, age)
    ↓
Create Pet object
    ↓
Call owner.add_pet(pet) — updates owner.pets list
    ↓
st.rerun() refreshes the page
    ↓
Page renders and displays new pet in the pet list
    ↓
Session state persists across reruns
```

### Key Design Decisions

- **No database yet**: All data lives in `st.session_state` (in-memory). Closes when session ends.
- **Direct method calls**: UI buttons directly call class methods (not a REST API layer).
- **Reactive updates**: `st.rerun()` after modifications ensures UI stays in sync with data.
- **Validation in logic layer**: Form validation happens in Task.validate(), not in UI.
- **Flexible scheduling**: Users can toggle task completion and regenerate plans on-demand.

### UI Features Implemented

✅ **Owner Setup**: Set name and daily availability
✅ **Pet Management**: Add/view/remove pets
✅ **Task Management**: Add/view/delete tasks per pet, mark complete/incomplete
✅ **Schedule Generation**: Create optimized daily plan with time accounting
✅ **Schedule Display**: Table view with pet names, priorities, durations, start times
✅ **Explanations**: Show which priority tasks were included and why

### Sample User Journey

1. Owner enters "Alice" and "3 hours" availability
2. Adds pet "Biscuit" (Golden Retriever, 3 years)
3. Adds tasks: Morning Walk (30 min, high), Feeding (10 min, high), Play (20 min, medium)
4. Clicks "Generate Schedule"
5. App displays: "All 3 tasks fit! Morning Walk starts at 00:00, Feeding at 00:30, Play at 00:40"
6. Owner can mark "Morning Walk" complete to regenerate plan

### Next Steps for Production

- Add persistent storage (SQLite or Firebase)
- Implement user authentication/accounts
- Add time-slot visualization (calendar/timeline view)
- Handle recurring tasks UI and logic
- Export schedule to calendar format (iCal)
- Add pet health records and vet appointment tracking
