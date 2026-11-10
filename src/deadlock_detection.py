"""
Deadlock Detection Algorithm

Detects deadlocked processes using Available,
Allocation and Request matrices.
"""


def detect_deadlock(available, allocation, request):

    n = len(allocation)
    m = len(available)

    if len(request) != n:
        raise ValueError("Allocation and Request rows must match.")

    if any(len(row) != m for row in allocation + request):
        raise ValueError("Matrix dimensions do not match.")

    work = available.copy()

    # Processes holding no resources are already finished
    finish = [
        all(resource == 0 for resource in allocation[i])
        for i in range(n)
    ]

    while True:
        found = False

        for i in range(n):

            if not finish[i]:

                # Check whether outstanding requests can be fulfilled
                if all(request[i][j] <= work[j] for j in range(m)):

                    # Release resources held by this process
                    for j in range(m):
                        work[j] += allocation[i][j]

                    finish[i] = True
                    found = True

        if not found:
            break

    deadlocked_processes = [
        f"P{i}" for i in range(n) if not finish[i]
    ]

    return {
        "deadlock_detected": len(deadlocked_processes) > 0,
        "deadlocked_processes": deadlocked_processes,
        "message": (
            "Deadlock detected!"
            if deadlocked_processes
            else "No deadlock detected."
        )
    }
    