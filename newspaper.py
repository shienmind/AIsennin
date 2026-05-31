"""AI新聞 - ターミナル新聞紙面スタイル"""

import textwrap
from datetime import date

WIDTH = 72

news = [
    {
        "category": "産業",
        "title": "OpenAI、GPT-5を正式発表　推論能力が飛躍的に向上",
        "body": (
            "OpenAIは最新モデル「GPT-5」を正式に発表した。従来モデルと比較して"
            "推論能力が大幅に向上しており、複雑な数学・科学問題においても人間の"
            "専門家に匹敵する精度を示した。API提供は来月より段階的に開始される予定。"
        ),
        "date": "2026年5月30日",
        "reporter": "編集部",
    },
    {
        "category": "研究",
        "title": "DeepMind、家庭用ロボットAI公開　汎用動作制御を実現",
        "body": (
            "Google DeepMindは人間の動作を高精度で模倣するロボット制御AIを公開した。"
            "料理・掃除・物品整理など多様な家庭内タスクを単一モデルでこなせる汎用性が"
            "注目を集めており、商用化に向けた実証実験が複数の家電メーカーと進行中だ。"
        ),
        "date": "2026年5月29日",
        "reporter": "科学技術部",
    },
    {
        "category": "政策",
        "title": "AI規制法案を閣議決定　高リスク系に審査義務",
        "body": (
            "日本政府は高リスクAIシステムへの第三者審査義務を盛り込んだ「AI安全確保法案」"
            "を閣議決定した。医療・金融・インフラ分野への導入には事前の適合性評価が必須となり、"
            "違反企業には最大1億円の罰則が科される。法案は2027年4月の施行を目指す。"
        ),
        "date": "2026年5月28日",
        "reporter": "政治部",
    },
]

CYAN  = "\033[96m"
BOLD  = "\033[1m"
DIM   = "\033[2m"
RESET = "\033[0m"
YELLOW = "\033[93m"
WHITE  = "\033[97m"

def hr(char="─"):
    return char * WIDTH

def center(text, char=" "):
    return text.center(WIDTH, char)

def char_width(c):
    cp = ord(c)
    # CJK and fullwidth characters count as 2
    if (0x1100 <= cp <= 0x115F or 0x2E80 <= cp <= 0x9FFF or
            0xA000 <= cp <= 0xA4CF or 0xAC00 <= cp <= 0xD7AF or
            0xF900 <= cp <= 0xFAFF or 0xFE10 <= cp <= 0xFE1F or
            0xFE30 <= cp <= 0xFE4F or 0xFF00 <= cp <= 0xFF60 or
            0xFFE0 <= cp <= 0xFFE6 or 0x1F300 <= cp <= 0x1F9FF):
        return 2
    return 1

def str_width(s):
    return sum(char_width(c) for c in s)

def wrap_body(text, indent=2):
    limit = WIDTH - indent
    lines, cur, cur_w = [], [], 0
    for ch in text:
        w = char_width(ch)
        if cur_w + w > limit:
            lines.append("".join(cur))
            cur, cur_w = [], 0
        cur.append(ch)
        cur_w += w
    if cur:
        lines.append("".join(cur))
    return "\n".join(" " * indent + l for l in lines)

today = date.today().strftime("%Y年%-m月%-d日（%A）").replace(
    "Monday","月曜").replace("Tuesday","火曜").replace("Wednesday","水曜"
    ).replace("Thursday","木曜").replace("Friday","金曜"
    ).replace("Saturday","土曜").replace("Sunday","日曜")

output = []

# ─── ヘッダー ───────────────────────────────────────────────
output.append(hr("━"))
output.append(BOLD + CYAN + center("  ██████  AI  新  聞  ██████  ") + RESET)
output.append(DIM  + center(f"〔 {today} 〕  第 1 号  定価：無料") + RESET)
output.append(hr("━"))
output.append("")

# ─── 記事ループ ─────────────────────────────────────────────
for i, item in enumerate(news):
    # カテゴリバッジ＋見出し
    badge = f"【{item['category']}】"
    output.append(YELLOW + BOLD + badge + RESET + BOLD + WHITE + f" {item['title']}" + RESET)
    output.append(DIM + f"  {item['date']}　{item['reporter']}" + RESET)
    output.append("")
    output.append(wrap_body(item["body"]))
    output.append("")

    if i < len(news) - 1:
        output.append(DIM + hr("┄") + RESET)
        output.append("")

# ─── フッター ───────────────────────────────────────────────
output.append(hr("━"))
output.append(DIM + center("AI新聞　©2026 AIsennin編集部　無断転載禁止") + RESET)
output.append(hr("━"))

print("\n".join(output))
