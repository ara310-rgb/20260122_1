import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

path = '국가별 신용장방식 결제비중_2017~2021.csv'
df = pd.read_csv(path, encoding='cp949')

# 데이터 전처리
cols = ['2017', '2018', '2019', '2020', '2021']
for col in cols :
    df[col] = df[col].str.rstrip('%').astype('float') / 100.0

# 1. 데이터 분석 (기존 로직 유지)
df['Change'] = df['2021'] - df['2017']

# 1-1 데이터 분석. 3번째 권역별 분석을 위한 매핑데이터 만들기
region_map = {
    '중국': '아시아', '인도네시아': '아시아', '대만': '아시아', '일본': '아시아', '베트남': '아시아',
    '인도': '아시아', '싱가포르': '아시아', '말레이시아': '아시아', '필리핀': '아시아', '태국': '아시아',
    '미국': '미주', '캐나다': '미주', '브라질': '미주', '멕시코': '미주', '아르헨티나': '미주', '칠레': '미주',
    '독일': '유럽', '프랑스': '유럽', '영국': '유럽', '이탈리아': '유럽', '폴란드': '유럽', '러시아': '유럽',
    '터키': '중동/유럽', '아랍에미리트 연합': '중동', '사우디아라비아': '중동', '쿠웨이트': '중동',
    '나이지리아': '아프리카', '남아프리카공화국': '아프리카', '이집트': '아프리카'
}
df['권역'] = df['국가명'].map(region_map).fillna('기타')

# 2. 시각화 설정 (한글 폰트)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 그래프 1 : bar chart
plt.figure(figsize=(10,6))
top_10_plot = df.sort_values(by='2021', ascending=False).head(10)
sns.barplot(x='2021', y='국가명', data=top_10_plot, palette='Reds_r', hue='국가명', legend=False)
plt.title('2021년 국가별 L/C 결제 비중 상위 10개국')
plt.xlabel('결제비중')
plt.ylabel('국가명')

# 그래프 2 : Line Chart
target_countries = ['터키','인도네시아','중국','베트남']
df_trend = df[df['국가명'].isin(target_countries)].set_index('국가명')[cols].T

plt.figure(figsize=(10,5))
df_trend.plot(kind='line', marker='o', ax=plt.gca()) 
plt.title('주요국 연도별 L/C 결제 비중 변화')
plt.ylabel('비중')
plt.xlabel('연도')
plt.legend(title='국가')
plt.grid(True)

plt.show()

# 그래프 3 : 대륙별 L/C거래 비중 평균 추이
regional_avg = df.groupby('권역')[cols].mean().T

plt.figure(figsize=(10,5))
regional_avg.plot(kind='line', marker='s', ax=plt.gca())
plt.title('대륙별 L/C 결제 비중 평균 추이')
plt.ylabel('평균 비중')
plt.xlabel('연도')

for region in regional_avg.columns :
    last_value = regional_avg[region].iloc[-1]

plt.legend(title='대륙', bbox_to_anchor=(1.05,1), loc='upper left')
plt.grid(True)
plt.tight_layout()

plt.show()
