import os
import csv
from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
import simpleaudio as sa
import numpy as np

# download and load all voice models
preload_models()

# Looks through all subdirectories of a path and returns the paths to every csv file with forward slash
def find_csvs(path):
    csvs = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".csv"):
                csvs.append(os.path.join(root, file).replace('\\', '/'))
    return csvs

# Returns the path to the directory containing the csv file
def get_dir(csv):
    return os.path.dirname(csv)

# Change csv from comma separated to semicolon separated, ignores commas inside quotes
def change_csv(csv_file):
    print(csv_file)
    input_data = []
    with open(csv_file, 'r', newline='') as f_in:
        reader = csv.reader(f_in, delimiter=',', quotechar='"')
        for row in reader:
            input_data.append(row)

    with open(csv_file, 'w', newline='') as f_out:
        writer = csv.writer(f_out, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(input_data)

# Returns the first and second columns of a csv file as a list of tuples
def get_data(csv):
    data = []
    with open(csv, 'r') as f:
        for line in f:
            line = line.strip().split(';')
            data.append((get_dir(csv) + "/" + line[0], line[1].strip('"')))
    return data

csvs = find_csvs('C:/Users/anton/AppData/Local/CrewChiefV4/sounds/alt/aiJane/personalisations/Anton/prefixes_and_suffixes')


#Change all csvs to semicolon separated
#for csvfile in csvs:
#    print(csvfile)
#    change_csv(csvfile)

# Combine all csv data into one list of tuples, each tuple is (path, text)
data = []
for csv in csvs:
    data += get_data(csv)

name = user_input = input("What name do you want to generate? ").lower().strip()

for d in data:
    satisfied = False
    while not satisfied:
        phrase = d[1] + " " + name
        audio_array = generate_audio(phrase, history_prompt="en_speaker_6")
        audio_array_16bit = np.int16(audio_array * 32767)
        write_wav(d[0], SAMPLE_RATE, audio_array_16bit)
        # Play the generated WAV file
        wave_obj = sa.WaveObject.from_wave_file(d[0])
        play_obj = wave_obj.play()
        play_obj.wait_done()
        # Ask the user if they are satisfied with the sound
        user_input = input("The phrase is: \"" + phrase + "\" Are you happy with the sound? (y/n/r): ").lower()
        if user_input == 'y':
            satisfied = True
        else:
            print("Re-generating...")
