import asyncio
import uvloop
import aiohttp
from bs4 import BeautifulSoup
import re

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

async def fetch_html(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            resp.raise_for_status()          # 若 HTTP 回傳 4xx/5xx，則拋錯
            return await resp.text()

def save_html(html, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"已將 {url} 的 HTML 存為 {filename}")

def parse_module_to_json(html: str) -> dict:
    soup = BeautifulSoup(html, 'html.parser')
    module = soup.find('div', class_='module module-um md_style1')

    # 抓出兩個表格
    tables = module.select('div.table-responsive table')
    roles = ['boy', 'girl']   # 對應「松苑」→ boy，「梅苑」→ girl
    result = {}

    for role, table in zip(roles, tables):
        # 取得每一列 (tr)
        mapping = {'gradNew': None, 'gradOld': None, 'undergradOld': None}
        for tr in table.find_all('tr'):
            cells = [td.get_text(strip=True) for td in tr.find_all('td')]
            label, value = cells
            # 將 '-' 或空字串當 None
            value = None if (value == '-' or value == '') else value
            if '研究所新生' in label:
                mapping['gradNew'] = value
            elif '研究所舊生' in label:
                mapping['gradOld'] = value
            elif '大學部舊生' in label:
                mapping['undergradOld'] = value
        result[role] = mapping

    # 抓更新時間
    time_text = module.find(text=re.compile(r'更新時間')).strip()
    m = re.search(r'更新時間\s*([\d/]+)\s*(\d{1,2}:\d{2})', time_text)
    if m:
        result['updateTime'] = f"{m.group(1)}-{m.group(2)}"

    return result

if __name__ == '__main__':
    url = 'https://utdormitory.utaipei.edu.tw/index.php'           # 請改成您要抓取的網址
    filename = 'html/page.html'                # 存檔名稱
    html_content = asyncio.run(fetch_html(url))
    save_html(html_content, filename)
    useful_content = parse_module_to_json(html_content)
    print(useful_content)


    # asyncio.run(save_html(url, filename))
