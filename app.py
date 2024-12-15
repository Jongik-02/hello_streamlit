import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

claim_df = pd.read_csv('claim.csv')
cntt_df = pd.read_csv('cntt.csv')
cust_df = pd.read_csv('cust.csv')

st.title("보험데이터 분석")
st.sidebar.header("목록")

analysis_type = st.sidebar.selectbox(
    "원하는 분석 종류를 선택해 주세요 :",
    ["Customer Analysis", "Claim Analysis", "Contract Analysis"]
)

if analysis_type == "Customer Analysis":
    st.header("Customer Analysis")
    
    gender_counts = cust_df['SEX'].value_counts()
    gender_labels = ["Male", "Female"] if 1 in gender_counts.index else ["Female", "Male"]
    st.subheader("성별 분포")
    fig, ax = plt.subplots()
    ax.pie(gender_counts, labels=gender_labels, autopct="%1.1f%%", startangle=90)
    st.pyplot(fig)

    st.header("나이 분포")
    age_data = cust_df['AGE']
    fig, ax = plt.subplots()
    ax.hist(age_data, bins=20, color='blue', alpha=0.7)
    ax.set_title('Age Distribution')
    ax.set_xlabel('Age')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)


    st.subheader("결혼 여부 분포")
    st.bar_chart(cust_df['WEDD_YN'].value_counts())

elif analysis_type == "Claim Analysis":
    st.header("Claim Analysis")
    
   
    st.subheader("보험금 청구 금액 분포")
    dmnd_summary = claim_df['DMND_AMT'].describe()
    st.write(dmnd_summary)
    total_claim_amount = claim_df['DMND_AMT'].sum()
    st.metric(label="총 보험금 금액", value=f"{total_claim_amount:,.0f}")
    
    fig, ax = plt.subplots()
    ax.hist(claim_df['DMND_AMT'], bins=50, color='green', alpha=0.7)
    ax.set_title("클레임 분포")
    ax.set_xlabel("클레임 양")
    ax.set_ylabel("빈도")

    st.subheader("보험금 청구 상위 10명")
    customer_claims = claim_df.groupby('CUST_ID')['DMND_AMT'].sum().reset_index()
    top_customers = customer_claims.sort_values(by='DMND_AMT', ascending=False).head(10)
    st.table(top_customers)

elif analysis_type == "Contract Analysis":
    st.header("Contract Analysis")
    
    # 보험 상품별 총 청구 금액
    st.subheader("보험 상품 별 총 청구 금액")
    contract_claims = pd.merge(cntt_df, claim_df, on=['CUST_ID', 'POLY_NO'], how='inner')
    product_claims = contract_claims.groupby('GOOD_CLSF_CDNM')['DMND_AMT'].sum().reset_index()
    st.bar_chart(product_claims.set_index('GOOD_CLSF_CDNM'))
    
    # 손실 계약 상위 10개
    st.subheader("손실 계약 상위 10개")
    contract_claims['LOSS'] = contract_claims['DMND_AMT'] - contract_claims['SUM_ORIG_PREM']
    high_loss_contracts = contract_claims.sort_values(by='LOSS', ascending=False).head(10)
    st.table(high_loss_contracts)

st.sidebar.info("추가 분석 내용은 스크롤을 아래로 내려주세요.")
st.title("고급 보험 데이터 분석")
st.sidebar.header("추가 분석")

# Sidebar 선택
analysis_type = st.sidebar.selectbox(
    "원하는 분석 종류를 선택해 주세요:",
    ["Regional Distribution", "Accident Type Claims", "Product Summary", "Housewife Claims Analysis"]
)

if analysis_type == "Regional Distribution":
    st.header("고객 지역 분석")
    region_counts = cust_df['CTPR'].value_counts()
    st.bar_chart(region_counts)
    st.write("각 다른 지역에서의 고객 분포.")

elif analysis_type == "Accident Type Claims":
    st.header("사고 유형 클레임")
    accident_claims = claim_df.groupby('ACCI_DVSN')['DMND_AMT'].sum().reset_index()
    accident_claims.columns = ['Accident Type', 'Total Claim Amount']
    st.bar_chart(accident_claims.set_index('Accident Type'))
    st.write("1 : 재해     2 : 교통재해      3: 질병.")

elif analysis_type == "Product Summary":
    st.header("보험 상품 요약")
    product_summary = cntt_df.groupby('GOOD_CLSF_CDNM').agg({
        'SUM_ORIG_PREM': ['sum', 'mean'],
        'MAIN_INSR_AMT': ['sum', 'mean']
    }).reset_index()
    product_summary.columns = ['Product Type', 'Total Premium', 'Average Premium', 
                               'Total Insurance Amount', 'Average Insurance Amount']
    st.dataframe(product_summary)
    st.write("다양한 상품 유형에 대한 보험료 및 보험 금액 요약.")

elif analysis_type == "Housewife Claims Analysis":
    st.header("주부 클레임 분석")
    housewife_claims = cust_df[cust_df['OCCP_GRP_2'] == '주부']['CUST_ID']
    housewife_claim_data = claim_df[claim_df['CUST_ID'].isin(housewife_claims)]
    housewife_total_claims = housewife_claim_data['DMND_AMT'].sum()
    total_claims = claim_df['DMND_AMT'].sum()
    housewife_claim_percentage = (housewife_total_claims / total_claims) * 100

    st.write(f"Total Claims by Housewives: {housewife_total_claims:,}")
    st.write(f"Total Claims: {total_claims:,}")
    st.write(f"주부들의 보험금 청구 비율: {housewife_claim_percentage:.2f}%")

