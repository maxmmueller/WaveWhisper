from picture_to_wav import convert_to_spectrogram

class Character:
    def __init__(self, active_segments):
        self.width = 541
        self.height = 1041

        # creates an empty image with white background
        # switching to arrays will improve speed -----------------------------------------
        # self.image = array('B', [0] * (self.width * self.height))
        self.image =  [[0 for _ in range(self.width)] for _ in range(self.height)]

        # x1, y1, x2, y2, height
        self.segments = {
            'A': (50, 0, 490, 0, 40),
            'B': (500, 50, 540, 50, 440),  
            'C': (500, 550, 540, 550, 440),
            'D': (50, 1000, 490, 1000, 40),
            'E': (0, 550, 40, 550, 440),
            'F': (0, 50, 40, 50, 440),
            'G1': (50, 500, 240, 500, 40),
            'G2': (300, 500, 490, 500, 40),
            'H': (55, 55, 235, 380, 100),
            'I': (250, 50, 290, 50, 440),
            'J': (305, 380, 485, 55, 100),
            'K': (55, 880, 235, 555, 100),
            'L': (250, 550, 290, 550, 440),
            'M': (305, 555, 485, 880, 100)
        }

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


    def render_character(self):
        for segment in self.active_segments:
            self.__draw_rectangle(self.segments.get(segment))

        duration = 1
        resolution = 100
        convert_to_spectrogram(self.image, duration, resolution,"1o.wav")

myChar = Character(("F", "E", "A", "G1", "G2", "B", "H"))
myChar.render_character()