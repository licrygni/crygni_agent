
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from loguru import logger


# ========================================
# 请求日志中间件
# ========================================

class LoggingMiddleware(BaseHTTPMiddleware):
    """
    请求日志中间件。

    记录 HTTP 请求方法、请求路径、
    响应状态码以及请求处理耗时。
    """

    async def dispatch(
        self,
        request: Request,
        call_next
    ) -> Response:

        # 记录请求开始时间
        start = time.perf_counter()

        # 记录请求信息
        logger.info(
            f"--> {request.method} {request.url.path}"
        )

        # 将请求传递给下一个中间件或路由
        response = await call_next(request)

        # 计算请求耗时（毫秒）
        elapsed = (time.perf_counter() - start) * 1000

        # 记录响应信息
        logger.info(
            f"<-- {request.method} {request.url.path} "
            f"status={response.status_code} "
            f"{elapsed:.2f}ms"
        )

        return response
