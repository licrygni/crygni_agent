from sqlalchemy import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.role.repository import RoleRepository
from src.modules.permission.repository import PermissionRepository
from src.modules.role.model import Role
from src.modules.role.schema import RoleCreate, RoleUpdate
from src.core.exceptions import BizException



class RoleService:
    def __init__(self, db: AsyncSession):
        self.repo = RoleRepository(db)
        self.permission_repo = PermissionRepository(db)

    async def create_role(self, data: RoleCreate) -> Role:
        # 检查 code 是否已存在
        exist_role = await self.repo.get_by_code(data.code)
        if exist_role:
            raise BizException(message=f"角色标识[{data.code}]已存在")
        role = Role(**data.model_dump())
        return await self.repo.create(role)

    async def get_role(self, role_id: int) -> Role:
        # 查不到抛异常
        role = await self.repo.get_by_id(role_id)
        if not role:
            raise BizException(message="角色不存在")
        return role

    async def list_roles(self) -> Sequence[Role]:
        # 查询所有角色
        return await self.repo.get_all()

    async def update_role(self, role_id: int, data: RoleUpdate) -> Role:
        role = await self.get_role(role_id)
        update_dict = data.model_dump(exclude_unset=True)
        for k, v in update_dict.items():
            setattr(role, k, v)
        return await self.repo.update(role)

    async def delete_role(self, role_id: int) -> None:
        await self.repo.delete_by_id(role_id)
        return None

    async def assign_permissions(self, role_id: int, permission_ids: list[int]) -> Role:
        # 1.查找角色，不存在抛异常
        role = await self.get_role(role_id)
        # 2.批量查询权限，校验id全部真实存在
        real_permissions = await self.permission_repo.get_by_ids(permission_ids)
        if len(real_permissions) != len(permission_ids):
            raise BizException(message="存在无效的权限ID")
        # 3.给角色的relationship赋值，多对多中间表自动维护
        role.permissions = real_permissions
        await self.repo.update(role)
        return role

    async def search_page(self, offset: int,
                          limit: int,
                          keyword: str | None) -> tuple[list[Role], int]:
        return await self.repo.search_page(offset, limit, keyword)
