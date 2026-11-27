from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import BizException, ERR_PERM_NOT_FOUND, ERROR_PERM_NOT_FOUND_MSG
from src.modules.permission.model import Permission
from src.modules.permission.schema import PermissionCreate, PermissionUpdate
from src.modules.permission.repository import PermissionRepository


class PermissionService:
    def __init__(self,db: AsyncSession) -> None:
        self.repo = PermissionRepository(db)

    async def create_permission(self, data: PermissionCreate) -> Permission:
        # 1. 检查code是否已存在，已存在则抛BizException
        exist = await self.repo.get_by_code(data.code)
        if exist:
            raise BizException(code=30001, message="权限标识code已存在")

        # 2. 创建Permission对象 3.调用repo.create保存
        return await self.repo.create(Permission(**data.model_dump()))

    async def get_permission(self, permission_id: int) -> Permission:
        # 查不到抛 BizException(code=404)
        obj = await self.repo.get_by_id(permission_id)
        if not obj:
            raise BizException(code=ERR_PERM_NOT_FOUND, message=ERROR_PERM_NOT_FOUND_MSG)
        return obj

    async def list_permissions(self) -> Sequence[Permission]:
        # 调用repo.get_all()
        return await self.repo.get_all()

    async def update_permission(self, permission_id: int, data: PermissionUpdate) -> Permission:
        obj = await self.get_permission(permission_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, field, value)
        return await self.repo.update(obj)

    async def delete_permission(self, permission_id: int) -> None:
        obj = await self.get_permission(permission_id)
        await self.repo.delete(obj)


    async def search_page(self, offset: int,
                          limit: int,
                          keyword: str | None) -> tuple[list[Permission], int]:
        return await self.repo.search_page(offset, limit, keyword)
