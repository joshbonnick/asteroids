import random

import pygame.draw

from circleshape import CircleShape
from constants import *
from logger import log_event

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

        asteroid_images = [
            "assets/sprites/asteroid.png",
            "assets/sprites/asteroid_2.png",
            "assets/sprites/asteroid_3.png",
        ]

        self.original_surface = pygame.transform.scale(
            pygame.image.load(asteroid_images[int(random.uniform(0, 2))]).convert_alpha(),
            pygame.Vector2(radius*2.1, radius*2.1)
        )

        self.rotation = random.uniform(0, 360)

        base_speed = random.uniform(-180, 180)
        self.rotation_speed = base_speed * (45 / radius)

        self.original_surface = pygame.transform.rotate(
            self.original_surface,
            self.rotation
        )

        self.surface = self.original_surface
        self.bounding_box = self.surface.get_rect()

    def draw(self, screen: pygame.Surface):
        self.bounding_box = self.surface.get_rect(center=self.position)
        screen.blit(self.surface, self.bounding_box)

    def update(self, dt):
        self.position += self.velocity * dt

        # Update rotation using delta time
        self.rotation += self.rotation_speed * dt

        # Keep it bounded (optional but clean)
        self.rotation %= 360

        # Rotate from original each frame
        self.surface = pygame.transform.rotate(self.original_surface, self.rotation)

        # Keep sprite centered
        self.bounding_box = self.surface.get_rect(center=self.position)

    def score(self):
        """Score received for shooting this asteroid"""
        return self.radius * ASTEROID_SCORE_MULTIPLIER

    def split(self):
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return []

        log_event("asteroid_split")

        asteroids = []
        for i in range(2):
            new_radius = self.radius - ASTEROID_MIN_RADIUS
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
            asteroid.velocity = self.velocity.rotate(angle) * 1.2
            asteroids.append(asteroid)

        return asteroids