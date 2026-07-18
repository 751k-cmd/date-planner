import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

# --- デザイン調整 ---
st.set_page_config(page_title="AIデートプランナー", page_icon="💘", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #fdfbf7; }
    .stButton>button { border-radius: 20px; background-color: #ff6b81; color: white; font-weight: bold; border: none; }
    </style>
    """, unsafe_allow_html=True)

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-3.5-flash')

st.title("💘 AI Date Planner")

# --- セッション状態の初期化 ---
if "last_plan" not in st.session_state:
    st.session_state["last_plan"] = ""

# --- 入力UI ---
area = st.text_input("📍 デートエリア")
col1, col2 = st.columns(2)
with col1: weather = st.radio("現在の天気", ["晴れ", "雨"], horizontal=True)
with col2: budget = st.selectbox("予算", ["3,000円以内", "5,000円以内", "10,000円以内", "それ以上"])

with st.expander("⚙️ こだわり設定（詳細）"):
    relationship = st.selectbox("関係性", ["マッチング直後", "数回デート済み", "交際中", "特別な記念日"])
    duration = st.selectbox("所要時間", ["ランチのみ", "半日（4時間）", "夕方〜夜", "一日", "宿泊"])
    plan_type = st.radio("プランタイプ", ["王道", "穴場", "コスパ重視", "贅沢"], horizontal=True)
    interests = st.text_input("興味のあること（例: カフェ巡り）")
    dislikes = st.text_input("苦手なもの（例: 人混み）")
    additional_notes = st.text_area("✍️ その他の予定・条件")
    include_conv = st.checkbox("会話ネタも提案してほしい", value=True)

# --- 生成・修正の共通プロンプト作成関数 ---
def get_prompt(base_plan, user_refinement=None):
    if user_refinement:
        return f"以下のプランを修正して: {user_refinement}\n\n【元プラン】\n{base_plan}"
    
    return f"""
    プロのデートプランナーとして、{relationship}の方との{weather}の日のデートプランを提案して。
    場所:{area}, 予算:{budget}, 所要時間:{duration}, タイプ:{plan_type}
    興味:{interests}, 苦手:{dislikes}, 条件:{additional_notes}
    
    【出力ルール】
    1. 時系列のプラン。
    2. 各スポットのGoogleマップURL添付。
    3. 移動時間・移動手段を考慮。
    4. 最後に主要スポットを巡るGoogleマップ検索URL(https://www.google.com/maps/dir/...)を一つ提示。
    5. 洗練されたトーンで。
    {"6. 会話ネタを3つ。" if include_conv else ""}
    """

# --- ボタン処理 ---
if st.button("プランを生成する") or st.button("この条件でプランを修正する"):
    # 修正ボタンが押された場合のみ、追加のリクエストを考慮
    refinement = st.session_state.get("refinement", "")
    with st.spinner("プランを構築中... 🪄"):
        prompt = get_prompt(st.session_state["last_plan"], refinement if "修正する" in st.button else None)
        response = model.generate_content(prompt)
        st.session_state["last_plan"] = response.text

# --- 表示エリア ---
if st.session_state["last_plan"]:
    st.markdown("---")
    st.markdown(st.session_state["last_plan"])
    
    # 地図の埋め込み（AIがdir/形式のURLを出力している前提）
    st.subheader("🗺️ デート動線マップ")
    st.info("※地図が表示されない場合は、AIが生成したテキスト内のGoogle Mapsリンクをご確認ください。")
    # 簡易的にURLを抽出して表示するロジックが必要な場合はここに追加します
    
    st.markdown("---")
    st.subheader("🛠 プランの微調整")
    st.session_state["refinement"] = st.text_input("調整したいポイント")