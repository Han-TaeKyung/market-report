import os, requests, json
from datetime import datetime

TOKEN = os.environ["NOTION_TOKEN"]
DB_ID = os.environ["NOTION_DATABASE_ID"]
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# 오늘 날짜 기준 가장 최신 보고서 가져오기
res = requests.post(
    f"https://api.notion.com/v1/databases/{DB_ID}/query",
    headers=HEADERS,
    json={"sorts": [{"property": "생성일시", "direction": "descending"}], "page_size": 1}
)
pages = res.json().get("results", [])
if not pages:
    print("보고서 없음 — 건너뜀")
    exit(0)

page = pages[0]
props = page["properties"]

# HTML코드 필드에서 내용 추출
html_blocks = props.get("HTML코드", {}).get("rich_text", [])
html = "".join(b["plain_text"] for b in html_blocks)

if not html:
    print("HTML 내용 없음 — 건너뜀")
    exit(0)

today = datetime.now().strftime("%Y%m%d")
os.makedirs("archive", exist_ok=True)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

with open(f"archive/{today}.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"배포 완료: {today}")
