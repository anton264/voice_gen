import re
import whisper
import string
from pyphonetics import Metaphone
from fuzzywuzzy import fuzz
from num2words import num2words


def perform_voice_recognition(file_path, model):
    """
    Performs voice recognition on a given file path and returns the text
    It will automatically detect the language
    """
    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(file_path)
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # decode the audio
    options = whisper.DecodingOptions()
    result = whisper.decode(model, mel, options)
    return result.text

def perform_voice_recognition_with_specific_language(file_path, model):
    """
    Performs voice recognition on a given file path and returns the text
    It uses the model with the specific language
    """
    #audio = whisper.load_audio(file_path)
    #audio = whisper.pad_or_trim(audio)
    #mel = whisper.log_mel_spectrogram(audio).to(model.device)
    transcription = model.transcribe(file_path)
    return transcription["text"]

def get_similarity_score(text: str, expected_result: str, phonetics=True) -> int:
    """
    Returns a number between 0 and 100, where 100 is a perfect match
    """
    if text is None or expected_result is None:
        return 0

    try:
        metaphone = Metaphone()
        text = remove_trailing_special_chars(text) or ""
        expected_result = remove_trailing_special_chars(expected_result) or ""
        text = convert_number_to_words(text) or ""
        expected_result = convert_number_to_words(expected_result) or ""
        text = remove_special_chars(text) or ""
        expected_result = remove_special_chars(expected_result) or ""
        if phonetics:
            text = metaphone.phonetics(text) or ""
            expected_result = metaphone.phonetics(expected_result) or ""
        # Compare with metaphone phonetics
        match = fuzz.ratio(text, expected_result)
    except Exception as e:
        print(f"An error occurred: {e}")
        match = 0

    return match


def convert_number_to_words(s: str) -> str:
    """
    Converts numbers in a string to words, e.g. "1" becomes "one"
    """
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


def remove_trailing_special_chars(input_str):
    # Define the allowed characters (alnum: alphanumeric characters)
    allowed_chars = set(string.ascii_letters +
                        string.digits + string.whitespace)

    # Find the last allowed character index
    last_allowed_char_index = len(input_str)
    for index, char in enumerate(reversed(input_str)):
        if char in allowed_chars:
            last_allowed_char_index = len(input_str) - index
            break

    # Slice the input string up to the last allowed character index
    return input_str[:last_allowed_char_index]
