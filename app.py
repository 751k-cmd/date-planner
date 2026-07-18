import streamlit as st
import google.generativeai as genai

# --- デザイン調整 ---
st.set_page_config(page_title="AIデートプランナー", page_icon="💘")

# CSSでスタイリッシュに仕上げる
st.markdown("""
    <style>
    .main { background-color: #fdfbf7; }
    h1 { color: #ff6b81; text-align: center; font-family: 'Helvetica', sans-serif; }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        background-color: #ff6b81;
        color: white;
        font-weight: bold;
        border: none;
        padding: 10px;
    }
    .stButton>button:hover { background-color: #ff4757; }
    </style>
    """, unsafe_allow_html=True)

# --- AIの準備 ---
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-3.5-flash')

# --- 画面構成 ---
st.title("💘 AI Date Planner")
st.write("今日のデートを、もっと特別に。")

area = st.text_input("📍 デートエリア")
col1, col2 = st.columns(2)
with col1:
    weather = st.radio("現在の天気", ["晴れ", "雨"], horizontal=True)
with col2:
    budget = st.selectbox("予算", ["3,000円以内", "5,000円以内", "10,000円以内", "それ以上"])

with st.expander("⚙️ こだわり設定（詳細）"):
    relationship = st.selectbox("関係性", ["マッチング直後", "数回デート済み", "交際中", "特別な記念日"])
    duration = st.selectbox("所要時間", ["ランチのみ", "半日", "夕方〜夜", "一日", "宿泊"])
    plan_type = st.radio("プランタイプ", ["王道", "穴場", "コスパ重視", "贅沢"], horizontal=True)
    interests = st.text_input("興味のあること")
    dislikes = st.text_input("苦手なもの")
    include_conv = st.checkbox("会話ネタも提案してほしい", value=True)

if st.button("プランを生成する"):
    if not area:
        st.warning("エリアを入力してください")
    else:
        with st.spinner("最高のプランを作成中... 🪄"):
            prompt = f"""
            プロのデートプランナーとして、{relationship}の方との{weather}の日のデートプランを提案してください。
            ・場所: {area}、予算: {budget}、所要時間: {duration}
            ・タイプ: {plan_type}
            ・興味: {interests if interests else "おまかせ"}、苦手: {dislikes if dislikes else "特になし"}

            1. {weather}に最適な時系列のプラン。
            2. 各スポットのGoogleマップURL: [施設名](https://www.google.com/maps/search/?api=1&query=施設名+エリア名)
            3. 移動時間も考慮すること。
            {"4. 会話ネタを3つ。" if include_conv else ""}
            5. 洗練された、わくわくするようなトーンで出力してください。
            """
            response = model.generate_content(prompt)
            st.markdown("---")
            st.markdown(response.text)