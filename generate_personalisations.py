import os
import csv
from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
import simpleaudio as sa
import numpy as np
from utilities import combineCsvs, find_csvs, get_data
# download and load all voice models
preload_models()

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
        while user_input == 'r':
            print("Re-playing...")
            play_obj = wave_obj.play()
            play_obj.wait_done()
            user_input = input("The phrase is: \"" + phrase + "\" Are you happy with the sound? (y/n/r): ").lower()
        if user_input == 'y':
            satisfied = True
        else:
            print("Re-generating...")
