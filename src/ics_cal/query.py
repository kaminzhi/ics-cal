import requests
from bs4 import BeautifulSoup


def fetch_events_by_keyword(year: int, keyword: str):
    """
    依年份抓取雲科大校務行事曆，並依關鍵字篩選事件。

    回傳: list[tuple[str, str]] => [(yyyy/mm/dd, description), ...]
    """
    url = f"https://events.yuntech.edu.tw/?&y={year}&view=YunTech&"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        events = soup.find_all('div', class_=['YunTech_calendar', 'YunTech_calendar_holiday'])

        results = []
        for event in events:
            date_el = event.find('div', class_='YunTech_calendar_date')
            desc_el = event.find('div', class_='YunTech_calendar_events')
            if not date_el or not desc_el:
                continue
            date = date_el.text.strip()
            description = desc_el.text.strip()
            if keyword in description:
                results.append((f"{year}/{date}", description))

        return results
    except requests.RequestException as e:
        print(f"請求失敗: {e}")
        return []


