from functools import lru_cache
from pathlib import Path
from urllib.parse import quote_plus

from pydantic_settings import BaseSettings, SettingsConfigDict

# ========================================
# 项目根目录
# ========================================

BASE_DIR = Path(__file__).resolve().parents[2]


# ========================================
# 项目配置
# ========================================


class Settings(BaseSettings):
    # ====================================
    # 基础服务与应用环境
    # ====================================

    APP_NAME: str = "crygni_agent"
    APP_ENV: str = "development"
    APP_DEBUG: bool = True
    APP_PORT: int = 8000

    # ====================================
    # MySQL 数据库配置
    # ====================================

    MYSQL_HOST: str = "127.0.0.1"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = ""
    MYSQL_DATABASE: str = "chenguang"

    # ====================================
    # MySQL 连接池配置
    # ====================================

    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 1800
    DB_POOL_PRE_PING: bool = True
    DB_ECHO: bool = False

    # ====================================
    # Redis 配置
    # ====================================

    REDIS_HOST: str = "127.0.0.1"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ""
    REDIS_DB: int = 0

    # ====================================
    # MinIO 配置
    # ====================================

    MINIO_ENDPOINT: str = "127.0.0.1:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_SECURE: bool = False
    MINIO_BUCKET_NAME: str = "chenguang-agent"

    # ====================================
    # 日志配置
    # ====================================

    LOG_LEVEL: str = "INFO"
    LOG_TO_FILE: bool = False
    LOG_DIR: str = "logs"
    LOG_FILE: str = "app.log"
    LOG_MAX_BYTES: int = 10 * 1024 * 1024
    LOG_BACKUP_COUNT: int = 5

    # ====================================
    # 异步数据库连接字符串
    # ====================================

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:

        username = quote_plus(self.MYSQL_USER)
        password = quote_plus(self.MYSQL_PASSWORD)
        database = quote_plus(self.MYSQL_DATABASE)

        return (
            f"mysql+asyncmy://{username}:{password}"
            f"@{self.MYSQL_HOST}:{self.MYSQL_PORT}"
            f"/{database}?charset=utf8mb4"
        )

    # ====================================
    # 环境变量配置
    # ====================================

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env", env_file_encoding="utf-8", extra="ignore"
    )


# ========================================
# 获取配置对象
# ========================================


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
