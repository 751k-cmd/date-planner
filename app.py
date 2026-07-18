import streamlit as st
import google.generativeai as genai

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-3.5-flash')

st.title("AIデートプランナー 💘")

# --- メイン設定 ---
area = st.text_input("デートエリア（例: 渋谷）")
col1, col2 = st.columns(2)
with col1:
    budget = st.selectbox("予算", ["3,000円以内", "5,000円以内", "10,000円以内", "それ以上"])
with col2:
    duration = st.selectbox("所要時間", ["ランチのみ", "半日（4時間）", "夕方〜夜", "一日", "宿泊"])

# --- 詳細設定（アコーディオンで収納） ---
with st.expander("詳細設定（こだわり派はこちら）"):
    plan_type = st.radio("プランタイプ", ["王道", "穴場", "コスパ重視", "贅沢"])
    visit_count = st.slider("デート回数（目安）", 1, 10, 1)
    include_conv = st.checkbox("会話ネタも提案してほしい")
    interests = st.text_input("興味のあること")
    dislikes = st.text_input("苦手なもの")

if st.button("プランを生成！"):
    if not area:
        st.warning("エリアを入力してください")
    else:
        st.info("プランと移動時間、会話ネタを構築中... 🪄")
        
        prompt = f"""
        あなたはプロのデートプランナーです。以下の条件でデートプランを提案してください。

        【条件】
        ・場所: {area}、予算: {budget}、所要時間: {duration}
        ・タイプ: {plan_type}、デート回数: {visit_count}回目
        ・興味: {interests if interests else "おまかせ"}、苦手: {dislikes if dislikes else "特になし"}

        【出力ルール】
        1. 移動手段と移動時間を含めた時系列のプラン。GoogleマップURLを添える。
        2. 【雨天時の対策】代替スポットを提示すること。
        3. { "会話ネタを3つ用意すること。" if include_conv else "" }
        4. 非常に見やすく、整理された形式で出力すること。
        """

        response = model.generate_content(prompt)
        st.write(response.text)