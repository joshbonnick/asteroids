from constants import SCORE_FILE, SCREEN_WIDTH
import json
import pygame

class Score(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        
        self.current = 0
        self.high = 0
        self.session = 0

        self.load()

        self._font = pygame.font.SysFont('Comic Sans MS', 30)
        self._color = (255, 0, 0)
        self._surfaces = None
        self._dirty = True  # needs initial render

    def draw(self, screen: pygame.Surface) -> None:
        if self._dirty:

            lines = [
                { "text": f"Score: {self.current}"},
                { "text": f"Highscore: {self.high}"},
                { "text": "Press R to Restart"},
            ]

            self._surfaces = [
                self._font.render(line["text"], True, self._color)
                for line in lines
            ]

            self._dirty = False

        y = 0
        for surface in self._surfaces:
            screen.blit(surface, (0, y))
            y += surface.get_height()

    def increment(self, delta):
        self.set_score(self.current + delta)
        self._dirty = True

    def set_score(self, score):
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