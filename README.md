# OS Laboratory Activity 3

## Multilevel Queue and Real-Time CPU Scheduling

### Student Information

| Field | Details |
| --- | --- |
| Name | Rhea Leen Castor |
| Course and Section | BSCA-3 |
| Instructor | Maria Fe Bahinting |
| Date Submitted | To be filled on submission |

### I. Introduction

This lab uses Python to simulate Multilevel Queue (MLQ), Rate Monotonic Scheduling (RMS), and Earliest Deadline First (EDF). The Gantt charts show when each process or task uses the CPU. The results show process waiting and turnaround times, task utilization, and deadline status.

### II. Objectives

- Explain how MLQ, RMS, and EDF select work for the CPU.
- Implement MLQ with Round Robin and First Come, First Served (FCFS).
- Simulate preemptive RMS and EDF in Python.
- Read Gantt charts and calculate scheduling results.
- Organize the programs, outputs, screenshots, and documentation in a GitHub repository.

### III. Scheduling Algorithms

| Algorithm | Rule |
| --- | --- |
| MLQ | Queue 1 uses Round Robin with a 2 ms quantum. Queue 2 uses FCFS. Queue 1 has priority over Queue 2. |
| RMS | The ready job from the task with the shortest period runs first. The priority order stays fixed. |
| EDF | The ready job with the earliest absolute deadline runs first. Priority can change as jobs arrive. |

### IV. Program Implementation

- **MLQ** adds each arriving process to its assigned queue. Queue 1 gets the CPU whenever it has ready work. A Queue 2 process interrupted by Queue 1 resumes with its remaining burst time.
- **RMS** creates a separate job for each periodic release. It selects the ready job with the shortest task period each millisecond.
- **EDF** also creates one job per release. It selects the ready job with the earliest absolute deadline. An earlier release time breaks a tie, followed by task ID.

The simulations use 1 ms steps and ignore context-switching overhead. RMS and EDF simulate one CPU for 20 ms. Each job's absolute deadline equals its release time plus its relative deadline.

Run the programs from the repository folder with Python 3.

```bash
python3 multilevel_queue/mlq.py
python3 real_time_scheduling/rms.py
python3 real_time_scheduling/edf.py
```

### V. Test Data

All times are in milliseconds.

#### MLQ Processes

| Process | Arrival Time | Burst Time | Queue |
| --- | ---: | ---: | ---: |
| P1 | 0 | 5 | 1 |
| P2 | 1 | 4 | 1 |
| P3 | 0 | 6 | 2 |
| P4 | 2 | 3 | 2 |
| P5 | 3 | 2 | 1 |

#### RMS and EDF Tasks

| Task | Execution Time (C) | Period (T) | Relative Deadline (D) |
| --- | ---: | ---: | ---: |
| T1 | 1 | 4 | 4 |
| T2 | 1 | 5 | 5 |
| T3 | 2 | 10 | 10 |

Each task releases its first job at 0 ms and repeats at its period.

### VI. Results and Discussion

#### MLQ

```text
| P1 [0–2] | P2 [2–4] | P1 [4–6] | P5 [6–8] |
| P2 [8–10] | P1 [10–11] | P3 [11–17] | P4 [17–20] |
```

| Process | Arrival (AT) | Burst (BT) | Completion (CT) | Turnaround (TAT) | Waiting (WT) |
| --- | ---: | ---: | ---: | ---: | ---: |
| P1 | 0 | 5 | 11 | 11 | 6 |
| P2 | 1 | 4 | 10 | 9 | 5 |
| P3 | 0 | 6 | 17 | 17 | 11 |
| P4 | 2 | 3 | 20 | 18 | 15 |
| P5 | 3 | 2 | 8 | 5 | 3 |

`TAT = CT - AT` and `WT = TAT - BT`.

- Average turnaround time = (11 + 9 + 17 + 18 + 5) / 5 = **12 ms**.
- Average waiting time = (6 + 5 + 11 + 15 + 3) / 5 = **8 ms**.

Queue 1 runs from 0 to 11 ms. Queue 2 then runs P3 and P4 in arrival order. The CPU is busy for all 20 ms in this run.

#### RMS and EDF

Both programs produce this Gantt chart for the given tasks.

```text
| T1 [0–1] | T2 [1–2] | T3 [2–4] | T1 [4–5] | T2 [5–6] |
| IDLE [6–8] | T1 [8–9] | IDLE [9–10] | T2 [10–11] |
| T3 [11–12] | T1 [12–13] | T3 [13–14] | IDLE [14–15] |
| T2 [15–16] | T1 [16–17] | IDLE [17–20] |
```

