'''
*** If there are more than 127 presets in the text file Serum will crash DAWs when loaded and on startup***

This script automates copying filenames of Serum synthesizer sound presets inside the designated directory 
to a preferences text file so that the presets can be accessed via MIDI program change messages. 
'''
import os

preset_folder = 'MTPC'
folder_path = r'/Users/matthewtryba/Dropbox/01 Matt/TRYBA ESSENTIAL SOUNDS/Xfer Records/Serum Presets/Presets/' + preset_folder
output_file = r'/Users/matthewtryba/Dropbox/01 Matt/TRYBA ESSENTIAL SOUNDS/Xfer Records/Serum Presets/System/ProgramChanges.txt'


# write the .txt file
with open(output_file, 'w') as f:

    # loop through folder
    for filename in sorted(os.listdir(folder_path)): # 'sorted' alphabetizes items in folder
        #skip .DS_Store file
        if filename == '.DS_Store':
            continue
        # write preset names to .txt file
        else:
            f.write(f'{preset_folder}/{filename}\n')