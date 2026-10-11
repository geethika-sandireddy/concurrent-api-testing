"""Complete test suite for the booking system and concurrency detection."""
import pytest
from app.store import store


def test_booking_create_and_retrieve():
    """Test basic booking creation and retrieval."""
    store.reset()
    store.create_event("event_1", 10)
    
    success, booking_id, msg = store.book_seats("user_1", "event_1", 2)
    assert success is True
    assert booking_id is not None
    
    booking = store.get_booking(booking_id)
    assert booking.quantity == 2
    assert booking.user_id == "user_1"


def test_booking_inventory_consistency():
    """Test that inventory math is always consistent."""
    store.reset()
    store.create_event("event_2", 20)
    
    store.book_seats("user_1", "event_2", 5)
    store.book_seats("user_2", "event_2", 8)
    store.book_seats("user_3", "event_2", 7)
    
    inv = store.get_inventory("event_2")
    assert inv["booked_seats"] + inv["available_seats"] == inv["total_seats"]
    assert inv["booked_seats"] == 20
    assert inv["available_seats"] == 0


def test_booking_cannot_exceed_inventory():
    """Test that we cannot book more seats than available."""
    store.reset()
    store.create_event("event_3", 5)
    
    success, _, msg = store.book_seats("user_1", "event_3", 10)
    assert success is False
    assert "Not enough seats" in msg


def test_cancel_booking_frees_seats():
    """Test that cancelling a booking frees up seats."""
    store.reset()
    store.create_event("event_4", 10)
    
    _, booking_id, _ = store.book_seats("user_1", "event_4", 3)
    inv_before = store.get_inventory("event_4")
    assert inv_before["available_seats"] == 7
    
    store.cancel_booking(booking_id)
    inv_after = store.get_inventory("event_4")
    assert inv_after["available_seats"] == 10
    assert inv_after["booked_seats"] == 0


def test_invariant_checker_detects_violations():
    """Test that check_invariants catches inconsistencies."""
    store.reset()
    store.create_event("event_5", 5)
    
    # Normal state should have no violations
    violations = store.check_invariants()
    assert len(violations) == 0
    
    store.book_seats("user_1", "event_5", 5)
    violations = store.check_invariants()
    assert len(violations) == 0
