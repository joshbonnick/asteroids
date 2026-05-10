from circleshape import CircleShape
from constants import *
import pygame

class Shot(CircleShape):
    def __init__(self, x, y, rotation):
        super().__init__(x, y, SHOT_RADIUS)
        self.velocity = PLAYER_SHOOT_SPEED

        self.image = pygame.image.load('assets/sprites/shot.png').convert_alpha()
        self.image = pygame.transform.rotate(self.image, rotation)
        self.image = pygame.transform.scale(self.image, (SHOT_RADIUS * 4, SHOT_RADIUS * 4))

        self.bounding_box = self.image.get_rect(center=self.position)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.bounding_box)

    def update(self, dt):
        self.position += self.velocity * dt
        self.bounding_box = self.image.get_rect(center=self.position)