"""AI News - RSS version: fetches 3 items from a public AI news RSS feed"""

import urllib.request
import xml.etree.ElementTree as ET
import re

RSS_URL = "https://feeds.feedburner.com/venturebeat/SZYF"  # VentureBeat AI feed

def strip_html(text):
    return re.sub(r"<[^>]+>", "", text or "").strip()

def fetch_ai_news(url, limit=3):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            xml_data = resp.read()
        root = ET.fromstring(xml_data)
        items = root.findall(".//item")[:limit]
        news = []
        for item in items:
            news.append({
                "title": strip_html(item.findtext("title")),
                "link": (item.findtext("link") or "").strip(),
                "date": item.findtext("pubDate", "")[:16],
            })
        return news
    except Exception as e:
        return [{"title": f"取得失敗: {e}", "link": "", "date": ""}]

news = fetch_ai_news(RSS_URL)

print("=" * 55)
print("  AI ニュース (RSS最新3件)")
print("=" * 55)
for i, item in enumerate(news, 1):
    print(f"\n[{i}] {item['title']}")
    if item["date"]:
        print(f"    日付: {item['date']}")
    if item["link"]:
        print(f"    URL: {item['link']}")
print("\n" + "=" * 55)
