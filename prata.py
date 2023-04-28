import os
import csv
from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav

# Download and load all voice models
preload_models()

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

csvs = find_csvs('D:/voice')

# Combine all csv data into one list of tuples, each tuple is (path, text)
def combineCsvs(get_data, csvs):
    data = []
    for csv in csvs:
        data += get_data(csv)
    return data

data = combineCsvs(get_data, csvs)

# Create audio files from the data
for d in data:
    print(d[0], d[1])
    audio_array = generate_audio(d[1], history_prompt="en_speaker_6")
    write_wav(d[0], SAMPLE_RATE, audio_array)