import array
import math
import struct
# from image_to_wav import __convert_to_spectrogram


class Character:
    # x1, y1, x2, y2, height
    segments = (
        (1, 0, 28, 0, 6),
        (24, 1, 29, 1, 29),  
        (24, 30, 29, 30, 26),
        (1, 54, 28, 54, 6),
        (0, 30, 5, 30, 26),
        (0, 1, 5, 1, 29),

        (1, 27, 14, 27, 6),
        (15, 27, 28, 27, 6),

        (6, 5, 15, 29, 6),
        (12, 2, 17, 2, 28),
        (14, 29, 23, 5, 6),

        (2, 52, 11, 29, 6),
        (12, 30, 17, 30, 29),
        (18, 29, 27, 52, 6)
    )

    width = 30
    height = 60


    def __init__(self, active_segments):
        # switching to arrays will improve speed -----------------------------------------
        # self.image = array.array('B', [0] * (self.width * self.height))
        # creates an empty image with white background
        self.image =  [[0 for _ in range(self.width)] for _ in range(self.height)]

        self.active_segments = active_segments
        

    def __draw_rectangle(self, dimensions):
        x1, y1, x2, y2, height = dimensions

        # uses bresenham's algorithm to draw the individual rows of a rectangle
        for i in range(height):
            current_x1 = x1
            current_y1 = y1 + i
            current_x2 = x2
            current_y2 = y2 + i
            
            dx = abs(current_x2 - current_x1)
            dy = abs(current_y2 - current_y1)
            sx = 1 if current_x1 < current_x2 else -1
            sy = 1 if current_y1 < current_y2 else -1
            err = dx - dy

            while True:
                # index = current_y1 * self.width + current_x1
                self.image[current_y1][current_x1] = 100

                if current_x1 == current_x2 and current_y1 == current_y2:
                    break
                # e2 = 2 * err
                e2 = err
                if e2 > -dy:
                    err -= dy
                    current_x1 += sx
                if e2 < dx:
                    err += dx
                    current_y1 += sy


    def __convert_to_spectrogram(self, duration, sample_rate = 44100, audio_channels=2, volume=1):

        # ensures the the Nyquist frequency isn't exeeded
        upper_frequency_boundary = sample_rate / 2 - sample_rate / 50
        lower_frequency_boundary = sample_rate / 4
        
        amount_of_samples = int(sample_rate * duration)

        raw_audio_data = array.array('f')
        normalized_audio_data = array.array('i') #h

        # resizes the image to fit the spectrogram
        self.__adjust_image_width(amount_of_samples)

        # converts the color data of the image to audio data
        for x in range(amount_of_samples):
            time_frame_value = 0.0
            for y in range(self.height):
                frequency = lower_frequency_boundary + ((self.height - y) * (upper_frequency_boundary - lower_frequency_boundary) / self.height)
                time_frame_value += self.image[y][x] * math.sin(2 * math.pi * frequency * x / sample_rate)
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
    

    def __adjust_image_width(self, new_width):
        original_height = len(self.image)
        original_width = len(self.image[0])
        resized_image = [[0 for _ in range(new_width)] for _ in range(original_height)]
        
        for y in range(original_height):
            for x in range(new_width):
                original_x = int(x * original_width / new_width)
                resized_image[y][x] = self.image[y][original_x]

        self.image = resized_image


    def render(self, audio_channels=2, duration=1, sample_rate=5000):
        for i, segment in enumerate(self.segments):
            if self.active_segments[i] == "0": continue

            # TODO
            # resizing can be done directly when drawing the character by multiplying  
            # amount_of_samples = int(sample_rate * duration) 
            # with the x-coordinate of the rect corner
            # the img array then needs to be initialized with the amount_of_samples as its width directly

            self.__draw_rectangle(segment)

        samples = self.__convert_to_spectrogram(duration, sample_rate, audio_channels)

        return samples
    
