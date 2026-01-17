# Holy Mail Bot 🕊️

這是一個用於自動生成聖經靈修郵件並定時發送的工具。它會從聖經 API 獲取隨機經文，並利用 LLM 生成深入的靈修感悟。

## 功能特點

- **自動獲取經文**：從聖經 API 隨機獲取多條經文。
- **AI 靈修生成**：使用 OpenAI 兼容的 API（如 DeepSeek）生成結構化的靈修內容。
- **定時發送**：支持設定時間間隔（如每 30 分鐘一封），自動持續運行。
- **副本發送**：郵件發送時會同時抄送（CC）給寄件人，方便留存。
- **HTML 格式**：優雅的 HTML 郵件格式，經文部分自動加框顯示。

## 快速開始

### 1. 環境準備

項目要求 Python 3.12+。推薦使用 `uv` 管理環境：

```bash
# 安裝依賴
uv sync
```

### 2. 配置環境變量

複製 `.env.example` 並重命名為 `.env`，然後填寫必要的配置：

```bash
cp .env.example .env
```

配置項說明：
- `smtp_server`: SMTP 服務器地址。
- `sender_mail`: 你的郵件地址。
- `sender_password`: 你的郵件授權碼或密碼。
- `recvicer_mail`: 收件人的郵件地址。
- `api_key`: OpenAI 兼容 API 的密鑰。
- `interval_minutes`: 發送時間間隔（單位：分鐘）。

### 3. 運行程序

```bash
# 使用 uv 運行
uv run main.py

# 或者直接運行
python main.py
```

## 項目結構

- `main.py`: 程序主入口，包含定時循環邏輯。
- `src/`: 源代碼目錄。
  - `bible.py`: 經文獲取邏輯。
  - `llm.py`: LLM 調用及 Prompt 處置。
  - `mail.py`: 郵件構造與發送邏輯。
  - `config.py`: 配置加載模塊。
- `prompts/`: 存放 LLM 角色的 Prompt 文件。

## 注意事項

- 請確保你的 SMTP 服務器已開啓授權發送。
- 若 API 調用失敗或網絡連接中斷，程序會記錄日誌並在下一個循環嘗試重新運行。