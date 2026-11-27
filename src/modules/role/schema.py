from pydantic import BaseModel
from typing import List
from src.modules.permission.schema import PermissionRead


class RoleCreate(BaseModel):
    code: str               # 角色标识，如 "admin"
    name: str               # 角色名称，如 "管理员"
    description: str | None = None


class RoleUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class RoleRead(BaseModel):
    id: int
    code: str
    name: str
    description: str | None
    permissions: List[PermissionRead] = []  # 嵌套返回角色拥有的权限

    model_config = {"from_attributes": True}


class RoleAssignPermissions(BaseModel):
    permission_ids: List[int]   # 要分配给该角色的权限 ID 列表