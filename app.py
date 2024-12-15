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

st.title("Advanced Insurance Data Analysis Dashboard")
st.sidebar.header("Select Additional Analysis")

# Sidebar 선택
analysis_type = st.sidebar.selectbox(
    "Choose the analysis you want to perform:",
    ["Regional Distribution", "Accident Type Claims", "Product Summary", "Housewife Claims Analysis"]
)

if analysis_type == "Regional Distribution":
    st.header("Customer Region Distribution")
    region_counts = cust_df['CTPR'].value_counts()
    st.bar_chart(region_counts)
    st.write("Distribution of customers across different regions.")

elif analysis_type == "Accident Type Claims":
    st.header("Accident Type Claims")
    accident_claims = claim_df.groupby('ACCI_DVSN')['DMND_AMT'].sum().reset_index()
    accident_claims.columns = ['Accident Type', 'Total Claim Amount']
    st.bar_chart(accident_claims.set_index('Accident Type'))
    st.write("Total claim amounts for each type of accident.")

elif analysis_type == "Product Summary":
    st.header("Insurance Product Summary")
    product_summary = cntt_df.groupby('GOOD_CLSF_CDNM').agg({
        'SUM_ORIG_PREM': ['sum', 'mean'],
        'MAIN_INSR_AMT': ['sum', 'mean']
    }).reset_index()
    product_summary.columns = ['Product Type', 'Total Premium', 'Average Premium', 
                               'Total Insurance Amount', 'Average Insurance Amount']
    st.dataframe(product_summary)
    st.write("Summary of premiums and insurance amounts for different product types.")

elif analysis_type == "Housewife Claims Analysis":
    st.header("Housewife Claims Analysis")
    housewife_claims = cust_df[cust_df['OCCP_GRP_2'] == '주부']['CUST_ID']
    housewife_claim_data = claim_df[claim_df['CUST_ID'].isin(housewife_claims)]
    housewife_total_claims = housewife_claim_data['DMND_AMT'].sum()
    total_claims = claim_df['DMND_AMT'].sum()
    housewife_claim_percentage = (housewife_total_claims / total_claims) * 100

    st.write(f"Total Claims by Housewives: {housewife_total_claims:,}")
    st.write(f"Total Claims: {total_claims:,}")
    st.write(f"Percentage of Claims by Housewives: {housewife_claim_percentage:.2f}%")

st.sidebar.info("Use the dropdown above to explore different analyses.")
