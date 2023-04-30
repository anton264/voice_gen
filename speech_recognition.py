import whisper
from fuzzywuzzy import fuzz


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
    match = fuzz.ratio(text, expected_result)
    return match

