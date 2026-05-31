"""AI News - Static version: shows 3 fixed AI news items"""

news = [
    {
        "title": "OpenAI、GPT-5を正式発表",
        "summary": "OpenAIは次世代モデルGPT-5を発表。推論能力が大幅に向上し、複雑な数学問題も解けるようになった。",
        "date": "2026-05-30",
    },
    {
        "title": "Google DeepMind、新しいロボットAIを公開",
        "summary": "DeepMindが人間の動作を模倣するロボット制御AIを公開。家庭内タスクをこなせる汎用性が注目を集めている。",
        "date": "2026-05-29",
    },
    {
        "title": "日本政府、AI規制法案を閣議決定",
        "summary": "日本政府は高リスクAIシステムへの規制を盛り込んだ法案を閣議決定。2027年施行を目指す。",
        "date": "2026-05-28",
    },
]

print("=" * 50)
print("  AI ニュース (本日のトップ3)")
print("=" * 50)
for i, item in enumerate(news, 1):
    print(f"\n[{i}] {item['title']}")
    print(f"    日付: {item['date']}")
    print(f"    {item['summary']}")
print("\n" + "=" * 50)
