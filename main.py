import asyncio
import logging
from src.bible import fetch_random_verses, format_verses_for_llm
from src.llm import generate_reflection
from src.mail import send_mail
from src.config import settings

# 設置日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def main():
    logging.info(f"Holy Mail Bot 已啟動，發送間隔：{settings.interval_minutes} 分鐘")
    
    while True:
        try:
            logging.info("開始獲取聖經經文...")
            verses = await fetch_random_verses(settings.quote_counts)
            if not verses:
                logging.error("未能獲取到任何經文。")
            else:
                verses_text = format_verses_for_llm(verses)
                logging.info("經文獲取成功，正在生成靈修感悟...")
                
                reflection = generate_reflection(verses_text)
                logging.info(f"感悟生成成功: {reflection['title']}")
                
                logging.info("正在發送郵件...")
                send_mail(reflection['title'], reflection['verse'], reflection['content'])
                logging.info("郵件發送完成！")
            
        except Exception as e:
            logging.error(f"執行過程中出錯: {e}")
        
        logging.info(f"等待 {settings.interval_minutes} 分鐘後進行下一次發送...")
        await asyncio.sleep(settings.interval_minutes * 60)

if __name__ == "__main__":
    asyncio.run(main())
