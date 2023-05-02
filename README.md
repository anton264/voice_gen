# README.md

## Voice Generation with Scoring

This is a Python script that reads CSV files containing text phrases from a specified directory, generates audio files using the BARK and WHISPER libraries, and scores the quality of the generated audio based on the similarity between the expected and recognized phrases using Speech Recognition.

### Dependencies

- BARK
- WHISPER
- Speech Recognition
- SciPy
- NumPy

### Usage

1. Set the working folder to the directory containing the CSV files with the text phrases.
   ```
   workfolder = 'D:/workdir2/corners'
   ```
2. Set the voice quality threshold and maximum number of retries for generating the audio files.
   ```
   voice_threshold = 90
   max_retries = 20
   ```
3. Run the script. It will process the CSV files, generate the audio files, and score the quality of the generated audio.

### How it Works

1. The script loads the voice recognition and generation models.
2. It finds all CSV files in the specified working folder and combines the data into one list.
3. The script creates or reuses an existing CSV file to store the generated audio files' scores.
4. It iterates through the list of phrases and generates audio files using the BARK library.
5. For each generated audio file, the script performs voice recognition using the WHISPER library and calculates a similarity score based on the expected and recognized phrases.
6. If the score is below the voice quality threshold, the script will generate a new audio file and retry voice recognition, up to the specified maximum number of retries.
7. The best-scoring audio file for each phrase will be saved in the working folder, and the scores will be stored in the "all_data.csv" file.

### Notes

- This script requires the BARK and WHISPER libraries to generate and recognize audio files. Ensure that they are installed and configured correctly.
- The voice quality threshold and maximum number of retries can be adjusted to balance the quality and processing time for generating the audio files.
- The script assumes the input CSV files contain phrases in the correct format. Ensure the CSV files are properly formatted before running the script.