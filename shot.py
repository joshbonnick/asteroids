from circleshape import CircleShape
from constants import *
from pygame.draw import circle

class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)
        self.velocity = PLAYER_SHOOT_SPEED

    def draw(self, screen):
        circle(screen, (255,0,0), self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt