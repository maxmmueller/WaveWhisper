import array
import math
import struct


class Character:
    # x1, y1, x2, y2, height of each segment of a virtual 14-segment display
    segments = (
        (1, 0, 28, 0, 6),      # a
        (24, 1, 29, 1, 29),    # b
        (24, 30, 29, 30, 26),  # c
        (1, 54, 28, 54, 6),    # d
        (0, 30, 5, 30, 26),    # e
        (0, 1, 5, 1, 29),      # f
        (1, 27, 14, 27, 6),    # g1
        (15, 27, 28, 27, 6),   # g2
        (6, 5, 15, 29, 6),     # h
        (12, 2, 17, 2, 28),    # i
        (14, 29, 23, 5, 6),    # j
        (2, 52, 11, 29, 6),    # k
        (12, 30, 17, 30, 29),  # l
        (18, 29, 27, 52, 6)    # m
    )

    width = 30
    height = 60


    def __init__(self, active_segments, samples_per_char):
        # initializes an all white image
        # self.image =  [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.image =  [[0 for _ in range(samples_per_char)] for _ in range(self.height)]
        self.active_segments = active_segments
        self.samples_per_char = samples_per_char
        

    def __draw_rectangle(self, dimensions):
        """Draws the segments of a virtual 14-segment display"""
        x1, y1, x2, y2, height = dimensions

        x1 = int(x1 / (self.width-1) * (self.samples_per_char-1))
        x2 = int(x2 / (self.width-1) * (self.samples_per_char-1))

        # uses Bresenham's algorithm to draw the individual rows of a rectangle
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


    def __convert_to_spectrogram(self, audio_channels=2, volume=0.1):
        # ensures the the Nyquist frequency isn't exeeded
        upper_frequency_boundary = self.carrier_rate / 2 - self.carrier_rate / 50
        lower_frequency_boundary = self.carrier_rate / 4
        
        raw_audio_data = array.array('f')
        normalized_audio_data = array.array('h')

        # resizes the image to fit the spectrogram
        # self.__adjust_image_width(self.samples_per_char)

        # converts the color data of the image to audio data
        for x in range(self.samples_per_char):
            time_frame_value = 0.0
            for y in range(self.height):
                frequency = lower_frequency_boundary + ((self.height - y) * (upper_frequency_boundary - lower_frequency_boundary) / self.height)
                time_frame_value += self.image[y][x] * math.sin(2 * math.pi * frequency * x / self.carrier_rate)
            raw_audio_data.append(time_frame_value)

        peak_frequency = max(raw_audio_data, key=abs)

        # normalizes the frequency values
        for i in range(len(raw_audio_data)):
            data = int(32767 * volume * raw_audio_data[i] / peak_frequency)
            normalized_audio_data.append(data)
            if audio_channels == 2:
                normalized_audio_data.append(data)

        frames = normalized_audio_data.tobytes()
        samples = struct.unpack_from('<' + 'h' * self.samples_per_char * audio_channels, frames)

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


    def render_char(self, audio_channels, carrier_rate):
        # self.samples_per_char = samples_per_char
        self.carrier_rate = carrier_rate
        # draws the character on a virtual 14-segment display
        for i, segment in enumerate(self.segments):
            if self.active_segments[i] == "0": continue

            self.__draw_rectangle(segment)

        # converts the character-image to audio data
        samples = self.__convert_to_spectrogram(audio_channels)

        return samples
