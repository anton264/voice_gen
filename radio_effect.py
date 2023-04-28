import os
import sys
from pydub import AudioSegment
from scipy.io import wavfile
import numpy as np

def apply_radio_effect(file_path):
    rate, data = wavfile.read(file_path)
    # Apply a high-pass and low-pass filter to simulate the radio effect
    # High-pass filter
    b = np.array([1, -3])
    a = np.array([1, -0.65])
    filtered_data = np.convolve(data, b) / a[0]
    
    # Low-pass filter
    low_pass_size = 15
    h = np.ones(low_pass_size) / low_pass_size
    filtered_data = np.convolve(filtered_data, h)
    
    # Write the radio effect data to a new WAV file
    output_path = os.path.splitext(file_path)[0] + '_radio.wav'
    wavfile.write(output_path, rate, filtered_data.astype(np.int16))

def process_directory(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.wav'):
                file_path = os.path.join(root, file)
                apply_radio_effect(file_path)
                print(f'Processed {file_path}')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python radio_effect.py <directory_path>")
        sys.exit(1)

    directory_path = sys.argv[1]
    process_directory(directory_path)
