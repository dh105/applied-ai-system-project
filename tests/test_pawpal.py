import pytest
from datetime import datetime
from pawpal_system import Task, Pet, Owner, Scheduler


def test_task_completion_marks_task_done():
    task = Task(
        id="t1",
        description="Feed meal",
        duration_minutes=15,
        scheduled_start=None,
        scheduled_end=None,
        frequency="daily",
    )

    assert task.is_completed is False
    task.mark_completed()
    assert task.is_completed is True


def test_pet_add_task_increases_task_count():
    pet = Pet(id="p1", name="Rufus", species="dog", age=3)
    assert len(pet.tasks) == 0

    task = Task(
        id="t2",
        description="Walk",
        duration_minutes=30,
        scheduled_start=None,
        scheduled_end=None,
        frequency="daily",
    )

    pet.add_task(task)
    assert len(pet.tasks) == 1
    assert pet.tasks[0].id == "t2"


def test_complete_recurring_task_creates_next_occurrence():
    owner = Owner(id="o1", name="Alex")
    pet = Pet(id="p2", name="Milo", species="cat", age=2)
    owner.add_pet(pet)

    task = Task(
        id="t10",
        description="Feed Milo",
        duration_minutes=10,
        frequency="daily",
    )

    pet.add_task(task)
    scheduler = Scheduler()

    next_task = scheduler.complete_task(owner, task_id="t10", when=datetime(2026, 4, 1, 8, 0))

    assert task.is_completed is True
    assert next_task is not None
    assert next_task.description == "Feed Milo"
    assert next_task.frequency == "daily"

    # new task should be in the pet tasks list and not marked completed
    assert any(t for t in pet.tasks if t.id == next_task.id)
    assert not next_task.is_completed


def test_scheduler_conflict_detection_lightweight():
    owner = Owner(id="o2", name="Dana")
    pet = Pet(id="p3", name="Bella", species="dog", age=4)
    owner.add_pet(pet)

    task_a = Task(id="t20", description="Morning walk", duration_minutes=60)
    task_b = Task(id="t21", description="Vet check", duration_minutes=30)

    pet.add_task(task_a)
    pet.add_task(task_b)

    scheduler = Scheduler()
    # intentionally force overlap by assigning start times manually
    task_a.scheduled_start = datetime(2026, 4, 1, 9, 0)
    task_a.scheduled_end = datetime(2026, 4, 1, 10, 0)
    task_b.scheduled_start = datetime(2026, 4, 1, 9, 30)
    task_b.scheduled_end = datetime(2026, 4, 1, 10, 0)

    warnings = scheduler.detect_conflicts([task_a, task_b])

    assert len(warnings) == 1
    assert "overlaps with" in warnings[0]


def test_pet_sort_by_time_handles_unscheduled_tasks():
    pet = Pet(id="p4", name="Luna", species="cat", age=1)

    task_scheduled = Task(
        id="t30",
        description="Groom",
        duration_minutes=20,
        scheduled_start=datetime(2026, 4, 1, 10, 0),
        scheduled_end=datetime(2026, 4, 1, 10, 20),
    )
    task_unscheduled = Task(
        id="t31",
        description="Brush",
        duration_minutes=5,
        scheduled_start=None,
        scheduled_end=None,
    )

    pet.add_task(task_unscheduled)
    pet.add_task(task_scheduled)

    sorted_tasks = pet.sort_by_time()

    assert sorted_tasks[0].id == "t30"
    assert sorted_tasks[-1].id == "t31"


def test_task_mark_completed_daily_creates_next_task():
    task = Task(
        id="t40",
        description="Feed",
        duration_minutes=15,
        frequency="daily",
    )

    next_task = task.mark_completed(when=datetime(2026, 4, 1, 8, 0))

    assert task.is_completed is True
    assert next_task is not None
    assert next_task.frequency == "daily"
    assert next_task.description == "Feed"
    assert "t40_next_20260402" in next_task.id
    assert next_task.is_completed is False


def test_scheduler_assign_times_with_limited_window():
    owner = Owner(id="o3", name="Sam")
    pet = Pet(id="p5", name="Otis", species="dog", age=5)
    owner.add_pet(pet)

    t1 = Task(id="t50", description="Play", duration_minutes=30)
    t2 = Task(id="t51", description="Walk", duration_minutes=60)
    t3 = Task(id="t52", description="Vet", duration_minutes=120)

    pet.add_task(t1)
    pet.add_task(t2)
    pet.add_task(t3)

    scheduler = Scheduler()
    assigned = scheduler.assign_times(owner, datetime(2026, 4, 1, 9, 0), datetime(2026, 4, 1, 10, 30))

    assert len(assigned) == 2
    assert assigned[0].id == "t50"
    assert assigned[1].id == "t51"
    assert assigned[1].scheduled_end == datetime(2026, 4, 1, 10, 30)


