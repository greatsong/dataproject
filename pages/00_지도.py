import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

st.set_page_config(page_title="서울 관광지 Top 10 (외국인 선호)", page_icon="🗺️", layout="wide")

st.title("🗺️ 외국인들이 좋아하는 서울의 주요 관광지 Top 10")
st.markdown(
    "서울 방문 외국인들이 많이 찾는 대표 명소 10곳을 폴리움(Folium) 지도로 한눈에 볼 수 있게 만들었습니다.\n"
    "마커를 눌러 간단한 설명과 주소를 확인해 보세요. 사이드바에서 지도 스타일과 표시 옵션을 바꿀 수 있어요."
)

# --- 데이터 (Top 10) ---
data = [
    {"rank": 1, "name_kr": "경복궁", "name_en": "Gyeongbokgung Palace", "lat": 37.579617, "lon": 126.977041,
     "desc": "조선의 법궁. 수문장 교대식으로 유명.", "addr": "서울 종로구 사직로 161", "tag": "궁궐/역사"},
    {"rank": 2, "name_kr": "북촌한옥마을", "name_en": "Bukchon Hanok Village", "lat": 37.582604, "lon": 126.983998,
     "desc": "전통 한옥 골목 풍경 명소.", "addr": "서울 종로구 계동길 일대", "tag": "전통마을"},
    {"rank": 3, "name_kr": "명동거리", "name_en": "Myeongdong Shopping Street", "lat": 37.563757, "lon": 126.985302,
     "desc": "쇼핑과 길거리 음식의 중심지.", "addr": "서울 중구 명동길 일대", "tag": "쇼핑"},
    {"rank": 4, "name_kr": "N서울타워(남산타워)", "name_en": "N Seoul Tower (Namsan)", "lat": 37.551169, "lon": 126.988227,
     "desc": "서울 전경을 내려다보는 전망 명소.", "addr": "서울 용산구 남산공원길 105", "tag": "전망/랜드마크"},
    {"rank": 5, "name_kr": "홍대거리", "name_en": "Hongdae (Hongik Univ. Area)", "lat": 37.557192, "lon": 126.922675,
     "desc": "젊음과 거리공연, 카페 문화의 중심.", "addr": "서울 마포구 홍익로 일대", "tag": "거리문화"},
    {"rank": 6, "name_kr": "인사동", "name_en": "Insadong", "lat": 37.574014, "lon": 126.985829,
     "desc": "전통 공예품과 찻집이 모여 있는 거리.", "addr": "서울 종로구 인사동길", "tag": "전통거리"},
    {"rank": 7, "name_kr": "롯데월드타워 & 석촌호수", "name_en": "Lotte World Tower & Seokchon Lake", "lat": 37.513068, "lon": 127.102528,
     "desc": "대한민국 최고층 타워와 호수 산책.", "addr": "서울 송파구 올림픽로 300", "tag": "전망/쇼핑"},
    {"rank": 8, "name_kr": "동대문디자인플라자(DDP)", "name_en": "Dongdaemun Design Plaza (DDP)", "lat": 37.566508, "lon": 127.009072,
     "desc": "자하 하디드가 설계한 미래적 건축물.", "addr": "서울 중구 을지로 281", "tag": "건축/디자인"},
    {"rank": 9, "name_kr": "광장시장", "name_en": "Gwangjang Market", "lat": 37.570127, "lon": 126.999559,
     "desc": "빈대떡, 마약김밥 등 길거리 음식 천국.", "addr": "서울 종로구 창경궁로 88", "tag": "전통시장/음식"},
    {"rank": 10, "name_kr": "청계천(청계광장)", "name_en": "Cheonggyecheon Stream (Cheonggye Plaza)", "lat": 37.569356, "lon": 126.977000,
     "desc": "도심 속 산책로와 야경 명소.", "addr": "서울 종로구 세종대로 99 앞", "tag": "산책/야경"},
]

df = pd.DataFrame(data)

with st.sidebar:
    st.header("표시 옵션")
    base_tile = st.selectbox("지도 스타일",
                             ["OpenStreetMap", "CartoDB positron", "CartoDB dark_matter", "Stamen Terrain", "Stamen Toner"])
    use_cluster = st.checkbox("마커 클러스터 사용", value=True)
    show_table = st.checkbox("데이터 표 보기", value=False)
    st.caption("Tip: 지도를 드래그/확대하고, 마커를 눌러 정보를 확인하세요.")

# 지도 중심
center = [37.5665, 126.9780]
m = folium.Map(location=center, zoom_start=12, tiles=base_tile)

if use_cluster:
    cluster = MarkerCluster().add_to(m)
    parent = cluster
else:
    parent = m

for _, row in df.iterrows():
    popup_html = f"""
    <div style='width:220px'>
        <h4>#{row['rank']} {row['name_kr']}<br><span style='font-size:12px;color:#888'>{row['name_en']}</span></h4>
        <p>{row['desc']}</p>
        <p><b>주소:</b> {row['addr']}</p>
        <p><b>태그:</b> {row['tag']}</p>
    </div>
    """
    folium.Marker(
        location=[row['lat'], row['lon']],
        popup=folium.Popup(popup_html, max_width=260),
        tooltip=f"#{int(row['rank'])} {row['name_kr']}",
        icon=folium.Icon(icon="star", prefix="fa")
    ).add_to(parent)

st_folium(m, width=None, height=650)

if show_table:
    st.subheader("데이터 표")
    st.dataframe(df[["rank", "name_kr", "name_en", "tag", "addr"]].sort_values("rank"))

st.markdown("---")
st.markdown("참고: 이 Top 10 목록은 서울을 대표하는 명소를 예시로 구성했습니다. 필요에 따라 `data` 리스트를 수정하면 됩니다.")
