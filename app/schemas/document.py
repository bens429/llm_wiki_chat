from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from app.core.models import FileType, Category


class TagBase(BaseModel):
    """标签基础模型"""
    name: str


class TagResponse(TagBase):
    """标签响应模型"""
    id: int
    
    class Config:
        from_attributes = True


class DocumentBase(BaseModel):
    """文档基础模型"""
    filename: str
    file_type: FileType
    category: Optional[Category] = None


class DocumentCreate(DocumentBase):
    """创建文档模型"""
    content: Optional[str] = None
    summary: Optional[str] = None
    keywords: Optional[str] = None


class DocumentResponse(DocumentBase):
    """文档响应模型"""
    id: int
    content: Optional[str] = None
    summary: Optional[str] = None
    keywords: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    tags: List[TagResponse] = []
    
    class Config:
        from_attributes = True


class SearchRequest(BaseModel):
    """搜索请求模型"""
    query: str


class SearchResult(BaseModel):
    """搜索结果模型"""
    document_id: int
    filename: str
    content: Optional[str] = None
    score: float
    tags: List[TagResponse] = []


class ChatRequest(BaseModel):
    """聊天请求模型"""
    query: str


class ChatResponse(BaseModel):
    """聊天响应模型"""
    answer: str
    sources: List[SearchResult] = []
