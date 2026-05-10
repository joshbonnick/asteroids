from constants import SCORE_FILE
import json

class Score:
    def __init__(self):
        self.current = 0
        self.high = 0
        self.session = 0

        self.load()

    def add(self, delta):
        self.set(self.current + delta)

    def set(self, score):
        self.current = score

        if self.current > self.high:
            self.high = self.current

    def save(self):
        try:
            with open(SCORE_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}

        if "sessions" not in data:
            data["sessions"] = {}

        data["sessions"][self.session] = self.current

        with open(SCORE_FILE, "w+") as f:
            f.write(json.dumps({
                "highscore": self.high,
                "sessions": data["sessions"]
            }))

    def load(self):
        try:
            with open(SCORE_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            if "highscore" in data:
                self.high = int(data["highscore"])
            else:
                self.high = 0

            if "sessions" in data:
                self.session = len(data["sessions"])
            else:
                self.session = 0

        except FileNotFoundError:
            self.high = 0
            self.session = 0