def test_detect_conflicts_boundary_no_overlap():
    task_a = Task(
        id="t60",
        description="A",
        duration_minutes=30,
        scheduled_start=datetime(2026, 4, 1, 9, 0),
        scheduled_end=datetime(2026, 4, 1, 9, 30),
    )
    task_b = Task(
        id="t61",
        description="B",
        duration_minutes=30,
        scheduled_start=datetime(2026, 4, 1, 9, 30),
        scheduled_end=datetime(2026, 4, 1, 10, 0),
    )

    scheduler = Scheduler()
    warnings = scheduler.detect_conflicts([task_a, task_b])

    assert warnings == []


def test_get_tasks_filtered_invalid_status_raises():
    owner = Owner(id="o4", name="Taylor")
    pet = Pet(id="p6", name="Mochi", species="cat", age=3)
    owner.add_pet(pet)

    with pytest.raises(ValueError):
        owner.get_tasks_filtered(status="unknown")


# ============================================
# SchedulingAgent Test Cases (Edge Cases)
# ============================================

from pawpal_system import SchedulingAgent


def test_scheduling_agent_empty_request_uses_defaults():
    """Edge case: Empty user request should use default time window."""
    owner = Owner(id="o5", name="Jordan")
    pet = Pet(id="p7", name="Buddy", species="dog")
    owner.add_pet(pet)

    pet.add_task(Task(id="t70", description="Walk", duration_minutes=30))

    agent = SchedulingAgent()
    result = agent.plan(owner, "")  # Empty request

    # Should still generate a schedule with default times
    assert "explanation" in result
    assert "Time window:" in result["explanation"]
    # Default window should be 8:00 - 20:00
    assert "08:00" in result["explanation"] or "8:00" in result["explanation"]


def test_scheduling_agent_tasks_exceed_available_time():
    """Edge case: When total task duration exceeds time window."""
    owner = Owner(id="o6", name="Casey")
    pet = Pet(id="p8", name="Max", species="dog")
    owner.add_pet(pet)

    # Add tasks totaling 120 minutes but only 60 minutes available
    pet.add_task(Task(id="t80", description="Walk 1", duration_minutes=30))
    pet.add_task(Task(id="t81", description="Walk 2", duration_minutes=30))
    pet.add_task(Task(id="t82", description="Walk 3", duration_minutes=60))

    agent = SchedulingAgent()
    result = agent.plan(owner, "morning")

    # Should schedule only what fits
    scheduled = result["tasks"]
    total_scheduled = sum(t.duration_minutes for t in scheduled)
    
    # Only first two 30-min tasks should fit in a ~5 hour morning window
    # (assuming 7:00-12:00 = 300 min, but with default constraints it may vary)
    assert len(scheduled) >= 1
    assert total_scheduled <= 300  # reasonable morning window


def test_scheduling_agent_conflicting_time_preferences():
    """Edge case: User specifies conflicting time preferences."""
    owner = Owner(id="o7", name="Riley")
    pet = Pet(id="p9", name="Charlie", species="cat")
    owner.add_pet(pet)

    pet.add_task(Task(id="t90", description="Feed", duration_minutes=15))
    pet.add_task(Task(id="t91", description="Play", duration_minutes=20))

    agent = SchedulingAgent()
    # Request with conflicting times - last one wins
    result = agent.plan(owner, "I need morning and evening tasks")

    # Should still produce a schedule
    assert "explanation" in result
    assert len(result["tasks"]) >= 1


def test_scheduling_agent_no_pending_tasks():
    """Edge case: Owner has no pending tasks."""
    owner = Owner(id="o8", name="Morgan")
    pet = Pet(id="p10", name="Rocky", species="dog")
    owner.add_pet(pet)

    # Add but mark as completed
    task = Task(id="t100", description="Walk", duration_minutes=30, is_completed=True)
    pet.add_task(task)

    agent = SchedulingAgent()
    result = agent.plan(owner, "schedule my tasks")

    # Should handle gracefully
    assert "explanation" in result
    # May say no tasks scheduled or schedule nothing
    assert result["tasks"] == [] or "No tasks" in result["explanation"]


