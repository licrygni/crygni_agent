from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.base_schema import PageResult
from src.core.deps import PageParams
from src.infra.database import get_db
from src.modules.permission.service import PermissionService
from src.core.base_schema import ResponseSchema
from src.modules.permission.schema import PermissionRead, PermissionCreate, PermissionUpdate

router = APIRouter(prefix="/permission",tags=["权限"])

def get_permission_service(db: AsyncSession = Depends(get_db))->PermissionService:
    return PermissionService(db)

# 分页查询权限
@router.get("/search",response_model=ResponseSchema[PageResult[PermissionRead]],summary="分页查询权限")
async def search_permissions(
                            svc:PermissionService = Depends(get_permission_service),
                             params:PageParams = Depends()):
    permissions, total_count= await svc.search_page(params.offset,params.page_size,params.keyword)
    perms = [PermissionRead.model_validate(p) for p in permissions]

    return ResponseSchema(data=PageResult(
        items=perms,
        total=total_count,
        page=params.page,
        page_size=params.page_size,
    ))

#权限详情
@router.get("/{permission_id}",response_model=ResponseSchema[PermissionRead],summary="获取权限详情")
async def get_permission(permission_id: int,
                         svc:PermissionService = Depends(get_permission_service)):
    # 查到数据库的permission：api调service
    perm= await svc.get_permission(permission_id)
    # api封装返回值：entity -> schema
    permission_read = PermissionRead.model_validate(perm)
    return ResponseSchema(data=permission_read)

@router.get("/",response_model=ResponseSchema[list[PermissionRead]],summary="获取所有权限")
async def get_all_permissions(svc:PermissionService = Depends(get_permission_service)):
    permissions= await svc.list_permissions()
    return ResponseSchema(data=[PermissionRead.model_validate(p) for p in permissions])

# 创建权限
@router.post("/",response_model=ResponseSchema[PermissionRead],summary="创建权限")
async def create_permission(permission: PermissionCreate,
                            svc:PermissionService = Depends(get_permission_service)):
    # 调用service.create_permission()
    perm= await svc.create_permission(permission)
    # entity -> schema
    return ResponseSchema(data=PermissionRead.model_validate(perm))

# 更新权限
@router.put("/{permission_id}",response_model=ResponseSchema[PermissionRead],summary="更新权限")
async def update_permission(permission_id: int,
                            data:PermissionUpdate,
                            svc:PermissionService = Depends(get_permission_service)):
    perm = await svc.update_permission(permission_id, data)
    return ResponseSchema(data=PermissionRead.model_validate(perm))

# 删除权限
@router.delete("/{permission_id}", response_model=ResponseSchema[None], summary="删除权限")
async def delete_permission(permission_id: int,
                            svc:PermissionService = Depends(get_permission_service)):
    await svc.delete_permission(permission_id)
    return ResponseSchema[None](data=None)
