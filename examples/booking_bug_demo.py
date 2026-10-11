"""Example concurrency scenario for the project README."""
from core.scheduler import BuggyInventoryStore, InterleaveScheduler, build_booking_workload


def demo_booking_bug() -> dict:
    """End-to-end demonstration of the race condition scenario."""
    bug_store = BuggyInventoryStore(total_seats=1)
    scheduler = InterleaveScheduler(bug_store)
    attempts = build_booking_workload(total_users=4, seats_per_booking=1)

    results = scheduler.run_workload(attempts, max_workers=4)
    return {
        "result_count": len(results),
        "available_after": bug_store.inventory["available"],
        "booked_after": bug_store.inventory["booked"],
        "operations": bug_store.operations,
    }
