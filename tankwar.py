import pygame
import sys,time,random,xlrd
from pygame.locals import *
from ball_tracking import *
from multiprocessing import *


screen_height = 800
screen_length = 780
length1 = 100
length2 = 580
height = 800
screen = pygame.display.set_mode((screen_length, screen_height))
clock = pygame.time.Clock()

# 定义玩家坦克，电脑坦克（若干强度），小树林嘿嘿嘿，
pygame.init()
pygame.font.init()


white = (255, 255, 255)
black = (0, 0, 0)
gold = (255, 215, 0)
yellow = (255, 255, 0)
red = (255, 0, 0)
light_red = (250, 128, 114)


def button(msg, x, y, width, height, i_c, a_c, is_multi = True, action = None):
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()

	if x + width > mouse[0] > x and y + height > mouse[1] > y:
		pygame.draw.rect(screen, a_c, (x, y, width, height))
		if click[0] == 1 and action != None:
			if action == "play":
				return is_multi
			elif action == "quit":
				sys.exit(0)
			elif action == '1':
				return 1
			elif action == '2':
				return 2
			elif action == '3':
				return 3
			elif action == 'menu':
				return 4
	else:
		pygame.draw.rect(screen, i_c, (x, y, width, height))


	small_text1 = pygame.font.SysFont('comicsansms', 20)
	text_surf1, text_rect1 = text_objects(msg, small_text1)
	text_rect1.center = (x + width/2, y + height/2)
	screen.blit(text_surf1, text_rect1)



def text_objects(text, font):
	text_Surface = font.render(text, True, black)
	return text_Surface, text_Surface.get_rect()

def message_display(text, center_x, center_y, font_size):
	display_text = pygame.font.SysFont('comicsansms', font_size)
	TextSurf, TextRect = text_objects(text, display_text)
	TextRect.center = (center_x, center_y)
	screen.blit(TextSurf, TextRect)


def start_menu():

	intro = True
	pygame.mixer.music.stop()
	pygame.mixer.music.load('src/track1.mp3')
	pygame.mixer.music.play(-1)
	while intro:
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		screen.fill(white)
		message_display("Battle City", 400, 200, 100)



		value1 = button("Single Player", 320, 350, 150, 50, gold, yellow, False, "play")
		if not value1 == None:
			return value1
		value2 = button("Double Player", 320, 450, 150, 50, gold, yellow, True, 'play')
		if not value2 == None:
			return value2
		button("Exit Game", 320, 550, 150, 50, red, light_red, True, "quit")









		pygame.display.update()
		clock.tick(30)




def level_select():
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		screen.fill(white)
		message_display('Level Select', 400, 200, 100)
		value1 = button("Level 1", 320, 350, 150, 50, gold, yellow, True, '1')
		if not value1 == None:
			return value1
		value2 = button("Level 2", 320, 450, 150, 50, gold, yellow, True, '2')
		if not value2 == None:
			return value2
		value3 = button("Level 3", 320, 550, 150, 50, gold, yellow, True, "3")
		if not value3 == None:
			return value3
		value4 = button('Return to Menu', 0, 0, 150, 50, red, light_red, True, 'menu')
		if not value4 == None:
			return value4
		pygame.display.update()
		clock.tick(30)





def game_end(txt):
	pygame.mixer.stop()
	if txt == 'You Win!':
		pygame.mixer.music.load('src/win.mp3')
	else:
		pygame.mixer.music.load('src/lose.mp3')
	pygame.mixer.music.play()
	while True:
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_SPACE:
					return
		screen.fill(white)
		message_display(txt, 400, 200, 100)
		message_display('Press Space to continue', 400, 300, 50)
		pygame.display.update()
		clock.tick(30)




