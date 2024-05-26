import wave
from message import Message
from audio_combine import Audio

def encrypt(message_text, carrier_audio_path, char_duration, char_sample_rate):
    with wave.open(carrier_audio_path, 'rb') as f:
        audio_channels = f.getparams().nchannels

    distinct_char_samples = Message.render_message(message_text, audio_channels, char_duration, char_sample_rate)

    message_samples = []
    for char in message_text:
        message_samples.append(distinct_char_samples[char])

    a1 = Audio(message_samples, "out/11.wav")
    a1.overlay_wavs("song.wav")


char_duration = 1
char_sample_rate = 10000

encrypt("TEST", "song.wav", char_duration, char_sample_rate)