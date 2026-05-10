from circleshape import CircleShape
import pygame
from constants import *
from shot import Shot
from score import Score
from maths import *

class Player(CircleShape):
    shot_cooldown = 0

    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)

        self.rotation = 0

        self.original_surface = pygame.transform.scale(
            pygame.image.load("assets/sprites/player.png").convert_alpha(),
            pygame.Vector2(PLAYER_RADIUS*2, PLAYER_RADIUS*2)
        )
        self.original_surface = pygame.transform.rotate(self.original_surface, 180)

        self.surface = self.original_surface
        self.bounding_box = self.surface.get_rect()

        self.shooting_sound = pygame.mixer.Sound("assets/sfx/laser.ogg")

    def draw(self, screen: pygame.Surface):
        self.bounding_box = self.surface.get_rect(center=self.position)
        return screen.blit(self.surface, self.bounding_box)

    def collides_with(self, other):
        if not hasattr(other, "position"):
            return False

        return (other.position - closest_point_on_triangle(other.position, *self.triangle())).length() < other.radius

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def update(self, dt):
        self.shot_cooldown -= dt

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

    def move(self, dt):
        self.position += pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SPEED * dt

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
        self.surface = pygame.transform.rotate(self.original_surface, -self.rotation)
        self.bounding_box = self.surface.get_rect()

    def shoot(self):
        if self.shot_cooldown > 0:
            return None

        self.shot_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS

        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

        self.shooting_sound.play()

        Score().shot_fired()

        return shot