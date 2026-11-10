from collections import deque


PROCESSES = [
    {"pid": "P1", "arrival": 0, "burst": 5, "queue": 1},
    {"pid": "P2", "arrival": 1, "burst": 4, "queue": 1},
    {"pid": "P3", "arrival": 0, "burst": 6, "queue": 2},
    {"pid": "P4", "arrival": 2, "burst": 3, "queue": 2},
    {"pid": "P5", "arrival": 3, "burst": 2, "queue": 1},
]
QUANTUM = 2


def schedule(processes, quantum):
    processes = sorted(
        (dict(process, remaining=process["burst"], completion=None) for process in processes),
        key=lambda process: (process["arrival"], process["pid"]),
    )
    pending = deque(processes)
    queue1 = deque()
    queue2 = deque()
    current_q1 = None
    current_q2 = None
    quantum_left = 0
    time = 0
    gantt = []

    while any(process["remaining"] > 0 for process in processes):
        while pending and pending[0]["arrival"] <= time:
            process = pending.popleft()
            if process["queue"] == 1:
                queue1.append(process)
            else:
                queue2.append(process)

        if current_q1 is None and queue1:
            current_q1 = queue1.popleft()
            quantum_left = quantum

        if current_q1 is not None:
            running = current_q1
            running["remaining"] -= 1
            quantum_left -= 1
            if running["remaining"] == 0:
                running["completion"] = time + 1
                current_q1 = None
            elif quantum_left == 0:
                queue1.append(running)
                current_q1 = None
        else:
            if current_q2 is None and queue2:
                current_q2 = queue2.popleft()
            running = current_q2
            if running is not None:
                running["remaining"] -= 1
                if running["remaining"] == 0:
                    running["completion"] = time + 1
                    current_q2 = None

        label = running["pid"] if running is not None else "IDLE"
        if gantt and gantt[-1][0] == label and gantt[-1][2] == time:
            gantt[-1] = (label, gantt[-1][1], time + 1)
        else:
            gantt.append((label, time, time + 1))
        time += 1

    return sorted(processes, key=lambda process: process["pid"]), gantt


def main():
    processes, gantt = schedule(PROCESSES, QUANTUM)
    print("MULTILEVEL QUEUE SCHEDULING")
    print(f"Queue 1: Round Robin (Quantum = {QUANTUM} ms)")
    print("Queue 2: FCFS")
    print("\nGANTT CHART (ms)")
    for start in range(0, len(gantt), 5):
        segments = [f"{pid} [{left}-{right}]" for pid, left, right in gantt[start : start + 5]]
        print("| " + " | ".join(segments) + " |")

    print("\nPROCESS PERFORMANCE (ms)")
    print(f"{'PID':<6}{'AT':>5}{'BT':>5}{'CT':>5}{'TAT':>5}{'WT':>5}")
    total_turnaround = 0
    total_waiting = 0
    for process in processes:
        turnaround = process["completion"] - process["arrival"]
        waiting = turnaround - process["burst"]
        total_turnaround += turnaround
        total_waiting += waiting
        print(
            f'{process["pid"]:<6}{process["arrival"]:>5}{process["burst"]:>5}'
            f'{process["completion"]:>5}{turnaround:>5}{waiting:>5}'
        )
    print(f"\nAverage Turnaround Time: {total_turnaround / len(processes):.2f} ms")
    print(f"Average Waiting Time: {total_waiting / len(processes):.2f} ms")


if __name__ == "__main__":
    main()
