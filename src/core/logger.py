
import sys
from pathlib import Path

from loguru import logger

from src.core.config import get_settings


# 防止重复初始化
_LOGGER_INITIALIZED = False


def setup_logger() -> None:
    """
    初始化日志系统。
    """

    global _LOGGER_INITIALIZED

    if _LOGGER_INITIALIZED:
        return

    settings = get_settings()

    # 移除 Loguru 默认处理器
    logger.remove()

    log_format = (
        "{time:YYYY-MM-DD HH:mm:ss} | "
        "{level} | "
        "{module}:{line} | "
        "{message}"
    )

    # 控制台输出
    logger.add(
        sys.stdout,
        level=settings.LOG_LEVEL,
        format=log_format,
        colorize=True,
    )

    # 文件输出
    if settings.LOG_TO_FILE:

        base_dir = Path(__file__).resolve().parents[2]

        log_dir = Path(settings.LOG_DIR)

        if not log_dir.is_absolute():
            log_dir = base_dir / log_dir

        log_dir.mkdir(parents=True, exist_ok=True)

        logger.add(
            str(log_dir / settings.LOG_FILE),
            level=settings.LOG_LEVEL,
            format=log_format,
            rotation=settings.LOG_MAX_BYTES,
            retention=settings.LOG_BACKUP_COUNT,
            encoding="utf-8",
        )

    _LOGGER_INITIALIZED = True
