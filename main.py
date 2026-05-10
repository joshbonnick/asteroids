import pygame
from logger import log_state
from constants import *
from player import Player

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}\nScreen height: {SCREEN_HEIGHT}")

    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    clock = pygame.time.Clock()
    delta_time = 0

    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit
        log_state()
        screen.fill((0, 0, 0))

        player.draw(screen)
        pygame.display.flip()

        delta_time = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
