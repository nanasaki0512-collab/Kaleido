import json
import os
import streamlit as st

# ページ設定 (ダークモード・ワイドレイアウト)
st.set_page_config(
    page_title="Kaleido - サイバーパンク・コラム", page_icon="🔮", layout="wide"
)

# サイバーパンク風カスタムCSS
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0b0f19;
        color: #00ffcc;
    }
    h1, h2, h3 {
        color: #00ffcc !important;
        font-family: 'Courier New', monospace;
    }
    .news-card {
        background-color: #131c2e;
        border: 1px solid #00ffcc;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 25px;
    }
    .date-badge {
        background-color: #ff007f;
        color: white;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .reaction-box {
        background-color: #1a233a;
        border-left: 4px solid #ff007f;
        padding: 15px;
        border-radius: 4px;
        margin-bottom: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def load_news():
    """JSONファイルを直接開き、最新記事が配列の先頭に来るように整列して返す"""
    if os.path.exists("news.json"):
        try:
            with open("news.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                articles = data.get("articles", [])
                return list(reversed(articles))
        except Exception as e:
            st.error(f"データ読み込みエラー: {e}")
            return []
    return []

st.title("🔮 Kaleido [カレイド]")
st.markdown("##### ――最新ニュースを多様なメタ認知視点と世間の反応で読み解く――")
st.markdown("---")

articles = load_news()

if not articles:
    st.warning("ニュースデータ（news.json）が見つからないか、データが空です。バックエンドの更新を実行するか、しばらくお待ちください。")
else:
    persona_info = {
        "history": {
            "name": "歴史学者",
            "desc": "超長期的視点（10年後・100年後からの大局観）",
            "color": "#ffaa00",
        },
        "mediator": {
            "name": "仲裁者",
            "desc": "当事者間の隠れたニーズ整理・合意形成の支援",
            "color": "#00ccff",
        },
        "structure": {
            "name": "社会起業家",
            "desc": "身近な言葉とたとえ話による社会構造の分析",
            "color": "#ff0055",
        },
        "sage": {
            "name": "賢者",
            "desc": "高次の視点・人間への深い理解・知恵と慈愛による気づきの促進",
            "color": "#bf00ff",
        },
        "lifestyle": {
            "name": "エッセイスト",
            "desc": "執着なく物事を受け流す、軽やかな達観ユーモア",
            "color": "#00ff66",
        },
    }

    for article in articles:
        with st.container():
            st.markdown('<div class="news-card">', unsafe_allow_html=True)

            pub_date = article.get("date", "日付不明")
            st.markdown(f'<span class="date-badge">📅 {pub_date}</span>', unsafe_allow_html=True)

            st.subheader(article.get("title", "タイトルなし"))
            st.write(f"**【要約】** {article.get('summary', '')}")

            public_reaction = article.get("public_reaction", "")
            if public_reaction:
                st.markdown(f'<div class="reaction-box"><strong>👥【世間の反応】</strong><br>{public_reaction}</div>', unsafe_allow_html=True)

            st.markdown("---")

            columns_data = article.get("columns", {})
            tab_keys = list(persona_info.keys())
            tab_labels = [persona_info[k]["name"] for k in tab_keys]

            tabs = st.tabs(tab_labels)

            for i, k in enumerate(tab_keys):
                with tabs[i]:
                    p_info = persona_info[k]
                    st.markdown(f"**【視点】** <span style='color:{p_info['color']}'>{p_info['desc']}</span>", unsafe_allow_html=True)
                    
                    comment = columns_data.get(k, "コメントがありません。")
                    st.markdown(f"> {comment}")

            st.markdown("</div>", unsafe_allow_html=True)
