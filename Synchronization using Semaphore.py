# sync_semaphore.py
# Classical Synchronization Problems using Semaphore
# (1) Producer-Consumer
# (2) Readers-Writers
# (3) Dining Philosophers

import threading
import time
import random

# ---------------------------
# 1) Producer-Consumer Problem
# ---------------------------
def run_producer_consumer():
    buffer = []
    BUFFER_SIZE = 5

    mutex = threading.Semaphore(1)  # binary semaphore (mutex)
    empty = threading.Semaphore(BUFFER_SIZE)  # initially all slots empty
    full = threading.Semaphore(0)  # initially no full slots

    def producer():
        for i in range(1, 11):
            item = random.randint(1, 100)
            empty.acquire()      # wait if buffer is full
            mutex.acquire()      # enter critical section
            buffer.append(item)
            print(f"[Producer] produced {item} | Buffer: {buffer}")
            mutex.release()      # exit critical section
            full.release()       # increment count of full slots
            time.sleep(random.uniform(0.5, 1.0))

    def consumer():
        for i in range(1, 11):
            full.acquire()       # wait if buffer is empty
            mutex.acquire()
            item = buffer.pop(0)
            print(f"[Consumer] consumed {item} | Buffer: {buffer}")
            mutex.release()
            empty.release()      # increment empty slot count
            time.sleep(random.uniform(0.5, 1.2))

    p = threading.Thread(target=producer)
    c = threading.Thread(target=consumer)

    p.start()
    c.start()
    p.join()
    c.join()
    print("Producer-Consumer using Semaphores completed.\n")


# ---------------------------
# 2) Readers-Writers Problem
# ---------------------------
def run_readers_writers():
    rw_mutex = threading.Semaphore(1)  # used by writers to block readers
    mutex = threading.Semaphore(1)     # protects read_count
    read_count = 0
    data = {"value": 0}

    def reader(reader_id):
        nonlocal read_count
        for _ in range(3):
            mutex.acquire()
            read_count += 1
            if read_count == 1:
                rw_mutex.acquire()  # first reader locks resource
            mutex.release()

            # Reading
            print(f"[Reader-{reader_id}] reading value = {data['value']}")
            time.sleep(random.uniform(0.3, 0.6))

            mutex.acquire()
            read_count -= 1
            if read_count == 0:
                rw_mutex.release()  # last reader releases resource
            mutex.release()
            time.sleep(random.uniform(0.3, 0.7))

    def writer(writer_id):
        for _ in range(2):
            rw_mutex.acquire()  # writers need exclusive access
            new_val = data["value"] + random.randint(1, 10)
            data["value"] = new_val
            print(f"[Writer-{writer_id}] writing value = {new_val}")
            time.sleep(random.uniform(0.4, 0.8))
            rw_mutex.release()
            time.sleep(random.uniform(0.5, 1.0))

    # Create threads
    readers = [threading.Thread(target=reader, args=(i + 1,)) for i in range(3)]
    writers = [threading.Thread(target=writer, args=(i + 1,)) for i in range(2)]

    for w in writers:
        w.start()
    for r in readers:
        r.start()

    for w in writers:
        w.join()
    for r in readers:
        r.join()

    print("Readers-Writers using Semaphores completed.\n")


# ---------------------------
# 3) Dining Philosophers Problem
# ---------------------------
def run_dining_philosophers():
    N = 5
    forks = [threading.Semaphore(1) for _ in range(N)]
    stop_flag = {"stop": False}
    runtime = 8

    def philosopher(i):
        left = forks[i]
        right = forks[(i + 1) % N]
        while not stop_flag["stop"]:
            print(f"[Philosopher-{i}] thinking...")
            time.sleep(random.uniform(0.5, 1.2))

            left.acquire()
            right.acquire()
            print(f"[Philosopher-{i}] eating...")
            time.sleep(random.uniform(0.5, 1.0))
            left.release()
            right.release()
            print(f"[Philosopher-{i}] finished eating.")

    threads = [threading.Thread(target=philosopher, args=(i,)) for i in range(N)]
    for t in threads:
        t.start()
    time.sleep(runtime)
    stop_flag["stop"] = True
    for t in threads:
        t.join()
    print("Dining Philosophers using Semaphores completed.\n")


# ---------------------------
# Driver Menu
# ---------------------------
def main():
    print("Classical Synchronization Problems using Semaphores")
    print("1) Producer-Consumer")
    print("2) Readers-Writers")
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
