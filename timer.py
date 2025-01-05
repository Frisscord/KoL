import time

class Timer:
    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_time = time.time()
        self.end_time = None
        print("Timer wurde gestartet.")

    def stop(self):
        if self.start_time is None:
            print("Timer wurde noch nicht gestartet.")
            return
        self.end_time = time.time()
        print("Timer gestoppt.")

    def calculate_time(self):
        if self.start_time is None:
            print("Timer wurde noch nicht gestartet.")
            return None
        if self.end_time is None:
            print("Timer läuft noch.")
            return None
        return self.end_time - self.start_time