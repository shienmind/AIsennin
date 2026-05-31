"""AI SECURITY FEED - Cyberpunk terminal newspaper for AI security engineers"""

import time
import sys
import random
from datetime import datetime, timezone

# ── ANSI palette ──────────────────────────────────────────────────────────────
R  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
BLINK  = "\033[5m"

# Foreground
G0  = "\033[38;5;22m"    # deep green
G1  = "\033[38;5;34m"    # green
G2  = "\033[38;5;40m"    # bright green
G3  = "\033[38;5;82m"    # lime
CY  = "\033[38;5;51m"    # cyan
AQ  = "\033[38;5;87m"    # aqua highlight
YL  = "\033[38;5;226m"   # yellow
OR  = "\033[38;5;208m"   # orange
RD  = "\033[38;5;196m"   # red
MG  = "\033[38;5;198m"   # magenta
WH  = "\033[38;5;255m"   # near-white
GR  = "\033[38;5;240m"   # grey

# Background
BG  = "\033[48;5;232m"   # near-black bg (applied to header bar)

W = 76  # terminal width

# ── helpers ───────────────────────────────────────────────────────────────────
def char_width(c):
    cp = ord(c)
    if (0x1100 <= cp <= 0x115F or 0x2E80 <= cp <= 0x9FFF or
            0xA000 <= cp <= 0xA4CF or 0xAC00 <= cp <= 0xD7AF or
            0xF900 <= cp <= 0xFAFF or 0xFE10 <= cp <= 0xFE1F or
            0xFE30 <= cp <= 0xFE4F or 0xFF00 <= cp <= 0xFF60 or
            0xFFE0 <= cp <= 0xFFE6):
        return 2
    return 1

def str_w(s):
    # visible width ignoring ANSI escapes
    import re
    plain = re.sub(r'\033\[[0-9;]*m', '', s)
    return sum(char_width(c) for c in plain)

def pad_right(s, total):
    """Pad string s (which may contain ANSI codes) to total visible width."""
    return s + " " * max(0, total - str_w(s))

def jline(text, width=W - 4, indent=0):
    """Word-wrap Japanese/ASCII mixed text to given visible width."""
    limit = width - indent
    lines, cur, cur_w = [], [], 0
    for ch in text:
        w = char_width(ch)
        if cur_w + w > limit:
            lines.append(" " * indent + "".join(cur))
            cur, cur_w = [], 0
        cur.append(ch)
        cur_w += w
    if cur:
        lines.append(" " * indent + "".join(cur))
    return lines

def box_line(inner, left="│ ", right=" │", fill=" "):
    """Render a single line inside the box border."""
    content_w = W - len(left) - len(right)
    plain_inner = inner
    import re
    plain_only = re.sub(r'\033\[[0-9;]*m', '', plain_inner)
    vis_w = sum(char_width(c) for c in plain_only)
    padding = max(0, content_w - vis_w)
    return G1 + left + R + plain_inner + " " * padding + G1 + right + R

def hbar(left="├", mid="─", right="┤", accent=None):
    inner = mid * (W - 2)
    if accent:
        # insert accent text centred
        import re
        label = accent
        label_w = sum(char_width(c) for c in re.sub(r'\033\[[0-9;]*m','',label))
        pad = (W - 2 - label_w) // 2
        inner = mid * pad + label + mid * (W - 2 - pad - label_w)
    return G1 + left + inner + right + R

def top_bar():
    return G1 + "╔" + "═" * (W - 2) + "╗" + R

def bot_bar():
    return G1 + "╚" + "═" * (W - 2) + "╝" + R

def mid_heavy(label=""):
    if label:
        import re
        lw = sum(char_width(c) for c in re.sub(r'\033\[[0-9;]*m','',label))
        pad = (W - 2 - lw) // 2
        inner = "═" * pad + label + "═" * (W - 2 - pad - lw)
    else:
        inner = "═" * (W - 2)
    return G1 + "╠" + inner + "╣" + R

def side(content=""):
    return G1 + "║" + R + content + G1 + "║" + R

def empty_row():
    return side(" " * (W - 2))

# ── THREAT LEVEL badge ────────────────────────────────────────────────────────
THREAT = {
    "CRITICAL": RD  + BOLD + "● CRITICAL" + R,
    "HIGH":     OR  + BOLD + "▲ HIGH    " + R,
    "MEDIUM":   YL  + BOLD + "◆ MEDIUM  " + R,
    "LOW":      G2  + BOLD + "▼ LOW     " + R,
    "INFO":     CY  + BOLD + "ℹ INFO    " + R,
}

