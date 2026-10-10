"""Concurrency workload generator and scheduler for InterleaveLab."""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Any, Dict, List
import time


@dataclass
class BookingAttempt:
    """One booking request in a concurrent workload."""
    user_id: str
    event_id: str
    quantity: int = 1
    label: str = ""


class BuggyInventoryStore:
    """An unsafe inventory store used to simulate a race condition.
    
    This class intentionally avoids locks so we can demonstrate
    how concurrent access without synchronization causes overselling bugs.
    """

    def __init__(self, total_seats: int):
        self.total_seats = total_seats
        self.inventory = {
            "available": total_seats,
            "booked": 0,
        }
        self.operations: List[str] = []

    def book_seats(self, user_id: str, event_id: str, quantity: int) -> Dict[str, Any]:
        """Unsafe booking logic that reads and writes without locks.
        
        The race condition happens because multiple threads can read the same
        available seat count before any of them write the updated value.
        """
        available_before = self.inventory["available"]
        self.operations.append(
            f"user={user_id} read available={available_before} qty={quantity}"
        )

        # Simulate interleaving: threads pause here after reading but before writing
        time.sleep(0.001)  # Small delay to increase chance of interleaving
        
        updated_available = available_before - quantity
        self.inventory["available"] = updated_available
        self.inventory["booked"] += quantity

        self.operations.append(
            f"user={user_id} wrote available={updated_available} booked={self.inventory['booked']}"
        )

        return {
            "success": True,
            "user_id": user_id,
            "event_id": event_id,
            "quantity": quantity,
            "available_after": updated_available,
            "booked_after": self.inventory["booked"],
        }


class InterleaveScheduler:
    """Runs many booking attempts in parallel to reproduce race conditions."""

    def __init__(self, store: BuggyInventoryStore):
        self.store = store
        self.execution_trace: List[str] = []

    def run_workload(self, attempts: List[BookingAttempt], max_workers: int = 4) -> List[Dict[str, Any]]:
        """Execute a workload in parallel to trigger race conditions.
        
        Args:
            attempts: List of booking attempts to execute concurrently
            max_workers: Number of concurrent threads
            
        Returns:
            List of results from each booking attempt
        """
        results: List[Dict[str, Any]] = []

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_map = {
                executor.submit(self._execute_attempt, attempt): attempt for attempt in attempts
            }

            for future in as_completed(future_map):
                results.append(future.result())

        return results

    def _execute_attempt(self, attempt: BookingAttempt) -> Dict[str, Any]:
        """Execute one booking attempt."""
        return self.store.book_seats(attempt.user_id, attempt.event_id, attempt.quantity)


def build_booking_workload(total_users: int = 5, seats_per_booking: int = 1) -> List[BookingAttempt]:
    """Create a workload where multiple users try to book seats simultaneously.
    
    This simulates a real-world scenario where many users try to book the final seat.
    """
    attempts: List[BookingAttempt] = []

    for i in range(total_users):
        attempts.append(
            BookingAttempt(
                user_id=f"user_{i + 1}",
                event_id="event_demo",
                quantity=seats_per_booking,
                label=f"attempt_{i + 1}",
            )
        )

    return attempts
