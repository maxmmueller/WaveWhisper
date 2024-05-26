import wave
import struct

class Audio:
    def __init__(self, message_char_samples, output_path):

        self.output_path = output_path
        # self.append_samples(message_file_paths)
        self.append_samples(message_char_samples)

        # self.audio_channels = audio_channels * char_duration
        # self.char_duration = char_duration
        # self.char_sample_rate = char_sample_rate

    def __read_wav(self, file_path):
        with wave.open(file_path, 'rb') as wf:
            params = wf.getparams()
            frames = wf.readframes(params.nframes)
            samples = struct.unpack_from('<' + 'h' * params.nframes * params.nchannels, frames)
        return samples
    

    def __write_wav(self, output_path, samples):
        with wave.open(output_path, 'wb') as wf:

            audio_channels = 2
            sample_rate = 10000
            amount_of_samples = 10000
            wf.setparams((audio_channels, 2, sample_rate, amount_of_samples, "NONE", "Uncompressed"))
            # wf.setparams(params)

            frames = struct.pack('<' + 'h' * len(samples), *samples)
            wf.writeframes(frames)


    def append_samples(self, message_char_samples):
        self.combined_message_samples = []

        # duration = 1
        # resolution = self.height
        # sample_rate = 10000

        for char_samples in message_char_samples:
            # samples = struct.unpack_from('<' + 'h' * params.nframes * params.nchannels, frames)

            self.combined_message_samples.extend(char_samples)

        # for file_path in message_file_paths:
        #     samples = self.__read_wav(file_path)
        #     # self.message_samples.append(samples)
        #     self.combined_message_samples.extend(samples)

        # self.__write_wav("message.wav", self.combined_message_samples)


    def overlay_wavs(self, carrier_path):
        # message_samples = self.__read_wav("message.wav")
        carrier_samples = self.__read_wav(carrier_path)

        combined_samples = []
        length1, length2 = len(self.combined_message_samples), len(carrier_samples)
        max_length = max(length1, length2)

        for i in range(max_length):
            sample1 = self.combined_message_samples[i] if i < length1 else 0
            sample2 = carrier_samples[i] if i < length2 else 0
            combined_samples.append(int((sample1 + sample2) / 2))

        self.__write_wav(self.output_path, combined_samples)



# file_paths = ['out/H.wav', 'out/A.wav', 'out/L.wav', 'out/L.wav', 'out/O.wav']
# a1 = Audio(file_paths, "test.wav")

# a1.overlay_wavs("song.wav")
