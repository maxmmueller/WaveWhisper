import array
import math
import wave
import time

def convert_to_spectrogram(image_array, duration, resolution, output_path, sample_rate = 44100, audio_channels=2, volume=1):
    start_time = time.time()

    # ensures the the Nyquist frequency isn't exeeded
    upper_frequency_boundary = sample_rate / 2 - sample_rate / 50
    lower_frequency_boundary = sample_rate / 4
    
    amount_of_samples = int(sample_rate * duration)

    raw_audio_data = array.array('f')
    normalized_audio_data = array.array('h')

    # resizes the image to fit the spectrogram using bilinear interpolation
    image_array = resize_image(image_array, amount_of_samples, resolution)

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

    with wave.open(output_path, 'w') as file:
        file.setparams((audio_channels, 2, sample_rate, amount_of_samples, "NONE", "Uncompressed"))
        file.writeframes(normalized_audio_data.tobytes())
        
        print(time.time() - start_time)


def resize_image(image, new_width, new_height):
    height = len(image)
    width = len(image[0])
    
    resized_image = [[0] * new_width for _ in range(new_height)]
    
    for new_row in range(new_height):
        for new_col in range(new_width):
            old_row = (new_row * height) / new_height
            old_col = (new_col * width) / new_width

            row1 = int(old_row)
            row2 = min(row1 + 1, height - 1)
            col1 = int(old_col)
            col2 = min(col1 + 1, width - 1)

            row_frac = old_row - row1
            col_frac = old_col - col1
            
            top_left = image[row1][col1]
            top_right = image[row1][col2]
            bottom_left = image[row2][col1]
            bottom_right = image[row2][col2]
            
            top = top_left + (top_right - top_left) * col_frac
            bottom = bottom_left + (bottom_right - bottom_left) * col_frac
            pixel_value = int(top + (bottom - top) * row_frac)
            
            resized_image[new_row][new_col] = pixel_value

    return resized_image