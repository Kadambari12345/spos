# Program: LRU (Least Recently Used) Page Replacement Algorithm
# Author: Fixed Version

pages = [2, 3, 2, 1, 5, 2, 4, 5, 3, 2, 5, 2]
frame_size = 3
frames = []
page_faults = 0

# Track recent use
recent_use = {}

print("------------------------------------------------------")
print("Ref Page | Frames (after insertion) | Page Fault?")
print("------------------------------------------------------")

for i in range(len(pages)):
    page = pages[i]

    # Case 1: Page Hit
    if page in frames:
        fault = "No"
    else:
        # Page Fault
        page_faults += 1
        fault = "Yes"

        if len(frames) < frame_size:
            frames.append(page)
        else:
            # Filter only pages currently in frames for LRU
            valid_recent_use = {k: v for k, v in recent_use.items() if k in frames}
            lru_page = min(valid_recent_use, key=valid_recent_use.get)
            frames.remove(lru_page)
            frames.append(page)

    # Update last used time
    recent_use[page] = i

    print(f"{page:^9}|{str(frames):^27}|{fault:^12}")

print("------------------------------------------------------")
print(f"Total Page Faults: {page_faults}")
print(f"Total Page Hits  : {len(pages) - page_faults}")
print("------------------------------------------------------")