class TankSprite(pygame.sprite.Sprite):
	
	def __init__(self, image, move_speed, shoot_speed, hp, position, direction):
		pygame.sprite.Sprite.__init__(self)
		self.src_image = pygame.image.load(image)
		self.move_speed = move_speed
		self.posx = position[0]
		self.preposx = self.posx
		self.posy = position[1]
		self.preposy = self.posy
		self.direction = direction
		self.is_moving = False
		self.templist = []
		self.rect = self.src_image.get_rect()
		self.rect.center = (self.posx, self.posy)
		self.bulletgroup = pygame.sprite.RenderPlain(BulletSprite(10, self.posx, self.posy, self.direction, 100))
		self.bulletgroup.empty()
		self.bulletlist = self.bulletgroup.sprites()
		self.damage = 100
		self.hp = 100
		self.length = 14
		self.shoot_speed = shoot_speed
		self.shoot_time = 1/shoot_speed
		self.time1 = time.clock()
		self.time1 = time.clock()
		self.time2 = 0
		self.is_dead = False
		self.explosion_count = 0
		explode1 = pygame.image.load('src/explode1.png')
		explode2 = pygame.image.load('src/explode2.png')
		explode3 = pygame.image.load('src/explode3.png')
		explode4 = pygame.image.load('src/explode4.png')
		explode5 = pygame.image.load('src/explode5.png')
		self.explodelist = [explode1, explode2, explode3, explode4, explode5]
		spawn1 = pygame.image.load('src/spawn1.png')
		spawn2 = pygame.image.load('src/spawn2.png')
		spawn3 = pygame.image.load('src/spawn3.png')
		spawn4 = pygame.image.load('src/spawn4.png')
		spawn5 = pygame.image.load('src/spawn5.png')
		spawn6 = pygame.image.load('src/spawn6.png')
		spawn7 = pygame.image.load('src/spawn7.png')
		self.spawnlist = [spawn1, spawn2, spawn3, spawn4, spawn5, spawn6, spawn7, spawn1, spawn2, spawn3, spawn4, spawn5, spawn6, spawn7]
		self.image =spawn1
		self.is_spawning = True
		self.dead = False
		self.spawn_count = 0
		self.can_collide = False
		self.is_invinsible = False
		self.invinsibletime1 = time.clock()
		self.invinsibletime2 = 0


	def spawn(self):
		if self.spawn_count >= len(self.spawnlist):
			self.is_spawning = False
			self.is_invinsible = True
			self.invinsibletime1 = time.clock()
			return
		self.is_spawning = True
		self.time2 = time.clock()
		if self.time2 - self.time1 > 0.1:
			self.image = self.spawnlist[self.spawn_count]
			self.rect = self.image.get_rect()
			self.rect.center = (self.posx, self.posy)
			self.spawn_count += 1
			self.time1 = time.clock()



	def respawn(self, position):
		self.is_dead = False
		self.is_spawning = True
		self.spawn_count = 0
		self.explosion_count = 0
		self.dead = False
		self.posx = position[0]
		self.posy = position[1]
		self.preposx = self.posx
		self.preposy = self.posy
		self.image = self.spawnlist[0]


	def invinsible(self):
		self.invinsibletime2 = time.clock()
		if self.invinsibletime2 - self.invinsibletime1 >= 3:
			self.hp = 100
			self.is_invinsible = False


	def update(self):
		if self.is_spawning:
			self.hp = 99999
			self.spawn()
			return
		if self.is_dead:
			self.bulletgroup.empty()
			self.dead_explosion()
			return
		if self.is_invinsible:
			self.hp = 99999
			self.invinsible()
		if self.is_moving:
			self.preposy = self.posy
			self.preposx = self.posx
			if self.direction == 1:
			    self.posy -= self.move_speed
			elif self.direction == 2:
			    self.posx += self.move_speed
			elif self.direction == 3:
			    self.posy += self.move_speed
			elif self.direction == 4:
			    self.posx -= self.move_speed
		self.bulletgroup.update()
		self.bulletlist = self.bulletgroup.sprites()
		self.image = pygame.transform.rotate(self.src_image, -(self.direction -1) * 90)
		self.rect = self.src_image.get_rect()
		self.rect.center = (self.posx, self.posy)
		self.can_collide = not self.is_dead


	def reset_position(self):
		self.posx = self.preposx
		self.posy = self.preposy


	def shoot(self):
		self.time2 = time.clock()
		if self.time2 - self.time1 < self.shoot_time:
			return
		else:
			self.time1 = time.clock()
			x = self.posx
			y = self.posy
			if self.direction == 1:
				y -= self.length
			elif self.direction == 2:
				x += self.length
			elif self.direction == 3:
				y += self.length
			elif self.direction == 4:
				x -= self.length
			self.bulletgroup.add(BulletSprite(8, x, y, self.direction, 100))


	def draw_bullet(self, screen):
		self.bulletgroup.draw(screen)


	def hit_tank(self, other_tank):
		hitlist = pygame.sprite.spritecollide(other_tank, self.bulletgroup, False)
		for bullet in hitlist:
			bullet.is_dead = True
		if not len(hitlist) == 0:
			other_tank.get_hit(self.damage)


	def get_hit(self, damage):
		self.hp -= damage
		if self.hp <= 0 and not self.is_dead:
			self.is_dead = True
			self.time1 = time.clock()
			self.dead_explosion()



	def dead_explosion(self):
			if self.explosion_count >= len(self.explodelist):
				self.kill()
				self.dead = True
			self.time2 = time.clock()
			if self.time2 - self.time1 > 0.15:
				self.image = self.explodelist[self.explosion_count]
				self.rect = self.image.get_rect()
				self.rect.center = (self.posx, self.posy)
				self.explosion_count += 1
				self.time1 = time.clock()







