from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    """
    項目配置類，自動從 .env 文件加載環境變量
    """
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    # SMTP 設置
    smtp_server: str
    smtp_port: int
    
    # 寄件人設置
    sender_mail: str
    sender_name: str
    sender_password: str
    
    # 收件人設置
    recvicer_mail: str

    # 寄件人與收件人真實姓名
    sender_real_name: str
    recvicer_real_name: str
    cc_mail: str
    
    # OpenAI API 設置
    api_key: str
    base_url: str
    model_id: str
    
    # Prompt 與 API 設置
    prompt_file: Path
    bible_api: str = "https://bible-api.com/data/cuv/random"
    quote_counts: int = 3
    interval_minutes: float = 30

# 全局配置實例
settings = Settings()
