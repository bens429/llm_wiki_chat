from PIL import Image
import pytesseract
import os
from app.core.config import settings


# 设置tesseract命令路径
if settings.TESSERACT_CMD:
    pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD


def extract_text_from_image(image_path: str) -> str:
    """从图片中提取文本"""
    try:
        # 打开图片
        image = Image.open(image_path)
        
        # 使用OCR提取文本
        text = pytesseract.image_to_string(image, lang='chi_sim+eng')
        
        return text
    except Exception as e:
        print(f"OCR提取失败: {e}")
        return ""
