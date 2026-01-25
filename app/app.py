import streamlit as st
import pandas as pd
import joblib

model = joblib.load('loan_risk_model.pkl')

st.set_page_config(page_title="Loan Risk Predictor", page_icon="💰", layout="centered")
st.title("💰 Loan Risk Prediction App")
st.markdown("Enter customer details below to predict loan risk and suggested approved amount.")

age = st.number_input("Age", min_value=18, max_value=100, value=30)
income = st.number_input("Income", min_value=0, value=50000)
emp = st.number_input("Employment Months", min_value=0, value=5)
amount = st.number_input("Loan Amount", min_value=0, value=10000)
intrest = st.number_input("Interest Rate", min_value=0.0, max_value=100.0, value=10.0)
status = st.selectbox("Ongoing Loan", [0,1])
default = st.selectbox("Has Previous Default?", [0, 1])
history = st.number_input("Credit History (years)", min_value=0, max_value=30, value=5)
ownership = st.selectbox("Ownership Type", ["OTHER", "OWN", "RENT","MORTGAGE"])
intend = st.selectbox("Loan Intention", ['PERSONAL', 'EDUCATION', 'MEDICAL', 'VENTURE', 'HOMEIMPROVEMENT','DEBTCONSOLIDATION'])
grade = st.selectbox("Grade", ['D', 'B', 'C', 'A', 'E', 'F', 'G'])

new_data = pd.DataFrame({
    'age': [age],
    'income': [income],
    'emp': [emp],
    'amount': [amount],
    'intrest': [intrest],
    'status': [status],
    'default': [default],
    'history': [history],
    'ownership_OTHER': [1 if ownership=="OTHER" else 0],
    'ownership_OWN': [1 if ownership=="OWN" else 0],
    'ownership_RENT': [1 if ownership=="RENT" else 0],
    'intend_EDUCATION': [1 if intend=="EDUCATION" else 0],
    'intend_HOMEIMPROVEMENT': [1 if intend=="HOMEIMPROVEMENT" else 0],
    'intend_MEDICAL': [1 if intend=="MEDICAL" else 0],
    'intend_PERSONAL': [1 if intend=="PERSONAL" else 0],
    'intend_VENTURE': [1 if intend=="VENTURE" else 0],
    'grade_B': [1 if grade=="B" else 0],
    'grade_C': [1 if grade=="C" else 0],
    'grade_D': [1 if grade=="D" else 0],
    'grade_E': [1 if grade=="E" else 0],
    'grade_F': [1 if grade=="F" else 0],
    'grade_G': [1 if grade=="G" else 0]
})

if st.button("Predict Loan Risk"):
    risk = model.predict(new_data)[0]
    if risk <= 20:
        category = 'Very Low'
        approved_amount = amount
        color = 'green'
    elif risk <= 40:
        category = 'Low'
        approved_amount = amount * 0.9
        color = 'limegreen'
    elif risk <= 60:
        category = 'Medium'
        approved_amount = amount * 0.7
        color = 'orange'
    elif risk <= 80:
        category = 'High'
        approved_amount = amount * 0.4
        color = 'orangered'
    else:
        category = 'Very High'
        approved_amount = 0
        color = 'red'

    st.markdown(f"**Predicted Loan Risk:** {risk:.2f}")
    st.markdown(f"**Risk Category:** <span style='color:{color}'>{category}</span>", unsafe_allow_html=True)
    st.markdown(f"**Approved Loan Amount:** {approved_amount:.2f}")
