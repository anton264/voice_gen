# README.md

## Voice Generation with Quality Threshold

This Python script generates voice clips using the BARK library and Whisper voice recognition model, ensuring the generated voices meet a specified quality threshold. The script processes CSV files containing phrases, generates voice clips for each phrase, and checks their quality using a voice recognition model. If the generated voice clip does not meet the quality threshold, the script retries until it reaches the maximum number of retries or finds a satisfactory voice clip.

### Dependencies

- bark_ssg==1.3.4
- fuzzywuzzy==0.18.0
- num2words==0.5.10
- numpy==1.20.3
- openai_whisper==20230314
- pydub==0.25.1
- pyphonetics==0.5.3
- scipy==1.7.3
- simpleaudio==1.0.4

### Installing Dependencies

To install the required dependencies, run the following command:

```bash
pip install -r requirements.txt
```

### Usage

1. Set the working folder path in the `workfolder` variable.
2. Set the quality threshold in the `voice_threshold` variable (minimum score for a sound to be considered good enough; the maximum score is 100).
3. Set the maximum number of retries in the `max_retries` variable.
4. Choose whether to use phonetics for text comparison in the `use_phonetics` variable (currently only works for English).
5. Choose whether to keep files that failed to generate in the `keep_failed_files` variable.
6. Run the script.

### How it Works

1. The script loads the Whisper voice recognition model.
2. It loads the BARK voice generation models.
3. It finds all CSV files in the specified working folder and combines their data into a list of tuples.
4. It creates or reuses an existing CSV file to store information about the generated voice clips.
5. For each phrase, the script generates a voice clip and checks its quality using the voice recognition model.
6. If the generated voice clip does not meet the quality threshold, the script retries until it reaches the maximum number of retries or finds a satisfactory voice clip.
7. It updates the information in the CSV file accordingly.

### Notes

- The script requires the BARK library, Whisper voice recognition model, and other dependencies listed in the `requirements.txt` file. Ensure that they are installed and configured correctly.
- Ensure that the working folder contains properly formatted CSV files with phrases to generate voice clips.
- The generated voice clips will be saved in the specified working folder, and the information about their quality will be stored in an `all_data.csvfile`.