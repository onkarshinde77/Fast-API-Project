from schema.user_inputs  import UserInput
import pandas as pd
import pickle

with open('model\model.pkl','rb') as f:
    model = pickle.load(f)

class_label = model.classes_.tolist()

def predict_model(data : UserInput):
    
    inputs = pd.DataFrame([data])
    predict_ = model.predict(inputs)[0]
    prob = model.predict_proba(inputs)[0]
    confidence = max(prob)
    class_prob = dict(zip(class_label,map(lambda x : round(x,4),prob)))
    return {
        'predicted category' : predict_,
        "confidence" : confidence,
        "class_prob" : class_prob
    }

