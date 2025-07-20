import requests
from bs4 import BeautifulSoup
import re
import json
import os
from dotenv import load_dotenv
import random
from datetime import datetime

load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

def fetch_html(url):
    resp = requests.get(url)
    resp.raise_for_status()            # 若 HTTP 回傳 4xx/5xx，則拋錯
    resp.encoding = 'utf-8'            # 明確指定編碼
    return resp.text

def save_html(html, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"已將 HTML 存為 {filename}")

def parse_module_to_json(html: str) -> dict:
    soup = BeautifulSoup(html, 'html.parser')
    module = soup.find('div', class_='module module-um md_style1')
    tables = module.select('div.table-responsive table')
    roles = ['boy', 'girl']
    result = {}

    for role, table in zip(roles, tables):
        mapping = {'gradNew': None, 'gradOld': None, 'undergradOld': None}
        for tr in table.find_all('tr'):
            label, value = [td.get_text(strip=True) for td in tr.find_all('td')]
            # 處理 '-' 或 空字串
            if value in ('', '-'):
                value = None
            if '研究所新生' in label:
                mapping['gradNew'] = value
            elif '研究所舊生' in label:
                mapping['gradOld'] = value
            elif '大學部舊生' in label:
                mapping['undergradOld'] = value
        result[role] = mapping

    # 擷取更新時間
    time_tag = module.find(string=re.compile(r'更新時間'))
    if time_tag:
        m = re.search(r'更新時間\s*([\d/]+)\s*(\d{1,2}:\d{2})', time_tag)
        if m:
            result['updateTime'] = f"{m.group(1)} {m.group(2)}"

    return result



def maid_notify(number: int, backend_time: str) -> dict:
    templates = [
        f"叩叩🔔 主人，小女僕來回報了✨\n目前候補號碼是 **{number}** 哦！\n請主人耐心等候💕 小女僕會隨時關注的📢",
        f"主人～💕 小女僕剛確認最新消息📢\n現在候補號碼來到 **{number}**！\n還請主人再稍候一會兒☕ 小女僕不會讓您錯過任何更新🔔",
        f"報告主人✨\n目前候補號碼已經到 **{number}** 了💌\n小女僕會乖乖繼續守著💕 等好消息一定馬上通知您📢",
        f"主人，我回來啦🔔\n剛剛確認了，目前候補號碼：**{number}**！\n請主人放心💕 進度小女僕會牢牢盯住的✨",
        f"主人💕 候補的進度又有變化📢\n目前已經到 **{number}** 了哦✨\n小女僕會一直陪伴主人等候☕",
        f"小女僕偷偷跑去查了一下🔔\n現在候補號碼是 **{number}**！\n希望很快能傳來好消息💕✨",
        f"主人，進度剛剛更新到 **{number}**📢\n別擔心💕 小女僕會乖乖守著🔔 直到候補成功為止✨",
        f"主人♡ 最新候補號碼是 **{number}**✨\n小女僕會幫主人牢牢記住📌 下一次也會馬上回報💌",
        f"報告報告🔔 候補進度更新：**{number}**✨\n主人請耐心☕ 剩下的就交給小女僕吧💕",
        f"進度來了📢 目前候補號碼：**{number}**！\n主人，喝杯茶☕ 休息一下💕 小女僕會幫您繼續盯著✨"
    ]
    
    message = random.choice(templates)

    # 兩個時間
    maid_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    footer_text = (
        f"候補名單更新時間：{backend_time}\n"
        f"小女僕回報時間：{maid_time}"
    )

    embed_payload = {
        "embeds": [
            {
                "title": "📢 女僕回報時間到啦！",
                "description": message,
                "color": 0xFFC0CB,  # 淡粉色
                "footer": {
                    "text": footer_text
                }
            }
        ]
    }
    return embed_payload

def send_discord_message(payload: dict):
    resp = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    resp.raise_for_status()

if __name__ == '__main__':
    url = 'https://utdormitory.utaipei.edu.tw/index.php'
    html = fetch_html(url)
    data = parse_module_to_json(html)
    print(data["updateTime"])
    message = maid_notify(data["boy"]["undergradOld"], data['updateTime'])
    send_discord_message(message)
