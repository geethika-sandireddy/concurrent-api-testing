"""Data models for the booking system."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class BookingStatus(str, Enum):
    """Booking status enumeration."""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    FAILED = "failed"


class BookingRequest(BaseModel):
    """Request model for creating a booking."""
    user_id: str
    event_id: str
    quantity: int = 1

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user_123",
                "event_id": "event_456",
                "quantity": 1
            }
        }


class BookingResponse(BaseModel):
    """Response model for a booking."""
    booking_id: str
    user_id: str
    event_id: str
    quantity: int
    status: BookingStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "booking_id": "booking_789",
                "user_id": "user_123",
                "event_id": "event_456",
                "quantity": 1,
                "status": "confirmed",
                "created_at": "2024-01-15T10:30:00",
                "updated_at": "2024-01-15T10:30:00"
            }
        }


class EventInventory(BaseModel):
    """Model for event inventory."""
    event_id: str
    total_seats: int
    available_seats: int
    booked_seats: int

    class Config:
        json_schema_extra = {
            "example": {
                "event_id": "event_456",
                "total_seats": 100,
                "available_seats": 50,
                "booked_seats": 50
            }
        }


class InvariantViolation(BaseModel):
    """Model for invariant violations found during testing."""
    violation_id: str
    violation_type: str
    description: str
    event_id: str
    details: dict
    timestamp: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "violation_id": "viol_001",
                "violation_type": "overselling",
                "description": "More seats sold than available",
                "event_id": "event_456",
                "details": {"booked": 101, "available": 100},
                "timestamp": "2024-01-15T10:30:00"
            }
        }
