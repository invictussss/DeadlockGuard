from src.bankers_algorithm import bankers_algorithm


def test_safe_state():
    available = [5, 4, 5]

    allocation = [
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2]
    ]

    need = [
        [7, 4, 3],
        [1, 2, 2],
        [6, 0, 0]
    ]

    result = bankers_algorithm(available, allocation, need)

    assert result["safe"] is True
    assert len(result["safe_sequence"]) == 3


def test_unsafe_state():
    available = [0, 0]

    allocation = [
        [1, 0],
        [0, 1]
    ]

    need = [
        [0, 1],
        [1, 0]
    ]

    result = bankers_algorithm(available, allocation, need)

    assert result["safe"] is False
    assert result["safe_sequence"] == []
    assert len(result["unfinished_processes"]) == 2


def test_all_processes_already_satisfied():
    available = [2, 2]

    allocation = [
        [1, 0],
        [0, 1]
    ]

    need = [
        [0, 0],
        [0, 0]
    ]

    result = bankers_algorithm(available, allocation, need)

    assert result["safe"] is True
    assert len(result["safe_sequence"]) == 2
