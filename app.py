from fastapi import FastAPI 
from fastapi.responses import JSONResponse
from pydantic import BaseModel ,Field ,computed_field 
from typing import Literal ,Annotated
import pickle
import pandas as pd

with open('model.pkl','rb') as f:
    model = pickle.load(f)
    
tier1 = ['Mumbai','Delhi','Bangalore','Chennai','Kolkata','Hyderabad','Pune']
tier2 = [
        "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
        "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
        "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
        "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
        "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
        "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]

app = FastAPI()

class UserInput(BaseModel):
    age:Annotated[int,Field(...,gt=0,lt=150,description="Age of user",examples=["22"])]
    weight:Annotated[float,Field(...,gt=0,lt=200,description="Weight in Kg",examples=["55.5"])]
    height:Annotated[float,Field(...,gt=0,lt=200,description="Height of user",examples=["55.5"])]
    income_lpa:Annotated[float,Field(...,gt=0,description="Incode in Rs.",examples=["10.2"])]
    smoker:Annotated[bool,Field(...,description="Do the Smoking user?",examples=["True"])]
    city:Annotated[str,Field(...,max_length=50,description="City of user",examples=["Pune"])]
    occupation:Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'],Field(...,description="Occupation  of user")]
    
    @computed_field
    @property
    def bmi(self) ->float:
        return round(self.weight/(self.height**2),3)
    
    @computed_field
    @property
    def life_style_risk(self) -> str:
        if self.smoker and self.bmi >30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"
        
    @computed_field
    @property
    def city_tire(self)->str:
        if self.city in tier1: return 1
        elif self.city in tier2: return 2
        else : return 3
    
    @computed_field
    @property
    def age_group(self)->str:
        if self.age <25:
            return "young"
        elif self.age<45:
            return "adult"
        elif self.age <60:
            return "middle_age"
        return "senior"

@app.post('/predict')
def predict(data : UserInput):
    
    inputs = pd.DataFrame([{
        "bmi" : data.bmi,
        "life_style_risk" : data.life_style_risk,
        "city_tier" : data.city_tire,
        "age_group" : data.age_group,
        "income_lpa" : data.income_lpa,
        "occupation" : data.occupation
    }])
    
    predict_ = model.predict(inputs)[0]
    return JSONResponse(status_code=200,content={"prediction" : predict_})