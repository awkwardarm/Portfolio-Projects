import os
import pandas as pd
from datetime import datetime
import psycopg2
from psycopg2.extras import execute_values
from sql_commands import create_table
from sql_table_schema_parser import SQLTableSchemaParser
import numpy as np


def main():
    process_files(folder_path, table_name, date_columns=date_col_indices)
    #preprocess_nan_to_null(df)
    #pass

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


def process_files(folder_path, table_name, date_columns):
    """
    Process each .csv file in the specified folder.
    """
    with psycopg2.connect(**db_params) as conn:
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.csv'):
                file_path = os.path.join(folder_path, file_name)
                df = pd.read_csv(file_path, header=None, delimiter='|')
                #df = df.replace({np.nan: None})
                preprocess_dates(df, date_columns=date_columns)
                preprocess_booleans(df, bool_columns=bool_col_indices)
                insert_data(df, conn, table_name)


def preprocess_dates(df, date_columns):
    """
    Converts date columns from MMYYYY to YYYY-MM-DD format, safely handling NaN values.
    :param df: DataFrame with data.
    :param date_columns: List of columns indices to be converted.
    """
    error_col_indices = []

    for col in date_columns:
        try:
            # Handle NaN values by only converting non-NaN values to int, otherwise leave as NaN
            df.iloc[:, col] = df.iloc[:, col].apply(lambda x: int(x) if not pd.isna(x) else x)
            
            # Convert to string, ensuring it's in the correct format even if not initially recognized as such
            df.iloc[:, col] = df.iloc[:, col].apply(lambda x: str(int(x)) if not pd.isna(x) else x)

            # Back fill leading zero for dates with length less than 6
            df.iloc[:, col] = df.iloc[:, col].apply(lambda x: x.zfill(6) if not pd.isna(x) and len(x) < 6 else x)

            # Parse the date using datetime.strptime and then format it into YYYY-MM-DD, skipping NaN values
            df.iloc[:, col] = pd.to_datetime(df.iloc[:, col], format='%m%Y', errors='coerce')

            # Replace NaT values with None, making it compatible for SQL insertion
            df.iloc[:, col] = df.iloc[:, col].apply(lambda x: None if pd.isna(x) else x)

            #print(df[col].dtype)
        except ValueError:
            error_col_indices.append(col)
        
    #print(f'Errors on columns  {error_col_indices}')
    
    return df


def preprocess_booleans(df, bool_columns):
    """
    Converts columns with "Y" and "N" values to boolean. All other values are set to NULL.
    :param df: DataFrame with data.
    :param bool_columns: List of columns indices to be converted.
    """
    for col in bool_columns:
        df.iloc[:,col] = df.iloc[:,col].apply(convert_to_bool)

    return df


def convert_to_bool(x):
    if x == 'N' or x == 'n':
        return False
    elif x == "Y" or x == 'y':
        return True
    else:
        return None    


'''INPUTS'''

#test_file = 'Y:\FannieMaeMortgageData\TestCsv\sf-loan-performance-data-sample.csv' 
test_file = '05 Mortgage Home Loan Analysis/test_csv_folder/2023_sample.csv'
df = pd.read_csv(test_file, header=None, delimiter='|')


# Database connection parameters
db_params = {
    "dbname": "mortgagesfm",
    "user": "postgres",
    "password": "acidponyunicornflubber",
    "host": "localhost",
    "port":"5432"
}

# Instantiate parser
sql_parser = SQLTableSchemaParser(sql_command=create_table)

# Get schema and date columns

date_col_indices = sql_parser.indices_by_type['DATE']

# Indices of columns to be converted to bool
bool_col_indices = sql_parser.indices_by_type['BOOLEAN']

# Replace '/path/to/your/csv/folder' with the actual folder path
#folder_path = "Y:\FannieMaeMortgageData\TestCsv"
folder_path = '05 Mortgage Home Loan Analysis/test_csv_folder'
table_name = 'mortgagesfm.sf_loan_performance'


if __name__ == "__main__":
    main()