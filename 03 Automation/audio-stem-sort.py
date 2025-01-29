import os
import sys
import re
import subprocess


def main(folder_path):
    """
    This script automates client deliverables by sorting audio files and creating mp3s. On average, ~ 50-150 audio files are processxed.

    Args:
        folder_path (str): Path to folder to sort, rename, and create mp3s.
    """
    # Get stem folder name
    folder_name = os.path.basename(folder_path)

    # list of valid audio extensions
    valid_extensions = [".wav", ".aif", ".aiff", ".mp3", ".m4a"]

    # List of audio stems
    mixes = [
        "mix_",
    ]

    main_stems = [
        "drums all",
        "bass all",
        "harm all",
        "leads all",
        "sfx all",
        "bvs all",
        "lead vox all",
    ]

    alt_mixes = ["vocalise and track_", "instrumental", "a cappella", "tv mix"]

    master = [
        "master_",
    ]

    file_paths = []
    # Walk all files in folder and get all file_paths
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # Check if valid audio file
            if any(file.lower().endswith(ext) for ext in valid_extensions):
                file_path = os.path.join(root, file)
                file_paths.append(file_path)

    # Get file_paths of all target stems
    paths_master = get_file_paths_from_target_list(
        targets=master, file_paths=file_paths
    )
    paths_main_stems = get_file_paths_from_target_list(
        targets=main_stems, file_paths=file_paths
    )
    paths_alt_mixes = get_file_paths_from_target_list(
        targets=alt_mixes, file_paths=file_paths
    )

    # Create directories inside the parent folder
    mixes_dir = os.path.join(folder_path, "02 Mixes")
    main_stems_dir = os.path.join(folder_path, "03 Main Stems")
    mix_stems_dir = os.path.join(folder_path, "04 Mix Stems")
    os.makedirs(mixes_dir, exist_ok=True)
    os.makedirs(main_stems_dir, exist_ok=True)
    os.makedirs(mix_stems_dir, exist_ok=True)

    # Remove main stems from "04 Mix Stems" folder
    for file in os.listdir(mix_stems_dir):
        file_path = os.path.join(mix_stems_dir, file)
        if file_path in paths_main_stems:
            os.remove(file_path)
            paths_main_stems.remove(
                file_path
            )  # remove found filepath from paths_main_stems
            print(f"Removed main stem file: {file_path}")

    # list of files to be converted to mp3
    mp3_paths = []

    # Rename and move alt_mixes
    move_audio_file(
        file_paths=paths_alt_mixes,
        target_folder=mixes_dir,
        mp3_paths=mp3_paths,
        parent_folder=folder_name,
        mp3=True,
    )

    move_audio_file(
        file_paths=paths_main_stems,
        target_folder=main_stems_dir,
        mp3_paths=mp3_paths,
        parent_folder=folder_name,
        mp3=False,
    )

    # Create mp3s
    create_mp3(mp3_paths)
    create_mp3(paths_master)


def get_file_paths_from_target_list(targets, file_paths):
    results = []
    # Get list of file_paths that contain strings from a target list.
    for file_path in file_paths:
        for target in targets:
            if target in str(file_path).lower():
                results.append(file_path)

    return results


def move_audio_file(file_paths, target_folder, mp3_paths, parent_folder, mp3=False):
    """Moves audio files to target folder and appends folder_name at end. Optionally marks audio files to be later converted to mp3.

    Args:
        file_paths (object): list of filepaths to move
        target_folder (object): destination folder
        mp3_paths (object): list of paths for mp3s
        folder_name (string): song name derived from folder_path
        mp3 (bool, optional): mark file_path for later creation of mp3 version. Defaults to False.
    """
    # Rename and move alt_mixes
    for file_path in file_paths:
        # Get filename
        file_name = os.path.basename(file_path)
        file_name_without_ext, extension = os.path.splitext(file_name)
        # use regex to remove digits followed by a space from beginning of the file_name
        new_file_name = re.sub(r"^\d+ ", "", file_name_without_ext)
        new_file_name = f"{new_file_name} - {parent_folder}" + extension
        new_file_path = os.path.join(target_folder, new_file_name)

        if mp3:
            # Add filepaths to be converted to mp3 later
            mp3_paths.append(new_file_path)
            print(f"File {new_file_path} to be converted to .mp3")

        # move and rename file
        os.rename(file_path, new_file_path)
        print(f"Moved and renamed: {file_path} -> {new_file_path}")


def create_mp3(file_paths):
    """Converts a list of audio files to mp3 format using ffmpeg.

    Args:
        file_paths (list): List of file paths to convert to mp3.
    """
    for file_path in file_paths:
        # Create the new file path with .mp3 extension
        mp3_file_path = os.path.splitext(file_path)[0] + ".mp3"
        # Use ffmpeg to convert the file to mp3 with specific settings
        subprocess.run(
            [
                "ffmpeg",
                "-i",
                file_path,
                "-codec:a",
                "libmp3lame",
                "-b:a",
                "320k",
                "-ac",
                "2",
                "-q:a",
                "0",
                mp3_file_path,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
        print(f"Converted {file_path} to {mp3_file_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python audio-stem-sort.py <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]
    main(folder_path)
