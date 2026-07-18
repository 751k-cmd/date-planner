import streamlit as st
import google.generativeai as genai

# --- AIの準備 ---
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
# あなたの環境で使える最新のモデルを指定！
model = genai.GenerativeModel('gemini-3.5-flash')

# --- 画面のUI ---
st.title("AIデートプランナー 💘")
st.write("条件を入力すると、AIが最適なデートプランを提案します！")

st.header("デートの条件を教えてください")

# MVPで決めた5つの条件
area = st.text_input("デートエリア（例: 渋谷、みなとみらい）")
budget = st.selectbox("予算", ["3,000円以内", "5,000円以内", "10,000円以内", "それ以上"])
indoor_outdoor = st.radio("希望の過ごし方", ["インドア派", "アウトドア派", "どちらでも"])
weather = st.radio("天気", ["晴れ", "雨"])
is_anniversary = st.checkbox("特別な記念日ですか？")

# ボタンが押された時の処理
if st.button("デートプランを提案してもらう！"):
    if not area:
        st.warning("デートエリアを入力してください！")
    else:
        st.info("AIがプランを考え中...数秒お待ちください 🪄")
        
        # --- AIへのお願い（プロンプト）を作成 ---
        anniversary_text = "はい（特別な記念日です）" if is_anniversary else "いいえ（通常のデートです）"
        
        prompt = f"""
        あなたは優秀なデートプランナーです。以下の条件に合わせて、最高のデートプランを提案してください。

        【条件】
        ・場所: {area}
        ・予算: {budget}
        ・希望: {indoor_outdoor}
        ・天気: {weather}
        ・記念日: {anniversary_text}

        【出力形式】
        1. 時系列のデートプラン（例: 13:00 〇〇でランチ...）
        2. このプランのおすすめポイント
        """

        # --- AIにプロンプトを投げて結果をもらう ---
        try:
            response = model.generate_content(prompt)
            st.success("デートプランが完成しました！")
            st.write(response.text)
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")