# Program: FIFO Page Replacement Algorithm
# Author: Example Solution

# Sample Input
pages = [2, 3, 2, 1, 5, 2, 4, 5, 3, 2, 5, 2]
frames = []
frame_size = 3
page_faults = 0

print("--------------------------------------------------")
print("Ref Page | Frames (after insertion) | Page Fault?")
print("--------------------------------------------------")

for page in pages:
    if page not in frames:
        # Page Fault occurs
        page_faults += 1
        if len(frames) < frame_size:
            frames.append(page)
        else:
            frames.pop(0)  # Remove the oldest page (FIFO)
            frames.append(page)
        fault = "Yes"
    else:
        fault = "No"
    print(f"{page:^9}|{str(frames):^27}|{fault:^12}")

print("--------------------------------------------------")
print(f"Total Page Faults: {page_faults}")
print(f"Total Page Hits  : {len(pages) - page_faults}")
print("--------------------------------------------------")
