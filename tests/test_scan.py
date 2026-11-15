# SPDX-License-Identifier: GPL-3.0-only
import asyncio
import importlib.util
from pathlib import Path
import unittest

path = Path(__file__).resolve().parents[1] / "custom_components/eta_readonly/scan.py"
spec = importlib.util.spec_from_file_location("eta_scan", path)
scan = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scan)


class ScanTests(unittest.IsolatedAsyncioTestCase):
    async def test_more_than_fifty_and_bounded_concurrency(self):
        active = peak = 0
        async def read(uri):
            nonlocal active, peak
            active += 1
            peak = max(peak, active)
            await asyncio.sleep(0)
            active -= 1
            return {"state": uri}
        points = {str(i): f"Sensor {i}" for i in range(123)}
        progress = []
        result = await scan.read_points(points, read, progress=progress.append)
        self.assertEqual(list(result), list(points))
        self.assertTrue(all(v is not None for v in result.values()))
        self.assertEqual(peak, 2)
        self.assertEqual(progress[-1], 1)
        self.assertEqual(progress, sorted(progress))

    async def test_failed_group_does_not_discard_valid_sensors(self):
        async def read(uri):
            if uri == "group":
                raise ValueError("Not a variable")
            if uri == "offline":
                raise TimeoutError
            return {"state": 0}
        result = await scan.read_points(["good", "group", "offline"], read)
        self.assertEqual(result["good"], {"state": 0})
        self.assertIsNone(result["group"])
        self.assertIsNone(result["offline"])

    async def test_empty_menu(self):
        async def read(uri):
            self.fail("Must not read for an empty menu")
        self.assertEqual(await scan.read_points([], read), {})

    async def test_cancellation_cleans_up_workers(self):
        active = 0
        started = asyncio.Event()
        async def read(uri):
            nonlocal active
            active += 1
            if active == 2:
                started.set()
            try:
                await asyncio.Event().wait()
            finally:
                active -= 1
        task = asyncio.create_task(scan.read_points(range(100), read))
        await asyncio.wait_for(started.wait(), 1)
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await task
        self.assertEqual(active, 0)

    async def test_unexpected_errors_are_not_silenced(self):
        async def read(uri):
            raise RuntimeError("Programming error")
        with self.assertRaises(ExceptionGroup):
            await scan.read_points(["a"], read)
