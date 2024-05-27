import pygame
import random

WIDTH = 480
HEIGHT = 600
FPS = 60

# colors R  G  B
BLACK = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()

running = True
while running:
	clock.tick(FPS)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	screen.fill(BLACK)
	pygame.display.flip()

pygame.quit()