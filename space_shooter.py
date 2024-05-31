import pygame

WIDTH = 480
HEIGHT = 600
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()

background = pygame.image.load("assets/starfield.png").convert()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)

class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("assets/playerShip.png").convert_alpha()
		self.image = pygame.transform.scale(self.image, (50, 38))
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH / 2
		self.rect.bottom = HEIGHT - 30

	def update(self):
		self.rect.x += joystick.get_axis(0) * 8
		self.rect.y += joystick.get_axis(1) * 5
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0
		if self.rect.bottom > HEIGHT:
			self.rect.bottom = HEIGHT
		if self.rect.top < HEIGHT * 3 / 4:
			self.rect.top = HEIGHT * 3 / 4

sprites_all = pygame.sprite.Group()
player = Player()
sprites_all.add(player)

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	sprites_all.update()

	screen.blit(background, background.get_rect())
	sprites_all.draw(screen)
	pygame.display.flip()

	clock.tick(FPS)

pygame.quit()