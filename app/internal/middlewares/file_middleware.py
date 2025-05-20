from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse


class LimitUploadSizeMiddleware(BaseHTTPMiddleware):
    MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB

    async def dispatch(self, request: Request, call_next):
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > self.MAX_UPLOAD_SIZE:
            return JSONResponse(
                {"detail": f"File exceeds {self.MAX_UPLOAD_SIZE // (1024 * 1024)} MB"},
                status_code=413,
            )
        return await call_next(request)
