import re
from typing import Optional
from app.core.models import Category


def process_text(text: str) -> str:
    """处理文本，包括去重、纠错等"""
    # 去除多余空白
    text = re.sub(r'\s+', ' ', text).strip()
    
    # 简单的去重处理
    sentences = text.split('. ')
    seen = set()
    unique_sentences = []
    for sentence in sentences:
        if sentence not in seen:
            seen.add(sentence)
            unique_sentences.append(sentence)
    text = '. '.join(unique_sentences)
    
    return text


def generate_summary(text: str) -> str:
    """生成文本摘要"""
    try:
        # 简单的摘要生成逻辑：取前3句话或前200字符
        sentences = text.split('。')
        if len(sentences) > 3:
            summary = '。'.join(sentences[:3]) + '。'
        else:
            summary = text
        
        # 如果摘要过长，截断
        if len(summary) > 200:
            summary = summary[:200] + '...'
        
        return summary
    except Exception as e:
        print(f"生成摘要失败: {e}")
        return text[:200] + "..." if len(text) > 200 else text


def extract_keywords(text: str) -> str:
    """提取关键词"""
    # 简单的关键词提取逻辑
    # 实际应用中可以使用更复杂的NLP模型
    import jieba
    from collections import Counter
    
    # 分词
    words = jieba.cut(text)
    
    # 过滤停用词
    stop_words = set(["的", "了", "在", "是", "我", "有", "和", "就", "不", "人", "都", "一", "一个", "上", "也", "很", "到", "说", "要", "去", "你", "会", "着", "没有", "看", "好", "自己", "这"])
    filtered_words = [word for word in words if word not in stop_words and len(word) > 1]
    
    # 统计词频
    word_counts = Counter(filtered_words)
    
    # 取前10个关键词
    top_keywords = [word for word, _ in word_counts.most_common(10)]
    
    return ','.join(top_keywords)


def categorize_document(text: str) -> Category:
    """分类文档"""
    # 简单的分类逻辑
    # 实际应用中可以使用更复杂的机器学习模型
    text_lower = text.lower()
    
    if any(keyword in text_lower for keyword in ["病历", "诊断", "治疗", "患者"]):
        return Category.MEDICAL_RECORD
    elif any(keyword in text_lower for keyword in ["制度", "规定", "章程", "办法"]):
        return Category.REGULATION
    elif any(keyword in text_lower for keyword in ["合同", "协议", "条款"]):
        return Category.CONTRACT
    elif any(keyword in text_lower for keyword in ["红头文件", "通知", "决定"]):
        return Category.RED_DOCUMENT
    elif any(keyword in text_lower for keyword in ["标书", "投标", "招标"]):
        return Category.BID_DOCUMENT
    elif any(keyword in text_lower for keyword in ["技术", "手册", "指南", "说明"]):
        return Category.TECHNICAL_MANUAL
    else:
        return Category.OTHER
