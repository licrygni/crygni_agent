from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool


    #从orm模型中读取数据时，需要设置from_attributes=True
    # 相当于java以前的 beanutils.copyProperties方法
    model_config = {"from_attributes": True}