import httpx
import logging
from typing import List, Dict, Any
from .config import settings

async def fetch_random_verses(count: int = 3) -> List[Dict[str, Any]]:
    """
    從 Bible API 獲取隨機聖經經文
    """
    verses = []
    async with httpx.AsyncClient() as client:
        for _ in range(count):
            try:
                # 這裡假設 API 返回單個隨機經文
                response = await client.get(settings.bible_api, timeout=10.0)
                response.raise_for_status()
                data = response.json()
                # 根據 bible-api.com 的格式，通常包含 'random_verse' 或类似的結構
                # 這裡直接存儲原始數據，後續由 LLM 解析
                verses.append(data)
            except Exception as e:
                logging.error(f"獲取聖經經文失敗: {e}")
    return verses

def format_verses_for_llm(verses: List[Dict[str, Any]]) -> str:
    """
    將經文列表格式化為 LLM 可讀的字符串
    """
    formatted = []
    for i, v in enumerate(verses, 1):
        # 假設結構中包含 'verses' 列表或直接包含 'text' 和 'reference'
        # 具體取決於 cuv/random 的返回格式
        # 這裡做一個簡單的提取
        verse_data = v.get("random_verse", {})
        book = verse_data.get("book", "Unknown")
        chapter = verse_data.get("chapter", 0)
        verse_num = verse_data.get("verse", 0)
        text = verse_data.get("text", "No text found")
        
        formatted.append(f"選項 {i}:\n引用: {book} {chapter}:{verse_num}\n內容: {text}")
    
    return "\n\n".join(formatted)
