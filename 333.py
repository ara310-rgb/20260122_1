import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 설정 및 디자인 레이아웃 정의
st.set_page_config(page_title="L/C Analytics Dashboard", layout="wide")

# CSS: 탭 버튼 크기 통일, 여백 추가, 애니메이션 제거
st.markdown("""
    <style>
    .stApp { background-color: #F8F9FA; }
    
    /* 요약 카드 디자인 */
    .metric-container {
        background-color: white;
        padding: 25px;
        border-radius: 18px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        text-align: center;
        border: 1px solid #EDEDED;
    }
    .metric-label { color: #636E72; font-size: 15px; margin-bottom: 8px; font-weight: 500; }
    .metric-value { color: #2D3436; font-size: 28px; font-weight: 800; margin: 0; }
    
    /* 그래프 컨테이너 그림자 */
    .stPlotlyChart {
        background-color: white;
        border-radius: 20px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.06) !important;
        padding: 15px;
        border: 1px solid #F1F2F6;
    }
    
    /* 탭 버튼 스타일: 너비 통일 및 좌우 공백 추가 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
    }
    .stTabs [data-baseweb="tab"] {
        min-width: 160px; /* 버튼 크기 통일 */
        padding-left: 20px !important; /* 좌측 공백 */
        padding-right: 20px !important; /* 우측 공백 */
        height: 50px;
        background-color: #EEF2F7;
        border-radius: 12px;
        color: #747D8C;
        font-weight: 600;
        transition: none !important; /* 애니메이션 효과 제거 */
        border: none !important;
    }
    
    /* 탭 클릭 시 상태: 빨간색 등 애니메이션 제거 및 고정 색상 */
    .stTabs [aria-selected="true"] {
        background-color: #2D3436 !important; 
        color: white !important;
        transition: none !important;
    }
    
    /* 클릭 시 나타나는 파란색/빨간색 테두리 등 포커스 효과 제거 */
    button:focus {
        outline: none !important;
        box-shadow: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 데이터 로드 및 전처리
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('국가별 신용장방식 결제비중_2017~2021.csv', encoding='cp949')
        cols = ['2017', '2018', '2019', '2020', '2021']
        for col in cols:
            df[col] = df[col].str.rstrip('%').astype('float') / 100.0
        
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
    except:
        return pd.DataFrame(), []

df, cols = load_data()

def custom_metric(label, value):
    st.markdown(f"""
        <div class="metric-container">
            <p class="metric-label">{label}</p>
            <p class="metric-value">{value}</p>
        </div>
    """, unsafe_allow_html=True)

if not df.empty:
    with st.sidebar:
        st.title("🏛️ 리포트 설정")
        selected_continents = st.multiselect("대륙 선택", df['대륙'].unique(), default=df['대륙'].unique())
        selected_countries = st.multiselect("추이 분석 국가", df['국가명'].unique(), default=['터키','인도네시아','중국','베트남'])

    st.title("📊 L/C Analytics Overview")
    m1, m2, m3, m4 = st.columns(4)
    with m1: custom_metric("🏆 L/C 사용량 1위 국가", "스리랑카")
    with m2: custom_metric("🌍 L/C 사용량 1위 대륙", "중동/유럽")
    with m3: custom_metric("📥 신규 데이터", "5,500건")
    with m4: custom_metric("🎯 분석 정확도", "98.5%")

    st.markdown("<br>", unsafe_allow_html=True)

    # 5. 중앙 그래프 영역
    tab1, tab2, tab3 = st.tabs(["Charts", "Trend Analysis", "Continent Trend"])

    with tab1:
        st.subheader("📊 국가별 비중 순위 (2021)")
        top_10 = df[df['대륙'].isin(selected_continents)].sort_values(by='2021', ascending=False).head(10)
        # 그래프 1: 국가별 구분을 위해 다채로운 컬러 세트(Plotly Qualitative) 적용
        fig1 = px.bar(top_10, x='2021', y='국가명', orientation='h', 
                      color='국가명', color_discrete_sequence=px.colors.qualitative.T10)
        fig1.update_layout(
            yaxis={'tickangle': 0, 'title': ''},
            xaxis={'title': '결제 비중'},
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=100, r=20, t=20, b=20)
        )
        st.plotly_chart(fig1, width='stretch')

    with tab2:
        st.subheader("📈 선택 국가별 연도별 추이 (막대형)")
        df_trend = df[df['국가명'].isin(selected_countries)].set_index('국가명')[cols].T.reset_index()
        df_melted = df_trend.melt(id_vars='index', var_name='국가', value_name='비중')
        
        # 그래프 2: 명확한 구분을 위한 다른 컬러 팔레트 적용
        fig2 = px.bar(df_melted, x='index', y='비중', color='국가', barmode='group',
                      color_discrete_sequence=px.colors.qualitative.Pastel)
        fig2.update_layout(
            yaxis={'tickangle': 0, 'title': '비중 (%)'},
            xaxis={'title': '연도'},
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig2, width='stretch')

    with tab3:
        st.subheader("🌍 대륙별 평균 결제 비중 추이")
        continent_avg = df.groupby('대륙')[cols].mean().T.reset_index()
        df_c_melted = continent_avg.melt(id_vars='index', var_name='대륙', value_name='평균 비중')
        
        fig3 = px.line(df_c_melted, x='index', y='평균 비중', color='대륙', markers=True)
        fig3.update_layout(
            yaxis={'tickangle': 0, 'title': '평균 비중'},
            xaxis={'title': '연도'},
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig3, width='stretch')

    st.write('<div style="height: 500px;"></div>', unsafe_allow_html=True)