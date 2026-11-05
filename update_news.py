import json
import os
import time
import feedparser
from google import genai
from google.genai.errors import ServerError, APIError

# ニュース取得元（Googleニュース、Yahoo!ニュースのRSS）
RSS_URLS = [
    "https://news.google.com/rss?hl=ja&gl=JP&ceid=JP:ja",          # Google ニュース Top
    "https://yahoo.co.jp/rss/topics/top-picks.xml",            # Yahoo! ニュース 主要
    "https://news.yahoo.co.jp/rss/topics/world.xml",                # Yahoo! ニュース 国際
    "https://news.yahoo.co.jp/rss/topics/business.xml"              # Yahoo! ニュース 経済
]

def fetch_latest_news(max_items=15):
    """
    Googleニュース・YahooニュースのRSSから最新記事と配信日時を取得する
    """
    articles = []
    seen_titles = set()

    for url in RSS_URLS:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            title = entry.get('title', '').strip()
            pub_date = entry.get('published', entry.get('updated', '日付不明'))
            
            if title and title not in seen_titles:
                seen_titles.add(title)
                summary = entry.get('summary', title)
                articles.append(
                    f"- 【タイトル】{title}\n"
                    f"  【日時】{pub_date}\n"
                    f"  【概要】{summary[:120]}"
                )
            
            if len(articles) >= max_items:
                break
        if len(articles) >= max_items:
            break
            
    return "\n".join(articles)

def generate_kaleido_news():
    raw_news = fetch_latest_news()
    
    # Gemini API クライアント初期化
    client = genai.Client()
    
    # プロンプトの構築
    prompt = f"""
以下は現在GoogleニュースおよびYahoo!ニュースから配信されている最新ニュースのリストです：

{raw_news}

上記の中から、世の中の関心が高く、多角的な視点で深掘りする価値のある重要ニュースを「3件」厳選してください（米政治・中間選挙、物価高、セキュリティ、少子化、国際情勢などのホットトピックを優先）。

選んだ3件のニュースそれぞれに対し、以下の4人の仮想アナリスト（ペルソナ）になりきってコラムを作成してください。

【ペルソナ定義】
1. history（70代・歴史学者）: 超長期的視点（10年後・100年後からの大局観）。
2. mediator（50代・仲裁者）: 当事者全員の隠れたニーズや本質的な課題を整理し、当事者同士が納得できる解決策（妥協点・合意）を見つけ出せるよう支援する視点。
3. structure（40代・社会起業家）: 実利主義、課題解決思考、数字思考に基づくシステム構造分析。共感性は低め。
4. lifestyle（60代・エッセイスト）: 達観・ユーモア・足元の暮らしの重視。

【出力フォーマット】
必ず以下の厳密なJSON形式のみで出力してください（Markdownのバッククォート等も含めないでください）：

{{
  "articles": [
    {{
      "id": 1,
      "date": "ニュースの配信日時（RSSから取得した日付をそのまま記載）",
      "title": "ニュースのタイトル",
      "summary": "ニュースの簡潔な要約（1〜2文）",
      "columns": {{
        "history": "歴史学者としてのコメント",
        "mediator": "仲裁者としてのコメント",
        "structure": "社会起業家としてのコメント",
        "lifestyle": "エッセイストとしてのコメント"
      }}
    }}
  ]
}}
"""

    # 混雑エラー対策：試行回数に応じて待ち時間を長くする（1回失敗後30秒、2回失敗後60秒）
    max_retries = 3
    retry_delays = [30, 60]  # 秒

    for attempt in range(1, max_retries + 1):
        try:
            print(f"Gemini API リクエスト送信中... (試行回数: {attempt}/{max_retries})")
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt,
                config={
                    "response_mime_type": "application/json"
                }
            )

            # 成功したらJSONを保存して終了
            data = json.loads(response.text)
            with open("news.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print("news.json updated successfully!")
            return

        except (ServerError, APIError) as e:
            print(f"サーバー混雑エラーが発生しました (試行 {attempt}回目): {e}")
            if attempt < max_retries:
                wait_time = retry_delays[attempt - 1]
                print(f"{wait_time}秒待機してサーバーの混雑緩和を待ちます...")
                time.sleep(wait_time)
            else:
                raise Exception("3回連続でサーバー混雑エラーが発生したため終了します。")
        except Exception as e:
            print(f"予期せぬエラーが発生しました: {e}")
            raise e

if __name__ == "__main__":
    generate_kaleido_news()
