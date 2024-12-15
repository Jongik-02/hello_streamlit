import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 데이터 로드
claim_df = pd.read_csv('claim.csv')
cntt_df = pd.read_csv('cntt.csv')
cust_df = pd.read_csv('cust.csv')

# Streamlit 대시보드 구성
st.title("Insurance Data Analysis Dashboard")
st.sidebar.header("Select Analysis")

# Sidebar 선택
analysis_type = st.sidebar.selectbox(
    "Choose the analysis you want to perform:",
    ["Customer Characteristics", "Claim Analysis", "Contract Analysis"]
)

if analysis_type == "Customer Characteristics":
    st.header("Customer Characteristics")
    
    # 성별 분포
    gender_counts = cust_df['SEX'].value_counts()
    gender_labels = ["Male", "Female"] if 1 in gender_counts.index else ["Female", "Male"]
    st.subheader("Gender Distribution")
    fig, ax = plt.subplots()
    ax.pie(gender_counts, labels=gender_labels, autopct="%1.1f%%", startangle=90)
    st.pyplot(fig)

    # 나이 분포
    st.subheader("Age Distribution")
    age_hist = cust_df['AGE'].plot(kind='hist', bins=20, alpha=0.7, color='blue')
    plt.xlabel("Age")
    plt.ylabel("Frequency")
    st.pyplot(plt)

    # 결혼 여부 분포
    st.subheader("Marital Status")
    st.bar_chart(cust_df['WEDD_YN'].value_counts())

elif analysis_type == "Claim Analysis":
    st.header("Claim Analysis")
    
    # 청구 금액 분포
    st.subheader("Claim Amount Distribution")
    st.write(claim_df['DMND_AMT'].describe())
    st.bar_chart(claim_df['DMND_AMT'].value_counts(bins=10))

    # 높은 청구 금액 상위 10명
    st.subheader("Top 10 Customers by Claim Amount")
    customer_claims = claim_df.groupby('CUST_ID')['DMND_AMT'].sum().reset_index()
    top_customers = customer_claims.sort_values(by='DMND_AMT', ascending=False).head(10)
    st.table(top_customers)

elif analysis_type == "Contract Analysis":
    st.header("Contract Analysis")
    
    # 보험 상품별 총 청구 금액
    st.subheader("Claims by Insurance Product")
    contract_claims = pd.merge(cntt_df, claim_df, on=['CUST_ID', 'POLY_NO'], how='inner')
    product_claims = contract_claims.groupby('GOOD_CLSF_CDNM')['DMND_AMT'].sum().reset_index()
    st.bar_chart(product_claims.set_index('GOOD_CLSF_CDNM'))
    
    # 손실 계약 상위 10개
    st.subheader("Top 10 Loss-Making Contracts")
    contract_claims['LOSS'] = contract_claims['DMND_AMT'] - contract_claims['SUM_ORIG_PREM']
    high_loss_contracts = contract_claims.sort_values(by='LOSS', ascending=False).head(10)
    st.table(high_loss_contracts)

st.sidebar.info("Use the dropdown above to explore different analyses.")
