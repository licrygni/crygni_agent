
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.core.config import settings
from src.core.logger import setup_logger


# ========================================
# 日志
# ========================================

logger = setup_logger()


# ========================================
# 创建异步数据库引擎
# ========================================

engine = create_async_engine(
    url=settings.SQLALCHEMY_DATABASE_URI,

    # 连接池配置
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_timeout=settings.DB_POOL_TIMEOUT,
    pool_recycle=settings.DB_POOL_RECYCLE,
    pool_pre_ping=settings.DB_POOL_PRE_PING,

    # SQL 调试模式
    echo=settings.DB_ECHO,
)


# ========================================
# 创建异步 Session 工厂
# ========================================

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False,
)


# ========================================
# 数据库连接检查
# ========================================

async def check_db_connection() -> bool:
    """
    检查 MySQL 数据库连接是否正常。
    """

    try:

        async with engine.connect() as connection:

            await connection.execute(text("SELECT 1"))

        logger.info("MySQL 数据库连接成功")

        return True

    except SQLAlchemyError:

        logger.exception("MySQL 数据库连接失败")

        raise


# ========================================
# 释放数据库连接池
# ========================================

async def dispose_db_engine() -> None:
    """
    释放数据库连接池资源。
    """

    await engine.dispose()

    logger.info("MySQL 数据库连接池已释放")
