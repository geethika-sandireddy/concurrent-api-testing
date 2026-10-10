# InterleaveLab 🔬

**Deterministic Concurrency Bug Detection for Backend APIs**

A developer tool that detects race conditions and concurrency bugs in backend APIs by generating controlled request interleavings, checking application invariants, and producing reproducible evidence of failures.

## 🎯 Problem Statement

Imagine an online booking system with one seat remaining. Two users book it simultaneously—and both receive confirmation. Ordinary tests miss this bug. **InterleaveLab detects it**, reproduces it, and generates a test you can replay after fixing.

## ✨ Core Features

- **Concurrent Workload Generation**: Simulate simultaneous API requests with controlled timing
- **Invariant Checking**: Detect violations like overselling inventory or duplicate processing
- **Deterministic Replay**: Reproduce failures using recorded request schedules
- **Counterexample Generation**: Show the exact sequence of events that caused the failure
- **Automated Regression Testing**: Verify bugs don't reappear after fixes
- **Benchmarking**: Measure detection rates, false positives, and execution time

## 🛠️ Tech Stack

- **Backend**: Python 3.11+, FastAPI
- **Database**: PostgreSQL
- **Testing**: pytest, Hypothesis
- **DevOps**: Docker, Docker Compose, GitHub Actions
- **Concurrency**: asyncio, threading
- **Monitoring**: Logging, metrics collection

## 📦 Project Structure

```
concurrent-api-testing/
├── app/                          # FastAPI application
│   ├── main.py                  # Application entry point
│   ├── models.py                # Data models
│   └── config.py                # Configuration
├── core/                         # Core engine
│   ├── workload_generator.py    # Concurrent workload simulation
│   ├── scheduler.py             # Request scheduling & interleaving
│   ├── invariant_checker.py     # Invariant violation detection
│   └── replayer.py              # Deterministic replay system
├── tests/                        # Test suite
│   ├── test_workload.py
│   ├── test_scheduler.py
│   └── test_benchmarks.py
├── examples/                     # Example scenarios
│   └── booking_system.py         # Online booking bug example
├── docker-compose.yml           # Local development stack
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 14+
- Docker & Docker Compose (optional)

### Local Setup

```bash
# 1. Clone the repository
git clone https://github.com/geethika-sandireddy/concurrent-api-testing.git
cd concurrent-api-testing

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up database
createdb interleavelab  # Or use Docker Compose

# 5. Run the application
uvicorn app.main:app --reload --port 8000
```

### Using Docker Compose

```bash
docker-compose up -d
# Application will be available at http://localhost:8000
```

## 📚 Usage Example

```python
from core.workload_generator import ConcurrentWorkload
from core.scheduler import DeterministicScheduler
from core.invariant_checker import InvariantChecker

# Define a booking scenario
workload = ConcurrentWorkload(
    num_concurrent_users=10,
    scenario="booking_system"
)

# Generate concurrent requests
requests = workload.generate()

# Run with deterministic scheduling
scheduler = DeterministicScheduler()
results = scheduler.execute(requests)

# Check for invariant violations
checker = InvariantChecker()
violations = checker.check(results)

if violations:
    print(f"Found {len(violations)} bugs!")
    for bug in violations:
        print(f"  - {bug.description}")
```

## 🔍 How It Works

1. **Scenario Definition**: Define your API endpoints and user interactions
2. **Workload Generation**: Create concurrent request patterns
3. **Scheduling**: Control request timing to trigger race conditions
4. **Execution**: Run requests against your API
5. **Invariant Checking**: Detect violations in application state
6. **Replay**: Reproduce failures deterministically
7. **Report**: Generate detailed bug reports with counterexamples

## 📊 Benchmarking

Run the included benchmarks to measure:
- Bug detection rates
- False positive ratio
- Execution time per scenario
- Memory usage

```bash
pytest tests/test_benchmarks.py -v --benchmark-only
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=core --cov-report=html

# Run only unit tests
pytest tests/ -m unit -v

# Run property-based tests
pytest tests/ -m hypothesis -v
```

## 🤝 Contributing

This project is built for learning and resume building. Contributions are welcome!

## 📝 License

MIT License - See LICENSE file for details

## 👤 Author

- **Geethika Sandireddy** - [@geethika-sandireddy](https://github.com/geethika-sandireddy)

---

**Made with ❤️ for detecting and fixing concurrency bugs**
