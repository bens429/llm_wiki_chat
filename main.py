from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from app.core.config import settings
from app.core.database import engine, Base
from app.api import endpoints

# 加载环境变量
load_dotenv()

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 应用启动和关闭事件
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时执行
    print("Starting up...")
    yield
    # 关闭时执行
    print("Shutting down...")

# 创建FastAPI应用
app = FastAPI(
    title="医疗知识库管理系统",
    description="基于RAG的医疗体系知识库管理系统",
    version="1.0.0",
    lifespan=lifespan
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(endpoints.router, prefix="/api")

# 挂载静态文件
frontend_path = os.path.join(os.path.dirname(__file__), "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

# 前端页面路由
@app.get("/index.html")
async def frontend():
    index_path = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"error": "Frontend not found"}

# 根路径 - 重定向到前端
@app.get("/")
async def root():
    index_path = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "医疗知识库管理系统 API"}

# 健康检查
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
