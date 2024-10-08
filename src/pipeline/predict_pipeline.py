import sys
import pandas as pd
from src.exception import CustomException
from src.utils import load_object

class PredictPipeline:
    def __init__(self):
        pass

    def predict(self, features):
        try:
            model_path='artifacts/model.pkl'
            preprocessor_path='artifacts/preprocessor.pkl'
            model=load_object(file_path=model_path)
            preprocessor=load_object(file_path=preprocessor_path)
            data_scaled=preprocessor.transform(features)
            preds=model.predict(data_scaled)
            return preds
        except Exception as e:
            raise CustomException(e,sys)

# AGE, GENDER, VETERAN, INCOME, NIGHTS, substanceabuse, completed, probation
class CustomData:
    def __init__(self,
        gender:str,
        age: int,
        substanceabuse: bool,
        veteran:bool,
        probation:bool,
        completed:bool,
        income:int):

        self.gender=gender
        self.age=age
        self.substanceabuse=substanceabuse
        self.veteran=veteran
        self.completed=completed
        self.probation=probation
        self.income=income

    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict = {
                "GENDER": [self.gender],
                "AGE": [self.age],
                "substanceabuse": [self.substanceabuse],
                "VETERAN": [self.veteran],
                "probation": [self.probation],
                "completed": [self.completed],
                "INCOME": [self.income]
            }
            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e,sys)
