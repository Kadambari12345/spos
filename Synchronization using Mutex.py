# sync_mutex.py
# Classical Synchronization Problems implemented with Mutex (threading.Lock)
# 1) Producer-Consumer (bounded buffer)
# 2) Readers-Writers (first problem: readers priority)
# 3) Dining Philosophers (forks as mutexes)
# Run: python sync_mutex.py

import threading
import time
import random

# ---------------------------
# 1) Producer - Consumer
# ---------------------------
def run_producer_consumer():
    buffer = []
    BUFFER_SIZE = 5
    lock = threading.Lock()
    produce_count = 10

    def producer():
        for i in range(1, produce_count + 1):
            item = random.randint(1, 100)
            produced = False
            while not produced:
                with lock:
                    if len(buffer) < BUFFER_SIZE:
                        buffer.append(item)
                        print(f"[Producer] produced {item} | buffer={buffer}")
                        produced = True
                    else:
                        # buffer full
                        # release lock and wait a bit
                        print("[Producer] buffer full, waiting...")
                time.sleep(0.5)
            time.sleep(random.uniform(0.2, 1.0))

    def consumer():
        for _ in range(1, produce_count + 1):
            consumed = False
            while not consumed:
                with lock:
                    if buffer:
                        item = buffer.pop(0)
                        print(f"[Consumer] consumed {item} | buffer={buffer}")
                        consumed = True
                    else:
                        print("[Consumer] buffer empty, waiting...")
                time.sleep(0.5)
            time.sleep(random.uniform(0.5, 1.2))

    p = threading.Thread(target=producer)
    c = threading.Thread(target=consumer)
    p.start()
    c.start()
    p.join()
    c.join()
    print("Producer-Consumer completed.\n")

# ---------------------------
# 2) Readers - Writers (Readers priority)
# ---------------------------
def run_readers_writers():
    data = {"value": 0}            # shared data
    read_count = {"count": 0}     # mutable counter
    mutex = threading.Lock()      # protect read_count
    rw_mutex = threading.Lock()   # exclusive access for writers

    def reader(reader_id):
        for _ in range(3):
            # entry section
            with mutex:
                read_count["count"] += 1
                if read_count["count"] == 1:
                    # first reader locks the resource for writers
                    rw_mutex.acquire()
            # critical section (reading)
            print(f"[Reader-{reader_id}] reading value = {data['value']}")
            time.sleep(random.uniform(0.2, 0.6))
            # exit section
            with mutex:
                read_count["count"] -= 1
                if read_count["count"] == 0:
                    # last reader releases resource
                    rw_mutex.release()
            time.sleep(random.uniform(0.2, 0.8))

    def writer(writer_id):
        for _ in range(2):
            # entry section (writers need exclusive access)
            with rw_mutex:
                # critical section (writing)
                new_val = data["value"] + random.randint(1, 10)
                print(f"[Writer-{writer_id}] writing value = {new_val}")
                data["value"] = new_val
                time.sleep(random.uniform(0.4, 1.0))
            time.sleep(random.uniform(0.5, 1.0))

    # Create threads
    readers = [threading.Thread(target=reader, args=(i+1,)) for i in range(3)]
    writers = [threading.Thread(target=writer, args=(i+1,)) for i in range(2)]

    # Start writers and readers
    for w in writers: w.start()
    for r in readers: r.start()
    for w in writers: w.join()
    for r in readers: r.join()

    print("Readers-Writers (readers-priority) completed.\n")

# ---------------------------
# 3) Dining Philosophers
# ---------------------------
def run_dining_philosophers():
    N = 5
    forks = [threading.Lock() for _ in range(N)]
    running_time = 8  # seconds to run the simulation
    stop_flag = {"stop": False}

    def philosopher(i):
        left = forks[i]
        right = forks[(i + 1) % N]
        while not stop_flag["stop"]:
            # Thinking
            print(f"[Philosopher-{i}] thinking.")
            time.sleep(random.uniform(0.5, 1.5))

            # To avoid deadlock: pick up the lower-numbered fork first
            first, second = (left, right) if id(left) < id(right) else (right, left)

            acquired_first = first.acquire(timeout=1)
            if not acquired_first:
                continue  # try again later
            acquired_second = second.acquire(timeout=1)
            if not acquired_second:
                first.release()
                continue

            # Eating (critical section)
            print(f"[Philosopher-{i}] eating.")
            time.sleep(random.uniform(0.5, 1.0))

            # Put down forks
            second.release()
            first.release()
            print(f"[Philosopher-{i}] finished eating and released forks.")

    threads = [threading.Thread(target=philosopher, args=(i,)) for i in range(N)]
    for t in threads: t.start()
    time.sleep(running_time)
    stop_flag["stop"] = True
    for t in threads: t.join()
    print("Dining Philosophers simulation completed.\n")

# ---------------------------
# Driver Menu
# ---------------------------
def main():
    print("Classical Synchronization Problems using Mutex")
    print("1) Producer-Consumer (bounded buffer)")
    print("2) Readers-Writers (readers priority)")
    print("3) Dining Philosophers")
    choice = input("Enter 1/2/3 to run (or q to quit): ").strip().lower()
    if choice == '1':
        run_producer_consumer()
    elif choice == '2':
        run_readers_writers()
    elif choice == '3':
        run_dining_philosophers()
    else:
        print("Exiting.")

if __name__ == "__main__":
    main()
