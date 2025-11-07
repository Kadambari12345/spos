# Program: Priority Scheduling (Non-Preemptive)
# Author: Example Solution
# Low priority number = higher priority

# Sample Input:
# Process  Arrival  Burst  Priority
# P1       0        8      1
# P2       0        6      2
# P3       2        1      3
# P4       3        2      0

processes = [
    {"pid": "P1", "arrival": 0, "burst": 8, "priority": 1},
    {"pid": "P2", "arrival": 0, "burst": 6, "priority": 2},
    {"pid": "P3", "arrival": 2, "burst": 1, "priority": 3},
    {"pid": "P4", "arrival": 3, "burst": 2, "priority": 0}
]

n = len(processes)
completed = []
current_time = 0

# Sort by arrival time first
processes.sort(key=lambda x: x["arrival"])

while len(completed) < n:
    # Find processes that have arrived and are not completed
    available = [p for p in processes if p["arrival"] <= current_time and p not in completed]
    
    if not available:
        # If no process has arrived yet, move time forward
        current_time += 1
        continue
    
    # Select process with highest priority (lowest number)
    available.sort(key=lambda x: x["priority"])
    current_process = available[0]
    
    # Start and complete process
    start_time = current_time
    completion_time = start_time + current_process["burst"]
    current_process["start"] = start_time
    current_process["completion"] = completion_time
    current_process["turnaround"] = completion_time - current_process["arrival"]
    current_process["waiting"] = current_process["turnaround"] - current_process["burst"]
    
    completed.append(current_process)
    current_time = completion_time

# Display the results
print("--------------------------------------------------------------")
print("Process | Arrival | Burst | Priority | Start | Completion | Turnaround | Waiting")
print("--------------------------------------------------------------")
total_tat = total_wt = 0
for p in processes:
    total_tat += p["turnaround"]
    total_wt += p["waiting"]
    print(f"{p['pid']:>7} | {p['arrival']:>7} | {p['burst']:>5} | {p['priority']:>8} | {p['start']:>5} | {p['completion']:>10} | {p['turnaround']:>10} | {p['waiting']:>7}")
print("--------------------------------------------------------------")
print(f"Average Turnaround Time: {total_tat/n:.2f}")
print(f"Average Waiting Time   : {total_wt/n:.2f}")
