import streamlit as st
import google.generativeai as genai

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-3.5-flash')

st.title("AIデートプランナー 💘")

# --- メイン設定 ---
area = st.text_input("デートエリア（例: 渋谷）")
col1, col2 = st.columns(2)
with col1:
    weather = st.radio("現在の天気", ["晴れ", "雨"], horizontal=True)
with col2:
    budget = st.selectbox("予算", ["3,000円以内", "5,000円以内", "10,000円以内", "それ以上"])

# --- 詳細設定 ---
with st.expander("詳細設定"):
    # 「回数」から「関係性」へ変更
    relationship = st.selectbox("現在の関係性", [
        "マッチング直後（初対面）", 
        "数回デート済み（距離を縮めたい）", 
        "交際中（恋人）", 
        "特別な記念日"
    ])
    duration = st.selectbox("所要時間", ["ランチのみ", "半日（4時間）", "夕方〜夜", "一日", "宿泊"])
    plan_type = st.radio("プランタイプ", ["王道", "穴場", "コスパ重視", "贅沢"], horizontal=True)
    interests = st.text_input("興味のあること（例: カフェ巡り）")
    dislikes = st.text_input("苦手なもの（例: 人混み）")
    include_conv = st.checkbox("会話ネタも提案してほしい", value=True)

if st.button("プランを生成！"):
    if not area:
        st.warning("エリアを入力してください")
    else:
        st.info(f"{relationship}のプランを構築中... 🪄")
        
        prompt = f"""
        あなたはプロのデートプランナーです。以下の条件でデートプランを提案してください。

        【条件】
        ・場所: {area}、予算: {budget}、天気: {weather}
        ・関係性: {relationship}
        ・所要時間: {duration}、プランタイプ: {plan_type}
        ・興味: {interests if interests else "おまかせ"}
        ・苦手: {dislikes if dislikes else "特になし"}

        【出力ルール】
        1. {relationship}という関係性にふさわしい距離感のプランにすること。
        2. {weather}の日に最適な時系列のプランを提案すること。
        3. 移動手段と、Googleマップ上の一般的な移動時間を考慮して記述すること。
        4. 各スポットにGoogleマップURLを必ず添えること。
        { "5. デートを盛り上げるための会話ネタを3つ提案すること。" if include_conv else "" }
        6. 余計な前置きは不要。すぐにプランを書き始めること。
        """

        response = model.generate_content(prompt)
        st.write(response.text)