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
================== test session starts ==================
platform win32 -- Python 3.14.2, pytest-9.1.0, pluggy-1.6.0
collected 20 items                                       

tests/test_pawpal.py::TestTask::test_task_completion PASSED [  5%]
tests/test_pawpal.py::TestTask::test_task_incomplete PASSED [ 10%]
tests/test_pawpal.py::TestTask::test_task_validation_valid PASSED [ 15%]
tests/test_pawpal.py::TestTask::test_task_validation_invalid_priority PASSED [ 20%]
tests/test_pawpal.py::TestTask::test_task_validation_invalid_duration PASSED [ 25%]
tests/test_pawpal.py::TestTask::test_task_priority_level_high PASSED [ 30%]
tests/test_pawpal.py::TestTask::test_task_priority_level_medium PASSED [ 35%]
tests/test_pawpal.py::TestTask::test_task_priority_level_low PASSED [ 40%]
tests/test_pawpal.py::TestPet::test_pet_add_task PASSED [ 45%]
tests/test_pawpal.py::TestPet::test_pet_add_multiple_tasks PASSED [ 50%]
tests/test_pawpal.py::TestPet::test_pet_add_invalid_task PASSED [ 55%]
tests/test_pawpal.py::TestPet::test_pet_remove_task PASSED [ 60%]
tests/test_pawpal.py::TestPet::test_pet_get_pending_tasks PASSED [ 65%]
tests/test_pawpal.py::TestPet::test_pet_get_info PASSED [ 70%]
tests/test_pawpal.py::TestOwner::test_owner_add_pet PASSED [ 75%]
tests/test_pawpal.py::TestOwner::test_owner_get_all_tasks PASSED [ 80%]
tests/test_pawpal.py::TestOwner::test_owner_availability PASSED [ 85%]
tests/test_pawpal.py::TestScheduler::test_scheduler_sort_by_priority PASSED [ 90%]
tests/test_pawpal.py::TestScheduler::test_scheduler_generate_plan_respects_time PASSED [ 95%]
tests/test_pawpal.py::TestScheduler::test_scheduler_pending_tasks_only PASSED [100%]

================== 20 passed in 0.15s ===================
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | | e.g., by priority, duration |
| Filtering | | e.g., skip tasks if time runs out |
| Conflict handling | | e.g., overlapping time slots |
| Recurring tasks | | e.g., daily vs. weekly |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
