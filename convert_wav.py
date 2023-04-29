import os
from pydub import AudioSegment

def convert_wav(input_path, output_path, bitrate=384000):
    audio = AudioSegment.from_wav(input_path)
    audio = audio.set_frame_rate(44100).set_channels(2)  # Assuming 44.1kHz and stereo
    audio.export(output_path, format="wav", bitrate=str(bitrate))
    print("Converted " + input_path + " to " + output_path)

def process_directory_tree(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith(".wav"):
                input_path = os.path.join(dirpath, filename)
                output_path = os.path.join(dirpath, os.path.splitext(filename)[0] + ".wav")
                convert_wav(input_path, output_path)

if __name__ == "__main__":
    root_dir = input("Enter the root directory path: ")
    process_directory_tree(root_dir)
    print("Conversion complete.")