CVE_COLORS = {
    "CRITICAL": RD, "HIGH": OR, "MEDIUM": YL, "LOW": G2, "INFO": CY,
}

# ── NEWS DATA ─────────────────────────────────────────────────────────────────
news = [
    {
        "id":       "AISEC-2026-0531-001",
        "threat":   "HIGH",
        "tag":      "ADVERSARIAL · LLM",
        "title":    "GPT-5 Jailbreak手法「ShadowPrompt v3」が公開――FewShot注入でガードレール突破",
        "body": (
            "セキュリティ研究者グループ Redacted Labsは、OpenAI GPT-5に対する新型プロンプト"
            "インジェクション「ShadowPrompt v3」を公開した。Few-Shot例示をシステムプロンプト"
            "境界付近に埋め込む手法で、安全フィルタのバイパス成功率は実験環境で約67%に達した。"
            "OpenAIはパッチ対応中と声明を発表。RAGパイプライン経由の二次汚染にも注意が必要。"
        ),
        "mitre":    "AML.T0054.002",
        "ioc":      "system_prompt injection / few-shot poisoning",
        "source":   "Redacted Labs Advisory RL-2026-319",
        "date":     "2026-05-30 09:14 UTC",
    },
    {
        "id":       "AISEC-2026-0531-002",
        "threat":   "CRITICAL",
        "tag":      "SUPPLY CHAIN · MLOps",
        "title":    "HuggingFace Hub で悪意あるPickleモデルが配布――推定8,000件以上ダウンロード",
        "body": (
            "HuggingFace公式リポジトリにて、正規モデルに偽装したPickle形式の悪意あるファイル"
            "が複数検出された。ロード時にリバースシェルを生成するコードが埋め込まれており、"
            "ML開発者の環境に直接侵入できる。safetensors形式への移行とscanpy/picklescanによる"
            "静的解析が推奨される。影響を受けたモデルIDはAdvisory参照。"
        ),
        "mitre":    "AML.T0010",
        "ioc":      "pickle deserialization RCE / HuggingFace repo: [REDACTED]",
        "source":   "HF Security Bulletin HF-SEC-2026-88",
        "date":     "2026-05-29 23:51 UTC",
    },
    {
        "id":       "AISEC-2026-0531-003",
        "threat":   "MEDIUM",
        "tag":      "POLICY · GOVERNANCE",
        "title":    "日本「AI安全確保法」閣議決定――高リスクAIに第三者監査義務・罰則最大1億円",
        "body": (
            "日本政府は高リスクAIシステム（医療・金融・重要インフラ）への第三者適合性評価を"
            "義務付ける「AI安全確保法案」を閣議決定した。レッドチーム試験・インシデント報告・"
            "モデルカード開示が義務化され、違反企業には最大1億円の行政罰が科される。"
            "2027年4月施行予定。セキュリティ評価フレームワークはIPAが策定を主導する。"
        ),
        "mitre":    "N/A",
        "ioc":      "N/A",
        "source":   "内閣府 AI政策室 Press Release 2026-05-28",
        "date":     "2026-05-28 10:00 JST",
    },
]

# ── RENDER ────────────────────────────────────────────────────────────────────
now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
session_id = f"0x{random.randint(0xA000, 0xFFFF):04X}"

out = []

# ══ TOP HEADER ════════════════════════════════════════════════════════════════
out.append(top_bar())

# ASCII art title — compressed to fit W=76
title_art = [
    r" █████╗ ██╗    ███████╗███████╗ ██████╗",
    r"██╔══██╗██║    ██╔════╝██╔════╝██╔════╝",
    r"███████║██║    ███████╗█████╗  ██║     ",
    r"██╔══██║██║    ╚════██║██╔══╝  ██║     ",
    r"██║  ██║██║    ███████║███████╗╚██████╗",
    r"╚═╝  ╚═╝╚═╝    ╚══════╝╚══════╝ ╚═════╝",
]
sub_art  = G3 + BOLD + "  N E W S F E E D   //   A I   T H R E A T   I N T E L L I G E N C E" + R
tagline  = GR + DIM  + f"  SESSION {session_id}  ▸  {now_utc}  ▸  CLASSIFICATION: TLP:WHITE" + R

