import json
import os
import time
import urllib.request
import feedparser
from google import genai
from google.genai.errors import ServerError, APIError

RSS_URLS = [
    "https://news.google.com/rss?hl=ja&gl=JP&ceid=JP:ja",
    "https://yahoo.co.jp/rss/topics/top-picks.xml",
    "https://news.yahoo.co.jp/rss/topics/world.xml",
    "https://news.yahoo.co.jp/rss/topics/business.xml"
]

def fetch_latest_news(max_items=20):
    articles = []
    seen_titles = set()

    for url in RSS_URLS:
        try:
            req = urllib.request.Request(
                url, 
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            with urllib.request.urlopen(req, timeout=5) as res:
                html_content = res.read()
                feed = feedparser.parse(html_content)
                
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
        except Exception as e:
            print(f"RSS取得スキップ ({url}): {e}")
            continue
            
        if len(articles) >= max_items:
            break
            
    return "\n".join(articles)

def load_existing_news():
    if os.path.exists("news.json"):
        try:
            with open("news.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("articles", [])
        except Exception:
            return []
    return []

def generate_kaleido_news():
    raw_news = fetch_latest_news()
    if not raw_news:
        raise Exception("ニュースの取得に失敗しました。")

    existing_articles = load_existing_news()
    existing_titles = [art.get("title", "") for art in existing_articles]
    existing_titles_str = "\n".join([f"- {t}" for t in existing_titles[-50:]])

    client = genai.Client()
    
    prompt = f"""
以下は現在GoogleニュースおよびYahoo!ニュースから配信されている最新ニュースのリストです：

{raw_news}

【重要：重複の禁止】
以下の「すでに過去に作成したニュースのタイトル一覧」に含まれるニュース、またはこれらと酷似したテーマ・内容のニュースは**絶対に選ばないでください**。完全に新しいテーマの重要ニュースを「3件」厳選してください。

■ 過去に作成したニュースのタイトル一覧：
{existing_titles_str}

上記を踏まえ、選んだ新しい3件のニュースそれぞれに対し、以下の構成でコラムを作成してください。
※専門用語（ビジネス用語や難しい言葉）は一切使わず、小学生や一般の人でもスッと理解できる簡単な言葉だけで記述してください。
※「世間の反応」、ニュースの要約、および5人の専門家のコメントは、それぞれ **必ず300字〜500字程度のボリューム** で詳しく記述してください。
※文章の中に勝手に改行文字（コントロール文字）を入れないでください。

【構成・ペルソナ定義】
1. public_reaction（世間の反応）: このニュースに対して、ネットや世間一般の人々がどのように受け止め、どんな声を上げているか、その空気感や反応を300〜500字で解説。
2. history（歴史学者）: 超長期的視点（10年後・100年後からの大局観）から分かりやすく解説。
3. mediator（仲裁者）: 当事者全員の隠れた気持ちやぶつかり合う理由を整理し、みんなが納得できる落としどころを提案。
4. structure（社会起業家）: 世の中の仕組みやお金・ルールの問題点を、専門用語を一切使わず、身近なたとえ話と簡単な言葉だけで構造的に解説。
5. sage（賢者）: 高次の視点（一段高い精神的視点）から物事を俯瞰し、人間の弱さや思いやり、人類全体の精神的成長と気づきを慈愛に満ちた簡単な言葉で語りかける。
6. lifestyle（エッセイスト）: 執着が一切なく、物事を気楽に受け流し、「まあ、なるようにしかならないさ」と風のように軽やかなユーモアで語る。

【出力フォーマット】
必ず以下の厳密なJSON形式のみで出力してください（Markdownのバッククォート等も含めないでください）：

{{
  "articles": [
    {{
      "date": "ニュースの配信日時",
      "title": "ニュースのタイトル",
      "summary": "ニュースの詳細な要約（300〜500字程度、わかりやすい言葉で）",
      "public_reaction": "世間の反応についての解説（300〜500字程度、簡単な言葉で）",
      "columns": {{
        "history": "歴史学者としてのコメント（300〜500字程度、簡単な言葉で）",
        "mediator": "仲裁者としてのコメント（300〜500字程度、簡単な言葉で）",
        "structure": "社会起業家としてのコメント（専門用語ゼロ、身近な例えと簡単な言葉で300〜500字程度）",
        "sage": "賢者としてのコメント（慈愛と気づきを促す言葉で300〜500字程度）",
        "lifestyle": "エッセイストとしてのコメント（執着がなく軽やかなトーンで300〜500字程度）"
      }}
    }}
  ]
}}
"""

    max_retries = 3
    retry_delays = [30, 60]

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

            # JSONパース時のエラーを防ぐため、不正な制御文字（改行等）を自動除去する処理を追加
            clean_text = response.text
            
            new_data = json.loads(clean_text, strict=False)
            new_articles = new_data.get("articles", [])

            combined_articles = new_articles + existing_articles
            unique_articles = []
            seen = set()
            for art in combined_articles:
                t = art.get("title")
                if t and t not in seen:
                    seen.add(t)
                    unique_articles.append(art)

            final_articles = unique_articles[:30]

            output_data = {"articles": final_articles}
            with open("news.json", "w", encoding="utf-8") as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
            print("news.json updated successfully with history (max 30 items)!")
            return

        except (ServerError, APIError) as e:
            print(f"サーバー混雑エラーが発生しました (試行 {attempt}回目): {e}")
            if attempt < max_retries:
                wait_time = retry_delays[attempt - 1]
                print(f"{wait_time}秒待機して再試行します...")
                time.sleep(wait_time)
            else:
                raise Exception("3回連続でサーバー混雑エラーが発生したため終了します。")
        except Exception as e:
            print(f"予期せぬエラーまたはJSONパースエラーが発生しました: {e}")
            if attempt == max_retries:
                raise e
            time.sleep(10)

if __name__ == "__main__":
    generate_kaleido_news()
