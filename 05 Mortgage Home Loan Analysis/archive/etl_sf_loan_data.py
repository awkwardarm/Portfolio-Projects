#import pandas as pd
#from pandas_schema import pandas_schema


def main():

    #indices_by_type = get_indices_by_type(schema_list)

    #preprocess_dates(sf_loan_performance, indices_by_type)

    # preprocess_booleans(sf_loan_performance, indices_by_type)

    # cast_types(sf_loan_performance, indices_by_type)
    pass


def get_indices_by_type(schema_list):
    """
    Creates dictionary of set of datatypes in pandas_schema
    """
    indices_by_type = {datatype:[] for datatype in list(set(pandas_schema.values()))}

    for key,_ in indices_by_type.items():
        for i,_ in enumerate(schema_list):
            if key in schema_list[i][1]:
                indices_by_type[key].append(i)
    
    return indices_by_type


def preprocess_dates(df, indices_by_type):
    """
    Converts date columns from MMYYYY to YYYY-MM-DD format, safely handling NaN values.
    :param df: DataFrame with data.
    :param date_columns: List of columns indices to be converted.
    """
    error_col_indices = []

    for col in indices_by_type['datetime64[ns]']:
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

        except ValueError:
            error_col_indices.append(col)
        
    #print(f'Errors on columns  {error_col_indices}')
    
    return df


def process_dates(df, indices_by_type):
    """
    Converts date columns from MMYYYY to YYYY-MM-DD format, safely handling NaN values.
    :param df: DataFrame with data.
    :param indices_by_type: Dictionary with 'datetime64[ns]' key pointing to list of column indices.
    """
    error_col_indices = []

    for col in indices_by_type['datetime64[ns]']:
        try:
            # Direct conversion to string and zero-filling
            df.iloc[:, col] = df.iloc[:, col].astype(str).str.zfill(6)

            # Convert to datetime format, specifying the original format to speed up parsing
            df.iloc[:, col] = pd.to_datetime(df.iloc[:, col], format='%m%Y', errors='coerce')
        
        except ValueError:
            error_col_indices.append(col)
        
    # Optionally, log errors (if frequent):
    # if error_col_indices:
    #     print(f'Errors on columns  {error_col_indices}')
    
    return df


def preprocess_booleans(df, indices_by_type):
    """
    Converts columns with "Y" and "N" values to boolean. All other values are set to NULL.
    :param df: DataFrame with data.
    :param bool_columns: List of columns indices to be converted.
    """
    for col in indices_by_type['bool']:
        df.iloc[:,col] = df.iloc[:,col].apply(convert_to_bool)

    return df


def convert_to_bool(x):
    if x == 'N' or x == 'n':
        return False
    elif x == "Y" or x == 'y':
        return True
    else:
        return None    


def cast_types(df, indices_by_type):
    for type in indices_by_type: #.remove(['bool', 'datetime64[ns]']):
        for col in indices_by_type[type]:
            df.iloc[:, col] = df.iloc[:, col].astype(type)


'''INPUTS'''

columns = list(pandas_schema.keys())
datatypes = list(pandas_schema.values())
schema_list = list(zip(columns, datatypes))
file_path = '/Users/matthewtryba/Desktop/subsampled_data.csv'
#file_path = 'Y:\FannieMaeMortgageData\subsampled_data.csv'

sf_loan_performance = pd.read_csv(file_path, sep='|', header=None, names=columns, low_memory=False)



if __name__ == "__main__":
    main()