import streamlit as st
import google.generativeai as genai

# --- デザイン調整 ---
st.set_page_config(page_title="AIデートプランナー", page_icon="💘")
st.markdown("""
    <style>
    .main { background-color: #fdfbf7; }
    .stButton>button { border-radius: 20px; background-color: #ff6b81; color: white; font-weight: bold; border: none; }
    </style>
    """, unsafe_allow_html=True)

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-3.5-flash')

st.title("💘 AI Date Planner")

# セッション状態の初期化（プランの履歴を保持するため）
if "chat_history" not in st.session_history:
    st.session_history["chat_history"] = []
if "last_plan" not in st.session_history:
    st.session_history["last_plan"] = ""

# --- 入力UI ---
area = st.text_input("📍 デートエリア")
col1, col2 = st.columns(2)
with col1: weather = st.radio("現在の天気", ["晴れ", "雨"], horizontal=True)
with col2: budget = st.selectbox("予算", ["3,000円以内", "5,000円以内", "10,000円以内", "それ以上"])

with st.expander("⚙️ こだわり設定"):
    relationship = st.selectbox("関係性", ["マッチング直後", "数回デート済み", "交際中", "特別な記念日"])
    duration = st.selectbox("所要時間", ["ランチのみ", "半日", "夕方〜夜", "一日", "宿泊"])
    plan_type = st.radio("プランタイプ", ["王道", "穴場", "コスパ重視", "贅沢"], horizontal=True)
    additional_notes = st.text_area("✍️ その他の予定・条件")

# --- 生成・修正ボタン ---
if st.button("プランを生成する"):
    with st.spinner("最高のプランを作成中... 🪄"):
        prompt = f"""
        プロのプランナーとして、{relationship}の方との{weather}の日のデートプランを提案して。
        場所:{area}, 予算:{budget}, 所要時間:{duration}, タイプ:{plan_type}
        条件:{additional_notes}
        1.時系列のプラン。2.GoogleマップURLを添付。3.移動時間を考慮。4.洗練されたトーンで。
        """
        response = model.generate_content(prompt)
        st.session_history["last_plan"] = response.text
        st.markdown(response.text)

# --- 共同編集エリア ---
if st.session_history["last_plan"]:
    st.markdown("---")
    st.subheader("🛠 プランの微調整")
    refinement = st.text_input("調整したいポイントを教えてください", placeholder="例：ランチをもっと軽めにして、カフェを美術館に変更して")
    
    if st.button("この条件でプランを修正する"):
        with st.spinner("プランをブラッシュアップ中... 🪄"):
            refinement_prompt = f"""
            以下の既存プランをベースに、ユーザーの要望を反映して修正したプランを提案してください。
            【既存プラン】
            {st.session_history["last_plan"]}
            
            【修正要望】
            {refinement}
            
            ルール：元のプランの良さを活かしつつ、要望通りに変更すること。
            """
            response = model.generate_content(refinement_prompt)
            st.session_history["last_plan"] = response.text
            st.markdown(response.text)