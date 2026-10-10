"""Invariant checks for detecting overselling and other concurrency issues."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List


@dataclass
class InvariantViolation:
    """A single invariant violation captured during a workload run."""
    name: str
    description: str
    event_id: str
    details: Dict[str, Any]
    timestamp: datetime


class InvariantChecker:
    """Detects invariant violations in concurrent booking scenarios."""

    def check_inventory(self, event_id: str, total_seats: int, available: int, booked: int) -> List[InvariantViolation]:
        """Check seat count invariants.
        
        Invariants:
        - available_seats >= 0 (can't have negative seats)
        - booked_seats >= 0 (can't have negative bookings)
        - available_seats + booked_seats == total_seats (conservation of seats)
        """
        violations: List[InvariantViolation] = []

        if available < 0:
            violations.append(
                InvariantViolation(
                    name="negative_available_seats",
                    description="Available seats became negative, indicating overselling.",
                    event_id=event_id,
                    details={"available": available, "booked": booked, "total": total_seats},
                    timestamp=datetime.now(),
                )
            )

        if booked < 0:
            violations.append(
                InvariantViolation(
                    name="negative_booked_seats",
                    description="Booked seats became negative.",
                    event_id=event_id,
                    details={"available": available, "booked": booked, "total": total_seats},
                    timestamp=datetime.now(),
                )
            )

        if booked + available != total_seats:
            violations.append(
                InvariantViolation(
                    name="seat_count_mismatch",
                    description="Booked seats and available seats no longer match the total.",
                    event_id=event_id,
                    details={"available": available, "booked": booked, "total": total_seats},
                    timestamp=datetime.now(),
                )
            )

        return violations

    def check_duplicates(self, event_id: str, attempts: List[Dict[str, Any]]) -> List[InvariantViolation]:
        """Catch duplicate logical operations in the same workload."""
        duplicates: List[InvariantViolation] = []
        seen = set()

        for attempt in attempts:
            user_id = attempt.get("user_id")
            key = (event_id, user_id)

            if key in seen:
                duplicates.append(
                    InvariantViolation(
                        name="duplicate_operation",
                        description=f"The same logical operation was processed twice for user {user_id}.",
                        event_id=event_id,
                        details={"user_id": user_id, "event_id": event_id},
                        timestamp=datetime.now(),
                    )
                )
            else:
                seen.add(key)

        return duplicates

    def run_checks(self, store_state: Dict[str, Any], attempts: List[Dict[str, Any]]) -> List[InvariantViolation]:
        """Run all invariant checks against a store state."""
        violations: List[InvariantViolation] = []
        total_seats = store_state.get("total_seats", 0)
        available = store_state.get("available", 0)
        booked = store_state.get("booked", 0)

        violations.extend(
            self.check_inventory(
                event_id=store_state.get("event_id", "unknown"),
                total_seats=total_seats,
                available=available,
                booked=booked,
            )
        )

        violations.extend(
            self.check_duplicates(
                event_id=store_state.get("event_id", "unknown"),
                attempts=attempts,
            )
        )

        return violations
