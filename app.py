import streamlit as st
import boto3
import json

st.title("Sarcopenia Prediction Interface")

# === Kullanıcıdan veriler alınır ===
AT = st.number_input("AT", format="%.4f")
BMI = st.number_input("BMI", format="%.2f")
CST = st.number_input("Chair Stand Test (CST)", format="%.2f")
Gait_Speed = st.number_input("Gait Speed (m/s)", format="%.2f")
Grip_Str = st.number_input("Grip Strength", format="%.2f")
STAR = st.number_input("STAR Score", format="%.2f")
Waist_Hip_Ratio = st.number_input("Waist-Hip Ratio", format="%.2f")

Age_Group_AGE_60_80 = st.selectbox("Age Group: 60–80?", [0, 1])
DM_Type2 = st.selectbox("Type 2 Diabetes", [0, 1])
Exercise_Status_3_4 = st.selectbox("Exercises 3-4/week", [0, 1])
Gender_M = st.selectbox("Gender: Male?", [0, 1])
OP = st.selectbox("Osteoporosis", [0, 1])
Total_Chronic = st.slider("Total Chronic Diseases", 0, 10, 1)

# === Derived fields ===
AT_STAR_Interaction = AT * STAR
Gender_M_OP_Interaction = Gender_M * OP
CST_Gait_Speed_Interaction = CST * Gait_Speed
BMI_square = BMI ** 2

# === Tüm özellikler bir araya getirilir ===
feature_order = [
    'AT', 'Age_Group_AGE 60-80', 'BMI', 'CST', 'DM_Type2',
    'Exercise_Status_3-4/week', 'Gait_Speed', 'Gender_M', 'Grip_Str', 'OP',
    'STAR', 'Total_Number_of_Chronic_Diseases', 'Waist_Hip_Ratio',
    'AT_STAR_Interaction', 'Gender_M_OP_Interaction',
    'CST_Gait_Speed_Interaction', 'BMI_square'
]

feature_values = [
    AT, Age_Group_AGE_60_80, BMI, CST, DM_Type2,
    Exercise_Status_3_4, Gait_Speed, Gender_M, Grip_Str, OP,
    STAR, Total_Chronic, Waist_Hip_Ratio,
    AT_STAR_Interaction, Gender_M_OP_Interaction,
    CST_Gait_Speed_Interaction, BMI_square
]

# === SageMaker Canvas formatında JSON hazırlanır ===
payload = {
    "data": {
        "features": {
            "names": feature_order,
            "values": [feature_values]
        }
    }
}
if st.button("Predict Sarcopenia Risk"):
    try:
        runtime = boto3.client("sagemaker-runtime", region_name="us-east-1")
        response = runtime.invoke_endpoint(
            EndpointName="canvas-my-sarco-model-deployment-07-09-2025-1-34",  
            ContentType="application/json",
            Body=json.dumps(payload)
        )
        result = json.loads(response['Body'].read().decode())
        st.success(f"Prediction Result: {result}")
    except Exception as e:
        st.error(f"Error calling endpoint: {e}")