class PlayerTank(TankSprite):

	def __init__(self, image, move_speed, shoot_speed, hp, position, direction, keylist):
		TankSprite.__init__(self, image, move_speed, shoot_speed, hp, position, direction)
		self.keylist = keylist
		self.type = 'player'








class AITank(TankSprite):

	def __init__(self, image, move_speed, shoot_speed, hp, position, direction):
		TankSprite.__init__(self, image, move_speed, shoot_speed, hp, position, direction)
		self.move_time = random.uniform(0, 2)
		self.movetime1 = time.clock()
		self.movetime1 = time.clock()
		self.movetime2 = 0
		self.shoottime1 = time.clock()
		self.shoottime2 = 0
		self.shoot_time_space = random.uniform(0, 1)
		self.type = 'computer'

	def update(self):
		self.movetime2 = time.clock()
		if self.movetime2 - self.movetime1 > self.move_time:
			rand = random.randint(1, 5)
			while rand == self.direction:
				rand = random.randint(1, 5)
			if rand == 5:
				rand = 3
			self.direction = rand
			self.move_time = random.uniform(0, 3)
			self.movetime1 = time.clock()
		if self.is_spawning:
			self.hp = 99999
			self.spawn()
			return
		if self.is_invinsible:
			self.hp = 99999
			self.invinsible()
		if self.is_dead:
			self.bulletgroup.empty()
			self.dead_explosion()
			return
		self.preposy = self.posy
		self.preposx = self.posx
		if self.direction == 1:
		    self.posy -= self.move_speed
		elif self.direction == 2:
		    self.posx += self.move_speed
		elif self.direction == 3:
		    self.posy += self.move_speed
		elif self.direction == 4:
		    self.posx -= self.move_speed
		self.bulletgroup.update()
		self.bulletlist = self.bulletgroup.sprites()
		self.image = pygame.transform.rotate(self.src_image, -(self.direction -1) * 90)
		self.rect = self.image.get_rect()
		self.rect.center = (self.posx, self.posy)
		self.can_collide = not (self.is_dead or self.is_spawning)


	def aishoot(self, tank_list, home_list):
		for tank in tank_list:
			if self.direction == 1:
				if self.posx >= tank.posx - self.length and self.posx <= tank.posx + self.length and self.posy > tank.posy:
					self.shoot()
			elif self.direction == 2:
				if self.posy >= tank.posy - self.length and self.posy <= tank.posy + self.length and self.posx < tank.posx:
					self.shoot()
			elif self.direction == 3:
				if self.posx >= tank.posx - self.length and self.posx <= tank.posx + self.length and self.posy < tank.posy:
					self.shoot()
			elif self.direction == 4:
				if self.posy >= tank.posy - self.length and self.posy <= tank.posy + self.length and self.posx > tank.posx:
					self.shoot()
		for home in home_list:
			if self.direction == 1:
				if self.posx >= home.posx - self.length and self.posx <= home.posx + self.length and self.posy > home.posy:
					self.shoot()
			elif self.direction == 2:
				if self.posy >= home.posy - self.length and self.posy <= home.posy + self.length and self.posx < home.posx:
					self.shoot()
			elif self.direction == 3:
				if self.posx >= home.posx - self.length and self.posx <= home.posx + self.length and self.posy < home.posy:
					self.shoot()
			elif self.direction == 4:
				if self.posy >= home.posy - self.length and self.posy <= home.posy + self.length and self.posx > home.posx:
					self.shoot()
		self.shoottime2 = time.clock()
		if self.shoottime2 - self.shoottime1 > self.shoot_time_space:
			self.shoottime1 = time.clock()
			self.shoot_time_space = random.uniform(0, 1)
			self.shoot()




	def reset_position(self):
		self.posx = self.preposx
		self.posy = self.preposy
		rand = random.randint(1, 4)
		while rand == self.direction:
			rand = random.randint(1, 4)
		self.direction = rand
		self.move_time = random.uniform(0, 2)
		self.movetime1 = time.clock()




