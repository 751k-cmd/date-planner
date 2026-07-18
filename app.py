import streamlit as st
import google.generativeai as genai
import re

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
if "last_plan" not in st.session_state:
    st.session_state["last_plan"] = ""
if "plan_updated" not in st.session_state:
    st.session_state["plan_updated"] = False

# --- 入力UI ---
area = st.text_input("📍 デートエリア")
col1, col2 = st.columns(2)
with col1: weather = st.radio("現在の天気", ["晴れ", "雨"], horizontal=True)
with col2: budget = st.selectbox("予算", ["3,000円以内", "5,000円以内", "10,000円以内", "それ以上"])

with st.expander("⚙️ こだわり設定（詳細）"):
    relationship = st.selectbox("関係性", ["マッチング直後", "数回デート済み", "交際中", "特別な記念日"])
    duration = st.selectbox("所要時間", ["ランチのみ", "半日（4時間）", "夕方〜夜", "一日", "宿泊"])
    plan_type = st.radio("プランタイプ", ["王道", "穴場", "コスパ重視", "贅沢"], horizontal=True)
    interests = st.text_input("興味のあること")
    dislikes = st.text_input("苦手なもの")
    additional_notes = st.text_area("✍️ その他の予定・条件")
    include_conv = st.checkbox("会話ネタも提案してほしい", value=True)

# --- 生成ロジック ---
def generate_plan(refinement=None):
    prompt = f"""
    プロのデートプランナーとして、{relationship}の方との{weather}の日のデートプランを提案して。
    場所:{area}, 予算:{budget}, 所要時間:{duration}, タイプ:{plan_type}
    興味:{interests}, 苦手:{dislikes}, 条件:{additional_notes}
    
    【出力ルール】
    1. 時系列プランと移動時間/手段の記載。
    2. GoogleマップURLの添付。
    3. プランの最後に「ROUTE_LOCATIONS: スポットA, スポットB, スポットC」という形式でルート地点のみを記載すること。
    {"4. 会話ネタを3つ。" if include_conv else ""}
    """
    if refinement:
        prompt = f"以下のプランを修正して: {refinement}\n\n【元プラン】\n{st.session_state['last_plan']}"
    
    with st.spinner("プランを構築中... 🪄"):
        response = model.generate_content(prompt)
        st.session_state["last_plan"] = response.text
        st.session_state["plan_updated"] = True

# --- 地図URL生成 ---
def get_map_embed_url(locations_str):
    locs = [l.strip() for l in locations_str.split(",")]
    if len(locs) < 2: return None
    
    origin = locs[0]
    destination = locs[-1]
    waypoints = "|".join(locs[1:-1])
    
    return f"https://www.google.com/maps/embed/v1/directions?key={MAPS_API_KEY}&origin={origin}&destination={destination}&waypoints={waypoints}"

# --- ボタン処理 ---
if st.button("プランを生成する"):
    generate_plan()
    st.rerun()

# --- 表示エリア ---
if st.session_state["last_plan"]:
    st.markdown("---")
    
    if st.session_state["plan_updated"]:
        st.success("プランを調整・生成しました！")
        st.session_state["plan_updated"] = False
    
    # ルート情報の抽出と地図表示
    route_match = re.search(r'ROUTE_LOCATIONS: (.+)', st.session_state["last_plan"])
    if route_match:
        map_url = get_map_embed_url(route_match.group(1))
        if map_url:
            st.subheader("🗺️ デート動線マップ")
            st.components.v1.iframe(map_url, width=800, height=500)
    
    with st.container(border=True):
        st.markdown(st.session_state["last_plan"])
    
    st.subheader("🛠 プランの微調整")
    refinement = st.text_input("調整したいポイント")
    if st.button("この条件でプランを修正する"):
        generate_plan(refinement)
        st.rerun()