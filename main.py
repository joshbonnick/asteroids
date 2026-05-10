import pygame

from asteroid import Asteroid
from asteroidfield import AsteroidField
from logger import log_state, log_event
from constants import *
from player import Player
from score import Score
from shot import Shot

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}\nScreen height: {SCREEN_HEIGHT}")

    pygame.init()
    pygame.font.init()
    running = True

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    clock = pygame.time.Clock()
    delta_time = 0

    updatable = pygame.sprite.Group()  # type: pygame.sprite.Group
    drawable = pygame.sprite.Group()  # type: pygame.sprite.Group
    asteroids = pygame.sprite.Group()  # type: pygame.sprite.Group
    shots = pygame.sprite.Group() # type: pygame.sprite.Group

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)

    score = Score(drawable)

    AsteroidField.containers = (updatable,)
    AsteroidField()

    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        log_state()
        screen.fill((0, 0, 0))

        updatable.update(delta_time)

        for asteroid in asteroids:
            if player.collides_with(asteroid):
                log_event("player_hit")
                print("Game over!")
                running = False

            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")

                    shot.kill()
                    asteroid.split()

                    score.shot_hit()
                    score.increment(asteroid.score())

        for sprite in drawable:
            sprite.draw(screen)

        pygame.display.flip()
        delta_time = clock.tick(60) / 1000

    score.save()

if __name__ == "__main__":
    main()