class BulletSprite(pygame.sprite.Sprite):

	def __init__(self, speed, posx, posy, direction, damage):
		pygame.sprite.Sprite.__init__(self)
		self.src_image = pygame.image.load('src/bullet.png')
		self.direction = direction
		self.speed = speed
		self.posx = posx
		self.posy = posy
		self.image = pygame.transform.rotate(self.src_image, -(self.direction -1) * 90)
		self.damage = damage
		self.rect = self.image.get_rect()
		self.rect.center = (self.posx, self.posy)
		self.time1 = time.clock()
		self.time1 = time.clock()
		self.time2 = 0
		explode1 = pygame.image.load('src/explode1.png')
		explode2 = pygame.image.load('src/explode2.png')
		explode3 = pygame.image.load('src/explode3.png')
		explode5 = pygame.image.load('src/explode5.png')
		self.explodelist = [explode1, explode2, explode3, explode5]
		self.explode_count = 0
		self.is_dead = False

	def update(self):
		if self.is_dead:
			self.dead_explosion()
			return
		else:
			if self.direction == 1:
				self.posy -= self.speed
			elif self.direction == 2:
			    self.posx += self.speed
			elif self.direction == 3:
			    self.posy += self.speed
			elif self.direction == 4:
			    self.posx -= self.speed
			self.rect = self.image.get_rect()
			self.rect.center = (self.posx, self.posy)




	def dead_explosion(self):
		if self.explode_count >= len(self.explodelist):
			self.kill()
		self.time2 = time.clock()
		if self.time2 - self.time1 > 0.15:
			self.image = self.explodelist[self.explode_count]
			self.explode_count += 1
			self.time1 = time.clock()




class map_elements(pygame.sprite.Sprite):

	def __init__(self, image, posx, posy):
		pygame.sprite.Sprite.__init__(self)
		self.posx = posx + 16
		self.posy = posy + 8
		self.position = (self.posx, self.posy)
		self.image = pygame.image.load(image)
		self.rect = self.image.get_rect()
		self.rect.center = self.position
		self.is_dead = False


	def dead(self):
		self.kill()





class Hard_Wall(map_elements):

	def __init__(self, posx, posy):
		map_elements.__init__(self, 'src/hard_wall.png', posx, posy)
		self.destroyable = False
		self.penetrable = False





class Wall(map_elements):

	def __init__(self, posx, posy):
		map_elements.__init__(self, 'src/wall.png', posx, posy)
		self.destroyable = True
		self.penetrable = False





class River(map_elements):

	def __init__(self, posx, posy):
		map_elements.__init__(self, 'src/river.png', posx, posy)
		self.destroyable = False
		self.penetrable = True





class Forest(map_elements):

	def __init__(self, posx, posy):
		map_elements.__init__(self, 'src/forest.png', posx - 8, posy)







class Home(map_elements):

	def __init__(self, posx, posy):
		map_elements.__init__(self, 'src/home.png', posx, posy)
		self.posx = posx + 16
		self.posy = posy + 16
		self.destroyable = True
		self.penetrable = False
		self.position = (self.posx, self.posy)
		self.rect = self.image.get_rect()
		self.rect.center = self.position
		self.is_dead = False


	def dead(self):
		self.image = pygame.image.load('src/dead_home.png')
		self.is_dead = True





def move(event, tank):
	keylist = tank.keylist

	cursor_g_x = cursor_loc[0] * screen_width
	cursor_g_y = cursor_loc[1] * screen_height
	cursor_r_x = cursor_loc[2] * screen_width
	cursor_r_y = cursor_loc[3] * screen_height
	
	time.sleep(0.001)

	cursor_g_x_update = cursor_loc[0] * screen_width
	cursor_g_y_update = cursor_loc[1] * screen_height
	cursor_r_x_update = cursor_loc[2] * screen_width
	cursor_r_y_update= cursor_loc[3] * screen_height

	if not hasattr(event, 'key'): 
		return
	is_key = event.key == keylist[0] or event.key == keylist[1] or event.key == keylist[2] or event.key == keylist[3] or event.key == keylist[4] or event.key == keylist[5]
	if is_key:
		if event.type == KEYDOWN:
			if len(tank.templist) == 0:
				tank.templist.append(event)

			detect = False
			for i in tank.templist:
				detect = detect or not(i.key == event.key)
			if detect:
				tank.templist.append(event)
			if event.key == keylist[4]:
				sys.exit(0)
			elif event.key == keylist[5]:
				tank.shoot()
			else:
				if (cursor_g_x_update-cursor_g_x)>=15: 
					tank.direction = 2
				elif (cursor_g_y_update-cursor_g_y)>=15:
					tank.direction = 4
				elif (cursor_g_x_update-cursor_g_x)<=-15:
					tank.direction = 1
				elif (cursor_g_y_update-cursor_g_y)<=-15:
					tank.direction = 3
				tank.is_moving = True

		elif event.type == KEYUP:
			for i in range(len(tank.templist)):
				if tank.templist[i].key == event.key:
					del tank.templist[i]
					break

			if len(tank.templist) == 0:
				tank.is_moving = False


def eliminate_repeat(lst):
	i = 0
	k = 1
	while i < len(lst):
		if k >= len(lst):
			i += 1
			k = i + 1
			continue
		if lst[i] == lst[k]:
			del lst[k]
		else:
			k += 1


