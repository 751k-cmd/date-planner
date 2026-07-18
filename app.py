import streamlit as st
import google.generativeai as genai
import re

# --- ページ設定 ---
st.set_page_config(page_title="AIデートプランナー", page_icon="💘", layout="wide")

# --- 設定 ---
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-3.5-flash')
MAPS_API_KEY = st.secrets["GOOGLE_MAPS_API_KEY"]

st.title("💘 AI Date Planner")

# --- 初期化 ---
if "last_plan" not in st.session_state:
    st.session_state["last_plan"] = ""

# --- 生成・修正関数 ---
def generate_plan(refinement=None):
    prompt = f"""
    プロのデートプランナーとして、デートプランを提案して。
    条件: {area}, {weather}, {budget}, {duration}, {plan_type}
    こだわり: {interests}, {dislikes}, {additional_notes}
    
    【ルール】
    1. 時系列プランと移動時間/手段の記載。
    2. GoogleマップURLの添付。
    3. プランの最後に「ROUTE_LOCATIONS: スポットA, スポットB, スポットC」と1行で記載すること。
    """
    if refinement:
        prompt = f"以下のプランを修正して: {refinement}\n\n【元プラン】\n{st.session_state['last_plan']}"
    
    with st.spinner("プランを構築中... 🪄"):
        response = model.generate_content(prompt)
        st.session_state["last_plan"] = response.text

# --- UI入力 ---
area = st.text_input("📍 デートエリア")
col1, col2 = st.columns(2)
with col1: weather = st.radio("現在の天気", ["晴れ", "雨"], horizontal=True)
with col2: budget = st.selectbox("予算", ["3,000円以内", "5,000円以内", "10,000円以内", "それ以上"])

with st.expander("⚙️ こだわり設定"):
    relationship = st.selectbox("関係性", ["マッチング直後", "数回デート済み", "交際中"])
    duration = st.selectbox("所要時間", ["ランチのみ", "半日（4時間）", "一日"])
    plan_type = st.radio("プランタイプ", ["王道", "穴場", "コスパ重視"], horizontal=True)
    interests = st.text_input("興味のあること")
    dislikes = st.text_input("苦手なもの")
    additional_notes = st.text_area("✍️ その他の予定・条件")
    include_conv = st.checkbox("会話ネタも提案", value=True)

# --- 生成ボタン ---
if st.button("プランを生成する"):
    generate_plan()
    st.rerun()

# --- 表示・修正エリア ---
if st.session_state["last_plan"]:
    st.markdown("---")
    
    # マップ表示ロジック
    route_match = re.search(r'ROUTE_LOCATIONS: (.+)', st.session_state["last_plan"])
    if route_match:
        locs = [l.strip() for l in route_match.group(1).split(",")]
        if len(locs) >= 2:
            st.subheader("🗺️ デート動線マップ")
            map_url = f"https://www.google.com/maps/embed/v1/directions?key={MAPS_API_KEY}&origin={locs[0]}&destination={locs[-1]}&waypoints={'|'.join(locs[1:-1])}"
            st.components.v1.iframe(map_url, width=800, height=500)

    with st.container(border=True):
        st.markdown(st.session_state["last_plan"])
    
    st.subheader("🛠 プランの微調整")
    refinement = st.text_input("調整したいポイント", key="refinement_input")
    if st.button("この条件でプランを修正する"):
        generate_plan(refinement)
        st.rerun()