for row in title_art:
    padded = G2 + BOLD + row.ljust(W - 2) + R
    out.append(G1 + "║" + R + padded + G1 + "║" + R)

out.append(empty_row())
out.append(side(sub_art  + " " * max(0, W - 2 - str_w(sub_art))))
out.append(side(tagline  + " " * max(0, W - 2 - str_w(tagline))))
out.append(empty_row())

# ══ ARTICLES ══════════════════════════════════════════════════════════════════
for idx, item in enumerate(news):
    tc = CVE_COLORS.get(item["threat"], WH)
    threat_badge = tc + BOLD + f"[{item['threat']:^8}]" + R
    tag_str      = AQ + f"  ▸ {item['tag']}" + R
    id_str       = GR + DIM + f"  ID:{item['id']}" + R

    # section divider
    label = G2 + BOLD + f" ◢ ALERT {idx+1:02d} / {len(news):02d} " + R
    out.append(mid_heavy(label))
    out.append(empty_row())

    # threat + tag row
    row1 = threat_badge + tag_str
    out.append(side(" " + row1 + " " * max(0, W - 2 - 1 - str_w(row1))))
    out.append(side(" " + id_str + " " * max(0, W - 2 - 1 - str_w(id_str))))
    out.append(empty_row())

    # title
    title_lines = jline(item["title"], width=W - 4, indent=0)
    for tl in title_lines:
        tl_colored = WH + BOLD + tl + R
        out.append(side("  " + tl_colored + " " * max(0, W - 4 - str_w(tl_colored))))

    out.append(empty_row())
    out.append(G1 + "║" + GR + DIM + "  " + "·" * (W - 6) + "  " + R + G1 + "║" + R)
    out.append(empty_row())

    # body
    body_lines = jline(item["body"], width=W - 6, indent=0)
    for bl in body_lines:
        bl_dim = GR + bl + R
        out.append(side("   " + bl_dim + " " * max(0, W - 5 - str_w(bl_dim))))

    out.append(empty_row())

    # metadata strip
    mitre_s  = YL  + f" MITRE: {item['mitre']}" + R
    ioc_s    = OR  + f"  IOC: {item['ioc']}" + R
    date_s   = GR  + DIM + f"  {item['date']}" + R
    src_s    = G2  + DIM + f"  SRC: {item['source']}" + R

    mitre_lines = jline(f"MITRE: {item['mitre']}", width=W - 6, indent=0)
    ioc_lines   = jline(f"IOC:   {item['ioc']}",   width=W - 6, indent=0)
    src_lines   = jline(f"SRC:   {item['source']}", width=W - 6, indent=0)

    out.append(G1 + "║" + G0 + "  " + "─" * (W - 6) + "  " + R + G1 + "║" + R)
    for ml in mitre_lines:
        s = "  " + YL + ml + R
        out.append(side(s + " " * max(0, W - 2 - str_w(s))))
    for il in ioc_lines:
        s = "  " + OR + il + R
        out.append(side(s + " " * max(0, W - 2 - str_w(s))))
    for sl in src_lines:
        s = "  " + G2 + DIM + sl + R
        out.append(side(s + " " * max(0, W - 2 - str_w(s))))

    ds = "  " + GR + DIM + f"DATE:  {item['date']}" + R
    out.append(side(ds + " " * max(0, W - 2 - str_w(ds))))
    out.append(empty_row())

# ══ FOOTER ════════════════════════════════════════════════════════════════════
footer_label = G2 + BOLD + " ◢ SYSTEM STATUS " + R
out.append(mid_heavy(footer_label))
out.append(empty_row())

status_items = [
    (G2,  "FEED",    "LIVE"),
    (YL,  "TLP",     "WHITE"),
    (CY,  "PROTO",   "v2.1.4"),
    (OR,  "ALERTS",  str(len(news))),
    (MG,  "ENC",     "AES-256"),
]
status_row = "  ".join(
    f"{c}[{k}: {v}]{R}" for c, k, v in status_items
)
out.append(side(" " + status_row + " " * max(0, W - 2 - 1 - str_w(status_row))))
out.append(empty_row())

copy = GR + DIM + "  © 2026 AIsennin SecOps Feed  ·  TLP:WHITE  ·  Redistribution permitted with attribution" + R
out.append(side(copy + " " * max(0, W - 2 - str_w(copy))))
out.append(empty_row())
out.append(bot_bar())

print("\n".join(out))
