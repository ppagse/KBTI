import streamlit as st
import pandas as pd
from distance import kbti_distance
from datas import questions, type_labels

# 리커트 척도 옵션 및 점수
likert_pairs = list(zip(
    ["전혀 그렇지 않다", "그렇지 않다", "약간 그렇지 않다", "보통이다", "약간 그렇다", "그렇다", "매우 그렇다"],
    [0, 1, 3, 5, 7, 9, 10]
))

# 쿼리 파라미터
page = st.query_params.get("page", "question")

# 세션 초기화
if "responses" not in st.session_state:
    st.session_state.responses = {}

# -------------------------
# 설문 페이지
# -------------------------
if page == "question":
    st.title("KBTI 유형테스트")

    for idx, q in enumerate(questions):
        st.write(f"**Q{idx + 1}. {q['q']}**")
        options = [label for label, _ in likert_pairs]
        selected_label = st.radio(
            label="",
            options=options,
            key=f"q_{idx}"
        )
        # 선택된 라벨에 해당하는 점수 저장
        selected_score = dict(likert_pairs)[selected_label]
        st.session_state.responses[idx] = selected_score

    if st.button("결과 보기"):
        st.query_params.page = "result"
        st.rerun()

# -------------------------
# 결과 페이지
# -------------------------
elif page == "result":
    st.title("KBTI 테스트 결과")

    score = {"G": 0, "S": 0, "P": 0, "CONT": 0, "A": 0, "O": 0, "CONS": 0, "I": 0}
    for idx, q in enumerate(questions):
        val = st.session_state.responses.get(idx, 0)
        score[q["type"]] += val

    result = kbti_distance(list(score.values()))
    st.subheader(f"당신과 플레이스타일이 맞는 야구선수는: {result}")
    
    df = pd.DataFrame({
        "유형": [type_labels[t] for t in score],
        "점수": [score[t] for t in score]
    })

    # 출력
    st.markdown("### 유형별 점수 분포")
    st.dataframe(df.set_index("유형"), use_container_width=True)
    st.bar_chart(data=df.set_index("유형"))

    if st.button("다시 하기"):
        st.session_state.responses = {}
        st.query_params.page = "question"
        st.rerun()
