import pandas as pd
import sqlite3
import os
from loan_data_layout import sqlite3_schema

def main():
    
    # Convert schema dictionary to a SQL CREATE TABLE statement
    columns_sql = ", ".join([f"\"{col}\" {dtype}" for col, dtype in sqlite3_schema.items()])
    create_table_sql = f"CREATE TABLE IF NOT EXISTS mortgages ({columns_sql});"

    # Set folder path of .csv files
    csv_folder_path = "Y:\FannieMaeMortgageData\TestCsv"
    
    # Set filepath for database
    db_path = "Y:\FannieMaeMortgageData\mortgages.db"

    # set sqlite3 connection
    conn = sqlite3.connect(db_path)

    # Create the table
    cursor = conn.cursor()
    cursor.execute(create_table_sql)
    conn.commit()
        

    # Iterate through the .csv files and insert data into the database
    for csv_file in os.listdir(csv_folder_path):
        if csv_file.endswith('.csv'):
            file_path = os.path.join(csv_folder_path, csv_file)
            
            # Read CSV file into DataFrame, assuming no header and delimiter is "|"
            df = pd.read_csv(file_path, header=None, delimiter='|')
            
            # If your CSV files have a fixed number of columns, you can rename the DataFrame columns to match your database schema
            df.columns = list(sqlite3_schema.keys())
            
            # Insert data into the database
            df.to_sql('mortgages', conn, if_exists='append', index=False, chunksize=20000)
    
    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()