from circleshape import CircleShape
import pygame
from constants import PLAYER_RADIUS, LINE_WIDTH

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)

        self.rotation = 0

    def draw(self, screen):
        return pygame.draw.polygon(screen, (255, 255, 255), self.triangle(), LINE_WIDTH)

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]