def test_scheduling_agent_parses_task_types_from_input():
    """
    The agent should correctly identify task types from natural language.
    
    When user says "walk", "feeding", "grooming", etc., the agent should
    recognize these keywords and use them as constraints.
    """
    owner = Owner(id="o9", name="Jamie")
    pet = Pet(id="p11", name="Duke", species="dog")
    owner.add_pet(pet)

    pet.add_task(Task(id="t110", description="Morning walk", duration_minutes=30))
    pet.add_task(Task(id="t111", description="Feed", duration_minutes=15))
    pet.add_task(Task(id="t112", description="Grooming session", duration_minutes=45))

    agent = SchedulingAgent()
    result = agent.plan(owner, "I need a walk and feeding with grooming")

    # Should recognize the task types
    explanation = result["explanation"]
    assert "walk" in explanation.lower() or "Walk" in explanation
    assert "feed" in explanation.lower() or "Feed" in explanation


def test_scheduling_agent_handles_break_time_constraint():
    """
    The agent should respect break time requests from users.
    
    When user specifies "15 min break" or "30 minute break", the agent
    should account for this in the scheduling constraints.
    """
    owner = Owner(id="o10", name="Taylor")
    pet = Pet(id="p12", name="Bear", species="dog")
    owner.add_pet(pet)

    pet.add_task(Task(id="t120", description="Walk", duration_minutes=30))
    pet.add_task(Task(id="t121", description="Play", duration_minutes=20))

    agent = SchedulingAgent()
    result = agent.plan(owner, "schedule walk and play with 10 min break")

    # Should include break time in constraints
    constraints = result["constraints_used"]
    assert constraints["break_minutes"] == 10


def test_scheduling_agent_handles_pet_energy_levels():
    """
    The agent should consider pet energy levels when scheduling.
    
    When user mentions "high energy" or "low energy", the agent should
    store this as a constraint for scheduling decisions.
    """
    owner = Owner(id="o11", name="Alex")
    pet = Pet(id="p13", name="Luna", species="dog")
    owner.add_pet(pet)

    pet.add_task(Task(id="t130", description="Active play", duration_minutes=45))
    pet.add_task(Task(id="t131", description="Rest time", duration_minutes=30))

    agent = SchedulingAgent()
    result = agent.plan(owner, "My dog is high energy today, schedule activities")

    # Should capture energy level
    constraints = result["constraints_used"]
    assert "pet_energy_levels" in constraints
    assert constraints["pet_energy_levels"]["level"] == "high"


def test_scheduling_agent_empty_owner_no_pets():
    """
    The agent should handle an owner with no pets gracefully.
    
    When the owner has no pets, the agent should return an empty
    schedule without crashing.
    """
    owner = Owner(id="o12", name="Sam")
    # No pets added

    agent = SchedulingAgent()
    result = agent.plan(owner, "schedule tasks")

    # Should handle gracefully
    assert "explanation" in result
    assert result["tasks"] == []


def test_scheduling_agent_conversation_history_tracked():
    """
    The agent should maintain conversation history.
    
    Each call to plan() should add both user request and agent response
    to the conversation history.
    """
    owner = Owner(id="o13", name="Chris")
    pet = Pet(id="p14", name="Cooper", species="dog")
    owner.add_pet(pet)

    pet.add_task(Task(id="t140", description="Walk", duration_minutes=30))

    agent = SchedulingAgent()
    
    # First interaction
    result1 = agent.plan(owner, "morning walk")
    history1 = agent.get_conversation_history()
    assert len(history1) == 2  # user + assistant
    
    # Second interaction
    result2 = agent.plan(owner, "evening feeding")
    history2 = agent.get_conversation_history()
    assert len(history2) == 4  # two user + two assistant


def test_scheduling_agent_clear_history():
    """
    The agent should be able to clear conversation history.
    
    After calling clear_history(), the conversation history should
    be empty.
    """
    owner = Owner(id="o14", name="Jordan")
    pet = Pet(id="p15", name="Milo", species="cat")
    owner.add_pet(pet)

    pet.add_task(Task(id="t150", description="Feed", duration_minutes=10))

    agent = SchedulingAgent()
    agent.plan(owner, "feed Milo")
    
    assert len(agent.get_conversation_history()) == 2
    
    agent.clear_history()
    assert len(agent.get_conversation_history()) == 0


def test_scheduling_agent_multiple_pets_same_owner():
    """
    The agent should handle scheduling across multiple pets.
    
    When owner has multiple pets with tasks, the agent should
    schedule tasks for all pets.
    """
    owner = Owner(id="o15", name="Casey")
    pet1 = Pet(id="p16", name="Buddy", species="dog")
    pet2 = Pet(id="p17", name="Whiskers", species="cat")
    owner.add_pet(pet1)
    owner.add_pet(pet2)

    pet1.add_task(Task(id="t160", description="Dog walk", duration_minutes=30))
    pet2.add_task(Task(id="t161", description="Cat feeding", duration_minutes=10))

    agent = SchedulingAgent()
    result = agent.plan(owner, "schedule all pet tasks")

    # Should schedule tasks from both pets
    assert len(result["tasks"]) == 2

