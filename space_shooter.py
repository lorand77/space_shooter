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

class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((50, 50))
		self.image.fill((0, 255, 0))
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH / 2
		self.rect.bottom = HEIGHT - 30

sprites_all = pygame.sprite.Group()
player = Player()
sprites_all.add(player)

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	screen.fill(BLACK)
	sprites_all.draw(screen)
	pygame.display.flip()

	clock.tick(FPS)

pygame.quit()