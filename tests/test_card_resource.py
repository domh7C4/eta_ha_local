# SPDX-License-Identifier: GPL-3.0-only
import ast
from pathlib import Path
from types import SimpleNamespace
from urllib.parse import urlsplit
import unittest


class CardResourceTests(unittest.IsolatedAsyncioTestCase):
    def make_setup(self, mode="storage", items=None):
        class Resources:
            def __init__(self):
                self.items = items or []
                self.created, self.updated = [], []
            async def async_get_info(self):
                return {"resources": len(self.items)}
            def async_items(self):
                return self.items
            async def async_create_item(self, data):
                self.created.append(data)
            async def async_update_item(self, item_id, data):
                self.updated.append((item_id, data))
        file = Path(__file__).resolve().parents[1] / "custom_components/eta_readonly/frontend.py"
        tree = ast.parse(file.read_text(encoding="utf-8"))
        nodes = [node for node in tree.body if isinstance(node, (ast.AsyncFunctionDef, ast.Assign))
                 and not (isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "_LOGGER" for t in node.targets))]
        ns = {"LOVELACE_DATA": "lovelace", "urlsplit": urlsplit,
              "_LOGGER": SimpleNamespace(warning=lambda *args: None)}
        exec(compile(ast.Module(body=nodes, type_ignores=[]), str(file), "exec"), ns)
        resources = Resources()
        hass = SimpleNamespace(data={"lovelace": SimpleNamespace(resource_mode=mode, resources=resources)})
        return ns, hass, resources

    async def test_registers_only_card_resource(self):
        ns, hass, resources = self.make_setup()
        await ns["async_setup_card_resource"](hass)
        self.assertEqual(resources.created, [{"url": ns["CARD_URL"], "res_type": "module"}])

    async def test_updates_own_resource_preserving_others(self):
        items = [{"id": "foreign", "url": "/local/flow-card.js", "type": "module"},
                 {"id": "eta", "url": "/eta_readonly/eta-heating-card.js?v=old", "type": "module"}]
        ns, hass, resources = self.make_setup(items=items)
        await ns["async_setup_card_resource"](hass)
        self.assertEqual(resources.created, [])
        self.assertEqual(resources.updated, [("eta", {"url": ns["CARD_URL"], "res_type": "module"})])
        self.assertEqual(items[0]["url"], "/local/flow-card.js")

    async def test_yaml_resources_are_not_modified(self):
        ns, hass, resources = self.make_setup(mode="yaml")
        await ns["async_setup_card_resource"](hass)
        self.assertFalse(resources.created or resources.updated)
