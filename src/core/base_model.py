from datetime import datetime

from sqlalchemy import BigInteger, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# ========================================
# ORM 基础类
# ========================================


class Base(DeclarativeBase):
    """所有 ORM Model 继承此类"""

    pass


# ========================================
# 创建时间和更新时间混入类
# ========================================


class TimestampMixin:
    """提供创建时间和更新时间字段"""

    # 创建时间：插入时由数据库自动生成
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), comment="创建时间"
    )

    # 更新时间：插入和更新时自动维护
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        comment="更新时间",
    )

# 所有orm的对象都要继承该类
class BaseModel(Base, TimestampMixin):
    __abstract__ = True
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
