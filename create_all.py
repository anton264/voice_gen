from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
import os
import shutil
import whisper
from utilities import combineCsvs, create_or_reuse_csv_with_all_data, find_csvs, get_data, insert_value_in_column, generate_sound_file, get_value_from_column
import speech_recognition as sr

os.system("cls")
print("👂 Loading voice recognition models...")
# voice_recognition_model = whisper.load_model("base.en")
voice_recognition_model = whisper.load_model("base")

# Download and load all voice models
print("🗣️  Loading voice generation models...")
preload_models()


# Looks through all subdirectories of a path and returns the paths to every csv file with forward slash
workfolder = 'D:/workdir2/corners'
voice_threshold = 90
max_retries = 20

csvs = find_csvs(workfolder)


# Combine all csv data into one list of tuples, each tuple is (path, text)
data = combineCsvs(get_data, csvs)

file_dir = workfolder
all_data_path = os.path.join(file_dir, "all_data.csvfile")

create_or_reuse_csv_with_all_data(data, all_data_path)

# Create audio files from the data
for item in data:
    file_path, expected_phrase = item

    # Check if the file already has a score
    raw_value = get_value_from_column(all_data_path, file_path, 4)
    previous_score = int(raw_value) if raw_value is not None else 0

    # Skip if the score is already above voice_threshold
    if previous_score >= voice_threshold:
        print(
            f"✅ Skipping {file_path} because it already has a score of {previous_score}, which is above the threshold of {voice_threshold}")
        continue

    score = 0
    # Check if the file already exists, if it does, check the score and update previous_score
    if os.path.isfile(file_path) and previous_score == 0:
        recognized_phrase = sr.perform_voice_recognition(
            file_path, voice_recognition_model)
        score = sr.get_similarity_score(
            recognized_phrase.lower(), expected_phrase.lower())
        print(
            f"The file {file_path} already exists and has a score of {score}")
        previous_score = score

    retries = 0
    max_score = score
    max_score_path = file_path
    insert_value_in_column(all_data_path, file_path, max_score, 4)

    while score < voice_threshold:
        temp_file_path = f"{file_path[:-4]}_{retries}.wav"
        generate_sound_file(temp_file_path, expected_phrase, 0.1)
        recognized_phrase = sr.perform_voice_recognition(
            temp_file_path, voice_recognition_model)
        score = sr.get_similarity_score(
            recognized_phrase.lower(), expected_phrase.lower())
        retries += 1

        # Update max_score and max_score_path
        if score > max_score:
            max_score = score
            max_score_path = temp_file_path
            # If the score is better than the previous score, copy the file to the original file path
            if score > previous_score:
                shutil.copy(max_score_path, file_path)
                # Save score to csv
                insert_value_in_column(all_data_path, file_path, max_score, 4)
        # Delete the temp file, it has served its purpose
        os.remove(temp_file_path)
        
        
        print(f"""💬 The file: {temp_file_path}\n👂 I heard: {recognized_phrase} \n📖 It should be: {expected_phrase} \n💯 It scored: {score} points\n🔢 This was attempt number {retries} out of {max_retries}\n🔂 The best attempt so far got a score of {max_score}""")
        if retries >= max_retries:
            print(f"🚫 The phrase: {expected_phrase} was skipped because it failed to reach the threshold of {voice_threshold} after {max_retries} retries\n🔂 The best attempt got a score of {max_score}")
            break
    insert_value_in_column(all_data_path, file_path, max_score, 4)
