
from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from src.core.config import get_settings
from src.core.logger import setup_logger
from src.core.exceptions import register_exception_handlers

from src.infra.database import engine

from src.middlewares.logging import LoggingMiddleware
from src.modules.user.api import router as user_router


# ========================================
# 1. 应用生命周期管理
# ========================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI 应用生命周期管理。

    yield 之前：应用启动时执行
    yield 之后：应用关闭时执行
    """

    # 初始化日志系统
    setup_logger()

    # 获取项目配置
    settings = get_settings()

    logger.info(
        f"{settings.APP_NAME} 启动... | "
        f"使用环境: {settings.APP_ENV}"
    )

    try:

        # ================================
        # 应用启动阶段
        # ================================

        # 后续可以在这里初始化 Redis
        # 后续可以在这里初始化 MinIO
        # 后续可以在这里加载其他资源

        # 应用启动成功，开始处理请求
        yield

    finally:

        # ================================
        # 应用关闭阶段
        # ================================

        logger.info("正在关闭数据库连接池...")

        # 释放异步数据库连接池
        await engine.dispose()

        logger.info(f"{settings.APP_NAME} 关闭...")


# ========================================
# 2. 创建 FastAPI 应用
# ========================================

def create_app() -> FastAPI:
    """
    创建并配置 FastAPI 应用实例。
    """

    settings = get_settings()

    # 创建应用
    app = FastAPI(
        title=settings.APP_NAME,
        version="1.0.0",
        debug=settings.APP_DEBUG,
        lifespan=lifespan,
    )

    # ================================
    # 注册中间件
    # ================================

    app.add_middleware(LoggingMiddleware)

    # ================================
    # 注册异常处理器
    # ================================

    register_exception_handlers(app)

    # ================================
    # 注册业务路由
    # ================================

    # 后续导入业务路由
    app.include_router(user_router,prefix="/api/v1")
    # app.include_router(agent_router)

    # ================================
    # 根路由
    # ================================

    @app.get("/")
    async def root():
        return {
            "message": "Hello World"
        }

    return app


# ========================================
# 3. 创建应用实例
# ========================================

app = create_app()