def check_tank_collide(tanklist):
	collidelist = []
	for i in range(len(tanklist)):
		if tanklist[i].posx - tanklist[i].length <= length1 or tanklist[i].posx + tanklist[i].length >= length2 or tanklist[i].posy - tanklist[i].length <= 0 or tanklist[i].posy + tanklist[i].length >= height:
			collidelist.append(tanklist[i])
		for k in range(i+1, len(tanklist)):
			if pygame.sprite.collide_rect(tanklist[i], tanklist[k]) and tanklist[i].can_collide and tanklist[k].can_collide:
				collidelist.append(tanklist[i])
				collidelist.append(tanklist[k])
	eliminate_repeat(collidelist)
	return collidelist


def tank_collide(lst, lst2):
	tanklist = lst.sprites()
	tanklist.extend(lst2.sprites())
	tank_collide_list = check_tank_collide(tanklist)
	if not len(tank_collide_list) == 0:
		for tank in tank_collide_list:
			tank.reset_position()


def tank_move(tank_group):
	tank_list = tank_group.sprites()
	for event in pygame.event.get():
		if not hasattr(event, 'key'): 
			return
		if event.key == K_ESCAPE:
			sys.exit(0)
		for tank in tank_list:
			move(event, tank)


def draw_bullet(tank_list, screen):
	for tank in tank_list:
		tank.draw_bullet(screen)


def check_hit(tank_list):
	for i in range(len(tank_list)):
		for bullet in tank_list[i].bulletlist:
			if bullet.posx > length2 or bullet.posx < length1 or bullet.posy > height or bullet.posy < 0:
				bullet.is_dead = True
		for k in range(len(tank_list)):
			if i == k or tank_list[i].type == tank_list[k].type:
				continue
			tank_list[i].hit_tank(tank_list[k])


def aishoot(player_tank_group, tankgroup, homegroup):
	tanklist = tankgroup.sprites()
	for tank in tanklist:
		tank.aishoot(player_tank_group, homegroup)


def check_wall_collide(tank, wall):
	return pygame.sprite.collide_rect(tank, wall) and tank.can_collide


def check_bullet_wall_collide(tank, wall):
	lst = pygame.sprite.spritecollide(wall, tank.bulletgroup, False)
	if not wall.penetrable:
		for bullet in lst:
			bullet.is_dead = True
	if not len(lst) == 0:
		if not wall.penetrable and wall.destroyable:
			wall.dead()


def wall_collide(tank_list, wall_list):
	for tank in tank_list:
		for wall in wall_list:
			if check_wall_collide(tank, wall):
				tank.reset_position()
			check_bullet_wall_collide(tank, wall)







# def text_objects(text, font):
#     # true = anti aliasing
#     textSurface = font.render(text, True, WHITE)
#     # return the text surface and it's rect for positioning
#     return textSurface, textSurface.get_rect()

# def button(msg,x,y,w,h,ic,ac,action=None):
# 	mouse = pygame.mouse.get_pos()
# 	click = pygame.mouse.get_pressed()

# 	if x+w > mouse[0] > x and y+h > mouse[1] > y:
# 		pygame.draw.rect(screen, ac,(x,y,w,h))
# 		if click[0] == 1 and action != None:
# 			action()         
# 	else:
# 		pygame.draw.rect(screen, ic,(x,y,w,h))
# 	smallText = pygame.font.SysFont("comicsansms",20)
# 	textSurf, textRect = text_objects(msg, smallText)
# 	textRect.center = ( (x+(w/2)), (y+(h/2)) )
# 	screen.blit(textSurf, textRect)

def quitgame():
	pygame.quit()
	quit()

def message_center(rect_group, text_group):
	addRect(rect_group, 0,0,100,800)
	addText(text_group, "player_1",10,150,20)
	player_1_ip = 'X' + str(5)


	addText(text_group, player_1_ip,10,180,20)
	addText(text_group, "player_2",10,280,20)
	player_2_ip = 'X' + str(5)
	addText(text_group, player_2_ip,10,310,20)
	addRect(rect_group, 580,0,200,800)
	level = "Level: " + str(1)
	addText(text_group, level,600,100, 25)
	addText(text_group, "ENEMY LEFT:",600,200, 25)
	enemy_number = str(10)
	addText(text_group, enemy_number,650,250, 50)



def addRect(group, left_x, top_x, width, height):
	s = ColorRect(left_x, top_x, width, height)
	group.append(s)


def addText(group, text, x, y, font_size):
	text = Text('comicsansms', font_size, text, x, y, (0,0,0))
	group.append(text)




class Text(object):

	def __init__(self, fontname, fontsize, text, posx, posy, color):
		self.font = pygame.font.SysFont('comicsansms', fontsize)
		self.surface = self.font.render(text, True, color, (posx, posy))
		self.posx = posx
		self.posy = posy
		self.color = color

	def update(self, text):
		self.text = text
		self.surface = self.font.render(text, True, self.color, (self.posx, self.posy))


		





