"""AI News - Claude version: uses Claude API to generate 3 AI news summaries"""

import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": (
                "今日のAIに関するニュースを3件、簡潔にまとめてください。"
                "各ニュースは以下の形式で出力してください:\n"
                "[番号] タイトル\n日付: YYYY-MM-DD\n概要: 1〜2文\n"
                "実際のニュースでなくても、それらしいAIトレンドのニュースでOKです。"
            ),
        }
    ],
)

print("=" * 55)
print("  AI ニュース (Claude生成)")
print("=" * 55)
print(message.content[0].text)
print("=" * 55)
