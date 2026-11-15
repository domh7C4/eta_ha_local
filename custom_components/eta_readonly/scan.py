# SPDX-License-Identifier: GPL-3.0-only
"""Bounded read-only discovery and polling without HA dependencies."""
import asyncio


async def read_points(points, read, *, errors=(OSError, ValueError, TimeoutError), progress=None):
    """Read every URI with two workers; mark failed reads without inventing values."""
    uris = list(points)
    pending = iter(uris)
    readings = {}
    completed = 0

    async def worker():
        nonlocal completed
        for uri in pending:
            try:
                readings[uri] = await read(uri)
            except errors:
                readings[uri] = None
            completed += 1
            if progress is not None:
                progress(completed / len(uris))

    # Cancellation of setup cancels and awaits both workers, including in-flight reads.
    async with asyncio.TaskGroup() as group:
        for _ in range(min(2, len(uris))):
            group.create_task(worker())
    return {uri: readings[uri] for uri in uris}
