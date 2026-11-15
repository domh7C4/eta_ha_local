# SPDX-License-Identifier: GPL-3.0-only
"""Local ETA reads and explicit writes, with strict response validation."""
import asyncio
from .parser import NS, menu, value, varinfo, xml_root
from .control import check_uri

class EtaClient:
    def __init__(self, session, host, port):
        self.session = session
        self.base = f"http://[{host}]:{port}" if ":" in host else f"http://{host}:{port}"

    async def get(self, path):
        async with asyncio.timeout(10):
            async with self.session.get(self.base + path, allow_redirects=False) as response:
                if response.status != 200:
                    raise ValueError(f"ETA HTTP {response.status}: {path}")
                data = bytearray()
                async for chunk in response.content.iter_chunked(65536):
                    data.extend(chunk)
                    if len(data) > 2_000_000:
                        raise ValueError("ETA response too large")
                return data.decode("utf-8-sig")

    async def menu(self):
        return menu(await self.get("/user/menu"))

    async def value(self, uri):
        return value(await self.get("/user/var/" + check_uri(uri)))

    async def varinfo(self, uri):
        uri = check_uri(uri)
        result = varinfo(await self.get("/user/varinfo/" + uri))
        if result["uri"] != uri:
            raise ValueError("Metadata URI does not match the requested point")
        return result

    async def write(self, uri, payload):
        """POST once only. Never retry a write automatically."""
        path = "/user/var/" + check_uri(uri)
        async with asyncio.timeout(10):
            async with self.session.post(self.base + path, data=payload,
                                         allow_redirects=False) as response:
                if response.status != 200:
                    raise ValueError(f"ETA write rejected: HTTP {response.status}")
                data = bytearray()
                async for chunk in response.content.iter_chunked(65536):
                    data.extend(chunk)
                    if len(data) > 2_000_000:
                        raise ValueError("ETA response too large")
                success = xml_root(data.decode("utf-8-sig")).find(NS + "success")
                if success is None or success.get("uri") != path:
                    raise ValueError("ETA did not confirm the requested write")
