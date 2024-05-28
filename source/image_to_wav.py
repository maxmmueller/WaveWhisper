import array
import math
import struct

def __convert_to_spectrogram(image_array, duration, resolution, output_path, sample_rate = 44100, audio_channels=2, volume=1):

    # ensures the the Nyquist frequency isn't exeeded
    upper_frequency_boundary = sample_rate / 2 - sample_rate / 50
    lower_frequency_boundary = sample_rate / 4
    
    amount_of_samples = int(sample_rate * duration)

    raw_audio_data = array.array('f')
    normalized_audio_data = array.array('i') #h

    # resizes the image to fit the spectrogram
    image_array = adjust_image_width(image_array, amount_of_samples)

    # converts the color data of the image to audio data
    for x in range(amount_of_samples):
        time_frame_value = 0.0
        for y in range(resolution):
            frequency = lower_frequency_boundary + ((resolution - y) * (upper_frequency_boundary - lower_frequency_boundary) / resolution)
            time_frame_value += image_array[y][x] * math.sin(2 * math.pi * frequency * x / sample_rate)
        raw_audio_data.append(time_frame_value)

    peak_frequency = max(raw_audio_data, key=abs)

    # normalizes the frequency values
    for i in range(len(raw_audio_data)):
        data = int(32767 * volume * raw_audio_data[i] / peak_frequency)
        normalized_audio_data.append(data)
        if audio_channels == 2:
            normalized_audio_data.append(data)

    # with wave.open(output_path, 'w') as file:
    #     file.setparams((audio_channels, 2, sample_rate, amount_of_samples, "NONE", "Uncompressed"))
    #     file.writeframes(normalized_audio_data.tobytes())
        
    frames = normalized_audio_data.tobytes()
    samples = struct.unpack_from('<' + 'h' * amount_of_samples * audio_channels, frames)

    return samples


def adjust_image_width(image, new_width):
    original_height = len(image)
    original_width = len(image[0])
    resized_image = [[0 for _ in range(new_width)] for _ in range(original_height)]
    
    for y in range(original_height):
        for x in range(new_width):
            original_x = int(x * original_width / new_width)
            resized_image[y][x] = image[y][original_x]
    
    return resized_image