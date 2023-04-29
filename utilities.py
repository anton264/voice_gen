

import csv
import os

from pydub import AudioSegment
from pydub.silence import detect_nonsilent


def remove_silence_from_audio(audio_file_path, output_file_path, silence_threshold=-40.0, min_silence_len=100):
    print(f"Processing {audio_file_path} -> {output_file_path}...")
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


def get_dir(csv):
    """
    Returns the path to the directory containing the csv file
    """
    return os.path.dirname(csv)


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


def get_data(csv):
    """
    Returns the first and second columns of a csv file as a list of tuples
    """
    data = []
    with open(csv, 'r') as f:
        for line in f:
            line = line.strip().split(';')
            data.append((get_dir(csv) + "/" + line[0], line[1].strip('"')))
    return data


def combineCsvs(get_data, csvs):
    """
    Combine all csv data into one list of tuples, each tuple is (path, text)
    """
    data = []
    for csv in csvs:
        data += get_data(csv)
    return data