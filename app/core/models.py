from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.core.database import Base


class FileType(str, enum.Enum):
    """文件类型枚举"""
    WORD = "word"
    PDF = "pdf"
    IMAGE = "image"
    SCAN = "scan"
    OTHER = "other"


class Category(str, enum.Enum):
    """文件分类枚举"""
    MEDICAL_RECORD = "medical_record"
    REGULATION = "regulation"
    CONTRACT = "contract"
    RED_DOCUMENT = "red_document"
    BID_DOCUMENT = "bid_document"
    TECHNICAL_MANUAL = "technical_manual"
    OTHER = "other"


class Document(Base):
    """文档模型"""
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_type = Column(Enum(FileType), nullable=False)
    category = Column(Enum(Category), nullable=True)
    content = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    keywords = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联标签
    tags = relationship("Tag", secondary="document_tags", back_populates="documents")


class Tag(Base):
    """标签模型"""
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    
    # 关联文档
    documents = relationship("Document", secondary="document_tags", back_populates="tags")


# 文档标签关联表
from sqlalchemy import Table

document_tags = Table(
    "document_tags",
    Base.metadata,
    Column("document_id", Integer, ForeignKey("documents.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True)
)
