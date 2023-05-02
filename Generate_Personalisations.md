# Generate Personalisations

## Personalized Voice Generation

This Python script generates personalized voice clips using the BARK library, given a name input. The script copies a template folder containing CSV files with phrases, generates personalized voice clips by appending the input name to each phrase, and saves them in a new folder. The user can review the generated voice clips and mark them as satisfactory, unsatisfactory, or requiring manual editing.

### Dependencies

- BARK
- SciPy
- NumPy

### Usage

1. Run the script.
2. Input the name you want to generate personalized voice clips for.
3. The script will create a new folder in the `createdPersonalisations` directory with the name provided, and copy the `personalisationTemplate` folder's content.
4. For each phrase, the script generates a voice clip and plays it back for the user to review.
5. The user can provide feedback by pressing:
    - 'y' if satisfied with the generated voice clip
    - 'n' if not satisfied and want to regenerate
    - 'e' if the clip requires manual editing
    - 'r' to replay the current clip
6. The script saves the user's feedback in an `all_data.csvfile`.
7. All files marked for manual editing will be listed in a `files_to_edit_manually.txt` file in the generated folder.

### How it Works

1. The script prompts the user for a name to generate personalized voice clips.
2. It creates a new folder in the `createdPersonalisations` directory and copies the `personalisationTemplate` folder's content.
3. The script finds all CSV files in the new folder and combines their data into a list of tuples.
4. It creates or reuses an existing CSV file to store feedback on the generated voice clips.
5. The script loads the BARK voice models.
6. For each phrase, the script generates a voice clip with the name appended and plays it back for the user to review.
7. The user can provide feedback on the generated voice clips, which will be saved in the `all_data.csvfile`.
8. Files marked for manual editing are listed in a `files_to_edit_manually.txt` file.

### Notes

- The script requires the BARK library to generate voice clips. Ensure that it is installed and configured correctly.
- The `personalisationTemplate` folder should contain properly formatted CSV files with phrases to generate personalized voice clips.
- The generated voice clips will be saved in a new folder under the `createdPersonalisations` directory, and the user's feedback will be stored in an `all_data.csvfile`.