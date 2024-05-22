import wave
import struct

def read_wav(file_path):
    with wave.open(file_path, 'rb') as wf:
        params = wf.getparams()
        frames = wf.readframes(params.nframes)
        samples = struct.unpack_from('<' + 'h' * params.nframes * params.nchannels, frames)
    return params, samples

def write_wav(file_path, params, samples):
    with wave.open(file_path, 'wb') as wf:
        wf.setparams(params)
        frames = struct.pack('<' + 'h' * len(samples), *samples)
        wf.writeframes(frames)

def overlay_wavs(samples1, samples2):
    combined_samples = []
    length1, length2 = len(samples1), len(samples2)
    max_length = max(length1, length2)

    for i in range(max_length):
        sample1 = samples1[i] if i < length1 else 0
        sample2 = samples2[i] if i < length2 else 0
        combined_samples.append(int((sample1 + sample2) / 2))

    return combined_samples

# Paths to your WAV files
file1_path = 'song.wav'
file2_path = '1o.wav'
output_path = 'combined.wav'

# Read the WAV files
params1, samples1 = read_wav(file1_path)
params2, samples2 = read_wav(file2_path)

# Ensure the parameters are the same
# if params1 != params2:
#     raise ValueError("The WAV files have different parameters and cannot be combined directly")

# Overlay the samples
combined_samples = overlay_wavs(samples1, samples2)

# Write the combined audio to a new file
write_wav(output_path, params1, combined_samples)

print(params1)
