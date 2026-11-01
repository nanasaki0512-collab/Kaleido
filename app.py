import streamlit as st
import json
import os

# --- ページ基本設定 ---
st.set_page_config(
    page_title="NEURO_NEWS // 認知分析端末",
    page_layout="wide",
    initial_sidebar_state="expanded"
)

# --- サイバーパンク風 Custom CSS ---
st.markdown("""
<style>
    /* 全体背景とベースフォント */
    .stApp {
        background-color: #080b11;
        color: #00f0ff;
        font-family: 'Consolas', 'Courier New', monospace;
    }
    
    /* ヘッダータイトル */
    .cyber-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #00f0ff;
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.7), 0 0 20px rgba(0, 240, 255, 0.4);
        border-bottom: 2px solid #ff0055;
        padding-bottom: 10px;
        margin-bottom: 25px;
    }
    
    /* ニュースカード */
    .news-box {
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid #00f0ff;
        border-left: 5px solid #00f0ff;
        border-radius: 4px;
        padding: 18px;
        margin-bottom: 20px;
        box-shadow: 0 0 12px rgba(0, 240, 255, 0.15);
    }
    
    /* ニュースタイトル */
    .news-title {
        color: #ffffff;
        font-size: 1.3rem;
        font-weight: bold;
        text-shadow: 0 0 5px rgba(255, 255, 255, 0.5);
    }

    /* 4人のペルソナ別コラムカード (ネオンカラー切り替え) */
    .persona-card {
        background: rgba(20, 24, 38, 0.85);
        border-radius: 6px;
        padding: 16px;
        margin-top: 10px;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    .persona-1 { border: 1px solid #ff0055; box-shadow: 0 0 8px rgba(255, 0, 85, 0.2); } /* 歴史視点 */
    .persona-2 { border: 1px solid #00ffaa; box-shadow: 0 0 8px rgba(0, 255, 170, 0.2); } /* 心理対話 */
    .persona-3 { border: 1px solid #00f0ff; box-shadow: 0 0 8px rgba(0, 240, 255, 0.2); } /* システム */
    .persona-4 { border: 1px solid #ffaa00; box-shadow: 0 0 8px rgba(255, 170, 0, 0.2); } /* 達観生活 */

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
st.markdown('<div class="cyber-title">SYSTEM // NEURO_NEWS [認知整理端末]</div>', unsafe_allow_html=True)
st.caption("国内の最新トピック3件に対し、多角的な視点（メタ認知）を持つ4人の仮想アナリストがコラムを展開します。")

# --- データ読み込み ---
if os.path.exists("news.json"):
    with open("news.json", "r", encoding="utf-8") as f:
        news_data = json.load(f)
else:
    news_data = []

if not news_data:
    st.info("⚡ 現在、システムデータを同期中です。手動実行または自動更新をお待ちください。")
else:
    # 今日のニュース3件をループ表示
    for idx, item in enumerate(news_data[:3]):
        st.markdown(f"""
        <div class="news-box">
            <div style="color: #ff0055; font-size: 0.8rem; font-weight: bold;">[TOPIC #{idx+1}] DATE: {item.get('date', 'TODAY')}</div>
            <div class="news-title">{item.get('title')}</div>
            <p style="color: #cbd5e1; font-size: 0.95rem; margin-top: 8px;">{item.get('summary')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 4人のコラムをタブ形式で整理
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
