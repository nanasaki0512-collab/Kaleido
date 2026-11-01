import json
import os
import streamlit as st

# --- ページ基本設定（必ず最初に記述） ---
st.set_page_config(
    page_title="Kaleido // 認知整理端末",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- サイバーパンク風 Custom CSS ---
st.markdown("""
<style>
    .stApp {
        background-color: #080b11;
        color: #00f0ff;
        font-family: 'Consolas', 'Courier New', monospace;
    }
    .cyber-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #00f0ff;
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.7);
        border-bottom: 2px solid #ff0055;
        padding-bottom: 10px;
        margin-bottom: 25px;
    }
    .news-box {
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid #00f0ff;
        border-left: 5px solid #00f0ff;
        border-radius: 4px;
        padding: 18px;
        margin-bottom: 20px;
    }
    .news-title {
        color: #ffffff;
        font-size: 1.3rem;
        font-weight: bold;
    }
    .persona-card {
        background: rgba(20, 24, 38, 0.85);
        border-radius: 6px;
        padding: 16px;
        margin-top: 10px;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    .persona-1 { border: 1px solid #ff0055; }
    .persona-2 { border: 1px solid #00ffaa; }
    .persona-3 { border: 1px solid #00f0ff; }
    .persona-4 { border: 1px solid #ffaa00; }
    .persona-tag {
        font-weight: bold;
        font-size: 0.85rem;
        padding: 2px 8px;
        border-radius: 3px;
        margin-bottom: 8px;
        display: inline-block;
    }
    .tag-1 { background: #ff0055; color: #fff; }
    .tag-2 { background: #00ffaa; color: #000; }
    .tag-3 { background: #00f0ff; color: #000; }
    .tag-4 { background: #ffaa00; color: #000; }
</style>
""", unsafe_allow_html=True)

# --- タイトル表示 ---
st.markdown('<div class="cyber-title">KALEIDO // 認知整理端末</div>', unsafe_allow_html=True)
st.caption("国内の最新トピックに対し、多角的な視点を持つ4人の仮想アナリストがコラムを展開します。")

# --- データ読み込み ---
if os.path.exists("news.json"):
    with open("news.json", "r", encoding="utf-8") as f:
        news_data = json.load(f)
else:
    news_data = []

if not news_data:
    st.info("⚡ 現在、システムデータを同期中です。GitHub Actionsの実行または手動更新をお待ちください。")
else:
    for idx, item in enumerate(news_data[:3]):
        st.markdown(f"""
        <div class="news-box">
            <div style="color: #ff0055; font-size: 0.8rem; font-weight: bold;">[TOPIC #{idx+1}] DATE: {item.get('date', 'TODAY')}</div>
            <div class="news-title">{item.get('title')}</div>
            <p style="color: #cbd5e1; font-size: 0.95rem; margin-top: 8px;">{item.get('summary')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        cols = item.get("columns", {})
        tab1, tab2, tab3, tab4 = st.tabs([
            "🏛️ 大局・歴史視点", 
            "🌱 心理・共感視点", 
            "⚙️ 構造・解決視点", 
            "🍵 達観・生活視点"
        ])
        
        with tab1:
            st.markdown(f"""
            <div class="persona-card persona-1">
                <span class="persona-tag tag-1">70代・歴史学者／大局観</span>
                <p style="color: #e2e8f0; margin-top: 5px;">{cols.get('history', '解析中...')}</p>
            </div>
            """, unsafe_allow_html=True)
            
        with tab2:
            st.markdown(f"""
            <div class="persona-card persona-2">
                <span class="persona-tag tag-2">50代・心理カウンセラー／共感</span>
                <p style="color: #e2e8f0; margin-top: 5px;">{cols.get('psychology', '解析中...')}</p>
            </div>
            """, unsafe_allow_html=True)
            
        with tab3:
            st.markdown(f"""
            <div class="persona-card persona-3">
                <span class="persona-tag tag-3">40代・社会起業家／構造分析</span>
                <p style="color: #e2e8f0; margin-top: 5px;">{cols.get('structure', '解析中...')}</p>
            </div>
            """, unsafe_allow_html=True)
            
        with tab4:
            st.markdown(f"""
            <div class="persona-card persona-4">
                <span class="persona-tag tag-4">60代・エッセイスト／達観・余白</span>
                <p style="color: #e2e8f0; margin-top: 5px;">{cols.get('lifestyle', '解析中...')}</p>
            </div>
            """, unsafe_allow_html=True)
            
        st.write("---")
