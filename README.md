# InterleaveLab

InterleaveLab is a Python project for detecting concurrency bugs in backend APIs. It focuses on a familiar problem: overselling inventory when multiple users act at the same time.

The project simulates concurrent booking requests, checks invariants, records a failing schedule, and replays the bug in a deterministic way.

## What it does

- Generates concurrent API-style workloads
- Checks for overselling and broken invariants
- Records the request sequence that caused the failure
- Replays the failing schedule deterministically
- Provides a small benchmark output for comparison

## Why this project is useful

This is a good resume project because it demonstrates:

- backend API thinking
- concurrency and race-condition analysis
- test design
- deterministic debugging
- reproducible bug reports

## Project structure

```text
concurrent-api-testing/
├── app/
│   ├── __init__.py
│   ├── api.py
│   ├── config.py
│   ├── main.py
│   ├── models.py
│   └── store.py
├── core/
│   ├── __init__.py
│   ├── benchmark.py
│   ├── invariant_checker.py
│   ├── replayer.py
│   └── scheduler.py
├── examples/
│   └── booking_bug_demo.py
├── tests/
│   ├── __init__.py
│   ├── test_replay.py
│   └── test_scheduler.py
├── .env.example
├── .gitignore
├── Dockerfile
├── README.md
├── docker-compose.yml
├── requirements.txt
└── setup.cfg
```

## Quick start

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest -q
```

## Example flow

```python
from core.scheduler import BuggyInventoryStore, InterleaveScheduler, build_booking_workload

store = BuggyInventoryStore(total_seats=1)
scheduler = InterleaveScheduler(store)
workload = build_booking_workload(total_users=2, seats_per_booking=1)
results = scheduler.run_workload(workload, max_workers=2)

print(store.inventory)
```

This intentionally produces a bad state where the available seat count goes below zero, which is the kind of bug the project helps detect.
