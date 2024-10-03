import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler, MaxAbsScaler

from src.exception import CustomException
from src.logger import logging

import os

from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_ob_file_path=os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    def get_transformer_object(self):
        try:
            numerical_columns = ['AGE', 'INCOME']
            categorical_columns = ['GENDER','VETERAN','substanceabuse','completed','probation']

            num_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="median")),
                    ("scaler",MaxAbsScaler())
                ])

            cat_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ("encoder",OneHotEncoder(handle_unknown="ignore",sparse_output=True))
                ]
            )

            logging.info("Column transformer initiated")

            preprocessor=ColumnTransformer(
                transformers=[
                    ("num",num_pipeline,numerical_columns),
                    ("cat",cat_pipeline,categorical_columns)
                ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e,sys)

    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info("Read train and test done ... obtaining preproc")
            logging.info(f"Applying preprocessor to train and test data")

            preprocessing_obj=self.get_transformer_object()
            target_column_name='NIGHTS'
            numerical_columns = ['AGE', 'INCOME']

            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]

            logging.info(f"apply preprocessor to train data")

            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]

            test_arr = np.c_[
                input_feature_test_arr, np.array(target_feature_test_df)
            ]

            save_object(
                file_path=self.data_transformation_config.preprocessor_ob_file_path,
                obj=preprocessing_obj
            )

            logging.info(f"[ Shape of input_feature_train_arr: {input_feature_train_arr.shape} ]")

            logging.info(f"Train Array Shape: {train_arr.shape}")
            logging.info(f"Train Array:\n {train_arr}")

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_ob_file_path
            )



        except Exception as e:
            raise CustomException(e,sys)
