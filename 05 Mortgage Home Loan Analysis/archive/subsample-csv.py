'''
Creates a subsample of the data for postgresql setup. 
'''

import pandas as pd

test_file = '/Users/matthewtryba/Desktop/2023Q3.csv'

df = pd.read_csv(test_file, header=None, delimiter='|')

df.iloc[:1001,:].to_csv('05 Mortgage Home Loan Analysis/test_csv_folder/2023_sample.csv',
                        sep='|', index=False, header=False)