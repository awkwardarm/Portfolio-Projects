import os
import pandas as pd
import librosa
import numpy as np


# Root directory of Native Instruments sounds
# root_directory = r"Y:\SOUNDS\Native Instruments"
# root_directory = r"G:\Native Instruments"
root_directory = r"C:\Users\matth\Desktop\Native Instruments"


def main():
    # columns = ['name', 'library', 'drum_type', 'file_path', 'mfcc', 'spectral_centroid', 'zcr']
    columns = ['name', 'library', 'drum_type', 'file_path', 'librosa_features']
    df = pd.DataFrame(columns=columns)

    # Empty list for concatetenating data to a dataframe
    rows_to_add = []

    # Find directories that contain drum samples
    for root, dirs, _ in os.walk(root_directory):
        for dir_name in dirs:
            rows_to_add.extend(process_directory(root, dir_name))

    # Convert the list of rows into a DataFrame and concatenate with the main DataFrame
    if rows_to_add:
        df = pd.concat([df, pd.DataFrame(rows_to_add)], ignore_index=True)

    df.to_json('ni_drums.json', orient="records", indent=4)
    df.to_pickle('ni_drums.pkl.gz', compression='gzip')


def extract_audio_features(file_path):
    """Extract spectral audio features using librosa library."""

    # Check to see if file suffix in list of extensions
    file_extensions = ['wav', 'aif', 'aiff', 'mp3', 'm4a']

    if file_path.split(".")[-1] in file_extensions:

        # Load drum sample
        y, sr = librosa.load(file_path, sr=None)

        hop_length = 256

        # Extract features
        mfcc = librosa.feature.mfcc(
            y=y, 
            sr=sr, 
            n_mfcc=13, 
            n_fft=1024, 
            hop_length=hop_length,
            n_mels=40,
            dct_type=2)
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr, n_fft=1024)
        spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)
        spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr, roll_percent=0.85)
        zcr = librosa.feature.zero_crossing_rate(y, hop_length=hop_length)
        rms = librosa.feature.rms(y=y)
        onset_strength = librosa.onset.onset_strength(y=y, sr=sr)

        # extract the librosa audio features to a single feature vector
        '''
        I'm blindly using mean. I should consider how to process the data for better performance.
        Do any of the features need to be scaled or normalized before this step? 
        '''

        features = np.hstack([
            np.mean(mfcc, axis=1),                    # Mean of MFCC coefficients
            np.mean(spectral_centroid, axis=1),       # Mean of Spectral Centroid
            np.mean(spectral_bandwidth, axis=1),      # Mean of Spectral Bandwidth
            np.mean(spectral_contrast, axis=1),       # Mean of Spectral Contrast
            np.mean(spectral_rolloff, axis=1),        # Mean of Spectral Rolloff
            np.mean(zcr, axis=1),                     # Mean of Zero-Crossing Rate
            np.mean(rms, axis=1),                     # Mean of RMS Energy
            np.mean(onset_strength),                  # Mean of Onset Strength
            ])

        # return mfcc, spectral_centroid, zcr
        return features
    
    else:
        # return None, None, None
        return None


def get_subfolders(target_path):
    """Get the list of subdirectories inside the 'Drums' folder."""
    return [os.path.join(target_path, subfolder) for subfolder in os.listdir(target_path) if os.path.isdir(os.path.join(target_path, subfolder))]


def get_drum_files(subfolder):
    """Get the list of drum files in a subfolder."""
    return [f for f in os.listdir(subfolder) if os.path.isfile(os.path.join(subfolder, f))]


def process_drum_file(file_name, subfolder, dir_name):
    """Process a single drum file and return its metadata."""
    file_path = os.path.join(subfolder, file_name)
    parent_directory_name = os.path.basename(os.path.dirname(file_path))
    # mfcc, spectral_centroid, zcr = extract_audio_features(file_path=file_path)
    features = extract_audio_features(file_path=file_path)

    return {
        'name': file_name,
        'library': dir_name,
        'drum_type': parent_directory_name.lower(),
        'file_path': file_path,
        'librosa_features':features
        # 'mfcc': mfcc,
        # 'spectral_centroid': spectral_centroid,
        # 'zcr': zcr
    }


def process_directory(root, dir_name):
    """Process a directory and return a list of row data."""
    # Looking for folders that contain folder/Samples/Drums in the Native Instruments library
    target_path = os.path.join(root, dir_name, "Samples", "Drums")

    # Return nothing if directory does not exist
    if not os.path.isdir(target_path):
        return []

    rows = []
    subfolders = get_subfolders(target_path)
    
    for subfolder in subfolders:
        drum_files = get_drum_files(subfolder)

        for file_name in drum_files:
            row_data = process_drum_file(file_name, subfolder, dir_name)
            rows.append(row_data)
    
    return rows


if __name__ == "__main__":
    main()
