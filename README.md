# InterleaveLab

InterleaveLab is a developer tool that detects race conditions and concurrency bugs in backend APIs by generating controlled request interleavings, checking application invariants, and producing reproducible evidence of failures.

## Why this project matters

Modern backend systems fail silently when multiple requests happen simultaneously. A booking API that allows two users to reserve the last seat, both receiving confirmation, represents a real production bug. Ordinary unit tests miss this. InterleaveLab focuses on generating controlled request interleavings, checking invariants, and producing clear evidence of failures.

## Core features

- Concurrent workload generation
- Invariant checking and violation detection
- Deterministic replay for reproducibility
- Counterexample generation for debugging
- Regression testing capabilities
- Benchmarking ready design

## Project structure

```
app/
  api/
    routes.py          API endpoints
  services/
    inventory.py       Booking logic and invariant checking
    interleaving.py    Request ordering and counterexample search
    engine.py          Orchestration layer
  config.py           Configuration constants
  main.py             Application factory
tests/
  test_inventory.py   Inventory tests
  test_api.py         API endpoint tests
  test_interleaving.py Interleaving logic tests
.github/workflows/
  ci.yml              GitHub Actions CI pipeline
```

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## API endpoints

### Health check

```bash
curl http://localhost:8000/health
```

### Get status

```bash
curl http://localhost:8000/status
```

### Detect concurrency bugs

```bash
curl -X POST http://localhost:8000/scenarios \
  -H "Content-Type: application/json" \
  -d '{"capacity": 1, "users": ["alice", "bob"]}'
```

### Replay a specific schedule

```bash
curl -X POST http://localhost:8000/replay \
  -H "Content-Type: application/json" \
  -d '{"capacity": 1, "schedule": ["alice_book", "bob_book"]}'
```

### Create booking

```bash
curl -X POST http://localhost:8000/book \
  -H "Content-Type: application/json" \
  -d '{"user_id": "alice", "booking_id": "b1", "quantity": 1}'
```

## Testing

Run all tests with verbose output:

```bash
pytest -v
```

Run specific test file:

```bash
pytest tests/test_inventory.py -v
```

With coverage:

```bash
pytest --cov=app tests/
```

## How it works

1. Define a scenario with users and inventory capacity
2. Engine generates all possible request orderings
3. Each ordering is executed against invariant checks
4. If a violation is found, the exact sequence is returned
5. Developers can replay and verify the fix

## Resume value

This project demonstrates solid backend engineering skills: concurrent systems thinking, API design, invariant based testing, and practical debugging techniques for production bugs.
