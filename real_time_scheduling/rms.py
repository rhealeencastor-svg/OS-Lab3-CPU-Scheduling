TASKS = [
    {"id": "T1", "C": 1, "T": 4, "D": 4},
    {"id": "T2", "C": 1, "T": 5, "D": 5},
    {"id": "T3", "C": 2, "T": 10, "D": 10},
]
SIMULATION_TIME = 20


def schedule(tasks, duration):
    jobs = []
    gantt = []
    for task in tasks:
        for release in range(0, duration, task["T"]):
            jobs.append({
                "id": task["id"],
                "period": task["T"],
                "release": release,
                "deadline": release + task["D"],
                "remaining": task["C"],
                "completion": None,
            })

    for time in range(duration):
        ready = [
            job for job in jobs
            if job["release"] <= time < job["deadline"] and job["remaining"] > 0
        ]
        label = "IDLE"
        if ready:
            running = min(ready, key=lambda job: (job["period"], job["release"], job["id"]))
            label = running["id"]
            running["remaining"] -= 1
            if running["remaining"] == 0:
                running["completion"] = time + 1

        if gantt and gantt[-1][0] == label and gantt[-1][2] == time:
            gantt[-1] = (label, gantt[-1][1], time + 1)
        else:
            gantt.append((label, time, time + 1))

    for job in jobs:
        if job["completion"] is not None and job["completion"] <= job["deadline"]:
            job["status"] = "MET"
        elif job["deadline"] <= duration:
            job["status"] = "MISSED"
        else:
            job["status"] = "PENDING"

    return sorted(jobs, key=lambda job: (job["release"], job["id"])), gantt


def main():
    tasks = sorted(TASKS, key=lambda task: (task["T"], task["id"]))
    jobs, gantt = schedule(tasks, SIMULATION_TIME)
    utilization = sum(task["C"] / task["T"] for task in tasks)
    count = len(tasks)
    bound = count * (2 ** (1 / count) - 1)
    print("RATE MONOTONIC SCHEDULING")
    print("Priority Order: " + " > ".join(task["id"] for task in tasks))
    print(f"CPU Utilization: {utilization:.2%}")
    print(f"RMS Sufficient Utilization Bound: {bound:.2%}")
    print("Sufficient-Bound Test:", "PASS" if utilization <= bound else "NOT PASSED")

    print("\nGANTT CHART (ms)")
    for start in range(0, len(gantt), 5):
        segments = [f"{pid} [{left}-{right}]" for pid, left, right in gantt[start : start + 5]]
        print("| " + " | ".join(segments) + " |")

    print("\nTASK INSTANCE RESULTS (ms)")
    print(f"{'Task':<6}{'Release':>8}{'Deadline':>10}{'Completion':>12}  Status")
    for job in jobs:
        completion = job["completion"] if job["completion"] is not None else "-"
        print(
            f'{job["id"]:<6}{job["release"]:>8}{job["deadline"]:>10}'
            f'{completion:>12}  {job["status"]}'
        )
    print(f'\nDeadline Misses: {sum(job["status"] == "MISSED" for job in jobs)}')


if __name__ == "__main__":
    main()
