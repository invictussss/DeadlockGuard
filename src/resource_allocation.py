"""
Resource Allocation Module

Handles processes, resources, allocation matrix,
maximum demand matrix and available resources.
"""


def calculate_available_resources(total_resources, allocation):
    """
    Calculate available resources.

    Available = Total Resources - Allocated Resources
    """

    if not allocation:
        return total_resources.copy()

    allocated = [
        sum(row[i] for row in allocation)
        for i in range(len(total_resources))
    ]

    available = [
        total_resources[i] - allocated[i]
        for i in range(len(total_resources))
    ]

    if any(resource < 0 for resource in available):
        raise ValueError("Allocated resources exceed total resources.")

    return available


def calculate_need_matrix(maximum, allocation):
    """
    Calculate remaining resource requirements.

    Need = Maximum - Allocation
    """

    if len(maximum) != len(allocation):
        raise ValueError("Maximum and Allocation must have equal rows.")

    need = []

    for i in range(len(maximum)):
        if len(maximum[i]) != len(allocation[i]):
            raise ValueError("Matrix dimensions do not match.")

        row = []

        for j in range(len(maximum[i])):
            difference = maximum[i][j] - allocation[i][j]

            if difference < 0:
                raise ValueError("Allocation cannot exceed maximum demand.")

            row.append(difference)

        need.append(row)

    return need


def create_resource_state(processes, resources, total_resources,
                          allocation, maximum):
    """
    Create complete resource allocation state.
    """

    if len(processes) != len(allocation):
        raise ValueError("Number of processes does not match allocation.")

    if len(processes) != len(maximum):
        raise ValueError("Number of processes does not match maximum.")

    if len(resources) != len(total_resources):
        raise ValueError("Number of resources does not match total resources.")

    for matrix in [allocation, maximum]:
        for row in matrix:
            if len(row) != len(resources):
                raise ValueError("Resource matrix dimensions do not match.")

    available = calculate_available_resources(
        total_resources, allocation
    )

    need = calculate_need_matrix(maximum, allocation)

    return {
        "processes": processes,
        "resources": resources,
        "total_resources": total_resources,
        "allocation": allocation,
        "maximum": maximum,
        "available": available,
        "need": need
    }
    