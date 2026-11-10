import streamlit as st
import pandas as pd

from src.resource_allocation import create_resource_state
from src.bankers_algorithm import bankers_algorithm
from src.deadlock_detection import detect_deadlock
from src.recovery import recover_deadlock


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="DeadlockGuard",
    page_icon="🛡️",
    layout="wide"
)


# --------------------------------------------------
# HELPER FUNCTION: MATRIX EDITOR
# --------------------------------------------------

def create_matrix_editor(title, description, processes, resources, key, default=0):

    st.subheader(title)
    st.caption(description)

    initial_data = pd.DataFrame(
        default,
        index=processes,
        columns=resources
    )

    edited_data = st.data_editor(
        initial_data,
        num_rows="fixed",
        use_container_width=True,
        hide_index=False,
        key=f"{key}_{len(processes)}_{len(resources)}",
        column_config={
            resource: st.column_config.NumberColumn(
                resource,
                min_value=0,
                step=1,
                format="%d"
            )
            for resource in resources
        },
        disabled=False
    )

    # Preserve original process order
    edited_data = edited_data.reindex(processes)

    return edited_data.astype(int).values.tolist()


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🛡️ DeadlockGuard")

st.subheader("Intelligent OS Resource Management Simulator")

st.caption(
    "Operating Systems Capstone Project | Developed by Vikash Kumar"
)

st.divider()


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("⚙️ System Configuration")

num_processes = st.sidebar.number_input(
    "Number of Processes",
    min_value=1,
    max_value=10,
    value=3,
    step=1
)

num_resources = st.sidebar.number_input(
    "Number of Resource Types",
    min_value=1,
    max_value=10,
    value=3,
    step=1
)

st.sidebar.info("Configure processes and resources below.")


processes = [f"P{i}" for i in range(num_processes)]

resources = [f"R{i}" for i in range(num_resources)]


# --------------------------------------------------
# RESOURCE CONFIGURATION
# --------------------------------------------------

st.header("1. Resource Configuration")

resource_cols = st.columns(num_resources)

total_resources = []

for j in range(num_resources):

    with resource_cols[j]:

        value = st.number_input(
            f"Total R{j}",
            min_value=0,
            value=[10, 5, 7][j] if j < 3 else 5,
            step=1,
            key=f"total_{j}"
        )

        total_resources.append(value)


# --------------------------------------------------
# ALLOCATION MATRIX
# --------------------------------------------------

st.divider()

allocation_data = create_matrix_editor(
    "2. Allocation Matrix",
    "Enter the currently allocated resources for each process.",
    processes,
    resources,
    "allocation",
    default=0
)


# --------------------------------------------------
# MAXIMUM DEMAND MATRIX
# --------------------------------------------------

st.divider()

maximum_data = create_matrix_editor(
    "3. Maximum Demand Matrix",
    "Enter the maximum resource requirements of each process.",
    processes,
    resources,
    "maximum",
    default=5
)


# --------------------------------------------------
# REQUEST MATRIX
# --------------------------------------------------

st.divider()

request_data = create_matrix_editor(
    "4. Request Matrix",
    "Enter the outstanding resource requests for deadlock detection.",
    processes,
    resources,
    "request",
    default=0
)


# --------------------------------------------------
# COMPLETE SYSTEM ANALYSIS
# --------------------------------------------------

st.divider()

st.header("5. Complete System Analysis")

st.write(
    "Run Banker's Algorithm and Deadlock Detection together."
)

if st.button(
    "🚀 Run Full System Analysis",
    type="primary",
    use_container_width=True
):

    try:

        state = create_resource_state(
            processes,
            resources,
            total_resources,
            allocation_data,
            maximum_data
        )

        banker_result = bankers_algorithm(
            state["available"],
            state["allocation"],
            state["need"]
        )

        detection_result = detect_deadlock(
            state["available"],
            state["allocation"],
            request_data
        )

        st.session_state["resource_state"] = state
        st.session_state["banker_result"] = banker_result
        st.session_state["detection_result"] = detection_result
        st.session_state["analysis_completed"] = True

        st.session_state["analysis_processes"] = processes.copy()
        st.session_state["analysis_resources"] = resources.copy()

        st.success("System analysis completed successfully!")

    except ValueError as error:

        st.session_state["analysis_completed"] = False

        st.error(f"Input Error: {error}")


# --------------------------------------------------
# ANALYSIS RESULTS
# --------------------------------------------------

