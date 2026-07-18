import streamlit as st
import google.generativeai as genai

# --- AIの準備 ---
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-3.5-flash')

# --- 画面のUI ---
st.title("AIデートプランナー 💘")

# パーソナライズ用の入力項目を追加
area = st.text_input("デートエリア（例: 渋谷）")
budget = st.selectbox("予算", ["3,000円以内", "5,000円以内", "10,000円以内", "それ以上"])
interests = st.text_input("興味のあること（例: カフェ巡り、映画、公園、食べ歩き）")
dislikes = st.text_input("苦手なこと・もの（例: 人混み、辛いもの、静かな場所）")
is_anniversary = st.checkbox("特別な記念日ですか？")

if st.button("プランを提案してもらう！"):
    if not area:
        st.warning("デートエリアを入力してください！")
    else:
        st.info("AIが雨天対応も含めてプランを構築中... 🪄")
        
        anniversary_text = "はい（特別な記念日です）" if is_anniversary else "いいえ（通常のデートです）"
        
        # プロンプトを強化：パーソナライズと雨天時の自動対応を追加
        prompt = f"""
        あなたはプロのデートプランナーです。以下の条件に基づき、最高のデートプランを提案してください。

        【条件】
        ・場所: {area}
        ・予算: {budget}
        ・興味: {interests if interests else "おまかせ"}
        ・苦手: {dislikes if dislikes else "特になし"}
        ・記念日: {anniversary_text}

        【出力ルール】
        1. 「晴れの日プラン」をメインで時系列に提案すること。
        2. 各スポットにGoogleマップのリンクを必ず添えること(形式: [施設名](https://www.google.com/maps/search/?api=1&query=施設名+エリア名))。
        3. 【雨天時の対策】として、メインプランのスポットの代わりに使える「雨でも楽しめる近隣の代替スポット」を必ず提案すること。
        4. 記念日や相手の好みに配慮したアドバイスも一言添えること。
        """

        try:
            response = model.generate_content(prompt)
            st.success("デートプランが完成しました！")
            st.write(response.text)
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")