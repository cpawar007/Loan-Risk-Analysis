import streamlit as st
import pandas as pd
import joblib
import os
import requests

st.set_page_config(page_title="Loan Risk Predictor", page_icon="💰", layout="centered")

MODEL_URL = "https://drive.google.com/uc?id=1hU6juGY2-nzAXLxfffWq75EOvb5Wq82X"
MODEL_PATH = "loan_risk_model_compressed.pkl"

if not os.path.exists(MODEL_PATH):
    with st.spinner("Downloading model... please wait ⏳"):
        r = requests.get(MODEL_URL)
        with open(MODEL_PATH, "wb") as f:
            f.write(r.content)

model = joblib.load(MODEL_PATH)

st.title("💰 Loan Risk Prediction System")
st.markdown("Enter applicant details to predict **loan risk & approved amount**")

age = st.number_input("Age", 18, 100, 30)
income = st.number_input("Annual Income", 0, value=50000)
emp = st.number_input("Employment Months", 0, value=24)
amount = st.number_input("Loan Amount", 0, value=10000)
intrest = st.number_input("Interest Rate (%)", 0.0, 100.0, 10.0)
status = st.selectbox("Ongoing Loan", [0,1])
default = st.selectbox("Previous Default", [0,1])
history = st.number_input("Credit History (years)", 0, 30, 5)

ownership = st.selectbox("House Ownership", ["OTHER", "OWN", "RENT","MORTGAGE"])
intend = st.selectbox("Loan Purpose", ["PERSONAL","EDUCATION","MEDICAL","VENTURE","HOMEIMPROVEMENT","DEBTCONSOLIDATION"])
grade = st.selectbox("Credit Grade", ["A","B","C","D","E","F","G"])

new_data = pd.DataFrame({
    'age':[age],
    'income':[income],
    'emp':[emp],
    'amount':[amount],
    'intrest':[intrest],
    'status':[status],
    'default':[default],
    'history':[history],
    'ownership_OTHER':[1 if ownership=="OTHER" else 0],
    'ownership_OWN':[1 if ownership=="OWN" else 0],
    'ownership_RENT':[1 if ownership=="RENT" else 0],
    'intend_EDUCATION':[1 if intend=="EDUCATION" else 0],
    'intend_HOMEIMPROVEMENT':[1 if intend=="HOMEIMPROVEMENT" else 0],
    'intend_MEDICAL':[1 if intend=="MEDICAL" else 0],
    'intend_PERSONAL':[1 if intend=="PERSONAL" else 0],
    'intend_VENTURE':[1 if intend=="VENTURE" else 0],
    'grade_B':[1 if grade=="B" else 0],
    'grade_C':[1 if grade=="C" else 0],
    'grade_D':[1 if grade=="D" else 0],
    'grade_E':[1 if grade=="E" else 0],
    'grade_F':[1 if grade=="F" else 0],
    'grade_G':[1 if grade=="G" else 0]
})

if st.button("Predict Loan Risk"):
    risk = model.predict(new_data)[0]

    if risk <= 20:
        category = "Very Low"
        approved = amount
        color = "green"
    elif risk <= 40:
        category = "Low"
        approved = amount * 0.9
        color = "limegreen"
    elif risk <= 60:
        category = "Medium"
        approved = amount * 0.7
        color = "orange"
    elif risk <= 80:
        category = "High"
        approved = amount * 0.4
        color = "orangered"
    else:
        category = "Very High"
        approved = 0
        color = "red"

    st.markdown("---")
    st.metric("Predicted Risk", f"{risk:.2f}")
    st.markdown(f"**Risk Category:** <span style='color:{color}; font-size:22px'>{category}</span>", unsafe_allow_html=True)
    st.metric("Approved Loan Amount", f"₹ {approved:,.0f}")
