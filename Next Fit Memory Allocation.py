# Program: Next Fit Memory Allocation Strategy
# Author: Example Solution

# Memory partitions (in KB)
partitions = [100, 500, 200, 300, 600]

# Processes (in KB)
processes = [212, 417, 112, 426]

# To store allocation results (-1 means not allocated)
allocation = [-1] * len(processes)

# Starting index for next fit search
last_index = 0
n = len(partitions)

# Next Fit Allocation Logic
for i in range(len(processes)):
    count = 0
    allocated = False
    j = last_index

    while count < n:  # loop through all partitions (circularly)
        if partitions[j] >= processes[i]:
            allocation[i] = j
            partitions[j] -= processes[i]
            last_index = j  # next search starts from here
            allocated = True
            break
        j = (j + 1) % n
        count += 1

    if not allocated:
        allocation[i] = -1  # not enough space found

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
