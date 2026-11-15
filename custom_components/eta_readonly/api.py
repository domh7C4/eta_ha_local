# SPDX-License-Identifier: GPL-3.0-only
"""GET-only local ETA client."""
import asyncio
from .parser import menu, value

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
        return value(await self.get("/user/var/" + uri))
