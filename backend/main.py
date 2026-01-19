import os
from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db, engine, Base
from models import Hero

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

@app.on_event("startup")
async def startup_event():
    # 这里的逻辑是：如果数据库里没有主角，就创建一个默认的
    async with engine.begin() as conn:
        # 生产环境通常不在这里创建表，而是靠 alembic，但开发环境为了保险可以留着
        # await conn.run_sync(Base.metadata.create_all) 
        pass

    async with AsyncSession(engine) as session:
        result = await session.execute(select(Hero))
        hero = result.scalars().first()
        if not hero:
            print("Creating default hero...")
            default_hero = Hero(
                name="ShadowSlayer",
                title="系统管理员",
                level=1,
                exp=0,
                cash=1000.0,
                avatar_url="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png",
                # JSON 数据直接存字典
                attributes=[
                    {"label": "力量 (STR)", "value": 10, "color": "#f56c6c"},
                    {"label": "智力 (INT)", "value": 10, "color": "#409eff"}
                ],
                skills=[
                    {"name": "Python 基础", "level": "Lv.1", "type": "info"}
                ]
            )
            session.add(default_hero)
            await session.commit()

# 修改：获取用户信息的接口
@app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    # 1. 查询数据库里的第一个 Hero
    result = await db.execute(select(Hero))
    hero = result.scalars().first()
    
    if not hero:
        return {"error": "No hero found"}
    
    # 2. 返回数据
    return {
        "username": hero.name,
        "title": hero.title,
        "level": hero.level,
        "exp": hero.exp,
        "avatarUrl": hero.avatar_url,
        "cash": hero.cash,
        "attributes": hero.attributes, # 数据库会自动把 JSON 转回 Python List/Dict
        "skills": hero.skills
    }

if __name__ == "__main__":
    import uvicorn
    # 启动服务，端口 8000
    import sys
    import asyncio

    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    uvicorn.run(app, host="0.0.0.0", port=8000)