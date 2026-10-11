"""Benchmark tests to measure concurrency bug detection."""
import pytest
from core.benchmark import run_benchmark


def test_benchmark_with_few_users():
    """Run benchmark with a small number of concurrent users."""
    report = run_benchmark(total_users=3, max_workers=3)
    
    assert report["attempts"] == 3
    assert report["oversold"] is True
    assert report["booked"] == 3
    assert report["available"] == -2  # 1 seat - 3 booked


def test_benchmark_with_many_users():
    """Run benchmark with more concurrent users."""
    report = run_benchmark(total_users=8, max_workers=4)
    
    assert report["oversold"] is True
    assert report["booked"] == 8
    assert report["available"] < 0


def test_benchmark_returns_trace():
    """Benchmark output should include operation trace."""
    report = run_benchmark(total_users=2, max_workers=2)
    
    assert "trace" in report
    assert len(report["trace"]) > 0
    # Trace should contain read and write operations
    assert any("read" in op for op in report["trace"])
    assert any("wrote" in op for op in report["trace"])
