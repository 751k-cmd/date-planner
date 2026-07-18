import streamlit as st
import google.generativeai as genai
import re
import urllib.parse
from streamlit.components.v1 import html

# --- ページ設定 ---
st.set_page_config(page_title="AIデートプランナー", page_icon="💘", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #fdfbf7; }
    .stButton>button { border-radius: 20px; background-color: #ff6b81; color: white; font-weight: bold; border: none; }
    </style>
    """, unsafe_allow_html=True)

# --- 設定 ---
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-3.5-flash')
MAPS_API_KEY = st.secrets["GOOGLE_MAPS_API_KEY"]

st.title("💘 AI Date Planner")

# --- セッション状態 ---
if "plan_data" not in st.session_state:
    st.session_state["plan_data"] = ""
if "is_refinement" not in st.session_state:
    st.session_state["is_refinement"] = False

# --- 入力UI ---
area = st.text_input("📍 デートエリア")
col1, col2 = st.columns(2)
with col1: weather = st.radio("現在の天気", ["晴れ", "雨"], horizontal=True)
with col2: budget = st.selectbox("予算", ["3,000円以内", "5,000円以内", "10,000円以内", "それ以上"])

with st.expander("⚙️ こだわり設定（詳細）", expanded=False):
    relationship = st.selectbox("関係性", ["マッチング直後", "数回デート済み", "交際中", "特別な記念日"])
    duration = st.selectbox("所要時間", ["ランチのみ", "半日（4時間）", "夕方〜夜", "一日", "宿泊"])
    plan_type = st.radio("プランタイプ", ["王道", "穴場", "コスパ重視", "贅沢"], horizontal=True)
    interests = st.text_input("興味のあること")
    dislikes = st.text_input("苦手なもの")
    additional_notes = st.text_area("✍️ その他の予定・条件")
    include_conv = st.checkbox("会話ネタも提案してほしい", value=True)

# --- 生成ロジック ---
def run_generation(refinement=None):
    with st.spinner("プランを構築中... 🪄"):
        base_info = f"場所:{area}, 天気:{weather}, 予算:{budget}, 関係性:{relationship}, 時間:{duration}, タイプ:{plan_type}, 興味:{interests}, 苦手:{dislikes}, 条件:{additional_notes}"
        prompt = f"以下のプランを修正して: {refinement}\n\n【元プラン】\n{st.session_state['plan_data']}\n\n【条件】\n{base_info}" if refinement else f"プロのプランナーとして、以下の条件でデートプランを提案して。\n{base_info}\n\n【ルール】\n1. 時系列プランと移動手段の記載。\n2. 会話ネタを3つ提案。" + ("\n3. 最後に必ず1行で「ROUTE_LOCATIONS: スポットA, スポットB, スポットC」と出力すること。" if True else "")
        
        response = model.generate_content(prompt)
        st.session_state["plan_data"] = response.text
        st.session_state["is_refinement"] = (refinement is not None)

# --- フラグメント処理 ---
@st.fragment
def display_plan():
    if st.session_state["plan_data"]:
        if st.session_state.get("is_refinement"):
            st.success("プランを調整・生成しました！")
            # JavaScriptで強制的にページトップへスクロール
            html("<script>window.scrollTo(0, 0);</script>")
        
        st.markdown("---")
        
        route_match = re.search(r'ROUTE_LOCATIONS: (.+)', st.session_state["plan_data"])
        if route_match:
            locs = [l.strip() for l in route_match.group(1).split(",")]
            if len(locs) >= 2:
                st.subheader("🗺️ デート動線マップ")
                map_url = f"https://www.google.com/maps/embed/v1/directions?key={MAPS_API_KEY}&origin={urllib.parse.quote(locs[0])}&destination={urllib.parse.quote(locs[-1])}&waypoints={'|'.join([urllib.parse.quote(l) for l in locs[1:-1]])}"
                st.components.v1.iframe(map_url, width=800, height=500)

        with st.container(border=True):
            st.markdown(st.session_state["plan_data"])
        
        st.subheader("🛠 プランの微調整")
        refinement = st.text_input("調整したいポイント")
        if st.button("この条件でプランを修正する"):
            run_generation(refinement)
            st.rerun()

if st.button("プランを生成する"):
    st.session_state["is_refinement"] = False
    run_generation()
    st.rerun()

display_plan()