"""API routes for the booking system."""
from fastapi import APIRouter, HTTPException, status
from datetime import datetime
from app.models import BookingRequest, BookingResponse, EventInventory, BookingStatus
from app.store import store


router = APIRouter(prefix="/api", tags=["bookings"])


@router.post("/events/{event_id}/initialize", status_code=status.HTTP_201_CREATED)
def initialize_event(event_id: str, total_seats: int):
    """Initialize an event with a specific number of seats."""
    if total_seats <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Total seats must be greater than 0"
        )
    
    store.create_event(event_id, total_seats)
    return {
        "event_id": event_id,
        "total_seats": total_seats,
        "message": "Event initialized successfully"
    }


@router.get("/events/{event_id}/inventory", response_model=EventInventory)
def get_event_inventory(event_id: str):
    """Get inventory status for an event."""
    inv = store.get_inventory(event_id)
    if inv["total_seats"] == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event {event_id} not found"
        )
    
    return EventInventory(
        event_id=event_id,
        total_seats=inv["total_seats"],
        available_seats=inv["available_seats"],
        booked_seats=inv["booked_seats"]
    )


@router.post("/bookings", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(booking_req: BookingRequest):
    """Create a new booking."""
    success, booking_id, message = store.book_seats(
        booking_req.user_id,
        booking_req.event_id,
        booking_req.quantity
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )
    
    booking = store.get_booking(booking_id)
    return BookingResponse(
        booking_id=booking.booking_id,
        user_id=booking.user_id,
        event_id=booking.event_id,
        quantity=booking.quantity,
        status=booking.status,
        created_at=booking.created_at,
        updated_at=booking.updated_at
    )


@router.get("/bookings/{booking_id}", response_model=BookingResponse)
def get_booking(booking_id: str):
    """Get a booking by ID."""
    booking = store.get_booking(booking_id)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Booking {booking_id} not found"
        )
    
    return BookingResponse(
        booking_id=booking.booking_id,
        user_id=booking.user_id,
        event_id=booking.event_id,
        quantity=booking.quantity,
        status=booking.status,
        created_at=booking.created_at,
        updated_at=booking.updated_at
    )


@router.get("/events/{event_id}/bookings")
def list_event_bookings(event_id: str):
    """List all bookings for an event."""
    bookings = store.get_all_bookings(event_id)
    return [
        BookingResponse(
            booking_id=b.booking_id,
            user_id=b.user_id,
            event_id=b.event_id,
            quantity=b.quantity,
            status=b.status,
            created_at=b.created_at,
            updated_at=b.updated_at
        )
        for b in bookings
    ]


@router.post("/bookings/{booking_id}/cancel")
def cancel_booking(booking_id: str):
    """Cancel a booking."""
    success = store.cancel_booking(booking_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not cancel booking {booking_id}"
        )
    
    return {"message": "Booking cancelled successfully", "booking_id": booking_id}


@router.post("/health-check")
def health_check():
    """Health check endpoint."""
    violations = store.check_invariants()
    return {
        "status": "healthy" if not violations else "unhealthy",
        "invariant_violations": violations,
        "timestamp": datetime.now()
    }


@router.post("/reset")
def reset_system():
    """Reset the entire system (for testing)."""
    store.reset()
    return {"message": "System reset successfully"}


@router.get("/debug/operations-log")
def get_operations_log():
    """Get the operations log (debugging)."""
    return {"operations": store.get_operations_log()}
