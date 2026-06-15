import asyncio
from run import run_tasks


class Tracker:
    def __init__(self):
        self.running = 0
        self.peak = 0
        self.started = []
        self.cleaned = []

    def make(self, name, secs):
        async def job():
            self.started.append(name)
            self.running += 1
            self.peak = max(self.peak, self.running)
            try:
                await asyncio.sleep(secs)
            finally:
                self.running -= 1
                self.cleaned.append(name)

        return job


def report(label, ok, detail=""):
    tag = "PASS" if ok else "FAIL"
    line = f"[{tag}] {label}"
    if detail:
        line += f"  ({detail})"
    print(line)


async def test_cap():
    # 6 jobs, only 2 at a time
    t = Tracker()
    jobs = [t.make(f"c{i}", 0.2) for i in range(6)]
    await run_tasks(jobs, max_concurrent=2)

    report("concurrency cap respected", t.peak <= 2, f"peak={t.peak}, max=2")
    expected = [f"c{i}" for i in range(6)]
    report("all jobs ran + cleaned", sorted(t.cleaned) == sorted(t.started) == expected)


async def test_cancel():
    t = Tracker()
    jobs = [t.make(f"x{i}", 5) for i in range(5)]
    task = asyncio.create_task(run_tasks(jobs, max_concurrent=2))

    await asyncio.sleep(0.3)
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass

    # anything that started should have hit its finally block
    clean = len(t.started) > 0 and set(t.started) == set(t.cleaned)
    report(
        "started jobs clean up on cancel",
        clean,
        f"started={sorted(t.started)} cleaned={sorted(t.cleaned)}",
    )


def main():
    asyncio.run(test_cap())
    asyncio.run(test_cancel())


if __name__ == "__main__":
    main()
