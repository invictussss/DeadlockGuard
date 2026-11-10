import pytest
from src.recovery import recover_deadlock


def test_process_termination_and_resource_release():
    available = [0, 0]
    allocation = [
        [1, 0],
        [0, 1]
    ]

    result = recover_deadlock(available, allocation, 0)

    assert result["terminated_process"] == "P0"
    assert result["released_resources"] == [1, 0]
    assert result["available_after_recovery"] == [1, 0]
    assert result["updated_allocation"] == [
        [0, 0],
        [0, 1]
    ]


def test_original_data_remains_unchanged():
    available = [0, 0]
    allocation = [
        [1, 0],
        [0, 1]
    ]

    recover_deadlock(available, allocation, 0)

    assert available == [0, 0]
    assert allocation == [
        [1, 0],
        [0, 1]
    ]


def test_invalid_process_index():
    available = [1, 1]
    allocation = [
        [1, 0],
        [0, 1]
    ]

    with pytest.raises(ValueError):
        recover_deadlock(available, allocation, 2)


def test_invalid_allocation_dimensions():
    available = [1, 1]
    allocation = [
        [1, 0],
        [0]
    ]

    with pytest.raises(ValueError):
        recover_deadlock(available, allocation, 0)
