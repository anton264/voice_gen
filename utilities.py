

import csv
import os
import numpy as np
from bark import SAMPLE_RATE, generate_audio

from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import simpleaudio as sa
from scipy.io.wavfile import write as write_wav


def remove_silence_from_audio(audio_file_path, output_file_path, silence_threshold=-40.0, min_silence_len=100):
    print(f"Removing silence {audio_file_path} -> {output_file_path}...")
    audio = AudioSegment.from_wav(audio_file_path)
    non_silent_ranges = detect_nonsilent(audio, min_silence_len, silence_threshold)

    if len(non_silent_ranges) == 0:
        print(f"No audio found in {audio_file_path}. Skipping.")
        return

    start_trim = non_silent_ranges[0][0]
    end_trim = non_silent_ranges[-1][1]
    trimmed_audio = audio[start_trim:end_trim]
    trimmed_audio.export(output_file_path, format="wav")


def remove_silence_from_all_files(root_dir, output_dir):
    for folder, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".wav"):
                input_path = os.path.join(folder, file)
                output_folder = os.path.relpath(folder, root_dir)
                os.makedirs(os.path.join(output_dir, output_folder), exist_ok=True)
                output_path = os.path.join(output_dir, output_folder, file)
                remove_silence_from_audio(input_path, output_path)
                print(f"Processed {input_path} -> {output_path}")


def find_csvs(path):
    """
    Looks through all subdirectories of a path and returns the paths to every csv file with forward slash
    """
    csvs = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".csv"):
                csvs.append(os.path.join(root, file).replace('\\', '/'))
    return csvs


def get_dir(csvFile):
    """
    Returns the path to the directory containing the csv file
    """
    return os.path.dirname(csvFile)


def change_csv(csv_file):
    """
    Change csv from comma separated to semicolon separated, ignores commas inside quotes
    """
    print(csv_file)
    input_data = []
    with open(csv_file, 'r', newline='') as f_in:
        reader = csv.reader(f_in, delimiter=',', quotechar='"')
        for row in reader:
            input_data.append(row)

    with open(csv_file, 'w', newline='') as f_out:
        writer = csv.writer(f_out, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(input_data)


def get_data(file_path, delimiter=';'):
    """
    Returns the first and second columns of a CSV file as a list of tuples.
    """
    data = []

    with open(file_path, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=delimiter)
        # Get path of csv file
        
        fileDir = os.path.dirname(file_path)
        
        for row in csv_reader:
            if len(row) >= 2:
                data.append((fileDir + "/" + row[0], row[1]))

    return data


def combineCsvs(get_data, csvs):
    """
    Combine all csv data into one list of tuples, each tuple is (path, text)
    """
    data = []
    for c in csvs:
        data += get_data(c)
    return data


def insert_value_in_column(file_path, search_value, new_value, column_number, delimiter=';'):
    data = []

    # Read the CSV file and store the content in a list
    with open(file_path, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=delimiter)
        for row in csv_reader:
            data.append(row)

    # Find the row based on the first column value and insert the new value in the specified column
    for row in data:
        if row[0] == search_value:
            if len(row) < column_number:
                row.extend([None] * (column_number - len(row)))  # Extend the row to have at least column_number columns
            row[column_number - 1] = new_value

    # Write the updated data to the CSV file
    with open(file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=delimiter)
        csv_writer.writerows(data)

def get_value_from_column(file_path, search_value, column_number, delimiter=';'):
    data = []

    # Read the CSV file and store the content in a list
    with open(file_path, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=delimiter)
        for row in csv_reader:
            data.append(row)

    # Find the row based on the first column value and return the value from the specified column
    for row in data:
        if row[0] == search_value:
            if len(row) < column_number:
                return None  # The row doesn't have the specified column, return None
            else:
                return row[column_number - 1]

    return None


def tuples_to_csv(tuples_list, file_name):
    with open(file_name, 'w', newline='') as theFile:
        csv_writer = csv.writer(theFile, delimiter=';')
        for row in tuples_list:
            csv_writer.writerow(row)


def get_all_files_to_edit_manually(all_data):
    files_to_edit_manually = []
    with open(all_data, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=';')
        for row in csv_reader:
            if row[2] == 'e':
                files_to_edit_manually.append(row[0])
    return files_to_edit_manually


def generate_sound_file(d, phrase, voice_waveform_temp=0.7, speaker_voice="en_speaker_6"):
    audio_array = generate_audio(
            phrase, history_prompt=speaker_voice, waveform_temp=voice_waveform_temp)
    audio_array_16bit = np.int16(audio_array * 32767)
    write_wav(d, SAMPLE_RATE, audio_array_16bit)
    remove_silence_from_audio(d, d)
    wave_obj = sa.WaveObject.from_wave_file(d)
    return wave_obj


# Check if all_data.csvfile exists, if it does compare length of data and all_data
def create_or_reuse_csv_with_all_data(data, all_data_path):
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


def play_sound_and_get_feedback_from_human(phrase, wave_obj):
    play_obj = wave_obj.play()
    play_obj.wait_done()
    user_input = input(
        f'The phrase is: \n\n "{phrase}"\n\nAre you happy with the sound? \n'
        f'(y)es\n(n)o (Re-generate)\n(r)eplay\n(e)dit manually later): '
    ).lower()

    return user_input