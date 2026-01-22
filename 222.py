import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 설정
st.set_page_config(page_title="L/C 결제 비중 대시보드", layout="wide")

# 2. 스타일 정의 (정적 디자인 및 글래스모피즘)
st.markdown("""
    <style>
    .main { background-color: #1A1A1B; color: #E0C097; }
    .glass-card {
        background: rgba(62, 39, 35, 0.1);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
    }
    h1, h2, h3 { color: #D4AF37 !important; font-weight: 700; }
    [data-testid="stMetricValue"] { color: #D4AF37 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. 데이터 로드 및 전처리
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('국가별 신용장방식 결제비중_2017~2021.csv', encoding='cp949')
        cols = ['2017', '2018', '2019', '2020', '2021']
        for col in cols:
            df[col] = df[col].str.rstrip('%').astype('float') / 100.0
        
        # '대륙' 맵핑 데이터
        continent_map = {
            '중국': '아시아', '인도네시아': '아시아', '대만': '아시아', '일본': '아시아', '베트남': '아시아',
            '인도': '아시아', '싱가포르': '아시아', '말레이시아': '아시아', '필리핀': '아시아', '태국': '아시아',
            '미국': '미주', '캐나다': '미주', '브라질': '미주', '멕시코': '미주', '아르헨티나': '미주', '칠레': '미주',
            '독일': '유럽', '프랑스': '유럽', '영국': '유럽', '이탈리아': '유럽', '폴란드': '유럽', '러시아': '유럽',
            '터키': '중동/유럽', '아랍에미리트 연합': '중동', '사우디아라비아': '중동', '쿠웨이트': '중동',
            '나이지리아': '아프리카', '남아프리카공화국': '아프리카', '이집트': '아프리카'
        }
        df['대륙'] = df['국가명'].map(continent_map).fillna('기타')
        return df, cols
    except FileNotFoundError:
        st.error("데이터 파일을 찾을 수 없습니다. 경로를 확인해주세요.")
        return pd.DataFrame(), []

df, cols = load_data()

if not df.empty:
    # 4. 사이드바
    with st.sidebar:
        st.header("📜 리포트 필터")
        selected_continents = st.multiselect("분석 대륙 선택", df['대륙'].unique(), default=df['대륙'].unique())
        selected_countries = st.multiselect("관심 국가 선택", df['국가명'].unique(), default=['터키','인도네시아','중국','베트남'])

    # 5. 메인 레이아웃
    st.title("🏛️ 글로벌 L/C 결제 트렌드 분석 리포트")
    
    # 상단 요약 섹션
    c1, c2 = st.columns(2)
    with c1:
        st.metric(label="🏆 L/C 사용량 1위 국가", value="스리랑카")
    with c2:
        st.metric(label="🌍 L/C 사용량 1위 대륙", value="중동/유럽")

    st.divider()

    # 중앙 탭 레이아웃
    tab1, tab2, tab3 = st.tabs(["📊 국가별 순위", "📈 주요국 추이", "🌍 대륙별 평균"])

    with tab1:
        st.subheader("대륙별 L/C 결제 비중 상위 10개국")
        top_10 = df[df['대륙'].isin(selected_continents)].sort_values(by='2021', ascending=False).head(10)
        fig1 = px.bar(top_10, x='2021', y='국가명', orientation='h', 
                      color='2021', color_continuous_scale='Reds')
        fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#E0C097")
        st.plotly_chart(fig1, width='stretch')

    with tab2:
        st.subheader("선택 국가별 연도별 추이")
        df_trend = df[df['국가명'].isin(selected_countries)].set_index('국가명')[cols].T
        fig2 = px.line(df_trend, markers=True)
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#E0C097")
        st.plotly_chart(fig2, width='stretch')

    with tab3:
        st.subheader("대륙별 L/C 결제 비중 평균 추이")
        continent_avg = df.groupby('대륙')[cols].mean().T
        fig3 = px.line(continent_avg, markers=True)
        fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#E0C097")
        st.plotly_chart(fig3, width='stretch')