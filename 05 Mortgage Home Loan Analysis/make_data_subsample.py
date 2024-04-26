from tqdm import tqdm
import pandas as pd
import os

def main():
    data_sampler(directory_path, directory_out, sampling_fraction, chunk_size)


def data_sampler(directory_path, directory_out, sampling_fraction, chunk_size):

    sampled_dfs = []

    # Wrap os.listdir with tqdm to show progress on files
    for filename in tqdm(os.listdir(directory_path), desc='Processing files'):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory_path, filename)
            
            chunk_list = []  # Temporary list to store chunk samples

            filename_numeric = quarter_string_to_num(filename)
            
            # Update: Use `tqdm` with `pd.read_csv` by converting the iterator to a list first to show chunk progress
            total_size = sum(1 for row in open(file_path, 'r'))
            chunk_progress = tqdm(total=total_size, desc=f'Reading {filename}', leave=False)
            
            for chunk in pd.read_csv(file_path, chunksize=chunk_size, delimiter='|', header=None, low_memory=False):
                sampled_chunk = chunk.sample(frac=sampling_fraction, random_state=42)

                # Add filename as a new column dynamically at the end w/o '.csv'
                num_cols = len(sampled_chunk.columns)
                sampled_chunk[num_cols] = filename[:-4]

                # Add filename_numeric as a new column dynamically at the end
                sampled_chunk[num_cols + 1] = filename_numeric


                chunk_list.append(sampled_chunk)
                chunk_progress.update(chunk_size)  # Update progress per chunk
            
            chunk_progress.close()  # Ensure the progress bar closes correctly
            sampled_df = pd.concat(chunk_list, ignore_index=True)
            sampled_dfs.append(sampled_df)

    final_sampled_df = pd.concat(sampled_dfs, ignore_index=True)

    output_path = os.path.join(directory_out, output_file_name)
    #output_path = '/Users/matthewtryba/Desktop/' + output_file_name
    #output_path = "C:\\Users\\matth\\Desktop\\" + output_file_name
    final_sampled_df.to_csv(output_path, sep="|", header=None, index=False)


def quarter_string_to_num(filename):

    '''
    # Convert filename to YYYY.Q as float. To preserve year: 0.00 = Q1, 0.25 = Q2, 0.5 = Q3, 0.75 = Q4
    '''

    filename_str = filename[:4] + "." + filename[-5]

    filename_num = ''

    if filename_str[-1] == '1':
        filename_num += filename_str[:-1] + '00'
    elif filename_str[-1] == '2':
        filename_num += filename_str[:-1] + '25'
    elif filename_str[-1] == '3':
        filename_num += filename_str[:-1] + '5'
    elif filename_str[-1] == '4':
        filename_num += filename_str[:-1] + '75'
    
    return float(filename_num)

'''INPUTS'''

# Define your directory path and other parameters as before
sampling_fraction = 0.005
chunk_size = 1000
#directory_path = '/Volumes/MT FATBOY/FannieMaeMortgageData/Performance_All'
directory_out = "C:\\Users\\matth\\Desktop"
directory_path = "Y:\FannieMaeMortgageData\Performance_All"
#directory_path = "Y:\\FannieMaeMortgageData\\TestCsv"
#output_file_name = "test.csv"
output_file_name = "subsampled_data_" + str(100*sampling_fraction) + "_pct.csv"

if __name__ == "__main__":
    main()