import time

class Timer:
    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_time = time.time()
        self.end_time = None

    def stop(self):
        if self.start_time is None:
            return
        self.end_time = time.time()

    def calculate_time(self):
        if self.start_time is None:
            return None
        if self.end_time is None:
            return None
        return self.end_time - self.start_time