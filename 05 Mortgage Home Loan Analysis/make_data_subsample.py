from tqdm import tqdm
import pandas as pd
import os

def main():
    data_sampler(directory_path, sampling_fraction, chunk_size)


def data_sampler(directory_path, sampling_fraction, chunk_size):

    sampled_dfs = []

    # Wrap os.listdir with tqdm to show progress on files
    for filename in tqdm(os.listdir(directory_path), desc='Processing files'):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory_path, filename)
            
            chunk_list = []  # Temporary list to store chunk samples
            
            # Update: Use `tqdm` with `pd.read_csv` by converting the iterator to a list first to show chunk progress
            total_size = sum(1 for row in open(file_path, 'r'))
            chunk_progress = tqdm(total=total_size, desc=f'Reading {filename}', leave=False)
            
            for chunk in pd.read_csv(file_path, chunksize=chunk_size, delimiter='|', header=None, low_memory=False):
                sampled_chunk = chunk.sample(frac=sampling_fraction)
                chunk_list.append(sampled_chunk)
                chunk_progress.update(chunk_size)  # Update progress per chunk
            
            chunk_progress.close()  # Ensure the progress bar closes correctly
            
            sampled_df = pd.concat(chunk_list, ignore_index=True)
            sampled_dfs.append(sampled_df)

    final_sampled_df = pd.concat(sampled_dfs, ignore_index=True)

    final_sampled_df.to_csv('/Users/matthewtryba/Desktop/subsampled_data.csv', sep="|", header=None, index=False)

'''INPUTS'''

# Define your directory path and other parameters as before
directory_path = '/Volumes/MT FATBOY/FannieMaeMortgageData/Performance_All'
sampling_fraction = 0.005
chunk_size = 10000

if __name__ == "__main__":
    main()