from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.models import Document
from app.schemas.document import SearchResult, ChatResponse
import os


async def chat(query: str, db: Session) -> ChatResponse:
    """与文档对话"""
    try:
        # 获取所有文档
        documents = db.query(Document).all()
        
        # 简单的相关性计算：统计查询词在文档中出现的次数
        query_words = query.lower().split()
        scored_docs = []
        
        for doc in documents:
            if doc.content:
                content_lower = doc.content.lower()
                score = sum(1 for word in query_words if word in content_lower)
                if score > 0:
                    scored_docs.append((doc, score))
        
        # 按分数排序
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        
        # 构建回答
        answer_parts = []
        sources = []
        
        for doc, score in scored_docs[:3]:
            answer_parts.append(doc.content[:500] if len(doc.content) > 500 else doc.content)
            search_result = SearchResult(
                document_id=doc.id,
                filename=doc.filename,
                content=doc.content[:300] + "..." if len(doc.content) > 300 else doc.content,
                score=float(score),
                tags=[{"id": tag.id, "name": tag.name} for tag in doc.tags]
            )
            sources.append(search_result)
        
        if not answer_parts:
            return ChatResponse(answer="没有找到相关的文档信息。", sources=[])
        
        # 构建回答
        answer = "根据检索到的文档，以下是相关信息：\n\n"
        answer += "\n\n---\n\n".join(answer_parts)
        
        return ChatResponse(answer=answer, sources=sources)
    except Exception as e:
        print(f"聊天失败: {e}")
        return ChatResponse(answer="抱歉，处理您的请求时出现了错误。", sources=[])


async def update_vectorstore(db: Session):
    """更新向量数据库（现在是简单的内存索引）"""
    # 这个函数现在不需要做任何事情，因为我们现在使用简单的文本匹配
    pass