class ColorRect(pygame.Surface):

	def __init__(self, posx, posy, width, height):
		pygame.Surface.__init__(self, (width, height))
		self.posx = posx
		self.posy = posy
		self.fill((240, 240, 240))






class Map(object):

	def __init__(self, map, tank_num, is_multi):
		self.map = map
		self.tank_num = tank_num
		self.is_multi = is_multi
		wall1 = Wall(300, 100)
		wall4 = Forest(200, 200)
		home1 = Home(100, 100)
		self.collide_wall_group = pygame.sprite.RenderPlain(wall1)
		self.collide_wall_group.empty()
		self.forest_group = pygame.sprite.RenderPlain(wall4)
		self.forest_group.empty()
		self.home_group = pygame.sprite.RenderPlain(home1)
		self.home_group.empty()
		self.spawntime1 = time.clock()
		self.spawntime1 = time.clock()
		self.spawntime2 = 0
		self.player_life = 3
		self.keylist1 = [K_RIGHT, K_LEFT, K_UP, K_DOWN, K_ESCAPE, K_KP_ENTER]
		self.keylist2 = [K_d, K_a, K_w, K_s, K_ESCAPE, K_SPACE]

		self.player2_life = 0
		self.player_tank_group = pygame.sprite.RenderPlain(PlayerTank('src/player_tank.png', 2, 4, 100, (378, 684), 1, self.keylist1))
		self.player_tank_group.empty()
		self.hostile_tank = AITank('src/enemy_tank.png', 3, 2, 200, (130, 30), 1)
		self.ai_tank_group = pygame.sprite.RenderPlain(self.hostile_tank)
		self.ai_tank_group.empty()
		self.mapdata = []
		self.aispawnspot = []
		self.playerspawnspot = []

		


	def start(self):
		self.read_map()
		self.draw_map()
		self.player_tank = PlayerTank('src/player_tank.png', 2, 4, 100, self.playerspawnspot[0], 1, self.keylist1)
		self.player_tank_group.add(self.player_tank)
		if self.is_multi:
			self.player_tank2 = PlayerTank('src/player_tank2.png', 2, 4, 100, self.playerspawnspot[1], 1, self.keylist2)
			self.player_tank_group.add(self.player_tank2)
			self.player2_life = 3
		aispawn = self.aispawnspot[random.randint(0, len(self.playerspawnspot) - 1)]
		self.ai_tank_group.add(AITank('src/enemy_tank.png', 2, 2, 200, aispawn, 1))
		self.tank_num -= 1



	def check_position(self, position):
		tanklist = self.player_tank_group.sprites()
		tanklist.extend(self.ai_tank_group.sprites())
		for tank in tanklist:
			if position[0] > tank.posx - tank.length and position[0] < tank.posx + tank.length and position[1] > tank.posy - tank.length and position[1] < tank.posy + tank.length:
				return False
		return True



	def spawn_ai_tank(self):
		self.spawntime2 = time.clock()
		if len(self.ai_tank_group.sprites()) >= 2 or self.tank_num <= 0:
			return
		position = random.randint(0, len(self.aispawnspot) - 1)
		while not self.check_position(self.aispawnspot[position]):
			position = random.randint(0, len(self.aispawnspot) - 1)
		if self.spawntime2 - self.spawntime1 > 1:
			self.ai_tank_group.add(AITank('src/enemy_tank.png', 2, 2, 200, self.aispawnspot[position], 1))
			self.spawntime1 = time.clock()
			self.tank_num -= 1
		

	def spawn_player_tank(self):
		if len(self.player_tank_group.sprites()) >= 2:
			return
		position = random.randint(0, len(self.playerspawnspot) - 1)
		while not self.check_position(self.playerspawnspot[position]):
			position = random.randint(0, len(self.playerspawnspot) - 1)
		if self.player_tank.dead and not self.player_life <= 0:
			self.player_life -= 1
			self.player_tank.respawn(self.playerspawnspot[position])
			self.player_tank_group.add(self.player_tank)


		elif self.is_multi:
			if self.player_tank2.is_dead and not self.player2_life <= 0:
				self.player_tank2.respawn(self.playerspawnspot[position])
				self.player_tank_group.add(self.player_tank2)
				self.player2_life -= 1


	def update(self):
		self.spawn_player_tank()
		self.spawn_ai_tank()




	def draw_hard_wall(self, hard_wall_x, hard_wall_y):
		hard_wall = Hard_Wall(hard_wall_x, hard_wall_y)
		self.collide_wall_group.add(hard_wall)


	def draw_forest(self, forest_x, forest_y):
		forest_1 = Forest(forest_x, forest_y)
		forest_2 = Forest(forest_x+15, forest_y)
		self.forest_group.add(forest_1)
		self.forest_group.add(forest_2)


	def draw_home(self, home_x, home_y):
		home = Home(home_x, home_y)
		self.home_group.add(home)


	def draw_river(self, river_x, river_y):
		river = River(river_x, river_y)
		self.collide_wall_group.add(river)


	def draw_wall(self, wall_x, wall_y):
		wall_1 = Wall(wall_x, wall_y)
		#wall_2 = Wall(wall_x, wall_y+16)
		self.collide_wall_group.add(wall_1)
		#self.collide_wall_group.add(wall_2)


	def draw_small_wall(self, small_wall_x, small_wall_y):
		small_wall = Wall(small_wall_x, small_wall_y)
		self.collide_wall_group.add(small_wall)



	def drawing_map_2(self):
		#E
		for i in range(0,5):
			self.draw_wall(146+32*i, 66)
		for i in range(0,7):
			self.draw_wall(146, 66+32*i)
		for i in range(0,5):
			self.draw_wall(146+32*i, 162)
		for i in range(0,5):
			self.draw_wall(146+32*i, 258)

		#S
		for i in range(0,4):
			self.draw_wall(358+32*i,66)
		for i in range(0,2):
			self.draw_wall(358,98+32*i)
		for i in range(0,4):
			self.draw_wall(358+32*i,162)
		for i in range(0,2):
			self.draw_wall(454,194+32*i)
		for i in range(0,4):
			self.draw_wall(358+32*i,258)

		#hard_wall
		self.draw_hard_wall(116,324)
		self.draw_hard_wall(484,324)

		#river
		for i in range(0,5):
			self.draw_river(240+32*i,316)
			self.draw_river(240+32*i,332)

		#forest
		for i in range(0,4):
			for j in range(0,3):
				self.draw_forest(148+16*i,308+16*j)
		for i in range(0,4):
			for j in range(0,3):
				self.draw_forest(452-16*i,308+16*j)

		#A
		for i in range(0,6):
			self.draw_wall(146,566-32*i)
		for i in range(0,5):
			self.draw_wall(146+32*i,374)
		for i in range(0,6):
			self.draw_wall(273,566-32*i)
		for i in range(0,3):
			self.draw_wall(177+32*i,502)

		#P
		for i in range(0,6):
			self.draw_wall(358,566-32*i)
		for i in range(0,4):
			self.draw_wall(358+32*i,374)
		for i in range(0,4):
			self.draw_wall(358+32*i,470)
		for i in range(0,3):
			self.draw_wall(454,374+32*i)
		
		#Home
		self.draw_home(300,668)
		for i in range(0,2):
			self.draw_wall(268,684-32*i)
		self.draw_small_wall(300,652)
		for i in range(0,2):
			self.draw_wall(332,684-32*i)




	def drawing_map_1(self):

		# top 1
		for i in range(1, 15, 2):
			self.draw_wall(100 + 30 + 16, 30 + 16 * i)
		for i in range(1, 15, 2):
			self.draw_wall(100 + 30 + 16, 380 + 16 * i)
		#wall

		#left
		self.draw_hard_wall(100 + 13, 325)

		#top 2
		for i in range(1, 15, 2):
			self.draw_wall(100 + 30 + 16 + 70, 30 + 16 * i)
		for i in range(1, 15, 2):
			self.draw_wall(100 + 30 + 16 + 70, 380 + 16 * i)

		#middle 1
		self.draw_wall(100 + 16 + 16 + 30 + 13, 320)
		self.draw_wall(100 + 16 + 16 + 30 + 16 + 29, 320)

		#top 3
		for i in range(1, 15, 2):
			self.draw_wall(100 + 30 + 16 + 62 + 62, 30 + 16 * i)
		for i in range(1, 15, 2):
			self.draw_wall(100 + 30 + 16 + 62 + 62, 348 + 16 * i)

		# middle 2
		self.draw_wall(100 + 30 + 16 + 62 + 62, 30 + 16 * 15 + 30)

		#top 4
		for i in range(1, 15, 2):
			self.draw_wall(100 + 30 + 16 + 62 + 62 + 62, 30 + 16 * i)
		for i in range(1, 15, 2):
			self.draw_wall(100 + 30 + 16 + 62 + 62 + 62, 348 + 16 * i)

		# middle 3
		self.draw_wall(100 + 30 + 16 + 62 + 62 + 62, 30 + 16 * 15 + 30)

		# middle bottom 1
		self.draw_wall(100 + 30 + 16 + 62 + 62 + 31, 30 + 16 * 15 + 30 + 120)

		#top 5
		for i in range(1, 17, 2):
			self.draw_wall(100 + 30 + 16 + 62 + 62 + 62 + 62, 30 + 16 * i)
		for i in range(1, 17, 2):
			self.draw_wall(100 + 30 + 16 + 62 + 62 + 62 + 62, 380 + 16 * i)

		#top 6
		for i in range(1, 17, 2):
			self.draw_wall(100 + 30 + 16 + 62 + 62 + 62 + 62 + 62, 30 + 16 * i)
		for i in range(1, 17, 2):
			self.draw_wall(100 + 30 + 16 + 62 + 62 + 62 + 62 + 62, 380 + 16 * i)

		#middle 4
		self.draw_wall(100 + 16 + 16 + 30 + 13 + 62 * 4 - 28, 335)
		self.draw_wall(100 + 16 + 16 + 30 + 16 + 29 + 62 * 4 - 28, 335)

		#right
		self.draw_hard_wall(490, 340)

		#home
		self.draw_home(302, 650)
		self.draw_wall(269, 650)
		self.draw_wall(269, 618)
		self.draw_wall(301, 618)
		self.draw_wall(333, 618)
		self.draw_wall(333, 650)







	def read_map(self):
		data = xlrd.open_workbook('src/map.xls')
		table = data.sheets()[self.map - 1]
		rownum = table.nrows
		for i in range(rownum):
			self.mapdata.append(table.row_values(i))


	def draw_map(self):
		for row in range(len(self.mapdata)):
			for col in range(len(self.mapdata[0])):
				if self.mapdata[row][col] == 1:
					self.draw_wall(100 + 32 * col, 16 * row)
				elif self.mapdata[row][col] == 2:
					self.draw_hard_wall(100 + 32 * col, 16 * row)
				elif self.mapdata[row][col] == 3:
					self.draw_river(100 + 32 * col, 16 * row)
				elif self.mapdata[row][col] == 4:
					self.draw_forest(100 + 32 * col, 16 * row)
				elif self.mapdata[row][col] == 5:
					self.aispawnspot.append((100 + 32 * col + 16, 16 * row + 16))
				elif self.mapdata[row][col] == 6:
					self.playerspawnspot.append((100 + 32 * col + 16, 16 * row + 16))
				elif self.mapdata[row][col] == 9:
					self.draw_home(100 + 32 * col, 16 * row)

				else:
					continue







