import re
from sql_commands import create_table
import pandas as pd
import numpy as np
from decimal import Decimal
from datetime import datetime, date, time, timedelta


class SQLTableSchemaParser:
    def __init__(self, sql_command):
        self.sql_command = sql_command
        self.schema_dict = self.get_schema_dict()
        self.schema_list = self.get_schema_list()
        self.date_col_indices = self.get_date_col_indices()
        self.bool_col_indices = self.get_bool_col_indices()
        self.indices_by_type = self.get_indices_by_type()


    def get_schema_dict(self):
        schema_string = self.remove_create_table_from_string()
        schema_list = schema_string.split(sep=', ')
        schema_dict = {}
        for item in schema_list:
            key, value = item.split(sep=' ')
            schema_dict[key] = value
        return schema_dict

    def get_schema_list(self):
        columns = []
        datatypes = []
        schema_string = self.remove_create_table_from_string()
        string_list = schema_string.split(sep=', ')
        for item in string_list:
            column, datatype = item.split(sep=' ')
            columns.append(column)
            datatypes.append(datatype)
        schema_list = list(zip(columns, datatypes))
        return schema_list


    def get_date_col_indices(self):
        date_col_indices = []
        schema_list = self.schema_list   

        for i, _ in enumerate(schema_list):
            if schema_list[i][1] == 'DATE':
                date_col_indices.append(i)
        return date_col_indices
    
    def get_bool_col_indices(self):
        bool_col_indices = []
        schema_list = self.schema_list   

        for i, _ in enumerate(schema_list):
            if schema_list[i][1] == 'BOOLEAN':
                bool_col_indices.append(i)
        return bool_col_indices
    
    def get_indices_by_type(self):
        indices_by_type = {'BOOLEAN':[],
                       'DATE':[],
                       'INTEGER':[],
                       'NUMERIC':[],
                       'VARCHAR':[]}
        schema_list = self.schema_list

        for key,_ in indices_by_type.items():
            for i, _ in enumerate(schema_list):
                if key in schema_list[i][1]:
                    indices_by_type[key].append(i)

        return indices_by_type


    def remove_create_table_from_string(self):
        pattern = r"CREATE TABLE\s+([^\(]+)\s\(\s"
        end_pattern = r"\s?\);"
        match = re.search(pattern, self.sql_command)
        end_match = re.search(end_pattern, self.sql_command)

        if match:
            return self.sql_command[:match.start()] + self.sql_command[match.end():end_match.start()]
        else:
            return self.sql_command


    def map_postgresql_to_python_datatypes(self):

        # get postgresql schema as dictionary
        schema_dict = self.get_schema_dict()

        # pre process

        postgres_to_pandas = {
            'integer': 'int64',
            'bigint': 'int64',
            'smallint': 'int32',
            'decimal': 'float64',  # Changed to float64 for general use; use 'object' if needing Decimal for precision
            'numeric': 'float64',  # Same note as for 'decimal'
            'real': 'float32',
            'double precision': 'float64',
            'char': 'object',  # 'object' in pandas corresponds to strings and more complex types
            'varchar': 'object',
            'text': 'object',
            'bytea': 'object',  # Handling binary data as objects
            'boolean': 'bool',
            'date': 'datetime64[ns]',  # pandas datetime type
            'timestamp': 'datetime64[ns]',
            'time': 'datetime64[ns]',  # No specific pandas type for time only; consider 'object' if storing time only
            'interval': 'timedelta64[ns]',  # pandas timedelta type
            'array': 'object'  # Arrays handled as objects, specific handling might be needed
            }


        pandas_dtypes = {col: postgres_to_pandas[str(pg_type).lower().split(sep='(')[0]] for col, pg_type in schema_dict.items()}

        return pandas_dtypes

if __name__ == "__main__":
    parser = SQLTableSchemaParser(create_table)
    print(parser.map_postgresql_to_python_datatypes())



   
