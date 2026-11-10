"""
Deadlock Recovery Module

Simulates deadlock recovery by terminating a selected
process and releasing its allocated resources.
"""


def recover_deadlock(available, allocation, process_index):

    n = len(allocation)
    m = len(available)

    # Validate process index
    if process_index < 0 or process_index >= n:
        raise ValueError("Invalid process index.")

    # Validate allocation matrix
    if any(len(row) != m for row in allocation):
        raise ValueError("Allocation matrix dimensions do not match.")

    # Create copies to preserve original data
    new_available = available.copy()
    new_allocation = [row.copy() for row in allocation]

    # Get resources held by the selected process
    released_resources = new_allocation[process_index].copy()

    # Release resources back to the system
    for j in range(m):
        new_available[j] += released_resources[j]

    # Terminate process by clearing its allocation
    new_allocation[process_index] = [0] * m

    return {
        "terminated_process": f"P{process_index}",
        "released_resources": released_resources,
        "available_after_recovery": new_available,
        "updated_allocation": new_allocation,
        "message": f"P{process_index} terminated successfully. Resources released."
    }
    