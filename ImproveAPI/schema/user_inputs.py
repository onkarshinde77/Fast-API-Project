from pydantic import BaseModel ,Field ,computed_field ,field_validator
from typing import Literal ,Annotated ,Dict
from user_data.user_data import tier1,tier2

class UserInput(BaseModel):
    age:Annotated[int,Field(...,gt=0,lt=150,description="Age of user",examples=["22"])]
    weight:Annotated[float,Field(...,gt=0,lt=200,description="Weight in Kg",examples=["55.5"])]
    height:Annotated[float,Field(...,gt=0,lt=200,description="Height of user",examples=["55.5"])]
    income_lpa:Annotated[float,Field(...,gt=0,description="Incode in Rs.",examples=["10.2"])]
    smoker:Annotated[bool,Field(...,description="Do the Smoking user?",examples=["True"])]
    city:Annotated[str,Field(...,max_length=50,description="City of user",examples=["Pune"])]
    occupation:Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'],Field(...,description="Occupation  of user")]
    
    @field_validator("city")
    @classmethod
    def city_normal(cls,v:str) ->str:
        return v.strip().title()
    
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

class Prediction_Responce(BaseModel):
    predicted_category:Annotated[str,Field(...,description="prediction of user",examples=["high"])]
    confidence : Annotated[float,Field(...,description="confidence of user",examples=[0.46])]
    class_prob : Annotated[Dict[str,float],Field(...,description="Probability of each posibility",
                                        examples=[{"class_prob": {
                                                        "High": 0.12,
                                                        "Low": 0.42,
                                                        "Medium": 0.46
                                                    }
                                             }])]
    
    