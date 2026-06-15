# cancel-async-tasks

Simple helper scripts and job artifacts for running and testing the cancel-async-tasks Teminal Bench 2.0 task.

## Overview

This repository contains small runner scripts and a verifier result of the task.

## Quick Start

Prerequisites: Python 3.8+ (3.13+ recommended).

Run the main runner:

```bash
python run.py
```

Run a local test harness:

```bash
python test_local.py
```

Run the Harbour command(Requires Docker)
```
harbor run -d terminal-bench/terminal-bench-2 -a oracle --include-task-name terminal-bench/cancel-async-tasks
```
## Output / Artifacts

`crtf.json` and `result.json` are the  generated artifacts and verifier output.

