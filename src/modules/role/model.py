from sqlalchemy import Table, Column, BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.modules.permission.model import Permission

from src.core.base_model import Base, BaseModel

# 角色与权限多对多中间表 复合主键（role_id,permission_id） 天然放重复效果
role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", BigInteger, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", BigInteger, ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True),
)

# 角色表 role.permissions
class Role(BaseModel):
    __tablename__ = "roles"

    code: Mapped[str] = mapped_column(String(100), unique=True, comment="角色编码")
    name: Mapped[str] = mapped_column(String(100), comment="角色名称")
    description: Mapped[str] = mapped_column(String(200), nullable=True, comment="角色描述")

    permissions: Mapped[list["Permission"]] = relationship(
        "Permission",
        secondary=role_permissions,
        lazy="selectin", # 立即加载
        # back_populates="roles"
    )

# 用户‑角色多对多中间表
user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", BigInteger, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", BigInteger, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
)