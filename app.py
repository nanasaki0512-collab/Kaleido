import json
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
        margin-bottom: 20px;
    }
    .date-badge {
        background-color: #ff007f;
        color: white;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def load_news():
  try:
    with open("news.json", "r", encoding="utf-8") as f:
      return json.load(f).get("articles", [])
  except FileNotFoundError:
    return []


st.title("🔮 Kaleido [カレイド]")
st.markdown(
    "##### ――最新ニュースを4つのメタ認知視点（サイバー・アナリスト）で読み解く――"
)
st.markdown("---")

articles = load_news()

if not articles:
  st.warning(
      "ニュースデータ（news.json）が見つからないか、データが空です。"
      "バックエンドの更新を実行するか、しばらくお待ちください。"
  )
else:
  # 添付していただいた実際の画像ファイル名にマッピング
  persona_info = {
      "history": {
          "name": "歴史学者",
          "desc": "超長期的視点（10年後・100年後からの大局観）",
          "color": "#ffaa00",
          "icon": "歴史学者_白背景.png",
      },
      "mediator": {
          "name": "仲裁者",
          "desc": "当事者間の隠れたニーズ整理・合意形成の支援",
          "color": "#00ccff",
          "icon": "仲裁者_白背景.png",
      },
      "structure": {
          "name": "社会起業家",
          "desc": "実利主義・課題解決思考・数字思考（共感性低）",
          "color": "#ff0055",
          "icon": "社会起業家_白背景.png",
      },
      "lifestyle": {
          "name": "エッセイスト",
          "desc": "執着なく物事を受け流す、達観したユーモア",
          "color": "#00ff66",
          "icon": "エッセイスト_白背景.png",
      },
  }

  for article in articles:
    with st.container():
      st.markdown('<div class="news-card">', unsafe_allow_html=True)

      # 配信日時の表示
      pub_date = article.get("date", "日付不明")
      st.markdown(
          f'<span class="date-badge">📅 {pub_date}</span>',
          unsafe_allow_html=True,
      )

      st.subheader(article.get("title", "タイトルなし"))
      st.write(f"**【要約】** {article.get('summary', '')}")

      st.markdown("---")

      # 4人のペルソナタブ
      columns_data = article.get("columns", {})
      tab_keys = list(persona_info.keys())
      tab_labels = [persona_info[k]["name"] for k in tab_keys]

      tabs = st.tabs(tab_labels)

      for i, k in enumerate(tab_keys):
        with tabs[i]:
          p_info = persona_info[k]

          # 画像と視点説明を横並びに表示
          col1, col2 = st.columns([1, 8])
          with col1:
            try:
              st.image(p_info["icon"], width=60)
            except Exception:
              st.write("🖼️")
          with col2:
            st.markdown(
                f"**【視点】** <span style='color:{p_info['color']}'>"
                f"{p_info['desc']}</span>",
                unsafe_allow_html=True,
            )

          comment = columns_data.get(k, "コメントがありません。")
          st.markdown(f"> {comment}")

      st.markdown("</div>", unsafe_allow_html=True)
