from datetime import datetime, timedelta, timezone
import jwt
from jwt import DecodeError
from jwt import InvalidSignatureError
from jwt import ExpiredSignatureError
from src.core.config import settings
from src.core.exceptions import BizException

ALGORITHM = "HS256"

# 配置OAuth2 Bearer 模式
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def _get_signing_key() -> str:
    signing_key = settings.JWT_SECRET_KEY.get_secret_value()
    if not signing_key:
        raise RuntimeError("JWT_SECRET_KEY must be set in .env")
    return signing_key


# 编码JWT，创建一个令牌。登录成功后，把用户信息传递过来。 生成的令牌以后发给前端。
# 前端每次请求都需要携带自己的授权令牌。
def encode_jwt(payload: dict) -> str:
    payload_copy = payload.copy()
    # 更新过期时间为30分钟后。注意使用 utc 时间
    payload_copy["exp"] = datetime.now(timezone.utc) + timedelta(minutes=30)
    payload_copy["iat"] = datetime.now(timezone.utc)

    return jwt.encode(payload_copy, key=_get_signing_key(), algorithm=ALGORITHM)


# 解码JWT，验证令牌的有效性。[从令牌中获取用户信息]
# 每次请求到达后端时，从请求头中提取令牌，然后调用此函数验证令牌的有效性。
# 返回 当时用户的信息（payload里面不要放敏感数据）
def decode_jwt(token: str) -> dict:
    """解析jwt token"""
    signing_key = _get_signing_key()
    try:
        payload = jwt.decode(token, key=signing_key, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise BizException(code=401, message="token已过期")
    except (InvalidSignatureError, DecodeError):
        raise BizException(code=401, message="token非法")
    except Exception:
        raise BizException(code=401, message="token解析失败")
