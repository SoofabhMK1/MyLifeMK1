# backend/database.py
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from pathlib import Path

# 加载 .env
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

# 获取数据库地址，如果没配置则给个默认值
# 注意：使用 postgresql+psycopg:// 指定使用 v3 驱动
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "myproject_db")

DATABASE_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

# 创建异步引擎
engine = create_async_engine(DATABASE_URL, echo=True)

# 创建会话工厂
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# 所有模型的基类
Base = declarative_base()

# 依赖注入函数：获取数据库会话
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session