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

## Smarter Scheduling

The scheduler now includes:

- Task sorting by duration, priority, and time.
- Pet-level and status-level filtering (`Owner.get_tasks_filtered`).
- Recurring task automation: marking daily/weekly tasks complete creates the next occurrence.
- Conflict detection (`Scheduler.detect_conflicts`) that returns warnings for overlapping tasks instead of crashing.
- Human-readable explanation output via `Scheduler.explain` including conflict warnings.

The update includes agentic workflow elements, creating a scheduling agent that handles the scheduling logic and interacts with the user to gather necessary information for scheduling. The agent would be responsible for understanding user preferences, constraints, and generating a schedule accordingly.

Limitations it should tackle: 
    - handling priority considerations rather than the greedy approach of scheduling the shortest task first. 
    - ensuring that the generated schedule is feasible and efficient and considering the time constraints of the user and the pet's needs, e.g accouting for the break time and the energy levels of the pet and the user.
    - providing explanations for the generated schedule to help the user understand the reasoning behind it.  

## 📸 System Diagram
 <a href="/assets/system-diagram.png" target="_blank"><img src='/assets/system-diagram.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>.
## Testing PawPal+
To run tests, type the following command in the terminal:

```bash
python -m pytest
```

Suggested checks:
- Verify tasks are returned in chronological order.
- Confirm that marking a daily task complete creates a new task for the following day.
- Verify that the scheduler returns warnings for overlapping times.


Confidence level = 5

## Features

PawPal+ includes practical planning features designed for daily pet care:

- Smart daily planning within a chosen time window.
- Clear schedule output with task start/end times.
- Built-in conflict warnings for overlapping tasks.
- Task views that can be sorted and filtered for quick review.
- Recurring care support for daily and weekly routines.
- Human-readable plan explanations so users understand scheduling decisions.

## How It Works

The current implementation uses the following algorithms and scheduling behaviors:

1. Greedy time-window scheduling
- Pending tasks are assigned from the chosen start time forward until the window is full.
- Tasks that do not fit in the remaining time are skipped.

2. Deterministic pre-scheduling sort
- Tasks are sorted before assignment to keep outputs consistent and repeatable.
- The scheduler uses completion state, duration, and description as ordering keys.

3. Chronological ordering for display
- Scheduled tasks are presented in start-time order to make the plan easy to follow.

4. Overlap-based conflict detection
- Scheduled intervals are compared for overlap.
- When conflicts exist, warning messages are generated instead of failing the run.

5. Filtered retrieval across owners and pets
- Tasks can be filtered by status (`all`, `pending`, `completed`).
- Optional pet-name filtering supports focused, pet-specific views.

6. Recurrence automation on completion
- Completing a task with `daily` or `weekly` frequency creates the next occurrence automatically.

7. Explainable output generation
- The scheduler builds a readable summary of scheduled tasks.
- Conflict warnings are included in the same explanation output when present.
## 📸 Demo
 <a href="/course_images/ai110/pawpal.png" target="_blank"><img src='/course_images/ai110/pawpal.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>.
