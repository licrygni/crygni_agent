from pydantic import BaseModel


# 创建权限 请求模型
class PermissionCreate(BaseModel):
    code: str               # 权限标识，如 "user:list"
    name: str               # 权限名称，如 "用户列表"
    description: str | None = None


# 更新权限 请求模型，code不允许修改
class PermissionUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


# 查询返回 响应模型
class PermissionRead(BaseModel):
    id: int
    code: str
    name: str
    description: str | None

    model_config = {"from_attributes": True}