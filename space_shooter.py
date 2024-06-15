# Space Shooter by Lorand
# based on tutorial from kidscancode.org
# Art from Kenney.nl

import pygame
import random
import math

WIDTH = 480
HEIGHT = 600
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

background = pygame.image.load("assets/starfield.png").convert()
explosion_anim = []
for i in range(9):
	img = pygame.image.load(f"assets/regularExplosion0{i}.png").convert_alpha()
	img = pygame.transform.scale(img, (50, 50))
	explosion_anim.append(img)

with open("high_score.txt", "r") as f:
	high_score = int(f.read())

clock = pygame.time.Clock()

pygame.mixer.init()
sound_shoot = pygame.mixer.Sound("assets/pew.wav")
sound_expl = pygame.mixer.Sound("assets/expl.wav")

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
		self.vx = 0
		self.vy = 0
		self.health = 100
		self.last_heal_time = pygame.time.get_ticks()
		self.heal_delay = 300
		self.is_alive = True

	def heal(self):
		now = pygame.time.get_ticks()
		if now - self.last_heal_time > self.heal_delay:
			self.last_heal_time = now
			self.health += 1
			if self.health > 100:
				self.health = 100

	def move(self):
		self.vx = joystick.get_axis(0) * 8
		self.vy = joystick.get_axis(1) * 5
		self.rect.x += self.vx
		self.rect.y += self.vy
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
		self.vx = player.vx * 0.4
		self.vy = -15 + player.vy * 0.4
		self.image = pygame.image.load("assets/laserBlue.png").convert_alpha()
		self.image = pygame.transform.scale(self.image, (7, 25))
		angle = math.atan(self.vx / self.vy)*90 / (math.pi / 2)
		self.image = pygame.transform.rotate(self.image, angle)
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.bottom = y

	def update(self):
		self.rect.x += self.vx
		self.rect.y += self.vy
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
			enemy_bullet = EnemyBullet(self.rect.centerx, self.rect.bottom, self.vx, self.vy)
			sprites_all.add(enemy_bullet)
			sprites_enemy_bullets.add(enemy_bullet)

	def update(self):
		self.move()
		self.shoot()

class EnemyBullet(pygame.sprite.Sprite):
	def __init__(self, x, y, vx, vy):
		pygame.sprite.Sprite.__init__(self)
		self.vx = vx*0.4
		self.vy = 12 + vy*0.4
		self.image = pygame.image.load("assets/laserRed.png").convert_alpha()
		self.image = pygame.transform.scale(self.image, (7, 25))
		self.image = pygame.transform.flip(self.image, False, True)
		angle = math.atan(self.vx / self.vy)*90 / (math.pi / 2)
		self.image = pygame.transform.rotate(self.image, angle)
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.top = y

	def update(self):
		self.rect.x += self.vx
		self.rect.y += self.vy
		if self.rect.top > HEIGHT:
			self.kill()

class Explosion(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = explosion_anim[0]
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.frame = 0
		self.last_update_time = pygame.time.get_ticks()
		self.frame_rate_millis = 50


	def update(self):
		now = pygame.time.get_ticks()
		if now - self.last_update_time > self.frame_rate_millis:
			self.last_update_time = now
			self.frame += 1
			if self.frame < len(explosion_anim):
				old_center = self.rect.center
				self.image = explosion_anim[self.frame]
				self.rect = self.image.get_rect()
				self.rect.center = old_center
			else:
				self.kill()

def create_enemy():
	global enemies_now
	enemy = Enemy()
	enemies_now += 1
	sprites_all.add(enemy)
	sprites_enemies.add(enemy)

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

def draw_text(surf, text, size, x, y, align):
	font_name = pygame.font.match_font("Comic Sans MS")
	font = pygame.font.Font(font_name, size)
	text_surf = font.render(text, True, "white")
	text_rect = text_surf.get_rect()
	if align == "center":
		text_rect.center = (x, y)
	elif align == "topright":
		text_rect.topright = (x, y)
	else:
		text_rect.topleft = (x, y)
	surf.blit(text_surf, text_rect)

score = 0
main_menu = True
running = True

while running:
	if main_menu:
		screen.blit(background, (0, 0))
		draw_text(screen, "Space Shooter", 50, WIDTH / 2, HEIGHT * 0.2, "center")
		draw_text(screen, f"Last score: {score}", 20, WIDTH / 2, HEIGHT * 0.35, "center")
		draw_text(screen, f"High score: {high_score}", 20, WIDTH / 2, HEIGHT * 0.4, "center")
		draw_text(screen, "Controls (Xbox):", 20, WIDTH / 2, HEIGHT * 0.53, "center")
		draw_text(screen, "B to start game", 20, WIDTH / 2, HEIGHT * 0.6, "center")
		draw_text(screen, "X to exit game", 20, WIDTH / 2, HEIGHT * 0.65, "center")
		draw_text(screen, "A to shoot", 20, WIDTH / 2, HEIGHT * 0.72, "center")
		draw_text(screen, "LS to move the ship", 20, WIDTH / 2, HEIGHT * 0.77, "center")
		pygame.display.flip()
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT or (event.type == pygame.JOYBUTTONDOWN and event.button == 2):
				running = False
			if event.type == pygame.JOYBUTTONDOWN and event.button == 1:
				main_menu = False
				
				sprites_all = pygame.sprite.Group()
				sprites_enemies = pygame.sprite.Group()
				sprites_player_bullets = pygame.sprite.Group()
				sprites_enemy_bullets = pygame.sprite.Group()
				player = Player()
				sprites_all.add(player)

				enemies_now = 0
				enemies_level = 2
				for i in range(enemies_level):
					create_enemy()
				
				score = 0
				scroll_speed = 1
				bg_y1 = 0
				bg_y2 = -HEIGHT

		clock.tick(FPS)

	else:
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
			sound_expl.play()
			enemy_explosion = Explosion(hit.rect.centerx, hit.rect.centery)
			sprites_all.add(enemy_explosion)
			score += 100
			if enemies_now == 0:
				enemies_level += 1
				for i in range(enemies_level):
					create_enemy()
				player.health = 100
				
		hits_player = pygame.sprite.spritecollide(player, sprites_enemy_bullets, dokill = True)
		if hits_player:
			player.health -= 20
			if player.health <= 0:
				sound_expl.play()
				player_explosion = Explosion(player.rect.centerx, player.rect.centery)
				sprites_all.add(player_explosion)
				player.is_alive = False
				player.death_time = pygame.time.get_ticks()
				player.kill()
				player.rect.center = (-1000, -1000)      # hack
				
		if not player.is_alive and not player_explosion.alive():
			now = pygame.time.get_ticks()
			if now - player.death_time > 2000:
				# running = False
				main_menu = True
				if score > high_score:
					high_score = score
					with open("high_score.txt", "w") as f:
						f.write(str(high_score))

		if player.vy > 3:
			scroll_speed = 1
		elif player.vy < -3:
			scroll_speed = 3
		else:
			scroll_speed = 2
		
		bg_y1 += scroll_speed
		bg_y2 += scroll_speed
		if bg_y1 > HEIGHT:
			bg_y1 = -HEIGHT
		if bg_y2 > HEIGHT:
			bg_y2 = -HEIGHT

		screen.blit(background, (0,bg_y1))
		screen.blit(background, (0,bg_y2))
		sprites_all.draw(screen)
		draw_health_bar(screen, 8, 8, player.health)
		draw_text(screen, str(score), 15, WIDTH - 12, 6, "topright")
		pygame.display.flip()

		clock.tick(FPS)

pygame.quit()