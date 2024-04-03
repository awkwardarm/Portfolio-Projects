import re
from sql_commands import create_table


'''
This script processes the postgreSQL CREATE TABLE command from sql_commands.py to return a schema_dict and list of date indices.
'''


def main():
    
    schema_dict = get_schema_dict_from_sql_create_table(create_table)

    date_col_indices = get_schema_dict_from_sql_create_table(create_table)

    return schema_dict, date_col_indices


def get_schema_dict_from_sql_create_table(sql_command=str):

    schema_string = remove_create_table_from_string(sql_command)
    
    # Split schema into list
    schema_list = schema_string.split(sep=', ')

    # Iterate through list and split into key value pairs on ' '
    schema_dict = {}
    for item in schema_list:
        key, value = item.split(sep=' ')
        schema_dict[key] = value
    
    return schema_dict


def get_date_col_indices_from_schema_dict(dictionary=dict):

    date_col_indices = []

    # Iterate through schema_dict and note all that have value of "DATE"
    
    # Start before the first column to account for zero-indexing
    i = -1 

    for key, value in dictionary.items():
        i += 1
        if value == 'DATE':
            date_col_indices.append(i)

    return date_col_indices


def remove_create_table_from_string(string=str):

    # Match up to and including starting paranthesis of schema
    pattern = r"CREATE TABLE\s+([^\(]+)\s\(\s"
    match = re.search(pattern, string)

    if match:
        # match.start() gives the start index of the matched string
        # match.end() gives the end index
        return string[:match.start()] + string[match.end():-3]
    else:
        # If there's no match, return the string as it is
        return string
    

if __name__ == "__main__":
    result = main()
