from image_to_wav import convert_to_spectrogram

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


    def __init__(self, active_segments, output_name):
        # switching to arrays will improve speed -----------------------------------------
        # self.image = array.array('B', [0] * (self.width * self.height))
        # creates an empty image with white background
        self.image =  [[0 for _ in range(self.width)] for _ in range(self.height)]

        self.active_segments = active_segments
        self.output_path = f"out/{output_name}.wav"
        

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

    def render(self, audio_channels=2, duration=1, sample_rate=5000):
        for i, segment in enumerate(self.segments):
            if self.active_segments[i] == "0": continue

            self.__draw_rectangle(segment)

        samples = convert_to_spectrogram(self.image, duration, self.height, self.output_path, sample_rate, audio_channels)

        return samples
