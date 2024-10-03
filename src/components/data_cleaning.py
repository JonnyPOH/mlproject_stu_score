import pandas as pd
import sys
from src.exception import CustomException
from src.logger import logging

class DataCleaning:
    def __init__(self):
        pass

    def clean_data(self, df, drop_columns=None):
        try:
            # Remove duplicate rows based on 'CLIENT_KEY'
            df_cleaned = df.drop_duplicates(subset='CLIENT_KEY')
            df_cleaned.reset_index(drop=True, inplace=True)

            logging.info("Removed duplicates based on CLIENT_KEY")

            # Drop 'CLIENT_KEY' and any other unnecessary columns
            df_cleaned = df_cleaned.drop(columns=['CLIENT_KEY'], axis=1, errors='ignore')

            if drop_columns:
                df_cleaned = df_cleaned.drop(columns=drop_columns, axis=1, errors='ignore')
                logging.info(f"Dropped additional columns: {drop_columns}")

            return df_cleaned

        except Exception as e:
            raise CustomException(e, sys)
