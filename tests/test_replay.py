"""Tests for replay and benchmark helpers."""
from core.benchmark import run_benchmark
from core.replayer import Replayer, build_demo_schedule


def test_replayer_reproduces_the_bug():
    """The fixed schedule should reproduce the oversell bug."""
    replayer = Replayer(total_seats=1)
    result = replayer.replay_schedule(build_demo_schedule())

    assert result.failed_invariant is True
    assert result.available == -1
    assert result.booked == 2


def test_benchmark_detects_oversell():
    """The benchmark output should show the negative-seat condition."""
    report = run_benchmark(total_users=3, max_workers=3)

    assert report["attempts"] == 3
    assert report["oversold"] is True
    assert report["booked"] == 3
