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

# --- 詳細設定（アコーディオン） ---
with st.expander("詳細設定（所要時間・こだわり・回数など）"):
    duration = st.selectbox("所要時間", ["ランチのみ", "半日（4時間）", "夕方〜夜", "一日", "宿泊"])
    plan_type = st.radio("プランタイプ", ["王道", "穴場", "コスパ重視", "贅沢"], horizontal=True)
    visit_count = st.slider("デート回数（目安）", 1, 10, 1)
    interests = st.text_input("興味のあること（例: カフェ巡り、映画）")
    dislikes = st.text_input("苦手なもの（例: 人混み、静かな場所）")
    include_conv = st.checkbox("会話ネタも提案してほしい", value=True)

if st.button("プランを生成！"):
    if not area:
        st.warning("エリアを入力してください")
    else:
        st.info(f"{weather}の日のデートプランを構築中... 🪄")
        
        prompt = f"""
        あなたはプロのデートプランナーです。以下の条件でデートプランを提案してください。

        【条件】
        ・場所: {area}、予算: {budget}、天気: {weather}
        ・所要時間: {duration}、プランタイプ: {plan_type}
        ・デート回数: {visit_count}回目
        ・興味: {interests if interests else "おまかせ"}
        ・苦手: {dislikes if dislikes else "特になし"}

        【出力ルール】
        1. {weather}の日に最適な時系列のプランを提案すること。
        2. 移動手段と、Googleマップ上の一般的な移動時間を考慮して記述すること。
        3. 各スポットにGoogleマップURLを必ず添えること(形式: [施設名](https://www.google.com/maps/search/?api=1&query=施設名+エリア名))。
        { "4. デートを盛り上げるための会話ネタを3つ提案すること。" if include_conv else "" }
        5. 余計な前置きは不要。すぐにプランを書き始めること。
        """

        response = model.generate_content(prompt)
        st.write(response.text)