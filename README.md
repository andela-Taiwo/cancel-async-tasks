# cancel-async-tasks

Simple helper scripts and job artifacts for running and testing the cancel-async-tasks Teminal Bench 2.0 task.

## Overview

This repository contains small runner scripts and a `jobs/` directory where run outputs and artifacts are stored.

## Quick Start

Prerequisites: Python 3.8+ (3.13+ recommended).

Run the main runner:

```bash
python run.py
```

Run a local test harness:

```bash
python local_test.py
```

Run the Harbour command(Requires Docker)
```
harbor run -d terminal-bench/terminal-bench-2 -a oracle --include-task-name terminal-bench/cancel-async-tasks
```
## Output / Artifacts

Job results, logs, and artifacts are written to the `jobs/` directory. Each run is placed in a timestamped subfolder (for example `jobs/2026-06-12__16-54-47/`) and contains `config.json`, `result.json`, and any generated artifacts and verifier output.

## Notes

- Inspect the latest job directory under `jobs/` to review run details and verifier outputs.
- If you need help running the scripts, open an issue or reach out to the maintainer.
