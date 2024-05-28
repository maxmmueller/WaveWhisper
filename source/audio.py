import wave
import struct

class Audio:
    def __init__(self, message_char_samples):
        self.__append_samples(message_char_samples)


    def __read_wav(self, file_path):
        with wave.open(file_path, 'rb') as f:
            params = f.getparams()
            frames = f.readframes(params.nframes)
            samples = struct.unpack_from('<' + 'h' * params.nframes * params.nchannels, frames)
        return samples
    

    def __write_wav(self, output_path, samples, params):
        with wave.open(output_path, 'wb') as f:
            f.setparams(params)
            frames = struct.pack('<' + 'h' * len(samples), *samples)
            f.writeframes(frames)


    def __append_samples(self, message_char_samples):
        self.combined_message_samples = []

        for char_samples in message_char_samples:
            self.combined_message_samples.extend(char_samples)


    def overlay_wavs(self, carrier_path, output_path):
        # message_samples = self.__read_wav("message.wav")
        carrier_samples = self.__read_wav(carrier_path)

        combined_samples = []
        length1, length2 = len(self.combined_message_samples), len(carrier_samples)
        max_length = max(length1, length2)

        for i in range(max_length):
            sample1 = self.combined_message_samples[i] if i < length1 else 0
            sample2 = carrier_samples[i] if i < length2 else 0
            combined_samples.append(int((sample1 + sample2) / 2))


        with wave.open(carrier_path, 'rb') as f:
            params = f.getparams()

        self.__write_wav(output_path, combined_samples, params)
