import asyncio
import uvloop
import aiohttp

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

def parse_module(html: str) -> dict:
    soup = BeautifulSoup(html, 'lxml')
    result = {}

    # 找到「松苑」和「梅苑」標題
    titles = [span.get_text(strip=True) for span in soup.select('div.meditor > div > div > span strong')]
    # 找到對應的 table 區塊
    tables = soup.select('div.table-responsive table')

    for title, table in zip(titles, tables):
        rows = []
        for tr in table.select('tr'):
            cols = [td.get_text(strip=True) for td in tr.select('td')]
            if len(cols) == 2:
                rows.append({
                    '身份': cols[0],
                    '名額/順位': cols[1]
                })
        result[title] = rows

    # 解析更新時間
    time_text = soup.find(text=re.compile(r'更新時間')).strip()
    # 例如 "更新時間 114/06/26 15:55"
    m = re.search(r'更新時間\s*([\d/]+)\s*([\d:]+)', time_text)
    if m:
        result['更新時間'] = f"{m.group(1)} {m.group(2)}"

    return result

if __name__ == '__main__':
    url = 'https://utdormitory.utaipei.edu.tw/index.php'           # 請改成您要抓取的網址
    filename = 'page.html'                # 存檔名稱
    html_content = asyncio.run(fetch_html(url))
    save_html(html_content, filename)
    useful_content = parse_module(html_content)
    print(useful_content)

    # asyncio.run(save_html(url, filename))
