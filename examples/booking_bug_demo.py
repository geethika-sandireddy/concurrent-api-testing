"""Example concurrency scenario used for demos and interviews."""
from core.scheduler import BuggyInventoryStore, InterleaveScheduler, build_booking_workload


def demo_booking_bug() -> dict:
    """Demonstrate how a broken booking system can oversell a single seat."""
    store = BuggyInventoryStore(total_seats=1)
    scheduler = InterleaveScheduler(store)
    attempts = build_booking_workload(total_users=4, seats_per_booking=1)

    results = scheduler.run_workload(attempts, max_workers=4)
    return {
        "result_count": len(results),
        "available_after": store.inventory["available"],
        "booked_after": store.inventory["booked"],
        "operations": store.operations,
    }
