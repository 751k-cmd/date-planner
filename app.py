import streamlit as st
import google.generativeai as genai

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-3.5-flash')

st.title("AIデートプランナー 💘")

# --- メイン設定 ---
area = st.text_input("デートエリア（例: 渋谷）")
col1, col2, col3 = st.columns(3)
with col1:
    weather = st.radio("現在の天気", ["晴れ", "雨"])
with col2:
    budget = st.selectbox("予算", ["3,000円以内", "5,000円以内", "10,000円以内", "それ以上"])
with col3:
    duration = st.selectbox("所要時間", ["ランチのみ", "半日", "一日"])

# --- 詳細設定（アコーディオン） ---
with st.expander("詳細設定"):
    plan_type = st.radio("プランタイプ", ["王道", "穴場", "コスパ重視", "贅沢"])
    include_conv = st.checkbox("会話ネタも提案する")

if st.button("プランを生成！"):
    if not area:
        st.warning("エリアを入力してください")
    else:
        st.info(f"{weather}の日のプランを構築中... 🪄")
        
        prompt = f"""
        あなたはプロのデートプランナーです。
        以下の条件で、{weather}の日用の最高のデートプランを1つ提案してください。

        【条件】
        ・場所: {area}、予算: {budget}、所要時間: {duration}
        ・タイプ: {plan_type}
        ・天気: {weather}

        【出力ルール】
        1. 晴れ/雨に関わらず、{weather}の日に最適なプランを時系列で作成する。
        2. 各スポットにGoogleマップURLを必ず添える。
        3. 移動手段と、Googleマップ上の一般的な移動時間を考慮して記述すること。
        { "4. 会話ネタを3つ用意すること。" if include_conv else "" }
        5. 余計な前置きは不要。すぐにプランを書き始めること。
        """

        response = model.generate_content(prompt)
        st.write(response.text)