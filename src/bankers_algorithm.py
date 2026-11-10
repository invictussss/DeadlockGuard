"""
Banker's Algorithm

Checks whether the system is in a safe state
and finds a possible safe execution sequence.
"""


def bankers_algorithm(available, allocation, need):
    """
    Execute Banker's Safety Algorithm.
    """

    work = available.copy()
    n = len(allocation)

    finish = [False] * n
    safe_sequence = []

    while len(safe_sequence) < n:

        found = False

        for i in range(n):

            if not finish[i]:

                # Check whether process needs can be satisfied
                if all(need[i][j] <= work[j]
                       for j in range(len(work))):

                    # Release allocated resources
                    for j in range(len(work)):
                        work[j] += allocation[i][j]

                    finish[i] = True
                    safe_sequence.append(i)
                    found = True

        if not found:
            break

    if all(finish):
        return {
            "safe": True,
            "safe_sequence": [f"P{i}" for i in safe_sequence],
            "message": "System is in a SAFE state."
        }

    unfinished = [
        f"P{i}" for i in range(n) if not finish[i]
    ]

    return {
        "safe": False,
        "safe_sequence": [],
        "unfinished_processes": unfinished,
        "message": "System is in an UNSAFE state."
    }
    