import os
import csv

def create_subtitles_csv(directory):
    for root, dirs, files in os.walk(directory):
        if root == directory:
            continue

        subtitle_file = os.path.join(root, 'subtitles.csv')
        wav_files = [f for f in files if f.endswith('.wav')]

        if wav_files:
            with open(subtitle_file, 'w', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile, delimiter=';')
                folder_name = os.path.basename(root)

                for wav_file in wav_files:
                    csv_writer.writerow([wav_file, folder_name])

if __name__ == "__main__":
    target_directory = input("Enter the directory path: ")
    create_subtitles_csv(target_directory)
