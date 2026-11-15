# SPDX-License-Identifier: GPL-3.0-only
"""Run the real coordinator write method with test-only HA substitutes."""
import ast
import asyncio
from pathlib import Path
from types import SimpleNamespace
import unittest
from test_control import control, NUMBER


class ValidationError(Exception):
    pass


class ClientError(Exception):
    pass


class WriteFlowTests(unittest.IsolatedAsyncioTestCase):
    def make_coordinator(self, enabled=True, writable=True, fail_post=False):
        class FakeClient:
            def __init__(self):
                self.posts = []
                self.metadata_requests = 0
            async def varinfo(self, uri):
                self.metadata_requests += 1
                return {**NUMBER, "writable": writable}
            async def write(self, uri, payload):
                self.posts.append((uri, payload))
                if fail_post:
                    raise TimeoutError
        class Base:
            async def async_request_refresh(self):
                self.refreshed = True
        file = Path(__file__).resolve().parents[1] / "custom_components/eta_readonly/__init__.py"
        tree = ast.parse(file.read_text(encoding="utf-8"))
        cls = next(node for node in tree.body if isinstance(node, ast.ClassDef))
        namespace = {"DataUpdateCoordinator": Base, "asyncio": asyncio,
                     "write_payload": control.write_payload, "ServiceValidationError": ValidationError,
                     "HomeAssistantError": RuntimeError, "aiohttp": SimpleNamespace(ClientError=ClientError)}
        exec(compile(ast.Module(body=[cls], type_ignores=[]), str(file), "exec"), namespace)
        obj = namespace[cls.name].__new__(namespace[cls.name])
        obj.entry = SimpleNamespace(options={"allow_write": enabled})
        obj.points = {"112/10021/0/0/1": "Sollwert"}
        obj.client = FakeClient()
        obj._write_lock = asyncio.Lock()
        obj.refreshed = False
        return obj

    async def test_disabled_access_never_posts(self):
        obj = self.make_coordinator(enabled=False)
        with self.assertRaises(ValidationError):
            await obj.async_write("112/10021/0/0/1", "40")
        self.assertEqual(obj.client.posts, [])
        self.assertEqual(obj.client.metadata_requests, 0)

    async def test_readonly_point_never_posts(self):
        obj = self.make_coordinator(writable=False)
        with self.assertRaises(ValidationError):
            await obj.async_write("112/10021/0/0/1", "40")
        self.assertEqual(obj.client.posts, [])

    async def test_unselected_point_never_posts(self):
        obj = self.make_coordinator()
        with self.assertRaises(ValidationError):
            await obj.async_write("112/10021/0/0/999", "40")
        self.assertEqual(obj.client.posts, [])

    async def test_success_posts_scaled_value_and_refreshes(self):
        obj = self.make_coordinator()
        await obj.async_write("112/10021/0/0/1", "40.5")
        self.assertEqual(obj.client.posts, [("112/10021/0/0/1", {"value": "405"})])
        self.assertTrue(obj.refreshed)

    async def test_timeout_is_not_retried(self):
        obj = self.make_coordinator(fail_post=True)
        with self.assertRaises(RuntimeError):
            await obj.async_write("112/10021/0/0/1", "40")
        self.assertEqual(len(obj.client.posts), 1)
        self.assertFalse(obj.refreshed)
