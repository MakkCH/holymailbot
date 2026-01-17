import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr
from .config import settings

def send_mail(subject: str, verse: str, content: str):
    """
    使用 SMTP 發送郵件，支持 HTML 格式，僅經文使用 Callout 和斜體
    """
    # 構造多部分郵件
    message = MIMEMultipart("alternative")
    
    # 設置寄件人，確保中文名稱正確編碼
    sender_encoded_name = Header(settings.sender_name, 'utf-8').encode()
    message['From'] = formataddr((sender_encoded_name, settings.sender_mail))
    message['To'] = settings.recvicer_mail
    message['Cc'] = settings.sender_mail
    message['Subject'] = Header(subject, 'utf-8')

    # HTML 模版 - 僅經文使用 Callout
    # 處理內容中的 ** 加粗
    formatted_content = content.replace('\n', '<br>').replace('**', '<b>').replace('**', '</b>')
    
    html_content = f"""
    <html>
    <body style="font-family: sans-serif; line-height: 1.6; color: #333; padding: 20px;">
        <div style="max-width: 600px;">
            <div style="background-color: #f0f2f5; border-left: 4px solid #ccd0d5; padding: 12px; margin-bottom: 20px; font-style: italic; color: #555;">
                {verse}
            </div>
            
            <div style="white-space: pre-wrap;">
                {formatted_content}
            </div>
            
            <p style="color: #888; font-size: 0.85em; margin-top: 40px; border-top: 1px solid #eee; padding-top: 10px;">
                <!--此郵件由 Holy Mail Bot 自動發送-->
            </p>
        </div>
    </body>
    </html>
    """

    # 添加純文本和 HTML 版本
    # 純文本版本合併經文與感悟
    plain_text = f"{verse}\n\n{content}"
    part1 = MIMEText(plain_text, "plain", "utf-8")
    part2 = MIMEText(html_content, "html", "utf-8")
    
    message.attach(part1)
    message.attach(part2)

    # 連接 SMTP 服務器並發送
    server = smtplib.SMTP(settings.smtp_server, settings.smtp_port)
    if settings.sender_password:
            server.login(settings.sender_mail, settings.sender_password)
    
    server.sendmail(settings.sender_mail, [settings.recvicer_mail, settings.sender_mail], message.as_string())
    server.quit()

