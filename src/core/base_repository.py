
from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


# ========================================
# 泛型定义
# ========================================

T = TypeVar("T")


# ========================================
# 通用 Repository 基类
# ========================================

class BaseRepository(Generic[T]):
    """
    通用数据库仓储基类。

    所有具体 Repository 都可以继承此类，
    复用基础 CRUD 操作。
    """

    def __init__(
        self,
        model: type[T],
        db: AsyncSession
    ):
        """
        初始化 Repository。

        Args:
            model: 当前操作的 ORM 模型
            db: 异步数据库会话
        """

        self.model = model
        self.db = db

    # ====================================
    # 根据 ID 获取数据
    # ====================================

    async def get_by_id(self, id: int) -> T | None:

        return await self.db.get(self.model, id)

    # ====================================
    # 分页获取数据
    # ====================================

    async def get_all(
        self,
        offset: int = 0,
        limit: int = 100
    ) -> list[T]:

        if offset < 0:
            raise ValueError("offset 不能小于 0")

        if limit <= 0:
            raise ValueError("limit 必须大于 0")

        stmt = (
            select(self.model)
            .offset(offset)
            .limit(limit)
        )

        result = await self.db.execute(stmt)

        return list(result.scalars().all())

    # ====================================
    # 创建数据
    # ====================================

    async def create(self, obj: T) -> T:

        self.db.add(obj)

        await self.db.flush()

        await self.db.refresh(obj)

        return obj

    # ====================================
    # 更新数据
    # ====================================

    async def update(self, obj: T) -> T:

        await self.db.flush()

        await self.db.refresh(obj)

        return obj

    # ====================================
    # 删除数据
    # ====================================

    async def delete(self, obj: T) -> None:

        await self.db.delete(obj)

        await self.db.flush()
