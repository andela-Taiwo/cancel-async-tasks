import asyncio
import logging
import signal

log = logging.getLogger(__name__)


# Run a list of async task factories, but only let max_concurrent of them
# go at once. A task blowing up gets logged and the rest keep going.
# Ctrl-C / SIGTERM cancels whatever's left and bails out cleanly.
async def run_tasks(tasks, max_concurrent, handle_signals=True):
    if max_concurrent <= 0:
        raise ValueError("max_concurrent needs to be > 0")

    sem = asyncio.Semaphore(max_concurrent)

    async def run_one(idx, func):
        # the semaphore limits concurrency
        async with sem:
            try:
                await func()
            except Exception:
                # no need to catch the error. it needs to propagate
                log.exception("task %d failed", idx)

    workers = [
        asyncio.create_task(run_one(i, f), name=f"task-{i}")
        for i, f in enumerate(tasks)
    ]
    if not workers:
        return

    gathered = asyncio.gather(*workers)

    # we shut down by cancelling the gather. this flag just tells us
    # afterwards whether the cancel was us (a signal) or someone else.
    stopping = False

    def stop():
        nonlocal stopping
        if stopping:
            return
        stopping = True
        log.info("got a stop signal, cancelling %d task(s)", len(workers))
        gathered.cancel()

    loop = asyncio.get_running_loop()
    hooked = []
    if handle_signals:
        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                loop.add_signal_handler(sig, stop)
            except (NotImplementedError, RuntimeError, ValueError):
                break
            hooked.append(sig)

    try:
        await gathered
    except asyncio.CancelledError:
        # make sure everything is  actually wound down before we return
        await asyncio.gather(*workers, return_exceptions=True)
        if not stopping:
            raise
    finally:
        for sig in hooked:
            loop.remove_signal_handler(sig)
