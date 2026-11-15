# SPDX-License-Identifier: GPL-3.0-only
"""Exercise real flow methods with small HA substitutes, not a full HA runtime."""
import ast
import asyncio
import ipaddress
from pathlib import Path
import re
from types import SimpleNamespace
import unittest
from test_scan import scan


class FlowBase:
    def __init_subclass__(cls, **kwargs):
        pass
    def _async_abort_entries_match(self, data):
        pass
    def async_show_progress(self, **kwargs):
        return {"type": "progress", **kwargs}
    def async_show_progress_done(self, **kwargs):
        return {"type": "progress_done", **kwargs}
    def async_update_progress(self, value):
        self.progress = value
    def async_create_entry(self, **kwargs):
        return {"type": "create_entry", **kwargs}
    def async_abort(self, **kwargs):
        return {"type": "abort", **kwargs}


class DiscoveryFlowTests(unittest.IsolatedAsyncioTestCase):
    def make_flow(self, menu, failed=()):
        class FakeClient:
            def __init__(self, *args):
                pass
            async def menu(self):
                return menu
            async def value(self, uri):
                await asyncio.sleep(0)
                if uri in failed:
                    raise ValueError("Unreadable group")
                return {"state": 1}
        source = Path(__file__).resolve().parents[1] / "custom_components/eta_readonly/config_flow.py"
        tree = ast.parse(source.read_text(encoding="utf-8-sig"))
        cls = next(n for n in tree.body if isinstance(n, ast.ClassDef))
        namespace = {
            "config_entries": SimpleNamespace(ConfigFlow=FlowBase), "DOMAIN": "eta_readonly",
            "EtaClient": FakeClient, "async_get_clientsession": lambda hass: None,
            "read_points": scan.read_points, "READ_ERRORS": (OSError, ValueError, TimeoutError),
            "ipaddress": ipaddress, "re": re,
        }
        exec(compile(ast.Module(body=[cls], type_ignores=[]), str(source), "exec"), namespace)
        flow = namespace[cls.name]()
        flow.hass = SimpleNamespace(async_create_task=asyncio.create_task)
        return flow

    async def test_first_setup_discovers_and_saves_more_than_fifty(self):
        menu = {str(i): f"Sensor {i}" for i in range(80)}
        flow = self.make_flow(menu, failed={"4"})
        result = await flow.async_step_user({"host": "192.168.1.10", "port": 8080, "interval": 60})
        self.assertEqual(result["type"], "progress")
        task = flow._scan_task
        again = await flow.async_step_discover()
        self.assertIs(again["progress_task"], task)
        await task
        done = await flow.async_step_discover()
        self.assertEqual(done["next_step_id"], "points")
        entry = await flow.async_step_points({"points": list(flow._found)})
        self.assertEqual(len(entry["data"]["points"]), 79)
        self.assertEqual(entry["data"]["discovery"], {"candidates": 80, "readable": 79, "skipped": 1})
        self.assertEqual(flow.progress, 1)

    async def test_no_readable_points_aborts(self):
        flow = self.make_flow({"group": "Group"}, failed={"group"})
        flow.connection = {"host": "eta.local", "port": 8080}
        await flow._async_discover()
        self.assertEqual(await flow.async_step_points(), {"type": "abort", "reason": "no_points"})

    async def test_empty_menu_aborts(self):
        flow = self.make_flow({})
        flow.connection = {"host": "eta.local", "port": 8080}
        await flow._async_discover()
        self.assertEqual(await flow.async_step_points(), {"type": "abort", "reason": "no_points"})
