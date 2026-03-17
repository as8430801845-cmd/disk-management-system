# Simulated Disk Management Tool (All-in-One)

DISK_SIZE = 100  # Total blocks on the virtual disk
disk = [None] * DISK_SIZE  # Initialize virtual disk with None
files = {}  # Dictionary to store file allocations


# --------------------------------------
# FILE ALLOCATION METHODS
# --------------------------------------

def allocate_contiguous(filename, size):
    if filename in files:
        return f"File '{filename}' already exists."
    if size <= 0:
        return "Invalid file size."

    for i in range(DISK_SIZE - size + 1):
        if all(disk[j] is None for j in range(i, i + size)):
            for j in range(i, i + size):
                disk[j] = filename
            files[filename] = ("contiguous", list(range(i, i + size)))
            return f"File '{filename}' allocated contiguously."
    return "No suitable contiguous space found."


def allocate_linked(filename, size):
    if filename in files:
        return f"File '{filename}' already exists."
    if size <= 0:
        return "Invalid file size."

    free_blocks = [i for i in range(DISK_SIZE) if disk[i] is None]
    if len(free_blocks) < size:
        return "Not enough free blocks."

    allocated = free_blocks[:size]
    for block in allocated:
        disk[block] = filename
    files[filename] = ("linked", allocated)
    return f"File '{filename}' allocated using linked allocation."


def delete_file(filename):
    if filename not in files:
        return f"File '{filename}' not found."
    _, blocks = files[filename]
    for block in blocks:
        disk[block] = None
    del files[filename]
    return f"File '{filename}' deleted."


# --------------------------------------
# DISK SCHEDULING ALGORITHMS
# --------------------------------------

def fcfs(requests, head):
    total = 0
    for r in requests:
        total += abs(r - head)
        head = r
    return total


def sstf(requests, head):
    total = 0
    remaining = requests[:]
    while remaining:
        closest = min(remaining, key=lambda x: abs(x - head))
        total += abs(closest - head)
        head = closest
        remaining.remove(closest)
    return total


def scan(requests, head, direction='right'):
    total = 0
    requests = sorted(requests)
    if direction == 'right':
        right = [r for r in requests if r >= head]
        left = [r for r in requests if r < head][::-1]

        for r in right:
            total += abs(r - head)
            head = r
        if left:
            total += abs(head - left[0])
            head = left[0]
            for r in left:
                total += abs(r - head)
                head = r
    else:
        left = [r for r in requests if r <= head][::-1]
        right = [r for r in requests if r > head]

        for r in left:
            total += abs(r - head)
            head = r
        if right:
            total += abs(head - right[0])
            head = right[0]
            for r in right:
                total += abs(r - head)
                head = r
    return total


# --------------------------------------
# UI FUNCTIONS
# --------------------------------------

def show_disk():
    print("\nDisk Status (100 blocks):")
    for i in range(0, DISK_SIZE, 10):
        row = disk[i:i+10]
        display = ['_' if b is None else b[0] for b in row]
        print(f"{i:02}-{i+9:02}:", ' '.join(display))


def show_files():
    print("\nFiles:")
    if not files:
        print("No files found.")
    else:
        for fname, (method, blocks) in files.items():
            print(f"- {fname} ({method}): Blocks {blocks}")


# --------------------------------------
# MAIN MENU
# --------------------------------------

def main():
    while True:
        print("\n--- Simulated Disk Management Tool ---")
        print("1. Create File (Contiguous)")
        print("2. Create File (Linked)")
        print("3. Delete File")
        print("4. Show Disk")
        print("5. Show Files")
        print("6. Run Disk Scheduling")
        print("7. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            fname = input("Filename: ")
            try:
                size = int(input("Size: "))
                print(allocate_contiguous(fname, size))
            except ValueError:
                print("Invalid input. Please enter an integer size.")

        elif choice == '2':
            fname = input("Filename: ")
            try:
                size = int(input("Size: "))
                print(allocate_linked(fname, size))
            except ValueError:
                print("Invalid input. Please enter an integer size.")

        elif choice == '3':
            fname = input("Filename to delete: ")
            print(delete_file(fname))

        elif choice == '4':
            show_disk()

        elif choice == '5':
            show_files()

        elif choice == '6':
            try:
                reqs = list(map(int, input("Enter requests (space-separated): ").split()))
                head = int(input("Initial head position: "))
                print(f"FCFS total head movement: {fcfs(reqs, head)}")
                print(f"SSTF total head movement: {sstf(reqs, head)}")
                print(f"SCAN (Right) total head movement: {scan(reqs, head, 'right')}")
                print(f"SCAN (Left) total head movement: {scan(reqs, head, 'left')}")
            except ValueError:
                print("Invalid input. Please enter space-separated integers.")

        elif choice == '7':
            print("Exiting.")
            break

        else:
            print("Invalid choice. Try again.")


if __name__  == "__main__":
    main()
