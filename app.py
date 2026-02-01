import streamlit as st
import pandas as pd
import altair as alt

# ページ設定
st.set_page_config(
    page_title="行動プライオリティベクトル",
    layout="wide"
)

# タイトル
st.title("行動プライオリティベクトル（試作版）")

# セッションステートの初期化
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

# 入力エリア

with st.form("task_form", clear_on_submit=True):
    task_name = st.text_input("タスクをすべて書き出してください", placeholder="例：ランニングに行く")

    # スライダーは1カラムで縦積みに表示
    impact = st.slider(
        "このタスクは、あなたの人生をどれくらい良くしますか？10点満点で採点してください",
        min_value=0,
        max_value=10,
        value=5,
        step=1,
        key="impact_slider"
    )

    effort = st.slider(
        "このタスクを実行するのに、どれくらいのエネルギーが必要ですか？10点満点で採点してください",
        min_value=0,
        max_value=10,
        value=5,
        step=1,
        key="effort_slider"
    )
    
    submitted = st.form_submit_button("タスクを追加")
    
    if submitted and task_name:
        new_task = {
            "タスク名": task_name,
            "影響度": impact,
            "労力": effort
        }
        st.session_state.tasks.append(new_task)
        st.success(f"「{task_name}」を追加しました！")
    elif submitted and not task_name:
        st.warning("タスク名を入力してください。")

# タスク一覧とグラフの表示
if st.session_state.tasks:
    st.header("タスク一覧と可視化")
    
    # タスク一覧（テーブル）
    df = pd.DataFrame(st.session_state.tasks)
    st.subheader("追加されたタスク")
    st.altair_chart(chart, use_container_width=True)    
    # 散布図（Altair）：x=労力、y=影響度、点にタスク名表示、スケール0-10固定
    st.subheader("優先度マップ")
    
    points = alt.Chart(df).mark_circle(size=100).encode(
        x=alt.X(
            "労力",
            title="労力",
            scale=alt.Scale(domain=[0, 10]),
            axis=alt.Axis(values=list(range(0, 11)), format="d")
        ),
        y=alt.Y(
            "影響度",
            title="影響度",
            scale=alt.Scale(domain=[0, 10]),
            axis=alt.Axis(values=list(range(0, 11)), format="d")
        ),
        tooltip=["タスク名", "影響度", "労力"],
    )
    
    # テキストラベルは白縁取りで重なっても視認しやすく
    labels = alt.Chart(df).mark_text(
        align="left",
        dx=8,
        dy=-8,
        fontSize=11,
        stroke="white",
        strokeWidth=3
    ).encode(
        x=alt.X(
            "労力",
            title="労力",
            scale=alt.Scale(domain=[0, 10]),
            axis=alt.Axis(values=list(range(0, 11)), format="d")
        ),
        y=alt.Y(
            "影響度",
            title="影響度",
            scale=alt.Scale(domain=[0, 10]),
            axis=alt.Axis(values=list(range(0, 11)), format="d")
        ),
        text="タスク名",
    )

    # 中央の基準線（縦=労力5、横=影響度5）
    center_v = alt.Chart(pd.DataFrame({"労力": [5]})).mark_rule(color="gray", strokeDash=[4, 4]).encode(
        x="労力:Q"
    )
    center_h = alt.Chart(pd.DataFrame({"影響度": [5]})).mark_rule(color="gray", strokeDash=[4, 4]).encode(
        y="影響度:Q"
    )

    chart = (points + labels + center_v + center_h).properties(width=600, height=400)
    st.altair_chart(chart, width="stretch")
    
    # 補助説明
    st.info("💡 **おすすめゾーン**: 影響度が高く（上）、労力が低い（左）のタスクは、最優先候補です。")
else:
    st.info("👆 上記のフォームからタスクを追加してください。")
