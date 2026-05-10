import singleton
from constants import SCORE_FILE, SCREEN_WIDTH
import json
import pygame

from singleton import singleton


@singleton
class Score(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        
        self.current = 0
        self.high = 0
        self.session = 0

        self.shots_fired = 0
        self.shots_hit = 0

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
            ]

            if self.shots_fired > 0:
                lines.append({ "text": f"Accuracy: {self.shots_hit / self.shots_fired * 100:.0f}%"})

            self._surfaces = [
                self._font.render(line["text"], True, self._color)
                for line in lines
            ]

            self._dirty = False

        line_spacing = 5
        y = 10 # 10px padding
        for surface in self._surfaces:
            rect = surface.get_rect(topright=(screen.get_width() - 10, y))
            screen.blit(surface, rect)
            y += surface.get_height() + line_spacing

    def increment(self, delta):
        self.set_score(self.current + delta)
        self._dirty = True

    def shot_fired(self, delta = 1):
        self.shots_fired += delta
        self._dirty = True

    def shot_hit(self, delta = 1):
        self.shots_hit += delta
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

        data["sessions"][self.session] = { "score": self.current, "shots_fired": self.shots_fired}

        with open(SCORE_FILE, "w+") as f:
            f.write(json.dumps({
                "sessions": data["sessions"]
            }, separators=(",", ":")) )

    def load(self):
        try:
            with open(SCORE_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            high = 0
            for session, entry in data["sessions"].items():
                self.session = max(self.session, int(session))
                score = entry["score"]
                if float(score) > high:
                    high = float(score)

            self.session += 1
            self.high = high

        except FileNotFoundError:
            self.high = 0
            self.session = 0