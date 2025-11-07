# Program: Round Robin (Preemptive) Scheduling
# Author: Example Solution
# Time Quantum = 2

# Sample Input:
# Process  Arrival  Burst
# P1       0        6
# P2       1        4
# P3       4        8
# P4       3        3

from collections import deque

# Input
time_quantum = 2
processes = [
    {"pid": "P1", "arrival": 0, "burst": 6},
    {"pid": "P2", "arrival": 1, "burst": 4},
    {"pid": "P3", "arrival": 4, "burst": 8},
    {"pid": "P4", "arrival": 3, "burst": 3}
]

# Sort by arrival time
processes.sort(key=lambda x: x["arrival"])

# Initialize
n = len(processes)
remaining_bt = [p["burst"] for p in processes]
completion_time = [0] * n
ready_queue = deque()
time = 0
completed = 0
visited = [False] * n

# Function to add processes that have arrived
def add_arrived_processes():
    for i in range(n):
        if processes[i]["arrival"] <= time and not visited[i] and remaining_bt[i] > 0:
            ready_queue.append(i)
            visited[i] = True

# Start scheduling
while completed != n:
    add_arrived_processes()
    if not ready_queue:
        time += 1
        continue

    index = ready_queue.popleft()

    # Execute for time quantum or remaining burst, whichever is smaller
    exec_time = min(time_quantum, remaining_bt[index])
    time += exec_time
    remaining_bt[index] -= exec_time

    # Add newly arrived processes while executing
    add_arrived_processes()

    # If process still has burst left, push to end of queue
    if remaining_bt[index] > 0:
        ready_queue.append(index)
    else:
        completed += 1
        completion_time[index] = time

# Calculate TAT and WT
for i in range(n):
    processes[i]["completion"] = completion_time[i]
    processes[i]["turnaround"] = processes[i]["completion"] - processes[i]["arrival"]
    processes[i]["waiting"] = processes[i]["turnaround"] - processes[i]["burst"]

# Display output
print("----------------------------------------------------------------------")
print("Process | Arrival | Burst | Completion | Turnaround | Waiting")
print("----------------------------------------------------------------------")
total_tat = total_wt = 0
for p in processes:
    total_tat += p["turnaround"]
    total_wt += p["waiting"]
    print(f"{p['pid']:>7} | {p['arrival']:>7} | {p['burst']:>5} | {p['completion']:>10} | {p['turnaround']:>10} | {p['waiting']:>7}")
print("----------------------------------------------------------------------")
print(f"Average Turnaround Time: {total_tat/n:.2f}")
print(f"Average Waiting Time   : {total_wt/n:.2f}")
