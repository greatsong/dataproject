import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------
# 1️⃣ 페이지 설정
# ---------------------------
st.set_page_config(page_title="MBTI by Country", page_icon="🌍", layout="centered")

# ---------------------------
# 2️⃣ 데이터 불러오기
# ---------------------------
@st.cache_data
def load_data():
    return pd.read_csv("countriesMBTI_16types.csv")

df = load_data()

# ---------------------------
# 3️⃣ 국가 선택
# ---------------------------
st.title("🌍 국가별 MBTI 유형 비율 대시보드")
st.markdown("국가를 선택하면 해당 국가의 MBTI 비율을 **Plotly 그래프로** 볼 수 있습니다.")

country_list = df["Country"].unique()
selected_country = st.selectbox("국가를 선택하세요:", sorted(country_list))

# ---------------------------
# 4️⃣ 선택한 국가 데이터 추출
# ---------------------------
country_data = df[df["Country"] == selected_country].iloc[0, 1:]
country_df = pd.DataFrame({
    "MBTI": country_data.index,
    "Ratio": country_data.values
}).sort_values("Ratio", ascending=False)

# ---------------------------
# 5️⃣ 색상 설정 (1등 빨간색 + 나머지 그라데이션)
# ---------------------------
gradient_colors = px.colors.sequential.Blues[::-1]  # 밝은 파랑 → 진한 파랑
# 1등은 빨간색, 나머지는 블루 톤 그라데이션 (16개 중 나머지 15개)
colors = ["#ff4b4b"] + gradient_colors[:len(country_df)-1]

# ---------------------------
# 6️⃣ Plotly 그래프
# ---------------------------
fig = px.bar(
    country_df,
    x="MBTI",
    y="Ratio",
    text=country_df["Ratio"].apply(lambda x: f"{x*100:.1f}%"),
    color=country_df["MBTI"],
    color_discrete_sequence=colors,
)

fig.update_traces(textposition="outside")
fig.update_layout(
    title=f"{selected_country}의 MBTI 유형 분포",
    xaxis_title="MBTI 유형",
    yaxis_title="비율",
    showlegend=False,
    plot_bgcolor="white",
    title_font=dict(size=22, color="#222", family="Arial"),
    font=dict(size=14),
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# 7️⃣ 요약 정보
# ---------------------------
top_type = country_df.iloc[0]
st.subheader("📊 요약 정보")
st.markdown(
    f"**{selected_country}**에서는 **{top_type['MBTI']}** 유형이 가장 많습니다 "
    f"({top_type['Ratio']*100:.2f}%)."
)
st.dataframe(country_df.style.format({"Ratio": "{:.2%}"}))
