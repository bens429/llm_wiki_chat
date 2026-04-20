# 医疗知识库管理系统

基于RAG（检索增强生成）技术的医疗体系知识库管理系统，适用于企业、医院、单位等机构的文档管理和智能检索。

## 功能特性

### 📄 文档处理
- 支持多种文件格式：Word、PDF、扫描件、图片等
- 自动识别文字、提取关键信息
- OCR光学字符识别，支持从图片和扫描件中提取文字

### 🏷️ 智能管理
- 自动分类：医疗病历、规章制度、合同、红头文件、标书、技术手册等
- 自动打标签、归档
- 关键词提取

### 🔍 搜索功能
- 关键词检索
- 模糊搜索（支持半个关键词匹配）
- 相关性排序

### ✨ 文本处理
- 自动去重
- 文本纠错
- 摘要总结

### 💬 智能对话
- 基于文档内容的问答
- RAG检索增强生成

## 技术栈

### 后端
- **FastAPI** - 高性能Web框架
- **SQLite** - 轻量级数据库
- **Python** - 主要开发语言

### 文件处理
- **PyPDF2** - PDF文件处理
- **python-docx** - Word文件处理
- **Pillow** - 图片处理
- **pytesseract** - OCR文字识别
- **jieba** - 中文分词

### 前端
- **HTML5/CSS3** - 页面结构与样式
- **Bootstrap 5** - UI框架
- **Axios** - HTTP请求

## 项目结构

```
llm_wiki_chat/
├── app/
│   ├── api/
│   │   └── endpoints.py          # API接口定义
│   ├── core/
│   │   ├── config.py             # 配置管理
│   │   ├── database.py           # 数据库配置
│   │   └── models.py             # 数据模型
│   ├── schemas/
│   │   └── document.py           # 数据Schema
│   └── services/
│       ├── file_processor.py     # 文件处理服务
│       ├── ocr_service.py        # OCR服务
│       ├── rag_service.py        # RAG对话服务
│       ├── search_service.py     # 搜索服务
│       └── text_processor.py     # 文本处理服务
├── frontend/
│   └── index.html                # 前端界面
├── main.py                       # 应用入口
├── requirements.txt               # 依赖列表
└── .env                          # 环境变量配置
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

编辑 `.env` 文件，配置必要的参数：

```env
# API配置（用于聊天功能）
API_KEY=your_api_key_here

# 模型配置
EMBEDDING_MODEL=all-MiniLM-L6-v2
LLM_MODEL=gpt-3.5-turbo
```

### 3. 启动服务

```bash
uvicorn main:app --reload
```

服务启动后，访问：
- API地址：http://127.0.0.1:8000
- 前端界面：打开 `frontend/index.html` 文件

### 4. 使用API

#### 上传文档
```bash
curl -X POST "http://localhost:8000/api/documents/upload" \
  -F "file=@/path/to/document.pdf"
```

#### 获取文档列表
```bash
curl -X GET "http://localhost:8000/api/documents"
```

#### 搜索文档
```bash
curl -X POST "http://localhost:8000/api/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "医疗病历"}'
```

#### 与文档对话
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "关于糖尿病的诊疗流程"}'
```

## API接口

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/` | 根路径 |
| GET | `/health` | 健康检查 |
| POST | `/api/documents/upload` | 上传文档 |
| GET | `/api/documents` | 获取文档列表 |
| GET | `/api/documents/{id}` | 获取单个文档 |
| POST | `/api/search` | 搜索文档 |
| POST | `/api/chat` | 与文档对话 |

## 使用说明

### 1. 上传文档
点击上传区域或拖拽文件到此处，支持批量上传。

### 2. 查看文档
在文档列表中点击任意文档查看详情，包括摘要、关键词、标签等。

### 3. 搜索文档
- 在搜索框中输入关键词
- 支持模糊搜索，即使只记得半个词也能搜到
- 搜索结果按相关性排序

### 4. 智能对话
在聊天区域输入问题，系统会从已上传的文档中检索相关信息并回答。

## 注意事项

1. **OCR功能**：使用pytesseract进行OCR识别，需要安装Tesseract OCR引擎
2. **聊天功能**：需要配置OpenAI API Key才能使用完整的LLM对话功能
3. **向量搜索**：默认使用简单文本匹配，如需向量语义搜索需配置embedding模型

## 许可证

MIT License
