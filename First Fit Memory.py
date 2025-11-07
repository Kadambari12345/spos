# Program: First Fit Memory Allocation Strategy
# Author: Example Solution

# Memory partitions (in KB)
partitions = [100, 500, 200, 300, 600]

# Processes (in KB)
processes = [212, 417, 112, 426]

# To store allocation results
allocation = [-1] * len(processes)

# First Fit Allocation Logic
for i in range(len(processes)):
    for j in range(len(partitions)):
        if partitions[j] >= processes[i]:
            # Allocate process to this partition
            allocation[i] = j
            partitions[j] -= processes[i]
            break  # move to the next process once allocated

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
