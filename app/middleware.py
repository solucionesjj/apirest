import time
import uuid
import os
from typing import Callable, Dict, Tuple
from starlette.types import ASGIApp, Receive, Scope, Send

RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))

class RateLimitStore:
    def __init__(self) -> None:
        self.store: Dict[str, Tuple[int, int]] = {}

    def check(self, key: str) -> Tuple[int, int]:
        now = int(time.time())
        window = now // 60
        count, win = self.store.get(key, (0, window))
        if win != window:
            count = 0
            win = window
        count += 1
        self.store[key] = (count, win)
        reset = (win + 1) * 60
        remaining = max(RATE_LIMIT_PER_MINUTE - count, 0)
        return remaining, reset

rate_store = RateLimitStore()

class RequestLoggerMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        request_id = str(uuid.uuid4())
        scope["request_id"] = request_id
        start = time.time()
        client_host = scope.get("client")[0] if scope.get("client") else ""
        remaining, reset = rate_store.check(client_host)

        status_code_holder = {"code": None}

        async def send_wrapper(message):
            if message.get("type") == "http.response.start":
                headers = message.setdefault("headers", [])
                headers.append((b"x-request-id", request_id.encode()))
                headers.append((b"x-ratelimit-limit", str(RATE_LIMIT_PER_MINUTE).encode()))
                headers.append((b"x-ratelimit-remaining", str(remaining).encode()))
                headers.append((b"x-ratelimit-reset", str(reset).encode()))
                status_code_holder["code"] = message.get("status")
            await send(message)

        await self.app(scope, receive, send_wrapper)
        duration_ms = int((time.time() - start) * 1000)
        route = scope.get("path", "")
        method = scope.get("method", "")
        status_code = status_code_holder["code"] or 0
        print(f"timestamp={int(time.time())} method={method} route={route} status={status_code} duration_ms={duration_ms} request_id={request_id}")
