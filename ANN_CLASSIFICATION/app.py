import numpy as np
import pandas as pd
import pickle
import streamlit as st
import tensorflow as tf
from pathlib import Path
BASE_DIR = Path(__file__).parent
model = tf.keras.models.load_model(BASE_DIR / "model.h5")
with open(BASE_DIR / "label_encoder_geo.pkl", "rb") as file:
    label_encoder_geo = pickle.load(file)

with open(BASE_DIR / "label_encoder_gender.pkl", "rb") as file:
    label_encoder_gender = pickle.load(file)

with open(BASE_DIR / "scaler.pkl", "rb") as file:
    scaler = pickle.load(file)
st.title('Customer Churn Prediction')
geography = st.selectbox(
    'Geography',
    label_encoder_geo.categories_[0]
)
gender = st.selectbox(
    'Gender',
    label_encoder_gender.classes_
)
age = st.slider('Age', 18, 92)
balance = st.number_input('Balance')
credit_score = st.number_input('Credit Score')
estimated_salary = st.number_input('Estimated Salary')
tenure = st.slider('Tenure', 0, 10)
num_of_products = st.slider('Number of Products', 1, 4)
has_cr_cred = st.selectbox('Has Credit Card', [0, 1])
is_active_member = st.selectbox('Is Active Member', [0, 1])
input_data = pd.DataFrame({
    'CreditScore': [credit_score],
    'Geography': [geography],
    'Gender': [gender],
    'Age': [age],
    'Tenure': [tenure],
    'Balance': [balance],
    'NumOfProducts': [num_of_products],
    'HasCrCard': [has_cr_cred],
    'IsActiveMember': [is_active_member],
    'EstimatedSalary': [estimated_salary]
})

input_data['Gender'] = label_encoder_gender.transform(
    input_data['Gender']
)

geo_encoded = label_encoder_geo.transform(
    [[geography]]
).toarray()

geo_encoded_df = pd.DataFrame(
    geo_encoded,
    columns=label_encoder_geo.get_feature_names_out(['Geography'])
)
input_data = pd.concat(
    [input_data, geo_encoded_df],
    axis=1
)

input_data.drop('Geography', axis=1, inplace=True)

input_data = input_data.reindex(
    columns=scaler.feature_names_in_,
    fill_value=0
)

input_data_scaled = scaler.transform(input_data)
prediction = model.predict(input_data_scaled)
prediction_proba = prediction[0][0]

st.write(f'Churn probability: {prediction_proba:.2%}')

if prediction_proba > 0.5:
    st.error('The customer is likely to churn.')
else:
    st.success('The customer is not likely to churn.')