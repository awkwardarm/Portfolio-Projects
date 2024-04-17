import pandas as pd
from pandas_schema import pandas_schema


def main():

    indices_by_type = get_indices_by_type(schema_list)
    print(indices_by_type)


def get_indices_by_type(schema_list):

    # Create dict of set of datatypes in pandas_schema
    indices_by_type = {datatype:[] for datatype in list(set(pandas_schema.values()))}

    for key,_ in indices_by_type.items():
        for i,_ in enumerate(schema_list):
            if key in schema_list[i][1]:
                indices_by_type[key].append(i)
    
    return indices_by_type







'''INPUTS'''

file_path = '/Users/matthewtryba/Desktop/subsampled_data.csv'
columns = pandas_schema.keys()
datatypes = pandas_schema.values()
schema_list = list(zip(columns, datatypes))


if __name__ == "__main__":
    main()