# Create a player tank
def game_process(map):
	pygame.mixer.music.stop()
	pygame.mixer.music.load('src/track3.mp3')
	pygame.mixer.music.play(-1)
	map.start()
	rect_group = []
	text_group = []
	message_center(rect_group, text_group)
	while True:
		if map.tank_num == 0 and len(map.ai_tank_group.sprites()) == 0:
			return('You Win!')
		elif map.home_group.sprites()[0].is_dead:
			return('You Lose!')
		elif map.player_life == 0 and map.player2_life == 0 and len(map.player_tank_group.sprites()) == 0:
			return('You Lose!')
		tank_list = map.player_tank_group.sprites() + map.ai_tank_group.sprites()
		wall_list = map.collide_wall_group.sprites() + map.home_group.sprites()
		clock.tick(60)
		tank_move(map.player_tank_group)

		# RENDERING
		screen.fill((0,0,0))
		map.update()
		map.player_tank_group.update()
		map.ai_tank_group.update()
		tank_collide(map.player_tank_group, map.ai_tank_group)
		wall_collide(tank_list, wall_list)
		aishoot(map.player_tank_group, map.ai_tank_group, map.home_group)
		check_hit(tank_list)

		text_group[1].update('Life x ' + str(map.player_life))
		if map.is_multi:
			text_group[3].update('Life x ' + str(map.player2_life))
		else:
			text_group[3].update('')
		text_group[4].update('Level: ' + str(map.map))
		text_group[6].update(str(map.tank_num))

		map.collide_wall_group.draw(screen)
		map.player_tank_group.draw(screen)
		map.ai_tank_group.draw(screen)
		map.home_group.draw(screen)
		map.forest_group.draw(screen)
		draw_bullet(tank_list, screen)
		for rect in rect_group:
			screen.blit(rect, (rect.posx, rect.posy))
		for text in text_group:
			screen.blit(text.surface, (text.posx, text.posy))
		pygame.display.flip()


def main():


	memory = 0
	write_end, read_end = Pipe()
	green_proc = Process(target=main_a, args=(write_end,))
	green_proc.start()
	# detector_proc = Process(target = detector, args = (write_end,))
	# detector_proc.start()
	cursor_loc = (0,0,0,0)


	while True:
		is_multi = start_menu()
		time.sleep(0.3)
		level = level_select()
		if level == 4:
			continue
		map = Map(level, 20, is_multi)
		result = game_process(map)
		time.sleep(0.5)
		game_end(result)


main()