import warnings
import numpy as np
from scipy.io import wavfile
from pathlib import Path

warnings.filterwarnings("ignore", message="Couldn't find ffmpeg or avconv.*")
from pydub import AudioSegment

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH


def relative(path: str):
    return ASSETS_PATH / Path(path)


def audio_steganography(text, audio_path, destination_path):
    """Hides a string in the spectrogram of a .wav audio file
    :param text: string containing the message
    :param audio_path: path to a .wav audio file
    :param destination_path: path to save the generated .wav file
    """

    audio = AudioSegment.from_file(audio_path)
    text_as_audio = np.array([])

    # iterates over the message and concatenates the corresponding character audio snippets
    for character in text:
        if (character.lower() == character and character.upper() != character and character != "ß"):
            character = f"smal_{character}"

        character = format(character)
        data = wavfile.read(relative(f"characters\\{character}.wav"))
        text_as_audio = np.concatenate((text_as_audio, data[1]))


    # overlays the text audio segment with the original audio
    text_as_audio = np.int16(text_as_audio)
    message = AudioSegment.from_mono_audiosegments(
        AudioSegment(
            data=text_as_audio.tobytes(), sample_width=2, frame_rate=44100, channels=1
        )
    )
    combined = audio.overlay(message)

    # exports the combined audio to the destination file
    combined.export(destination_path, format="wav")


def format(character):
    replacements = {
        " ": "sp",
        "\\": "backslash",
        "/": "slash",
        "<": "smaller",
        ">": "greater",
        "?": "question",
        '"': "quotation",
        ":": "colon",
        ".": "period",
        "*": "asterisk",
        "|": "line",
        "`": "'",
        "´": "'",
        "\n": "sp"
    }

    if character in replacements:
        return replacements[character]
    
    return character
