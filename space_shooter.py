import pygame
import random

WIDTH = 480
HEIGHT = 600
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")
background = pygame.image.load("assets/starfield.png").convert()

clock = pygame.time.Clock()

pygame.mixer.init()
sound_shoot = pygame.mixer.Sound("assets/pew.wav")
sound_enemy_expl = pygame.mixer.Sound("assets/expl.wav")

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
		self.health = 100
		self.last_heal_time = pygame.time.get_ticks()
		self.heal_delay = 300

	def heal(self):
		now = pygame.time.get_ticks()
		if now - self.last_heal_time > self.heal_delay and enemies_now > 1:
			self.last_heal_time = now
			self.health += 1
			if self.health > 100:
				self.health = 100

	def move(self):
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

	def update(self):
		self.heal()
		self.move()

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

enemies_now = 0
enemies_level = 2

def create_enemy():
	global enemies_now
	enemy = Enemy()
	enemies_now += 1
	sprites_all.add(enemy)
	sprites_enemies.add(enemy)

for i in range(enemies_level):
	create_enemy()

def draw_health_bar(surf, x, y, health):
	if health < 0:
		health = 0
	BAR_LENGHT = 100
	BAR_HEIGHT = 10
	fill = health / 100 * BAR_LENGHT
	outline_rect = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
	fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
	pygame.draw.rect(surf, "green", fill_rect)
	pygame.draw.rect(surf, "white", outline_rect, 2)

def draw_text(surf, text, size, x, y):
	font_name = pygame.font.match_font("Comic Sans MS")
	font = pygame.font.Font(font_name, size)
	text_surf = font.render(text, True, "white")
	text_rect = text_surf.get_rect()
	text_rect.topright = (x, y)
	surf.blit(text_surf, text_rect)

score = 0

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.JOYBUTTONDOWN and event.button == 0:
			player_bullet = PlayerBullet(player.rect.centerx, player.rect.top)
			sprites_all.add(player_bullet)
			sprites_player_bullets.add(player_bullet)
			sound_shoot.play()

	sprites_all.update()

	hits_enemy = pygame.sprite.groupcollide(sprites_enemies, sprites_player_bullets, dokilla = True, dokillb = True)
	for hit in hits_enemy:
		enemies_now -= 1
		if enemies_now == 0:
			enemies_level += 1
			for i in range(enemies_level):
				create_enemy()
		score += 100
		sound_enemy_expl.play()

	hits_player = pygame.sprite.spritecollide(player, sprites_enemy_bullets, dokill = True)
	if hits_player:
		player.health -= 20
		if player.health <= 0:
			running = False

	screen.blit(background, background.get_rect())
	sprites_all.draw(screen)
	draw_health_bar(screen, 5, 5, player.health)
	draw_text(screen, str(score), 15, WIDTH - 15, 5)
	pygame.display.flip()

	clock.tick(FPS)

pygame.time.wait(4000)
pygame.quit()