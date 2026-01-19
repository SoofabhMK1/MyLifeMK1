# backend/models.py
from sqlalchemy import Column, Integer, String, Float, JSON
from database import Base

class Hero(Base):
    __tablename__ = "heroes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)   # 角色名
    title = Column(String)                  # 称号
    level = Column(Integer, default=1)      # 等级
    exp = Column(Integer, default=0)        # 经验值
    avatar_url = Column(String)             # 头像链接
    cash = Column(Float, default=0.0)       # 现金
    
    # --- 核心灵活性设计 ---
    # attributes 存放: {"力量": 85, "智力": 90, "魅力": 10}
    # 以后想加 "幸运" 或 "精神"，直接往 JSON 里写，不用改表结构
    attributes = Column(JSON, default=dict) 
    
    # skills 存放: [{"name": "Python", "level": "Lv.5", "type": "success"}]
    skills = Column(JSON, default=list)