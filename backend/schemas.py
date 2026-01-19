from pydantic import BaseModel
from typing import List, Optional

# 技能结构
class Skill(BaseModel):
    name: str
    level: str
    type: str

# 读取用户信息时返回的结构
class UserDisplay(BaseModel):
    username: str
    title: str
    avatar_url: str
    level: int
    exp: int
    cash: float
    strength: int
    intelligence: int
    agility: int
    charm: int
    skills: List[Skill] = []

    class Config:
        from_attributes = True # 允许从 ORM 模型读取数据

# 登录时接收的结构
class Token(BaseModel):
    access_token: str
    token_type: str