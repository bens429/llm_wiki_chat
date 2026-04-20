from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """应用配置"""
    # 数据库配置
    DATABASE_URL: str
    
    # 向量数据库配置
    CHROMA_DB_PATH: str = "./chromadb"
    
    # API配置
    API_KEY: str
    
    # OCR配置
    TESSERACT_CMD: str = "tesseract"
    
    # 模型配置
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    LLM_MODEL: str = "gpt-3.5-turbo"
    
    # 应用配置
    APP_NAME: str = "医疗知识库管理系统"
    APP_VERSION: str = "1.0.0"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# 创建全局配置实例
settings = Settings()
