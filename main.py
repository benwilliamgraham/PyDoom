import math
import random
from mathematics import *
from ctypes import *
import pygame
from pygame.locals import *

import os

os.environ['SDL_VIDEO_WINDOW_POS'] = "140, 30"

#sound initialization
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()

#window initialization
from OpenGL.GL import *
from OpenGL.GLU import *
pygame.init()
display = (1080,600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL | OPENGLBLIT)
gluPerspective(70, (display[0] / display[1]), 0.1, 64.0)
glClearColor(0, 0, 0, 0)
glEnableClientState(GL_VERTEX_ARRAY)
glEnableClientState(GL_TEXTURE_COORD_ARRAY)
glEnableClientState(GL_COLOR_ARRAY)
glAlphaFunc(GL_GREATER, 0.5)
glEnable(GL_ALPHA_TEST)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glEnable(GL_BLEND)
pygame.display.set_icon(pygame.image.load("assets/icon.png"))

#create game clock
clock = pygame.time.Clock()

#other imports
import assets
from world import *
from entity import *

def main(): 
	world = eval(open("maps/map2.wad", "rt").read())

	world.mesh()

	player = Player(Vec3(1, 3, 11.5), Vec3(0, 0, 0))
	gamemode = "title"
	running = True

	assets.music.set_volume(0.2)
	assets.music.play(-1)

	#game loop
	while running:
		if gamemode == "title":
			glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
			glPushMatrix()
			glTranslatef(0, 0, -1)
			glScale(2.5, 1.4, 1)
			glBindTexture(GL_TEXTURE_2D, assets.title)
			glBindBuffer(GL_ARRAY_BUFFER, assets.entityVBO[0])
			glVertexPointer(3, GL_FLOAT, 0, None)
			glBindBuffer(GL_ARRAY_BUFFER, assets.entityVBO[1])
			glTexCoordPointer(2, GL_FLOAT, 0, None)
			glBindBuffer(GL_ARRAY_BUFFER, assets.entityVBO[2])
			glColorPointer(3, GL_FLOAT, 0, None)
			glDrawArrays(GL_QUADS, 0, 4 * 12)
			glPopMatrix()
			events = pygame.event.get()
			keys = pygame.key.get_pressed()
			for event in events:
				if event.type == pygame.QUIT:
					running = False
			if keys[K_ESCAPE]:
				running = False
			if keys[K_b]:
				gamemode = "running"
			#actualy draw screen
			pygame.display.flip()
			clock.tick(60)
		else:
			#check to make sure the window isn't being closed
			events = pygame.event.get()
			keys = pygame.key.get_pressed()
			for event in events:
				if event.type == pygame.QUIT:
					running = False
			if keys[K_ESCAPE]:
				running = False

			#update the player
			world.player.control(world, keys, display)
			if world.player.health <= 0:
				print("You Lost")
				main()
				gamemode = "exit"
			if len(world.entities) == 0:
				print("You Won")
				main()
				gamemode = "exit"

			#clear the screen
			glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

			#draw everything
			world.draw()

			#actualy draw screen
			pygame.display.flip()
			clock.tick(60)
	print(clock.get_fps())
	pygame.quit()
	quit()

main()