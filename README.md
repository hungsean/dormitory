# 臺北市立大學宿舍候補狀態通知

這是一個 Python 腳本，可以自動抓取臺北市立大學學生宿舍的候補網頁，並透過 Discord Webhook 發送最新的候補人數通知。

## 功能

* 自動爬取並解析最新的宿舍候補人數。
* 支援研究所與大學部的男生、女生候補狀態。
* 透過 Discord Webhook，以「女僕小幫手」的風格發送即時通知。
* 可彈性設定要關注的候補對象。

## 安裝與設定

1. **複製專案**

    ```bash
    git clone https://github.com/your-username/your-repository-name.git
    cd your-repository-name
    ```

2. **安裝依賴**
    本專案使用 [uv](https://github.com/astral-sh/uv) 作為套件管理工具。

    ```bash
    uv sync
    ```

    或者，如果您使用 `pip`：

    ```bash
    pip install -r requirements.txt
    ```

    *依賴套件*
    * `beautifulsoup4`
    * `python-dotenv`
    * `requests`

3. **設定環境變數**
    複製 `.env.example` 並重新命名為 `.env`：

    ```bash
    cp .env.example .env
    ```

    然後在 `.env` 檔案中填入您的 Discord Webhook URL：

    ```env
    DISCORD_WEBHOOK_URL="YOUR_DISCORD_WEBHOOK_URL"
    ```

## 使用方法

直接執行 `main.py` 即可。

```bash
python main.py
```

您可以修改 `main.py` 中的 `if __name__ == '__main__':` 區塊，來指定您想關注的候補對象，例如 `data["girl"]["gradNew"]` 代表研究所新生女生的候補。

## 授權

本專案採用 [MIT License](LICENSE) 授權。
