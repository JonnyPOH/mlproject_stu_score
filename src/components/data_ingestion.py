import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.components.data_transformation import DataTransformationConfig, DataTransformation
from src.components.data_cleaning import DataCleaning

@dataclass
class DataIngestionConfig:
    train_data_path: str=os.path.join('artifacts',"train.csv")
    test_data_path: str=os.path.join('artifacts',"test.csv")
    raw_data_path: str=os.path.join("artifacts","data.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()
        self.data_cleaning = DataCleaning()

    def initiate_data_ingestion(self,columns_to_drop=None):
        logging.info("Entered the data ingestion method")
        try:
            df=pd.read_csv('/home/jonnyoh/code/JonnyPOH/portfolio/projects/mlproject_stu_score/data/homeless_prep.csv')
            logging.info('data read successfully')

            cleaned_df = self.data_cleaning.clean_data(df, drop_columns=columns_to_drop)
            logging.info('data cleaned successfully')

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)

            cleaned_df.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            logging.info('train test split initiated')
            train_set,test_set=train_test_split(cleaned_df,test_size=0.2,random_state=42)
            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info('ingestion of the data is completed')

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            raise CustomException(e,sys)

if __name__=="__main__":
    data_ingestion=DataIngestion()
    train_data, test_data = data_ingestion.initiate_data_ingestion()

    columns_to_drop=['CLIENT_KEY','assistancetype','required']
    data_transformation=DataTransformation()
    data_transformation.initiate_data_transformation(train_data,test_data)
