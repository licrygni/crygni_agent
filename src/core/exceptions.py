
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from loguru import logger


# ========================================
# 自定义业务异常
# ========================================

class BizException(Exception):
    """
    自定义业务异常类。

    code: 业务异常状态码
    message: 异常提示信息
    """

    def __init__(
        self,
        code: int = 400,
        message: str = "业务处理失败"
    ):
        self.code = code
        self.message = message

        super().__init__(message)


# ========================================
# 注册全局异常处理器
# ========================================

def register_exception_handlers(app: FastAPI) -> None:
    """
    统一注册全局异常处理器。
    """

    # ------------------------------------
    # 业务异常处理
    # ------------------------------------

    @app.exception_handler(BizException)
    async def biz_exception_handler(
        request: Request,
        exc: BizException
    ):
        """
        处理自定义业务异常。
        """

        return JSONResponse(
            status_code=200,
            content={
                "code": exc.code,
                "message": exc.message,
                "data": None
            }
        )

    # ------------------------------------
    # 全局未知异常处理
    # ------------------------------------

    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request,
        exc: Exception
    ):
        """
        处理未被捕获的其他异常。
        """

        logger.exception(f"Unhandled exception: {exc}")

        return JSONResponse(
            status_code=500,
            content={
                "code": 500,
                "message": "服务器内部错误",
                "data": None
            }
        )
