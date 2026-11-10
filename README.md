# DeadlockGuard
### Intelligent OS Resource Management Simulator

DeadlockGuard is a Python-based Operating System simulator designed to demonstrate resource allocation, deadlock detection, and deadlock recovery through an interactive Streamlit web interface.

The project helps users understand how operating systems manage resources and handle deadlock situations using fundamental OS algorithms.

## 1. Project Objectives

- Understand resource allocation in operating systems.
- Implement Banker's Safety Algorithm.
- Detect deadlocks using Available, Allocation, and Request matrices.
- Simulate deadlock recovery through process termination.
- Provide an interactive GUI for testing different scenarios.

## 2. Features

- Configure the number of processes and resources.
- Enter Total Resource, Allocation, Maximum Demand, and Request matrices.
- Calculate Available Resources and Need Matrix.
- Check system safety using Banker's Algorithm.
- Detect deadlocked processes.
- Recover from deadlock by terminating a selected process.
- Automatically recheck the system after recovery.
- Display updated resource allocation.

## 3. Algorithms Implemented

### Banker's Safety Algorithm
Determines whether the system is in a safe or unsafe state and finds a possible safe execution sequence.

### Deadlock Detection Algorithm
Uses the Available, Allocation, and Request matrices to identify processes involved in a deadlock.

### Deadlock Recovery
Simulates terminating a selected process and releasing its allocated resources back to the system.

## 4. Technologies Used

- Python
- Streamlit
- NumPy
- Pandas
- Plotly
- Pytest

## 5. Project Structure

```text
Deadlock-Detection-Recovery-Simulator/
│
├── app.py
├── requirements.txt
├── README.md
│
├── src/
│   ├── __init__.py
│   ├── resource_allocation.py
│   ├── bankers_algorithm.py
│   ├── deadlock_detection.py
│   └── recovery.py
│
├── tests/
│   ├── test_bankers.py
│   ├── test_deadlock.py
│   └── test_recovery.py
│
└── utils/
    ├── __init__.py
    └── visualization.py
```

## 6. Installation and Setup

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Navigate to the project directory:

```bash
cd Deadlock-Detection-Recovery-Simulator
```

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate the environment:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 7. Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal to access the DeadlockGuard dashboard.

## 8. Run Tests

Execute the complete test suite:

```bash
python -m pytest tests/ -v
```

### Testing Results

| Module | Test Cases | Result |
|---|---:|---|
| Banker's Algorithm | 3 | Passed |
| Deadlock Detection | 4 | Passed |
| Deadlock Recovery | 4 | Passed |
| **Total** | **11** | **11 Passed** |

## 9. Project Limitations

- The project simulates resource allocation rather than managing actual operating system resources.
- Recovery simulates process termination; it does not terminate real OS processes.
- The system uses manually entered resource matrices.
- The simulator is intended for educational purposes.

## 10. Future Scope

- Support for additional deadlock handling strategies.
- More advanced resource allocation visualizations.
- Exporting simulation results.
- Extended testing with larger process and resource configurations.

## 11. Conclusion

DeadlockGuard demonstrates important Operating System concepts through an interactive simulation environment. It combines resource allocation, safety checking, deadlock detection, and recovery into a single application.

The project provides a practical learning experience for understanding deadlock management in operating systems.

---

**Project Name:** DeadlockGuard  
**Domain:** Operating Systems  
**Language:** Python  
**Interface:** Streamlit
