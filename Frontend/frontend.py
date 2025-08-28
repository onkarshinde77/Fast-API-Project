import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/predict/"

st.title("Insurence Premium Category Predictor")
st.markdown("Enter your detainl below :")

age = st.number_input("Age",max_value=150,min_value=1,value=30)
wt = st.number_input("Weight (Kg)",min_value=1,value=50)
ht = st.number_input("Height (m)",min_value=1,value=55)
income = st.number_input("Annual Income (LPA)",value=10)
smoker = st.selectbox("Are you smoker?",options=[True,False])
city = st.text_input("City",value="Pune")
occupation = st.selectbox("Occupation",options=['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'])

if st.button("Predict Premium Category") :
    input_data = {
        "age" : age,
        "weight" : wt,
        "height" : ht,
        "income_lpa" : income,
        "smoker" : smoker,
        "city" : city,
        "occupation" : occupation
    }
    
    try : 
        responce = requests.post(API_URL,json=input_data)
        if responce.status_code==200:
            result = responce.json()
            st.success(f"Predict Category : **{result['prediction']}**")
        else:
            st.error(f"API Error : {responce.status_code} - {responce.text}")
    except:
        st.error("Could not connect to fast API Server")
        
    
