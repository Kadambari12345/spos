# Program: SJF (Preemptive) Scheduling Algorithm
# Author: Example Solution
# Shortest Remaining Time First (SRTF)

# Sample Input:
# Process   Arrival  Burst
# P1        0        6
# P2        1        4
# P3        4        8
# P4        3        3

processes = [
    {"pid": "P1", "arrival": 0, "burst": 6},
    {"pid": "P2", "arrival": 1, "burst": 4},
    {"pid": "P3", "arrival": 4, "burst": 8},
    {"pid": "P4", "arrival": 3, "burst": 3}
]

n = len(processes)
remaining_time = [p["burst"] for p in processes]
complete = 0
time = 0
minm = 999999999
shortest = 0
check = False

completion_time = [0] * n

# Sorting by arrival time
processes.sort(key=lambda x: x["arrival"])

while complete != n:
    # Find process with minimum remaining time at current time
    for j in range(n):
        if (processes[j]["arrival"] <= time and
            remaining_time[j] < minm and
            remaining_time[j] > 0):
            minm = remaining_time[j]
            shortest = j
            check = True

    if not check:
        time += 1
        continue

    # Reduce remaining time
    remaining_time[shortest] -= 1
    minm = remaining_time[shortest]
    if minm == 0:
        minm = 999999999

    # If process gets completely executed
    if remaining_time[shortest] == 0:
        complete += 1
        check = False
        finish_time = time + 1
        completion_time[shortest] = finish_time

    time += 1

# Calculate Turnaround and Waiting Time
for i in range(n):
    processes[i]["completion"] = completion_time[i]
    processes[i]["turnaround"] = processes[i]["completion"] - processes[i]["arrival"]
    processes[i]["waiting"] = processes[i]["turnaround"] - processes[i]["burst"]

# Display Table
print("----------------------------------------------------------")
print("Process | Arrival | Burst | Completion | Turnaround | Waiting")
print("----------------------------------------------------------")
total_tat = total_wt = 0
for p in processes:
    total_tat += p["turnaround"]
    total_wt += p["waiting"]
    print(f"{p['pid']:>7} | {p['arrival']:>7} | {p['burst']:>5} | {p['completion']:>10} | {p['turnaround']:>10} | {p['waiting']:>7}")

print("----------------------------------------------------------")
print(f"Average Turnaround Time: {total_tat/n:.2f}")
print(f"Average Waiting Time   : {total_wt/n:.2f}")
