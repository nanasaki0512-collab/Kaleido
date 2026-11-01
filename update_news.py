import json
import os
from datetime import datetime, timezone, timedelta
from google import genai
from google.genai.errors import ServerError, APIError

def generate_cognitive_news(existing_titles):
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    excluded_text = ""
    if existing_titles:
        excluded_text = "\n【過去に生成済みの重複不可タイトル】\n" + "\n".join([f"- {t}" for t in existing_titles[:25]])

    prompt = """
    あなたは多角的な思考・メタ認知を促すニュースアナライザーです。
    日本国内で【ここ1〜3日以内】に話題になっている最新ニュースを【必ず合計3件】選び、それぞれのニュースに対して精神的に成熟した4人の人物視点から個別のコラム（各200〜300字）を執筆してください。
    """ + excluded_text + """

    【取り上げるニュースの条件】
    ・日本国内で直近3日以内に話題になっている社会、テクノロジー、カルチャー、地域などの出来事（3件）。
    ・スポーツやゴシップ・単なる炎上批判は避けてください。

    【4人の仮想人物（コラム執筆者）】
    1. history（70代・歴史学者）: 超長期的視点。歴史の文脈に照らし、「10年後・100年後からどう見えるか」という大局観を語る。
    2. psychology（50代・臨床心理士）: 感情への寄り添い。過剰な批判を避け、当事者や人々の不安・葛藤を優しく受容する。
    3. structure（40代・社会起業家）: システム思考。個人批判をやめ、社会の仕組みや課題の構造、建設的な前進を分析する。
    4. lifestyle（60代・エッセイスト）: 達観とユーモア。執着をほぐし、「世間が騒がしくても足元の暮らしを大切にする」心の余裕を提案する。

    【出力フォーマット（JSON形式のみ）】
    必ず以下のJSON配列（3要素）を出力してください（```json などのコードブロック囲みは不要です）。

    [
        {
            "title": "ニュースのタイトル（固有名詞を含める）",
            "summary": "ニュースの客観的な概要（100〜150字）",
            "columns": {
                "history": "歴史学者によるコラム",
                "psychology": "心理カウンセラーによるコラム",
                "structure": "社会起業家によるコラム",
                "lifestyle": "エッセイストによるコラム"
            }
        },
        ... （合計3件）
    ]
    """

    models_to_try = ['gemini-3.8-flash', 'gemini-2.5-flash']
    response = None
    last_error = None

    for model_name in models_to_try:
        try:
            print(f"モデル '{model_name}' で生成を試みます...")
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )
            print(f"モデル '{model_name}' での生成に成功しました。")
            break
        except (ServerError, APIError) as e:
            print(f"エラーが発生したためモデルを切り替えます: {e}")
            last_error = e
            continue

    if response is None:
        raise last_error

    text = response.text.strip()
    if text.startswith("```json"): text = text[7:]
    if text.startswith("```"): text = text[3:]
    if text.endswith("```"): text = text[:-3]
    
    new_items = json.loads(text.strip())
    
    jst = timezone(timedelta(hours=9))
    today_str = datetime.now(jst).strftime("%Y-%m-%d")
    for item in new_items:
        item["date"] = today_str
        
    return new_items

if __name__ == "__main__":
    existing_news = []
    existing_titles = []
    if os.path.exists("news.json"):
        try:
            with open("news.json", "r", encoding="utf-8") as f:
                existing_news = json.load(f)
                existing_titles = [item.get("title", "") for item in existing_news]
        except Exception:
            existing_news = []
            
    new_news_list = generate_cognitive_news(existing_titles)
    combined_news = new_news_list + existing_news
    
    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(combined_news, f, ensure_ascii=False, indent=4)