if st.session_state.get("analysis_completed", False):

    state = st.session_state["resource_state"]

    banker_result = st.session_state["banker_result"]

    detection_result = st.session_state["detection_result"]

    st.divider()

    st.header("📊 Analysis Results")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Processes", len(state["processes"]))

    with col2:
        st.metric("Resource Types", len(state["resources"]))

    with col3:
        st.metric("Available Resources", sum(state["available"]))

    result_col1, result_col2 = st.columns(2)

    with result_col1:

        st.write("**Available Resources**")

        st.dataframe(
            pd.DataFrame(
                [state["available"]],
                columns=state["resources"]
            ),
            use_container_width=True
        )

    with result_col2:

        st.write("**Need Matrix**")

        st.dataframe(
            pd.DataFrame(
                state["need"],
                index=state["processes"],
                columns=state["resources"]
            ),
            use_container_width=True
        )

    # Banker's Algorithm

    st.divider()

    st.subheader("1️⃣ Banker's Algorithm")

    if banker_result["safe"]:

        st.success("System is in a SAFE state.")

        st.write(
            "**Safe Sequence:**",
            " → ".join(banker_result["safe_sequence"])
        )

    else:

        st.error("System is in an UNSAFE state.")

        st.write(
            "**Unfinished Processes:**",
            ", ".join(banker_result["unfinished_processes"])
        )

    # Deadlock Detection

    st.divider()

    st.subheader("2️⃣ Deadlock Detection")

    if detection_result["deadlock_detected"]:

        st.error("Deadlock Detected!")

        st.write(
            "**Deadlocked Processes:**",
            ", ".join(detection_result["deadlocked_processes"])
        )

    else:

        st.success("No deadlock detected.")

    # Allocation Matrix

    st.divider()

    st.subheader("Complete Allocation Matrix")

    st.dataframe(
        pd.DataFrame(
            state["allocation"],
            index=state["processes"],
            columns=state["resources"]
        ),
        use_container_width=True
    )


# --------------------------------------------------
# DEADLOCK RECOVERY
# --------------------------------------------------

st.divider()

st.header("6. Deadlock Recovery")

st.write(
    "Select a process to terminate and release its allocated resources."
)

selected_process = st.selectbox(
    "Select Process",
    range(num_processes),
    format_func=lambda x: f"P{x}"
)

if st.button(
    "🔄 Recover System",
    use_container_width=True
):

    try:

        state = create_resource_state(
            processes,
            resources,
            total_resources,
            allocation_data,
            maximum_data
        )

        recovery_result = recover_deadlock(
            state["available"],
            state["allocation"],
            selected_process
        )

        # Automatic deadlock re-check after recovery
        updated_detection = detect_deadlock(
            recovery_result["available_after_recovery"],
            recovery_result["updated_allocation"],
            request_data
        )

        st.session_state["recovery_result"] = recovery_result
        st.session_state["post_recovery_detection"] = updated_detection
        st.session_state["recovery_processes"] = processes.copy()
        st.session_state["recovery_resources"] = resources.copy()

        st.success(recovery_result["message"])

    except ValueError as error:

        st.error(f"Recovery Error: {error}")


# --------------------------------------------------
# RECOVERY RESULTS
# --------------------------------------------------

if "recovery_result" in st.session_state:

    result = st.session_state["recovery_result"]
    detection = st.session_state["post_recovery_detection"]

    st.subheader("Recovery Results")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Terminated Process",
            result["terminated_process"]
        )

    with col2:

        st.metric(
            "Resources Released",
            sum(result["released_resources"])
        )

    st.write("**Released Resources:**")
    st.write(result["released_resources"])

    st.write("**Available Resources After Recovery:**")
    st.write(result["available_after_recovery"])

    st.write("**Updated Allocation Matrix:**")

    st.dataframe(
        pd.DataFrame(
            result["updated_allocation"],
            index=st.session_state["recovery_processes"],
            columns=st.session_state["recovery_resources"]
        ),
        use_container_width=True
    )

    st.divider()

    st.subheader("7. Automatic Deadlock Re-check")

    if detection["deadlock_detected"]:

        st.error("Deadlock still exists after recovery!")

        st.write(
            "**Remaining Deadlocked Processes:**",
            ", ".join(detection["deadlocked_processes"])
        )

    else:

        st.success("Deadlock successfully resolved! System is deadlock-free.")

        st.write("All remaining processes can proceed.")

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "DeadlockGuard | Operating Systems Capstone Project | 2026"
)
