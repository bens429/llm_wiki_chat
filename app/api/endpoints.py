from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.models import Document, Tag
from app.schemas import document as document_schemas
from app.services import file_processor, rag_service, search_service

router = APIRouter()


@router.post("/documents/upload", response_model=document_schemas.DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """上传文档"""
    try:
        # 处理文件
        document = await file_processor.process_file(file, db)
        return document
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/documents", response_model=List[document_schemas.DocumentResponse])
async def get_documents(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取文档列表"""
    query = db.query(Document)
    if category:
        query = query.filter(Document.category == category)
    documents = query.offset(skip).limit(limit).all()
    return documents


@router.get("/documents/{document_id}", response_model=document_schemas.DocumentResponse)
async def get_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    """获取单个文档"""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="文档不存在")
    return document


@router.post("/search", response_model=List[document_schemas.SearchResult])
async def search_documents(
    query: document_schemas.SearchRequest,
    db: Session = Depends(get_db)
):
    """搜索文档"""
    results = await search_service.search(query.query, db)
    return results


@router.post("/chat", response_model=document_schemas.ChatResponse)
async def chat_with_documents(
    query: document_schemas.ChatRequest,
    db: Session = Depends(get_db)
):
    """与文档对话"""
    response = await rag_service.chat(query.query, db)
    return response
