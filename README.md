# crygni_agent
一站式管理agent、大模型、提示词、知识库的平台

登录接口使用项目根目录 `.env` 中的 `JWT_SECRET_KEY` 签发令牌。可用以下命令生成密钥。

```sh
python -c "import secrets; print(secrets.token_hex(32))"
```
