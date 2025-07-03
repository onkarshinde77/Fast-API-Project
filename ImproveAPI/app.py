from fastapi import FastAPI 
from fastapi.responses import JSONResponse
from schema.user_inputs import UserInput , Prediction_Responce
from model.predict import predict_model

app = FastAPI()
Model_Flow =  "1.0.0"


@app.get('/')
def index():
    return {"message": "Welcome to Sarkar API"}

@app.get('/health')
def health():
    return {
        "status": "ok",
        "Version": Model_Flow
    }

@app.post('/predict',response_model=Prediction_Responce)
def predict(data : UserInput):
    
    inputs ={
        "bmi" : data.bmi,
        "life_style_risk" : data.life_style_risk,
        "city_tier" : data.city_tire,
        "age_group" : data.age_group,
        "income_lpa" : data.income_lpa,
        "occupation" : data.occupation
    }
    try:
        predict_ = predict_model(inputs)
        return JSONResponse(status_code=200,content={"prediction" : predict_})
    except:
        return JSONResponse(status_code=500,content={"error" : "Internal Server Error"})