import re
import whisper
from pyphonetics import Metaphone
from fuzzywuzzy import fuzz
from num2words import num2words


def perform_voice_recognition(file_path):
    """
    Performs voice recognition on a given file path and returns the text
    """
    model = whisper.load_model("base")
# load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(file_path)
    audio = whisper.pad_or_trim(audio)
# make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
# decode the audio
    options = whisper.DecodingOptions()
    result = whisper.decode(model, mel, options)
    return result.text


def get_similarity_score(text: str, expected_result: str) -> int:
    """
    Returns a number between 0 and 100, where 100 is a perfect match
    """
    metaphone = Metaphone()   
    text = convert_number_to_words(text)
    expected_result = convert_number_to_words(expected_result)
    text = remove_special_chars(text)
    expected_result = remove_special_chars(expected_result)
    # Compare with metaphone phonetics
    match = fuzz.ratio(metaphone.phonetics(text), metaphone.phonetics(expected_result))
    return match

def convert_number_to_words(s: str) -> str:
    def is_number(word: str) -> bool:
        return re.match(r'^-?\d+(\.\d+)?$', word)

    def split_leading_zero(word: str) -> str:
        if word.startswith('0') and len(word) > 1:
            return '0 ' + word[1:]
        return word

    words = s.split()
    converted_words = []

    for word in words:
        word = split_leading_zero(word)
        if is_number(word):
            word = num2words(float(word))
        converted_words.append(word)

    return ' '.join(converted_words)


def remove_special_chars(text: str) -> str:
    """
    Removes special characters and punctuation from the input string.
    """
    return re.sub(r"[^\w\s]", "", text)    