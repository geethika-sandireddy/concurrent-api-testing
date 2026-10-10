"""In-memory store for bookings and inventory."""
import threading
from typing import Dict, List
from datetime import datetime
from app.models import BookingStatus


class Booking:
    """Internal booking data structure."""
    def __init__(self, booking_id: str, user_id: str, event_id: str, 
                 quantity: int, status: BookingStatus):
        self.booking_id = booking_id
        self.user_id = user_id
        self.event_id = event_id
        self.quantity = quantity
        self.status = status
        self.created_at = datetime.now()
        self.updated_at = datetime.now()


class EventInventoryStore:
    """Thread-safe in-memory store for event inventory and bookings."""
    
    def __init__(self):
        self.lock = threading.RLock()  # Reentrant lock
        self.inventory: Dict[str, Dict[str, int]] = {}
        self.bookings: Dict[str, Booking] = {}
        self.booking_counter = 0
        self.operations_log: List[str] = []  # For debugging

    def create_event(self, event_id: str, total_seats: int) -> None:
        """Create a new event with initial inventory."""
        with self.lock:
            if event_id not in self.inventory:
                self.inventory[event_id] = {
                    "total_seats": total_seats,
                    "available_seats": total_seats,
                    "booked_seats": 0
                }
                self.operations_log.append(f"create_event: {event_id} with {total_seats} seats")

    def get_inventory(self, event_id: str) -> Dict[str, int]:
        """Get current inventory for an event."""
        with self.lock:
            if event_id in self.inventory:
                return self.inventory[event_id].copy()
            return {"total_seats": 0, "available_seats": 0, "booked_seats": 0}

    def book_seats(self, user_id: str, event_id: str, quantity: int) -> tuple:
        """Attempt to book seats. Returns (success, booking_id, message)."""
        with self.lock:
            if event_id not in self.inventory:
                return False, None, f"Event {event_id} not found"
            
            inv = self.inventory[event_id]
            
            # Invariant check: booked + available should equal total
            current_total = inv["booked_seats"] + inv["available_seats"]
            if current_total != inv["total_seats"]:
                return False, None, "Invariant violation: seat count mismatch"
            
            # Check if enough seats available
            if inv["available_seats"] < quantity:
                return False, None, f"Not enough seats. Requested: {quantity}, Available: {inv['available_seats']}"
            
            # Book the seats
            self.booking_counter += 1
            booking_id = f"booking_{self.booking_counter}"
            
            booking = Booking(booking_id, user_id, event_id, quantity, BookingStatus.CONFIRMED)
            self.bookings[booking_id] = booking
            
            # Update inventory
            inv["available_seats"] -= quantity
            inv["booked_seats"] += quantity
            
            self.operations_log.append(
                f"book_seats: user={user_id}, event={event_id}, qty={quantity}, booking={booking_id}"
            )
            
            return True, booking_id, "Booking confirmed"

    def get_booking(self, booking_id: str) -> Booking:
        """Get a booking by ID."""
        with self.lock:
            return self.bookings.get(booking_id)

    def get_all_bookings(self, event_id: str) -> List[Booking]:
        """Get all bookings for an event."""
        with self.lock:
            return [b for b in self.bookings.values() if b.event_id == event_id]

    def cancel_booking(self, booking_id: str) -> bool:
        """Cancel a booking and free up seats."""
        with self.lock:
            if booking_id not in self.bookings:
                return False
            
            booking = self.bookings[booking_id]
            if booking.status == BookingStatus.CANCELLED:
                return False  # Already cancelled
            
            # Free up seats
            inv = self.inventory[booking.event_id]
            inv["available_seats"] += booking.quantity
            inv["booked_seats"] -= booking.quantity
            
            booking.status = BookingStatus.CANCELLED
            booking.updated_at = datetime.now()
            
            self.operations_log.append(
                f"cancel_booking: booking={booking_id}, qty={booking.quantity}"
            )
            
            return True

    def reset(self) -> None:
        """Reset store to initial state."""
        with self.lock:
            self.inventory.clear()
            self.bookings.clear()
            self.booking_counter = 0
            self.operations_log.clear()
            self.operations_log.append("reset: store cleared")

    def get_operations_log(self) -> List[str]:
        """Get the log of all operations (for debugging/tracing)."""
        with self.lock:
            return self.operations_log.copy()

    def check_invariants(self) -> List[str]:
        """Check all invariants and return violations."""
        violations = []
        with self.lock:
            # Invariant 1: total seats should equal booked + available
            for event_id, inv in self.inventory.items():
                total = inv["booked_seats"] + inv["available_seats"]
                if total != inv["total_seats"]:
                    violations.append(
                        f"Event {event_id}: Seat count mismatch. "
                        f"Booked {inv['booked_seats']} + Available {inv['available_seats']} != Total {inv['total_seats']}"
                    )
                
                # Invariant 2: no negative seats
                if inv["available_seats"] < 0:
                    violations.append(f"Event {event_id}: Negative available seats: {inv['available_seats']}")
                if inv["booked_seats"] < 0:
                    violations.append(f"Event {event_id}: Negative booked seats: {inv['booked_seats']}")
            
            # Invariant 3: no duplicate bookings
            booking_ids = list(self.bookings.keys())
            if len(booking_ids) != len(set(booking_ids)):
                violations.append("Duplicate booking IDs detected")
        
        return violations


# Global store instance
store = EventInventoryStore()
