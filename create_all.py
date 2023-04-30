from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
import os

from utilities import combineCsvs, create_or_reuse_csv_with_all_data, find_csvs, get_data, insert_value_in_column, generate_sound_file, get_value_from_column
import speech_recognition as sr

# Download and load all voice models
print("Loading voice models...")
preload_models()

# Looks through all subdirectories of a path and returns the paths to every csv file with forward slash
csvs = find_csvs('D:/voice')

# Combine all csv data into one list of tuples, each tuple is (path, text)
data = combineCsvs(get_data, csvs)

file_dir = 'D:/voice'
all_data_path = os.path.join(file_dir, "all_data.csvfile")

create_or_reuse_csv_with_all_data(data, all_data_path)

# Create audio files from the data
for d in data:
    print(d[0], d[1])
    # Check if the file already has a score
    raw_value = get_value_from_column(all_data_path, d[0], 4)
    previous_score = int(raw_value) if raw_value is not None else 0
    # Skip if the score is already above 70
    if previous_score > 70:
        print("Skipping", d[0], "because it already has a score of", previous_score)
        continue
    score = 0
    # Check if the file already exists, if it does, check the score
    if os.path.isfile(d[0]) and previous_score == 0:
        voice_recognizer = sr.perform_voice_recognition(d[0])
        score = sr.get_similarity_score(voice_recognizer, d[1])
        print(f"The file {d[0]} already exists and has a score of {score}")
    retries = 0
    while score < 70:
        generate_sound_file(d[0], d[1])
        voice_recognizer = sr.perform_voice_recognition(d[0])
        score = sr.get_similarity_score(voice_recognizer, d[1])
        retries += 1
        if retries > 5:
            break
    # Save score to csv
    insert_value_in_column(all_data_path, d[0], score, 4)
