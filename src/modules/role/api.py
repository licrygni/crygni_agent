from src.core.deps import PageParams
from src.modules.permission.schema import PermissionRead
from src.core.base_schema import ResponseSchema, PageResult
from src.modules.role.schema import RoleRead
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.role.schema import RoleCreate, RoleUpdate, RoleAssignPermissions
from src.modules.role.service import RoleService
from src.infra.database import get_db

router = APIRouter(prefix="/roles", tags=["角色"])

# 核心就看
# 1.依赖注入：定义 RoleService 实例的创建，需要 AsyncSession 依赖
# 2.参数位置注入：使用 Depends 注入 Service依赖
# 3.api 调用 service 甩锅式敲代码；api接受请求，交给service处理返回业务数据，api把业务数据封装为前端要用的


def get_role_service(db: AsyncSession = Depends(get_db)) -> RoleService:
    return RoleService(db)


# POST  /roles 创建角色
@router.post(path="/roles", response_model=ResponseSchema[RoleRead])
async def create_role(
    role: RoleCreate,
    service: RoleService = Depends(get_role_service)
):
    data = await service.create_role(role)
    return ResponseSchema[RoleRead](data=RoleRead.model_validate(data))


# GET  /roles/{role_id} 角色详情(含权限列表)
@router.get(path="/roles/{role_id}", response_model=ResponseSchema[RoleRead])
async def get_role(
    role_id: int,
    service: RoleService = Depends(get_role_service)
):
    data = await service.get_role(role_id)
    permissions = [PermissionRead.model_validate(p) for p in data.permissions]
    rd = RoleRead.model_validate(data)
    rd.permissions = permissions
    return ResponseSchema[RoleRead](data=rd)


# 分页查询角色
@router.get("/search",response_model=ResponseSchema[PageResult[RoleRead]],summary="分页查询角色")
async def search_roles(
                            svc:RoleService = Depends(get_role_service),
                             params:PageParams = Depends()):
    roles, total_count= await svc.search_page(params.offset,params.page_size,params.keyword)
    roles = [RoleRead.model_validate(r) for r in roles]

    return ResponseSchema(data=PageResult(
        items=roles,
        total=total_count,
        page=params.page,
        page_size=params.page_size,
    ))

# GET  /roles 角色列表
@router.get(path="/roles", response_model=ResponseSchema[list[RoleRead]])
async def get_roles(
    service: RoleService = Depends(get_role_service)
):
    data = await service.list_roles()
    return ResponseSchema[list[RoleRead]](data=[RoleRead.model_validate(r) for r in data])


# PUT  /roles/{role_id} 更新角色
@router.put(path="/roles/{role_id}", response_model=ResponseSchema[RoleRead])
async def update_role(
    role_id: int,
    role: RoleUpdate,
    service: RoleService = Depends(get_role_service)
):
    data = await service.update_role(role_id, role)
    return ResponseSchema[RoleRead](data=RoleRead.model_validate(data))


# DELETE  /roles/{role_id} 删除角色
@router.delete(path="/roles/{role_id}", response_model=ResponseSchema[None])
async def delete_role(
    role_id: int,
    service: RoleService = Depends(get_role_service)
):
    await service.delete_role(role_id)
    return ResponseSchema[None](data=None)


# PUT  /roles/{role_id}/permissions 给角色分配权限
@router.put(path="/{role_id}/permissions", response_model=ResponseSchema[RoleRead])
async def update_role_permissions(
    role_id: int,
    role_permissions: RoleAssignPermissions,
    service: RoleService = Depends(get_role_service)
):
    data = await service.assign_permissions(role_id, role_permissions.permission_ids)
    return ResponseSchema[RoleRead](data=RoleRead.model_validate(data))
