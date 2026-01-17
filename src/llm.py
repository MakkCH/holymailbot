import openai
from typing import Dict
from .config import settings

def get_llm_client() -> openai.OpenAI:
    """
    獲取 OpenAI 客戶端實例
    """
    return openai.OpenAI(
        api_key=settings.api_key,
        base_url=settings.base_url
    )

def generate_reflection(verses_text: str) -> Dict[str, str]:
    """
    調用 LLM 生成郵件內容、標題和選定的經文
    """
    client = get_llm_client()
    
    # 讀取 prompt 模板
    with open(settings.prompt_file, 'r', encoding='utf-8') as f:
        prompt_template = f.read()
    
    # 填充佔位符
    user_prompt = prompt_template.format(
        sender_name=settings.sender_real_name,
        receiver_name=settings.recvicer_real_name,
        verses=verses_text
    )
    
    response = client.chat.completions.create(
        model=settings.model_id,
        messages=[
            {"role": "system", "content": "你是一名資深的基督徒學生，擅長分享聖經感悟並用繁體中文寫作。"},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7
    )
    
    full_text = response.choices[0].message.content
    
    # 解析標題、經文和內容
    title = "每日靈修"
    verse = ""
    content = full_text
    
    lines = full_text.split('\n')
    for line in lines:
        if line.startswith("TITLE:"):
            title = line.replace("TITLE:", "").strip()
        elif line.startswith("VERSE:"):
            verse = line.replace("VERSE:", "").strip()
        elif line.startswith("CONTENT:"):
            # 獲取 CONTENT 之後的所有內容
            content = full_text.split("CONTENT:")[1].strip()
            break
            
    return {"title": title, "verse": verse, "content": content}