RMS gives T1 the highest priority, followed by T2 and T3. At 12 ms, T1 interrupts T3 because T1 has the shorter period. EDF makes the same choice because T1's absolute deadline is 16 ms and T3's is 20 ms. T3 resumes at 13 ms and finishes at 14 ms.

The CPU utilization is `U = 1/4 + 1/5 + 2/10 = 0.65 = 65%`. The CPU runs jobs for 13 of the 20 ms. The RMS sufficient bound for three tasks is `3(2^(1/3) - 1)`, or about 77.98%. The 65% utilization passes this test. It also passes the EDF utilization test for independent, preemptible periodic tasks on one CPU with deadlines equal to periods and no scheduling overhead.

| Task | Release | Absolute Deadline | Completion | RMS Status | EDF Status |
| --- | ---: | ---: | ---: | --- | --- |
| T1 | 0 | 4 | 1 | Met | Met |
| T2 | 0 | 5 | 2 | Met | Met |
| T3 | 0 | 10 | 4 | Met | Met |
| T1 | 4 | 8 | 5 | Met | Met |
| T2 | 5 | 10 | 6 | Met | Met |
| T1 | 8 | 12 | 9 | Met | Met |
| T2 | 10 | 15 | 11 | Met | Met |
| T3 | 10 | 20 | 14 | Met | Met |
| T1 | 12 | 16 | 13 | Met | Met |
| T2 | 15 | 20 | 16 | Met | Met |
| T1 | 16 | 20 | 17 | Met | Met |

All 11 jobs meet their deadlines in both runs.

| Program | Saved Output | Execution Screenshot |
| --- | --- | --- |
| MLQ | [mlq_output.txt](outputs/mlq_output.txt) | [MLQ screenshot](screenshots/01_MLQ.jpg) |
| RMS | [rms_output.txt](outputs/rms_output.txt) | [RMS screenshot](screenshots/02_RMS.jpg) |
| EDF | [edf_output.txt](outputs/edf_output.txt) | [EDF screenshot](screenshots/03_EDF.jpg) |

### VII. Algorithm Comparison

| Criterion | MLQ | RMS | EDF |
| --- | --- | --- | --- |
| Scheduling basis | Queue priority | Task period | Absolute deadline |
| Priority | Fixed by queue | Fixed by task period | Changes with ready jobs |
| Preemption | Queue 1 can interrupt Queue 2 | A higher-priority job can interrupt | An earlier deadline can interrupt |
| Use | Processes with different needs | Periodic tasks with fixed priorities | Tasks that need to meet deadlines |
| Deadline tracking | None in this simulation | Yes | Yes |

### VIII. Conclusion

MLQ ran the interactive queue first and left the batch queue to run afterward. RMS and EDF both completed all 11 jobs by their deadlines at 65% utilization. The Gantt charts show how priority determines which process runs and when it can resume.

### Guide Questions

1. **What is the main difference between MLQ and Multilevel Feedback Queue scheduling?**  
   MLQ keeps each process in its assigned queue. Multilevel Feedback Queue can move processes between queues based on their behavior.
2. **Why does MLQ use different algorithms for different queues?**  
   Interactive processes benefit from short turns. Batch processes can run in arrival order. Each queue can use the policy that fits its work.
3. **How does RMS decide which task runs first?**  
   It chooses the ready job from the task with the shortest period.
4. **Why is RMS a fixed-priority algorithm?**  
   Each task's priority depends on its period. The period stays the same for every release.
5. **How does EDF choose the next task?**  
   It chooses the ready job with the earliest absolute deadline.
6. **Why is EDF a dynamic-priority algorithm?**  
   Each new job has its own absolute deadline. A newly released job can become the first choice.
7. **What happens when a newly released job has an earlier deadline under EDF?**  
   It interrupts the current job. The current job stays ready with its remaining execution time.
8. **Why is CPU utilization important?**  
   It measures how much CPU time the tasks need. It helps check whether the CPU can handle the workload under the scheduling test's assumptions.
9. **Can a task set below 100% utilization still miss a deadline?**  
   Yes. Short deadlines can require more work in a brief interval than the CPU can finish. If two jobs released together each need 2 ms and both are due in 3 ms, they need 4 ms before the deadline. They miss a deadline even if each repeats only every 10 ms, giving 40% utilization.
10. **Which algorithm is recommended for periodic real-time tasks?**  
    EDF is a good choice when deadlines drive the schedule. It runs the most urgent ready job first and can use up to 100% CPU under the assumptions used in this lab. RMS is useful when fixed priorities are preferred.
