from src.core.base_repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Sequence

from src.modules.permission.model import Permission


class PermissionRepository(BaseRepository[Permission]):
    SEARCH_FIELDS = [
        'code',
        'name',
    ]
    def __init__(self, db: AsyncSession):
        super().__init__(Permission, db)

    # 按照code查询权限
    async def get_by_code(self, code: str) -> Permission | None:
        # 根据code查询权限，code是唯一的，返回Permission或者None
        return await self.db.scalar(
            select(Permission).filter(Permission.code == code)
        )
    async def get_by_ids(self, ids: list[int]) -> list[Permission]:
        # 根据id列表查询权限，返回权限列表
        result = await self.db.scalars(select(Permission).where(Permission.id.in_(ids)))
        return result.all()

    async def search_page(self, offset: int, limit: int, keyword: str | None) -> tuple[list[Permission], int]:
        return await self.get_page(offset, limit, keyword, self.SEARCH_FIELDS)
