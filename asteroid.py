import random

import pygame.draw

from circleshape import CircleShape
from constants import *
from logger import log_event


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, (255,255,255), self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return []

        log_event("asteroid_split")

        asteroids = []
        for i in range(2):
            new_radius = self.radius / ASTEROID_KINDS
            if new_radius < ASTEROID_MIN_RADIUS:
                new_radius = ASTEROID_MIN_RADIUS

            if i == 0:
                new_x = self.position.x + new_radius
                new_y = self.position.y + new_radius
                angle = random.uniform(20, 50)
            else:
                new_x = self.position.x - new_radius
                new_y = self.position.y - new_radius
                angle = -random.uniform(20, 50)

            asteroid = Asteroid(new_x, new_y, new_radius)
            asteroid.velocity = self.velocity.rotate(angle)
            asteroids.append(asteroid)

        return asteroids