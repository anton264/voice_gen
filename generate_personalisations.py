import os
from bark import preload_models
from distutils.dir_util import copy_tree
from utilities import (
    create_or_reuse_csv_with_all_data,
    generate_sound_file,
    get_all_files_to_edit_manually,
    find_csvs,
    get_data,
    insert_value_in_column,
    get_value_from_column,
    play_sound_and_get_feedback_from_human,
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

create_or_reuse_csv_with_all_data(data, all_data_path)

# Download and load all voice models
print("Loading voice models...")
preload_models()

for entry in data:
    satisfied = False
    while not satisfied:
        already_approved = get_value_from_column(all_data_path, entry[0], 3)
        if already_approved is not None:
            print(f"Skipping {entry[0]} because it is already approved with value: {already_approved}")
            break
        phrase = f"{entry[1]} {name}"
        wave_obj = generate_sound_file(entry[0], phrase)
        # Ask the user if they are satisfied with the sound
        user_input = play_sound_and_get_feedback_from_human(phrase, wave_obj)
        while user_input == 'r':
            print("Re-playing...")
            user_input = play_sound_and_get_feedback_from_human(phrase, wave_obj)
        if user_input == 'y':
            insert_value_in_column(all_data_path, entry[0], user_input, 3)
            satisfied = True
        elif user_input == 'e':
            insert_value_in_column(all_data_path, entry[0], user_input, 3)
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


