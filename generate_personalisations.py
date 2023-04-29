import os
import csv
from bark import preload_models
from distutils.dir_util import copy_tree
from utilities import (
    generate_sound_file,
    get_all_files_to_edit_manually,
    find_csvs,
    get_data,
    insert_value_in_third_column,
    tuples_to_csv,
    get_value_from_third_column,
)

os.system("cls")

name = input("What name do you want to generate? ").lower().strip()

file_dir = os.path.join("createdPersonalisations", name)

# Copy personalisations to a new folder
copy_tree("personalisationTemplate", file_dir)

csv_files = find_csvs(file_dir)


# Combine all csv data into one list of tuples, each tuple is (path, text)
data = [item for csv_file in csv_files for item in get_data(csv_file)]

all_data_path = os.path.join(file_dir, "all_data.csvfile")

# Check if all_data.csvfile exists, if it does compare length of data and all_data
if os.path.isfile(all_data_path):
    with open(all_data_path, 'r', newline='') as csvfile:
        all_data_length = sum(1 for row in csv.reader(csvfile, delimiter=';'))
        data_length = len(data)
        if all_data_length != data_length:
            print(
                f"Length of data and all_data.csvfile are not equal, \n"
                f"the length of all_data.csvfile is {all_data_length} and the length of data is {data_length}"
                f"\nthis means that there is a mismatch between all the subtitles.csv files and the aggregated all_data.csvfile,"
                f"\nyou need to manually check if the data is correct and then delete or edit the all_data.csvfile and run this script again"
            )
            exit()
        else:
            print("Length of data and all_data.csvfile are equal, skipping creation of all_data.csvfile")
else:
    print("all_data.csvfile does not exist, creating it")
    tuples_to_csv(data, all_data_path)

# Download and load all voice models
print("Loading models...")
preload_models()

def play_sound_and_get_feedback_from_human(phrase, wave_obj):
    play_obj = wave_obj.play()
    play_obj.wait_done()
    user_input = input(
        f'The phrase is: \n\n "{phrase}"\n\nAre you happy with the sound? \n'
        f'(y)es\n(n)o (Re-generate)\n(r)eplay\n(e)dit manually later): '
    ).lower()

    return user_input

for entry in data:
    satisfied = False
    while not satisfied:
        already_approved = get_value_from_third_column(all_data_path, entry[0])
        if already_approved is not None:
            print(f"Skipping {entry[0]} because it is already approved with value: {already_approved}")
            break
        phrase = f"{entry[1]} {name}"
        wave_obj = generate_sound_file(entry, phrase)
        # Ask the user if they are satisfied with the sound
        user_input = play_sound_and_get_feedback_from_human(phrase, wave_obj)
        while user_input == 'r':
            print("Re-playing...")
            user_input = play_sound_and_get_feedback_from_human(phrase, wave_obj)
        if user_input == 'y':
            insert_value_in_third_column(all_data_path, entry[0], user_input)
            satisfied = True
        elif user_input == 'e':
            insert_value_in_third_column(all_data_path, entry[0], user_input)
            satisfied = True
        else:
            print("Re-generating...")


# Get all files marked as 'e' in all_data.csvfile
files_to_edit_manually = get_all_files_to_edit_manually(all_data_path)

#Write all files marked as 'e' to a file
files_to_edit_path = os.path.join(file_dir, "files_to_edit_manually.txt")
with open(files_to_edit_path, "w") as myfile:
    for f in files_to_edit_manually:
        myfile.write(f"{f}\n")

# Remove all csv files from the folder tree, they cause problems in crew chief
for csv_file in csv_files:
    os.remove(csv_file)

print("\n-------------------------------------------\n")
print(f"All done! The files are located in:\n{os.path.abspath(file_dir)}"
f"\n\nYou need to manually edit the files listed in: \n{os.path.abspath(files_to_edit_path)} to make them sound good")
print("\n-------------------------------------------\n")

