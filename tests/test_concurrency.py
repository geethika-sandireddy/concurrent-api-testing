"""Tests for the concurrency scheduler and bug detection."""
import pytest
from core.scheduler import (
    BuggyInventoryStore,
    InterleaveScheduler,
    build_booking_workload,
    BookingAttempt,
)
from core.invariant_checker import InvariantChecker


def test_buggy_store_oversells_single_seat():
    """The buggy store should demonstrate overselling with concurrent access."""
    store = BuggyInventoryStore(total_seats=1)
    scheduler = InterleaveScheduler(store)
    
    # Two users try to book the last seat simultaneously
    attempts = [
        BookingAttempt(user_id="user_1", event_id="demo", quantity=1),
        BookingAttempt(user_id="user_2", event_id="demo", quantity=1),
    ]
    
    results = scheduler.run_workload(attempts, max_workers=2)
    
    # Both should "succeed" but inventory should be negative
    assert len(results) == 2
    assert store.inventory["booked"] == 2
    assert store.inventory["available"] == -1


def test_invariant_checker_catches_overselling():
    """The invariant checker should detect when available goes negative."""
    checker = InvariantChecker()
    
    bad_state = {
        "event_id": "demo",
        "total_seats": 1,
        "available": -1,
        "booked": 2,
    }
    
    violations = checker.run_checks(bad_state, [])
    
    # Should catch both negative seats and seat count mismatch
    violation_names = {v.name for v in violations}
    assert "negative_available_seats" in violation_names
    assert "seat_count_mismatch" in violation_names


def test_build_booking_workload():
    """Test that workload builder creates correct booking attempts."""
    workload = build_booking_workload(total_users=5, seats_per_booking=2)
    
    assert len(workload) == 5
    assert all(a.quantity == 2 for a in workload)
    assert all(a.event_id == "event_demo" for a in workload)
    assert workload[0].user_id == "user_1"
    assert workload[4].user_id == "user_5"
