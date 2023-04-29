from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav

from utilities import combineCsvs, find_csvs, get_data

# Download and load all voice models
preload_models()

# Looks through all subdirectories of a path and returns the paths to every csv file with forward slash
csvs = find_csvs('D:/voice')

# Combine all csv data into one list of tuples, each tuple is (path, text)
data = combineCsvs(get_data, csvs)

# Create audio files from the data
for d in data:
    print(d[0], d[1])
    audio_array = generate_audio(d[1], history_prompt="en_speaker_6")
    write_wav(d[0], SAMPLE_RATE, audio_array)