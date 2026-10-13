# MITC101 Advanced Data Structures — Seed S=7148

**Student:** John Lynnard Pdlaoan  
**Student ID:** 26-2387-148 MIT  
**Scenario:** SwiftCargo Logistics PH (fictional)

This repository contains Python implementations organized by Tasks 1–4, smoke/unit tests, benchmark and algorithm outputs, and charts. It is a reproducible working draft, not a claim of instructor approval or a substitute for being able to explain the work orally.

## Requirements
- Python 3.10+
- Standard library only for source/tests
- `matplotlib` is needed only to regenerate charts; current chart PNGs are included.

## Run
From this directory:
```bash
python task1/task1.py
python task2/task2.py
python task3/task3.py
python task3/hash_analysis.py
python task4/task4.py
python -m unittest discover -s tests -v
```
Benchmark generation is available by importing `task1.task1.benchmark`. Bubble sort is measured only for sizes <= 10,000 because its quadratic runtime makes the 100,000+ case impractical; the skipped case is labeled, not fabricated.

## Seed-specific parameters
- S = 7148
- Task 1 n = 1,000 + S = 8148
- Hiring simulation m = 50 + (S mod 50) = 98
- Task 2 stack actions = 10 + (S mod 10) = 18
- Task 2 circular queue capacity = 20 + (S mod 30) = 28
- Task 3 hash table size = smallest prime greater than 1,000 + S = 8161
- Task 4 knapsack capacity W = 20 + (S mod 11) = 29 kg

## Output files
- `sample_outputs/task1_benchmark.json`: actual measured timings from the current environment.
- `sample_outputs/hash_analysis.json`: measured probes for a deterministic generated dataset.
- `sample_outputs/red_black_insert_log.json`: insertion events for red-black tree.
- `sample_outputs/test_results.txt`: unit-test run.
- `charts/`: benchmark and simulation charts.

## Important caveats / verify before submission
1. Re-run tests and all programs on the machine/environment used for submission; timings vary by hardware and Python version.
2. The brief requests diagrams of the red-black tree after **each** insertion. The JSON event log documents recolors/rotations, but visual per-step diagrams still need to be generated or drawn and verified.
3. Hash table formulas in the assignment are simplified expectations. The load factor for 5,000 keys at table size 8161 is about 0.613; classical unsuccessful-search estimates vary with probing assumptions and clustering. Discuss assumptions rather than claiming an exact match.
4. Validate the tree height convention (edges versus nodes) against your instructor's preference.
5. Review the report, run the code yourself, and be prepared to explain design choices and results.
6. The generated report is a draft. Confirm APA details, page count and course formatting after opening the PDF/DOCX. Add instructor-required edits before LMS submission.


