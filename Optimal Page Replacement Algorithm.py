# Program:# Program: LRU (Least Recently Used) Page Replacement Algorithm
# Author: Example Solution

# Sample Input
pages = [2, 3, 2, 1, 5, 2, 4, 5, 3, 2, 5, 2]
frame_size = 3
frames = []
page_faults = 0

# To keep track of page usage (recency)
recent_use = {}

print("------------------------------------------------------")
print("Ref Page | Frames (after insertion) | Page Fault?")
print("------------------------------------------------------")

for i in range(len(pages)):
    page = pages[i]

    # Case 1: Page already present (Hit)
    if page in frames:
        fault = "No"
    else:
        # Page fault
        page_faults += 1
        fault = "Yes"

        # If there is still space in frames
        if len(frames) < frame_size:
            frames.append(page)
        else:
            # Find least recently used page
            lru_page = min(recent_use, key=recent_use.get)
            frames.remove(lru_page)
            frames.append(page)

    # Update recent use
    recent_use[page] = i

    print(f"{page:^9}|{str(frames):^27}|{fault:^12}")

print("------------------------------------------------------")
print(f"Total Page Faults: {page_faults}")
print(f"Total Page Hits  : {len(pages) - page_faults}")
print("------------------------------------------------------")

# Author: Example Solution

# Sample Input
pages = [2, 3, 2, 1, 5, 2, 4, 5, 3, 2, 5, 2]
frame_size = 3
frames = []
page_faults = 0

print("------------------------------------------------------")
print("Ref Page | Frames (after insertion) | Page Fault?")
print("------------------------------------------------------")

for i in range(len(pages)):
    page = pages[i]
    
    # Case 1: Page already in frame (Hit)
    if page in frames:
        fault = "No"
    else:
        page_faults += 1
        fault = "Yes"
        
        # Case 2: Empty space available
        if len(frames) < frame_size:
            frames.append(page)
        else:
            # Case 3: Need to replace a page optimally
            farthest = -1
            index_to_replace = -1
            for j in range(len(frames)):
                # Check how far in future this frame page will be used
                if frames[j] not in pages[i+1:]:
                    index_to_replace = j
                    break
                else:
                    next_use = pages[i+1:].index(frames[j])
                    if next_use > farthest:
                        farthest = next_use
                        index_to_replace = j
            # Replace page
            frames[index_to_replace] = page

    print(f"{page:^9}|{str(frames):^27}|{fault:^12}")

print("------------------------------------------------------")
print(f"Total Page Faults: {page_faults}")
print(f"Total Page Hits  : {len(pages) - page_faults}")
print("------------------------------------------------------")
