import re
from sql_commands import create_table

class SQLTableSchemaParser:
    def __init__(self, sql_command):
        self.sql_command = sql_command
        self.schema_dict = self.get_schema_dict()
        self.date_col_indices = self.get_date_col_indices()


    def get_schema_dict(self):
        schema_string = self.remove_create_table_from_string()
        schema_list = schema_string.split(sep=', ')
        schema_dict = {}
        for item in schema_list:
            key, value = item.split(sep=' ')
            schema_dict[key] = value
        return schema_dict


    def get_date_col_indices(self):
        date_col_indices = []
        i = -1
        for key, value in self.schema_dict.items():
            i += 1
            if value == 'DATE':
                date_col_indices.append(i)
        return date_col_indices


    def remove_create_table_from_string(self):
        pattern = r"CREATE TABLE\s+([^\(]+)\s\(\s"
        end_pattern = r"\s?\);"
        match = re.search(pattern, self.sql_command)
        end_match = re.search(end_pattern, self.sql_command)

        #print(end_match.start())
        if match:
            return self.sql_command[:match.start()] + self.sql_command[match.end():end_match.start()]
        else:
            return self.sql_command


if __name__ == "__main__":
    parser = SQLTableSchemaParser(create_table)



   
