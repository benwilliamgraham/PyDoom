import math
import random
from mathematics import *
from ctypes import *
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from texture import *
from world import *
from entity import *

import os

os.environ['SDL_VIDEO_WINDOW_POS'] = "140, 30"

def main(): 
	pygame.init()
	display = (1080,600)
	clock = pygame.time.Clock()
	pygame.display.set_mode(display, DOUBLEBUF|OPENGL|OPENGLBLIT)

	gluPerspective(85, (display[0]/display[1]), 0.1, 50.0)
	glClearColor(0, 0, 0, 0)
	glEnableClientState(GL_VERTEX_ARRAY)
	glEnableClientState(GL_TEXTURE_COORD_ARRAY)
	glEnableClientState(GL_COLOR_ARRAY)
	glEnable(GL_DEPTH_TEST)
	#glEnable(GL_CULL_FACE)
	glEnable(GL_ALPHA_TEST)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	glEnable(GL_BLEND)

	world = eval(open("maps/map1.wad", "rt").read())

	world.mesh()

	entities = []

	player = Player(Vec3(1, 3, 11.5), Vec3(0, 0, 0))
	running = True

	#gui
	crosshairs = loadTexture("assets/crosshairs.png")
	cvert = [
		-0.5, 0.5, -12,
		-0.5, -0.5, -12,
		0.5, -0.5, -12,
		0.5, 0.5, -12
	]
	ctex = [
		0, 1,
		0, 0,
		1, 0,
		1, 1
	]
	ccol = [1] * 12
	cvbo = glGenBuffers(3)
	glBindBuffer(GL_ARRAY_BUFFER, cvbo[0])
	glBufferData(GL_ARRAY_BUFFER, len(cvert) * 4, (c_float * len(cvert))(*cvert), GL_STATIC_DRAW)
	glBindBuffer(GL_ARRAY_BUFFER, cvbo[1])
	glBufferData(GL_ARRAY_BUFFER, len(ctex) * 4, (c_float * len(ctex))(*ctex), GL_STATIC_DRAW)
	glBindBuffer(GL_ARRAY_BUFFER, cvbo[2])
	glBufferData(GL_ARRAY_BUFFER, len(ccol) * 4, (c_float * len(ccol))(*ccol), GL_STATIC_DRAW)

	entities.append(Door(Vec3(-0.01, 2.5, 11.5)))
	entities.append(Door(Vec3(23.01, 2.5, 11.5)))
	for i in range(1):
		entities.append(Slime(Vec3(random.randint(1, 20), 4, random.randint(1, 20))))

	while running:
		events = pygame.event.get()
		keys = pygame.key.get_pressed()
		for event in events:
			if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
				running = False

		player.control(world, entities, keys, display)
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		glEnable(GL_DEPTH_TEST)
		glPushMatrix()
		glRotatef(player.rotation.x, 1, 0, 0)
		glRotatef(player.rotation.y, 0, 1, 0)
		glTranslatef(-player.position.x, -player.position.y - 0.3, -player.position.z)
		for ent in range(len(entities) - 1, -1, -1):
			entities[ent].draw()
			if entities[ent].update(world, player) == True:
				entities.pop(ent)
		world.draw()
		#gui
		glPopMatrix()
		glDisable(GL_DEPTH_TEST)
		glBindTexture(GL_TEXTURE_2D, crosshairs)
		glBindBuffer(GL_ARRAY_BUFFER, cvbo[0])
		glVertexPointer(3, GL_FLOAT, 0, None)
		glBindBuffer(GL_ARRAY_BUFFER, cvbo[1])
		glTexCoordPointer(2, GL_FLOAT, 0, None)
		glBindBuffer(GL_ARRAY_BUFFER, cvbo[2])
		glColorPointer(3, GL_FLOAT, 0, None)
		glDrawArrays(GL_QUADS, 0, 4 * 12)
		#end gui
		pygame.display.flip()
		clock.tick(60)
	print(clock.get_fps())
	pygame.quit()
	quit()


main()