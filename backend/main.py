import os
from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# 1. 加载环境变量
# 获取当前文件(main.py)的父目录的父目录，也就是项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent
# 加载根目录下的 .env 文件
load_dotenv(dotenv_path=BASE_DIR / ".env")

app = FastAPI()

# 2. 配置 CORS (解决跨域问题)
# 前端通常运行在 localhost:5173 (Vite默认端口)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 定义 OAuth2 模式，tokenUrl 指向获取 token 的接口路径
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 3. 登录接口 /token
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # 从环境变量读取正确的用户名和密码
    correct_username = os.getenv("ADMIN_USER")
    correct_password = os.getenv("ADMIN_PASSWORD")

    # 验证账号密码
    if form_data.username != correct_username or form_data.password != correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 登录成功，返回 token (这里演示返回简单的 bearer token)
    return {"access_token": form_data.username, "token_type": "bearer"}

# 4. 一个受保护的测试接口（可选，用于测试登录后获取数据）
@app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    return {"user": token, "message": "欢迎进入主页！"}

if __name__ == "__main__":
    import uvicorn
    # 启动服务，端口 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)