import os
import pandas as pd
from datetime import datetime
import psycopg2
from psycopg2.extras import execute_values
from DateColumnsScript import date_columns


"""
Working on pre-processing dates. It seems that either my columns are out of order or the data in the columns labeled "DATE" in the glossary is incorrect.
"""


# Database connection parameters
db_params = {
    "dbname": "mortgagesfm",
    "user": "postgres",
    "password": "acidponyunicornflubber",
    "host": "localhost",
    "port":"5432"
}

def preprocess_dates(df, date_columns):
    """
    Converts date columns from MMYYYY to YYYY-MM-DD format.
    :param df: DataFrame with data.
    :param date_columns: List of columns indices to be converted.
    """
    for col in date_columns:
        # Convert to string, ensuring it's in the correct format even if not initially recognized as such
        df.iloc[:,col] = df.iloc[:,col].astype(str)
        # Parse the date using datetime.strptime and then format it into YYYY-MM-DD
        df.iloc[:,col] = df.iloc[:,col].apply(lambda x: datetime.strptime(x, '%m%Y').strftime('%Y-%m-%d'))

def insert_data(df, conn, table_name):
    """
    Insert data from a DataFrame into the specified table.
    """
    tuples = [tuple(x) for x in df.to_numpy()]
    query = f"INSERT INTO {table_name} VALUES %s"
    cursor = conn.cursor()
    try:
        execute_values(cursor, query, tuples)
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cursor.close()

def process_files(folder_path, table_name):
    """
    Process each .csv file in the specified folder.
    """
    with psycopg2.connect(**db_params) as conn:
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.csv'):
                file_path = os.path.join(folder_path, file_name)
                df = pd.read_csv(file_path, header=None, delimiter='|')
                preprocess_dates(df, date_columns=date_columns)
                print(df.head())
                #insert_data(df, conn, table_name)

# Replace '/path/to/your/csv/folder' with the actual folder path
folder_path = "Y:\FannieMaeMortgageData\TestCsv"
table_name = 'mortgagesfm.sf_loan_performance'

process_files(folder_path, table_name)

