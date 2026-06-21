# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
Owner: Alice (available: 3.0 hours)

Pets: Biscuit (Golden Retriever, 3 years old), Luna (Siamese Cat, 5 years old)

Added 3 tasks to Biscuit
Added 3 tasks to Luna

Total tasks in system: 6

Tasks sorted by priority:
  - Feeding (high, 5 min)
  - Feeding (high, 10 min)
  - Litter Box Cleaning (high, 10 min)
  - Morning Walk (high, 30 min)
  - Play with Toy (medium, 15 min)
  - Play Session (medium, 20 min)

============================================================
Daily Plan for Alice
============================================================

1. [○ TODO] FEEDING
   Pet: Luna
   Duration: 5 min | Priority: high
   Details: Breakfast kibble

2. [○ TODO] FEEDING
   Pet: Biscuit
   Duration: 10 min | Priority: high
   Details: Breakfast meal

3. [○ TODO] LITTER BOX CLEANING
   Pet: Luna
   Duration: 10 min | Priority: high
   Details: Clean and refill litter box

4. [○ TODO] MORNING WALK
   Pet: Biscuit
   Duration: 30 min | Priority: high
   Details: Brisk walk in the park

5. [○ TODO] PLAY WITH TOY
   Pet: Luna
   Duration: 15 min | Priority: medium
   Details: Interactive wand toy

6. [○ TODO] PLAY SESSION
   Pet: Biscuit
   Duration: 20 min | Priority: medium
   Details: Fetch with tennis ball

------------------------------------------------------------
Total time needed: 90 minutes (1.5 hours)
Available time: 180.0 minutes (3.0 hours)
✓ All scheduled tasks fit within available time!
============================================================
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
=============== test session starts ===============
platform win32 -- Python 3.14.2, pytest-9.1.0, pluggy-1.6.0
collected 30 items                                

tests/test_pawpal.py::TestTask::test_task_completion PASSED [  3%]
tests/test_pawpal.py::TestTask::test_task_incomplete PASSED [  6%]
tests/test_pawpal.py::TestTask::test_task_validation_valid PASSED [ 10%]
tests/test_pawpal.py::TestTask::test_task_validation_invalid_priority PASSED [ 13%]
tests/test_pawpal.py::TestTask::test_task_validation_invalid_duration PASSED [ 16%]
tests/test_pawpal.py::TestTask::test_task_priority_level_high PASSED [ 20%]
tests/test_pawpal.py::TestTask::test_task_priority_level_medium PASSED [ 23%]
tests/test_pawpal.py::TestTask::test_task_priority_level_low PASSED [ 26%]
tests/test_pawpal.py::TestPet::test_pet_add_task PASSED [ 30%]
tests/test_pawpal.py::TestPet::test_pet_add_multiple_tasks PASSED [ 33%]
tests/test_pawpal.py::TestPet::test_pet_add_invalid_task PASSED [ 36%]
tests/test_pawpal.py::TestPet::test_pet_remove_task PASSED [ 40%]
tests/test_pawpal.py::TestPet::test_pet_get_pending_tasks PASSED [ 43%]
tests/test_pawpal.py::TestPet::test_pet_get_info PASSED [ 46%]
tests/test_pawpal.py::TestOwner::test_owner_add_pet PASSED [ 50%]
tests/test_pawpal.py::TestOwner::test_owner_get_all_tasks PASSED [ 53%]
tests/test_pawpal.py::TestOwner::test_owner_availability PASSED [ 56%]
tests/test_pawpal.py::TestScheduler::test_scheduler_sort_by_priority PASSED [ 60%]
tests/test_pawpal.py::TestScheduler::test_scheduler_generate_plan_respects_time PASSED [ 63%]
tests/test_pawpal.py::TestScheduler::test_scheduler_pending_tasks_only PASSED [ 66%]
tests/test_pawpal.py::TestSmartAlgorithms::test_sort_by_time PASSED [ 70%]
tests/test_pawpal.py::TestSmartAlgorithms::test_filter_by_pet PASSED [ 73%]
tests/test_pawpal.py::TestSmartAlgorithms::test_filter_by_status PASSED [ 76%]
tests/test_pawpal.py::TestSmartAlgorithms::test_detect_conflicts PASSED [ 80%]
tests/test_pawpal.py::TestSmartAlgorithms::test_no_conflicts PASSED [ 83%]
tests/test_pawpal.py::TestSmartAlgorithms::test_recurring_task_generation PASSED [ 86%]
tests/test_pawpal.py::TestSmartAlgorithms::test_recurring_weekly_task PASSED [ 90%]
tests/test_pawpal.py::TestSmartAlgorithms::test_one_time_task_no_recurrence PASSED [ 93%]
tests/test_pawpal.py::TestSmartAlgorithms::test_assign_time_slots PASSED [ 96%]
tests/test_pawpal.py::TestSmartAlgorithms::test_pet_mark_task_complete_with_recurrence PASSED [100%]

=============== 30 passed in 0.15s ===============
```

**Test Coverage:**
- **Original tests (20)**: Task validation, pet/owner/scheduler basics, priority sorting, time constraints
- **Smart algorithm tests (10)**: Time-based sorting, pet/status filtering, conflict detection, recurring tasks, time slot assignment

## 📐 Smarter Scheduling

The PawPal+ scheduler implements several intelligent algorithms to optimize daily pet care plans:

| Feature | Method(s) | Description | Example |
|---------|-----------|-------------|---------|
| **Priority Sorting** | `Scheduler.sort_by_priority()` | Sort tasks by importance (high→medium→low), with shorter tasks first as tiebreaker | Morning Walk (high, 30m) before Grooming (low, 45m) |
| **Time-based Sorting** | `Scheduler.sort_by_time()` | Sort tasks by scheduled time slot (HH:MM format, earliest first) | 08:00 Walk before 14:30 Play |
| **Pet Filtering** | `Scheduler.filter_by_pet(pet_name)` | Show only tasks for a specific pet | Tasks for "Biscuit" vs "Luna" |
| **Status Filtering** | `Scheduler.filter_by_status(completed)` | Filter tasks by completion status (pending vs completed) | Show only incomplete tasks for today's schedule |
| **Conflict Detection** | `Scheduler.detect_conflicts()` | Identify tasks scheduled at same time and suggest reassignment | Flags "Walk @ 08:00" + "Feeding @ 08:00" |
| **Recurring Tasks** | `Task.mark_complete()` + `frequency` field | Auto-generate next occurrence when daily/weekly tasks are marked complete | Daily Feeding → creates tomorrow's feeding automatically |
| **Time Slot Assignment** | `Scheduler.assign_time_slots(tasks, start_time)` | Automatically calculate start times for unscheduled tasks | 5 tasks → 08:00, 08:30, 08:40, 09:00, 09:30 |
| **Availability Fitting** | `Scheduler.generate_plan(available_minutes)` | Fit maximum high-priority tasks within time constraints | 3 hours available → fit 6 tasks (90 min used, 90 min free) |

### Algorithm Highlights

**Greedy Priority-Based Scheduling:**
- Sort all pending tasks by priority (high→low, duration short→long)
- Sequentially add tasks to the plan until available time runs out
- Time complexity: O(n log n) for sorting, O(n) for fitting
- Space complexity: O(n) for sorted task list

**Smart Filtering:**
- Filter tasks across all pets and return matching subset
- Used in UI to show per-pet workload
- Helps owners focus on one pet at a time

**Conflict Detection:**
- Group tasks by time_slot (HH:MM)
- Flag groups with 2+ tasks at same time
- Returns warning messages for UI to display
- Currently checks **exact** time matches (not duration overlaps)

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
