# SPDX-License-Identifier: GPL-3.0-only
"""Exercise the real HTTP client against in-memory HTTP response substitutes."""
import importlib
from pathlib import Path
import sys
from types import ModuleType
import unittest

package = ModuleType("eta_transport_test")
package.__path__ = [str(Path(__file__).resolve().parents[1] / "custom_components/eta_readonly")]
sys.modules[package.__name__] = package
api = importlib.import_module(package.__name__ + ".api")
URI = "112/10021/0/0/12080"


def xml(body):
    return ('<eta xmlns="http://www.eta.co.at/rest/v1">' + body + '</eta>').encode()


class Response:
    def __init__(self, body, status=200):
        self.body, self.status, self.content = body, status, self
    async def __aenter__(self):
        return self
    async def __aexit__(self, *args):
        return False
    async def iter_chunked(self, size):
        # Exercise fragmented XML responses.
        for index in range(0, len(self.body), 17):
            yield self.body[index:index + 17]


class Session:
    def __init__(self, response):
        self.response, self.calls = response, []
    def get(self, url, **kwargs):
        self.calls.append(("GET", url, kwargs))
        return self.response
    def post(self, url, **kwargs):
        self.calls.append(("POST", url, kwargs))
        return self.response


class ApiTests(unittest.IsolatedAsyncioTestCase):
    async def test_post_encoding_and_success(self):
        session = Session(Response(xml(f'<success uri="/user/var/{URI}"/>')))
        client = api.EtaClient(session, "eta.local", 8080)
        payload = {"value": "400", "begin": "0", "end": "48"}
        await client.write(URI, payload)
        self.assertEqual(session.calls, [("POST", f"http://eta.local:8080/user/var/{URI}",
                                        {"data": payload, "allow_redirects": False})])

    async def test_rejection_or_wrong_acknowledgement(self):
        for response in (Response(xml('<error/>')), Response(xml('<success uri="/wrong"/>')),
                         Response(b'failed', 500), Response(b'', 302)):
            session = Session(response)
            with self.assertRaises(ValueError):
                await api.EtaClient(session, "eta.local", 8080).write(URI, {"value": "1"})
            self.assertEqual(len(session.calls), 1)

    async def test_metadata_matches_requested_uri(self):
        body = xml(f'<varInfo><variable uri="{URI}" isWritable="1"><type>TEXT</type></variable></varInfo>')
        session = Session(Response(body))
        info = await api.EtaClient(session, "eta.local", 8080).varinfo(URI)
        self.assertTrue(info["writable"])
        with self.assertRaises(ValueError):
            await api.EtaClient(session, "eta.local", 8080).varinfo("112/10021/0/0/1")

    async def test_invalid_uri_never_contacts_controller(self):
        session = Session(Response(b''))
        with self.assertRaises(ValueError):
            await api.EtaClient(session, "eta.local", 8080).write("../api", {"value": "1"})
        self.assertFalse(session.calls)
