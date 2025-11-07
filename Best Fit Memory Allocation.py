# Program: Best Fit Memory Allocation Strategy
# Author: Example Solution

# Memory partitions (in KB)
partitions = [100, 500, 200, 300, 600]

# Processes (in KB)
processes = [212, 417, 112, 426]

# To store allocation results
allocation = [-1] * len(processes)

# Best Fit Allocation Logic
for i in range(len(processes)):
    best_index = -1
    for j in range(len(partitions)):
        if partitions[j] >= processes[i]:
            if best_index == -1 or partitions[j] < partitions[best_index]:
                best_index = j
    if best_index != -1:
        # Allocate process to the best partition
        allocation[i] = best_index
        partitions[best_index] -= processes[i]

# Display results
print("------------------------------------------------------------")
print("Process No | Process Size | Partition Allocated | Remaining Space")
print("------------------------------------------------------------")
for i in range(len(processes)):
    if allocation[i] != -1:
        print(f"{i+1:^11}|{processes[i]:^14}|{allocation[i]+1:^20}|{partitions[allocation[i]]:^16}")
    else:
        print(f"{i+1:^11}|{processes[i]:^14}|{'Not Allocated':^20}|{'-':^16}")
print("------------------------------------------------------------")
