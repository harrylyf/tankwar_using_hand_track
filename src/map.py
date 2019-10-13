import pygame, random
from pygame.locals import *
from sys import exit


screen = pygame.display.set_mode((700,700))

class map_elements(pygame.sprite.Sprite):

	def __init__(self, image, posx, posy):
		pygame.sprite.Sprite.__init__(self)
		self.posx = posx
		self.posy = posy
		self.position = (posx, posy)
		self.image = pygame.image.load(image)
		self.rect = self.image.get_rect()
		self.rect.center = self.position

	def draw(self):
		screen.blit(self.image,self.position)


def draw_hard_wall(hard_wall_x, hard_wall_y):
	hard_wall = map_elements('hard_wall.png', hard_wall_x, hard_wall_y)
	hard_wall.draw()

def draw_forest(forest_x, forest_y):
	forest_1 = map_elements('forest.png', forest_x, forest_y)
	forest_2 = map_elements('forest.png', forest_x+15, forest_y)
	forest_1.draw()
	forest_2.draw()

def draw_home(home_x, home_y):
	home = map_elements('home.png', home_x, home_y)
	home.draw()

def draw_river(river_x, river_y):
	river = map_elements('river.png', river_x, river_y)
	river.draw()

def draw_wall(wall_x, wall_y):
	wall_1 = map_elements('wall.png', wall_x, wall_y)
	wall_2 = map_elements('wall.png', wall_x, wall_y+16)
	wall_1.draw()
	wall_2.draw()

def draw_small_wall(small_wall_x, small_wall_y):
	small_wall = map_elements('wall.png', small_wall_x, small_wall_y)
	small_wall.draw()

def drawing_map_2():
	#E
	for i in range(0,5):
		draw_wall(146+32*i, 66)
	for i in range(0,7):
		draw_wall(146, 66+32*i)
	for i in range(0,5):
		draw_wall(146+32*i, 162)
	for i in range(0,5):
		draw_wall(146+32*i, 258)

	#S
	for i in range(0,4):
		draw_wall(358+32*i,66)
	for i in range(0,2):
		draw_wall(358,98+32*i)
	for i in range(0,4):
		draw_wall(358+32*i,162)
	for i in range(0,2):
		draw_wall(454,194+32*i)
	for i in range(0,4):
		draw_wall(358+32*i,258)

	#hard_wall
	draw_hard_wall(116,324)
	draw_hard_wall(484,324)

	#river
	for i in range(0,5):
		draw_river(240+32*i,316)
		draw_river(240+32*i,332)

	#forest
	for i in range(0,4):
		for j in range(0,3):
			draw_forest(148+16*i,308+16*j)
	for i in range(0,4):
		for j in range(0,3):
			draw_forest(452-16*i,308+16*j)

	#A
	for i in range(0,6):
		draw_wall(146,566-32*i)
	for i in range(0,5):
		draw_wall(146+32*i,374)
	for i in range(0,6):
		draw_wall(273,566-32*i)
	for i in range(0,3):
		draw_wall(177+32*i,502)

	#P
	for i in range(0,6):
		draw_wall(358,566-32*i)
	for i in range(0,4):
		draw_wall(358+32*i,374)
	for i in range(0,4):
		draw_wall(358+32*i,470)
	for i in range(0,3):
		draw_wall(454,374+32*i)
	
	#Home
	draw_home(300,668)
	for i in range(0,2):
		draw_wall(268,684-32*i)
	draw_small_wall(300,652)
	for i in range(0,2):
		draw_wall(332,684-32*i)


running = True

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == K_ESCAPE:
			running = False
	screen.fill((0,0,0))
	drawing_map_2()
	pygame.display.flip()

pygame.display.update()



# def eliminate_repeat(lst):
# 	i = 0
# 	k = 1
# 	while i < len(lst):
# 		if k >= len(lst):
# 			i += 1
# 			k = i + 1
# 			continue
# 		if lst[i] == lst[k]:
# 			del lst[k]
# 		else:
# 			k += 1

# def check_tank_wall_collide(group):
# 	tanklist = group.sprites()
# 	walllist = group.sprites()
# 	collidelist = []
# 	for i in range(len(tanklist)):
# 		for k in range(i+1, len(walllist)):
# 			if pygame.sprite.collide_rect(tanklist[i], walllist[k]):
# 				collidelist.append(tanklist[i])
# 				collidelist.append(walllist[k])
# 	eliminate_repeat(collidelist)
# 	return collidelist


# def tank_wall_collide(lst):
# 	tank_wall_collide_list = check_tank_wall_collide(lst)
# 	if not len(tank_wall_collide_list) == 0:
# 		for tank in tank_wall_collide_list:
# 			tank.reset_position()

