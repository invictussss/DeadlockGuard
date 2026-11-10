import pytest
from src.deadlock_detection import detect_deadlock


def test_deadlock_detected():
    available = [0, 0]

    allocation = [
        [1, 0],
        [0, 1]
    ]

    request = [
        [0, 1],
        [1, 0]
    ]

    result = detect_deadlock(available, allocation, request)

    assert result["deadlock_detected"] is True
    assert result["deadlocked_processes"] == ["P0", "P1"]


def test_no_deadlock():
    available = [1, 1]

    allocation = [
        [1, 0],
        [0, 1]
    ]

    request = [
        [0, 1],
        [1, 0]
    ]

    result = detect_deadlock(available, allocation, request)

    assert result["deadlock_detected"] is False
    assert result["deadlocked_processes"] == []


def test_process_holding_zero_resources():
    available = [0, 0]

    allocation = [
        [0, 0],
        [1, 0]
    ]

    request = [
        [1, 1],
        [0, 1]
    ]

    result = detect_deadlock(available, allocation, request)

    assert result["deadlock_detected"] is True
    assert result["deadlocked_processes"] == ["P1"]


def test_invalid_matrix_dimensions():
    available = [1, 1]

    allocation = [
        [1, 0],
        [0, 1]
    ]

    request = [
        [0, 1]
    ]

    with pytest.raises(ValueError):
        detect_deadlock(available, allocation, request)
