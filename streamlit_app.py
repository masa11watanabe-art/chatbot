
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="社内規程AIナビ", page_icon="📘")

st.title("📘 社内規程AIナビ")
st.caption("架空の会社の規程を使ったデモアプリです")
st.info("社員の「ちょっと聞きたい」に、AIが規程を根拠に回答します。")

# デモ用の架空の社内規程
rules = """
【ABC株式会社 社内規程（架空のサンプル）】

第1条（年次有給休暇）
入社6か月後、所定の出勤率を満たした社員に
年次有給休暇を10日付与する。
その後の付与日数は法令および勤続年数による。

第2条（結婚休暇）
社員本人が結婚する場合、特別休暇を5日付与する。
取得する際は事前に上長へ申請する。

第3条（忌引休暇）
配偶者、父母または子が死亡した場合は5日、
祖父母または兄弟姉妹の場合は3日の特別休暇を付与する。

第4条（出張旅費）
国内出張における宿泊費の上限は1泊15,000円とする。
交通費は合理的な経路による実費を精算する。

第5条（出張日当）
国内出張の日当は、役職にかかわらず1日3,000円とする。

第6条（在宅勤務）
在宅勤務は所属部門長の事前承認を必要とする。
対象者は会社が定める条件を満たす社員とする。

第7条（資格取得支援）
会社が指定する資格の受験料を会社が負担する。
対象資格と支援条件は人事総務部が別途案内する。
"""

with st.expander("📚 デモ用の社内規程を見る"):
    st.text(rules)

api_key = st.text_input(
    "OpenAI APIキー",
    type="password",
    help="APIキーはGitHubのプログラムに書かないでください。"
)

st.subheader("💬 社内規程について質問する")

examples = [
    "結婚したら何日休めますか？",
    "国内出張の日当はいくらですか？",
    "宿泊費の上限を教えてください",
    "在宅勤務は自由にできますか？",
    "育児休業の期間は何日ですか？",
]

selected = st.selectbox(
    "質問例を選ぶこともできます",
    ["自由に質問する"] + examples
)

question = st.text_input(
    "質問を入力してください",
    value="" if selected == "自由に質問する" else selected,
    placeholder="例：結婚したら何日休めますか？"
)

if st.button("🔍 AIに質問する", type="primary"):
    if not api_key:
        st.warning("先にOpenAI APIキーを入力してください。")
    elif not question.strip():
        st.warning("質問を入力してください。")
    else:
        with st.spinner("社内規程を確認しています..."):
            try:
                client = OpenAI(api_key=api_key)

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "あなたはABC株式会社の社内規程案内AIです。"
                                "回答は必ず以下の社内規程だけを根拠にしてください。"
                                "規程に記載のない情報は推測せず、"
                                "『このサンプル規程では確認できません。"
                                "人事総務部にお問い合わせください。』と回答してください。"
                                "回答はわかりやすい日本語で簡潔に説明してください。"
                                "回答の最後には、必ず根拠となる条文番号を示してください。"
                                "関連条文がない場合は、条文番号を付けないでください。"
                                "この規程は架空のデモ用であり、実際の会社のルール"
                                "ではないことに注意してください。\n\n"
                                + rules
                            ),
                        },
                        {"role": "user", "content": question},
                    ],
                    temperature=0,
                )

                answer = response.choices[0].message.content
                st.success("回答")
                st.write(answer)

            except Exception as e:
                st.error("AIとの接続でエラーが発生しました。")
                st.code(str(e))

st.divider()
st.caption(
    "※本アプリは講義用の試作品です。"
    "掲載規程はすべて架空であり、実際の就業規則ではありません。"
)
