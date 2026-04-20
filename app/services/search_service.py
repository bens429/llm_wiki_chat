from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.core.models import Document
from app.schemas.document import SearchResult


async def search(query: str, db: Session) -> List[SearchResult]:
    """搜索文档"""
    # 基于关键词的数据库搜索
    documents = db.query(Document).filter(
        or_(
            Document.filename.ilike(f"%{query}%"),
            Document.content.ilike(f"%{query}%"),
            Document.keywords.ilike(f"%{query}%")
        )
    ).all()
    
    # 简单的相关性计算
    query_words = query.lower().split()
    scored_docs = []
    
    for doc in documents:
        if doc.content:
            content_lower = doc.content.lower()
            score = sum(1 for word in query_words if word in content_lower)
            scored_docs.append((doc, float(score)))
        else:
            scored_docs.append((doc, 0.0))
    
    # 按分数排序
    scored_docs.sort(key=lambda x: x[1], reverse=True)
    
    # 构建结果
    results = []
    for doc, score in scored_docs[:20]:
        search_result = SearchResult(
            document_id=doc.id,
            filename=doc.filename,
            content=doc.content[:300] + "..." if doc.content and len(doc.content) > 300 else (doc.content or ""),
            score=score,
            tags=[{"id": tag.id, "name": tag.name} for tag in doc.tags]
        )
        results.append(search_result)
    
    return results
