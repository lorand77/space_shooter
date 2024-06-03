import pygame
import random

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

class PlayerBullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("assets/laserBlue.png").convert_alpha()
		self.image = pygame.transform.scale(self.image, (7, 25))
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.bottom = y

	def update(self):
		self.rect.y -= 15
		if self.rect.bottom < 0:
			self.kill()

class Enemy(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(f"assets/enemy{random.randint(1, 3)}.png").convert_alpha()
		self.image = pygame.transform.scale(self.image, (51, 42))
		self.rect = self.image.get_rect()
		self.rect.centerx = random.randint(50, WIDTH - 50)
		self.rect.top = 0
		self.vx = random.uniform(-6, 6)
		self.vy = random.uniform(0, 4)
		self.shoot_delay = random.uniform(500, 1000)
		self.last_shot_time = pygame.time.get_ticks()

	def move(self):
		self.vx += random.gauss(0, 0.2)
		self.vy += random.gauss(0, 0.15)
		if self.vx > 6:
			self.vx = 6
		if self.vx < -6:
			self.vx = -6
		if self.vy > 4:
			self.vy = 4
		if self.vy < -4:
			self.vy = -4
		
		self.rect.x += self.vx
		self.rect.y += self.vy
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
			self.vx = -self.vx * 0.8
		if self.rect.left < 0:
			self.rect.left = 0
			self.vx = -self.vx * 0.8
		if self.rect.bottom > HEIGHT / 2:
			self.rect.bottom = HEIGHT / 2
			self.vy = -self.vy * 0.8
		if self.rect.top < 0:
			self.rect.top = 0
			self.vy = -self.vy * 0.8

	def shoot(self):
		now = pygame.time.get_ticks()
		if now - self.last_shot_time > self.shoot_delay:
			self.last_shot_time = now
			enemy_bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
			sprites_all.add(enemy_bullet)
			sprites_enemy_bullets.add(enemy_bullet)

	def update(self):
		self.move()
		self.shoot()

class EnemyBullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("assets/laserRed.png").convert_alpha()
		self.image = pygame.transform.scale(self.image, (7, 25))
		self.image = pygame.transform.flip(self.image, False, True)
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.top = y

	def update(self):
		self.rect.y += 12
		if self.rect.top > HEIGHT:
			self.kill()

sprites_all = pygame.sprite.Group()
sprites_enemies = pygame.sprite.Group()
sprites_player_bullets = pygame.sprite.Group()
sprites_enemy_bullets = pygame.sprite.Group()
player = Player()
sprites_all.add(player)

def enemy_create():
	enemy = Enemy()
	sprites_all.add(enemy)
	sprites_enemies.add(enemy)

for i in range(2):
	enemy_create()

enemies_killed = 0

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.JOYBUTTONDOWN and event.button == 0:
			player_bullet = PlayerBullet(player.rect.centerx, player.rect.top)
			sprites_all.add(player_bullet)
			sprites_player_bullets.add(player_bullet)

	sprites_all.update()

	hits = pygame.sprite.groupcollide(sprites_enemies, sprites_player_bullets, dokilla = True, dokillb = True)
	for hit in hits:
		enemy_create()
		enemies_killed += 1
		if enemies_killed % 5 == 0:
			enemy_create()

	screen.blit(background, background.get_rect())
	sprites_all.draw(screen)
	pygame.display.flip()

	clock.tick(FPS)

pygame.quit()