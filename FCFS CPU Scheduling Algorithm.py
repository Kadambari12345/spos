# Program: FCFS CPU Scheduling Algorithm
# Author: Example Solution
# Non-preemptive First Come First Served scheduling

# Sample Input:
# Process ID   Arrival Time   Burst Time
# P1           0              3
# P2           2              6
# P3           4              4
# P4           6              5
# P5           8              2

# --------------------------

# Define process details
processes = [
    {"pid": "P1", "arrival": 0, "burst": 3},
    {"pid": "P2", "arrival": 2, "burst": 6},
    {"pid": "P3", "arrival": 4, "burst": 4},
    {"pid": "P4", "arrival": 6, "burst": 5},
    {"pid": "P5", "arrival": 8, "burst": 2}
]

# Sort by arrival time
processes.sort(key=lambda x: x["arrival"])

# Initialize variables
current_time = 0
for p in processes:
    if current_time < p["arrival"]:
        current_time = p["arrival"]  # wait for process to arrive
    p["start"] = current_time
    p["completion"] = current_time + p["burst"]
    p["turnaround"] = p["completion"] - p["arrival"]
    p["waiting"] = p["turnaround"] - p["burst"]
    current_time = p["completion"]

# Display results
print("------------------------------------------------------")
print("Process | Arrival | Burst | Start | Completion | Turnaround | Waiting")
print("------------------------------------------------------")
total_tat = total_wt = 0
for p in processes:
    total_tat += p["turnaround"]
    total_wt += p["waiting"]
    print(f"{p['pid']:>7} | {p['arrival']:>7} | {p['burst']:>5} | {p['start']:>5} | {p['completion']:>10} | {p['turnaround']:>10} | {p['waiting']:>7}")
print("------------------------------------------------------")
print(f"Average Turnaround Time: {total_tat/len(processes):.2f}")
print(f"Average Waiting Time   : {total_wt/len(processes):.2f}")
