# Program: LRU (Least Recently Used) Page Replacement Algorithm
# Author: Example Solution

# Sample Input
pages = [2, 3, 2, 1, 5, 2, 4, 5, 3, 2, 5, 2]
frame_size = 3
frames = []
page_faults = 0# Program: LRU (Least Recently Used) Page Replacement Algorithm
# Author: Example Solution

# Sample Input
pages = [2, 3, 2, 1, 5, 2, 4, 5, 3, 2, 5, 2]
frame_size = 3
frames = []
page_faults = 0

# To track when each page was last used
recent_use = {}

print("------------------------------------------------------")
print("Ref Page | Frames (after insertion) | Page Fault?")
print("------------------------------------------------------")

for i in range(len(pages)):
    page = pages[i]

    # Case 1: Page Hit (already in frames)
    if page in frames:
        fault = "No"
    else:
        # Page Fault
        page_faults += 1
        fault = "Yes"

        # Case 2: If frame not full → add page
        if len(frames) < frame_size:
            frames.append(page)
        else:
            # Case 3: Frame full → remove least recently used page
            lru_page = min(recent_use, key=recent_use.get)
            frames.remove(lru_page)
            frames.append(page)

    # Update usage info (mark current time)
    recent_use[page] = i

    print(f"{page:^9}|{str(frames):^27}|{fault:^12}")

print("------------------------------------------------------")
print(f"Total Page Faults: {page_faults}")
print(f"Total Page Hits  : {len(pages) - page_faults}")
print("------------------------------------------------------")


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
