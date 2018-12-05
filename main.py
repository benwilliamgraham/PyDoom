import math
import random
from mathematics import *
from ctypes import *
import pygame
from pygame.locals import *

#sound initialization
pygame.mixer.pre_init(44100, -8, 1, 512)
pygame.mixer.init()
pygame.mixer.set_num_channels(16)

#window initialization
from OpenGL.GL import *
from OpenGL.GLU import *
pygame.init()
display = (1080,600)
screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL | OPENGLBLIT)
gluPerspective(70, (display[0] / display[1]), 0.1, 1000.0)
glClearColor(30 / 255, 0 / 255, 4 / 255, 1)
#glClearColor(0, 0, 0, 0)
glEnableClientState(GL_VERTEX_ARRAY)
glEnableClientState(GL_TEXTURE_COORD_ARRAY)
glEnableClientState(GL_COLOR_ARRAY)
glAlphaFunc(GL_GREATER, 0.5)
glEnable(GL_ALPHA_TEST)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glEnable(GL_BLEND)
pygame.display.set_icon(pygame.image.load("assets/icon.png"))
pygame.display.set_caption("PYDOOM")

#other imports
import assets
from world import *
from entity import *

#create game clock
clock = pygame.time.Clock()

#create music
assets.music.set_volume(0.25)
assets.music.play(-1)

#level selection
def select():
	pygame.mouse.set_visible(True)
	selected = 0
	transitioning = False
	levelNames = [
		Button(Vec2(800, 60), "    Reactor"),
		Button(Vec2(800, 60), " Control Room"),
		Button(Vec2(800, 60), "   The Grind")
	]

	title = Button(Vec2(250, 50), "Play Level:", True)
	title.texture = assets.selectLevel
	play = Button(Vec2(250, 420), " Play")
	optionsMenu = Button(Vec2(250, 480), " Options")
	mainMenu = Button(Vec2(250, 540), " Main Menu")

	prev = Button(Vec2(680, 590), " < Prev")
	prov = Button(Vec2(990, 590), "       Next >")

	while True:
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

		world = assets.levelDisplays[selected]

		world.player.rotation.y += 1
		world.player.rotation.x = 60
		world.player.position.y = 60
		world.player.position.x = 32 - 40 * math.sin(world.player.rotation.y * 3.1415 / 180)
		world.player.position.z = 32 + 40 * math.cos(world.player.rotation.y * 3.1415 / 180)

		#create transformation matrix
		glEnable(GL_DEPTH_TEST)
		glPushMatrix()
		#shift
		glTranslatef(32, 0, 0)
		#rotate
		glRotatef(world.player.rotation.x, 1, 0, 0)
		glRotatef(world.player.rotation.y, 0, 1, 0)
		#center
		glTranslatef(-world.player.position.x, -world.player.position.y - 0.3, -world.player.position.z)

		#draw the level
		glBindTexture(GL_TEXTURE_2D, world.tileset)
		glBindBuffer(GL_ARRAY_BUFFER, world.vbo[0])
		glVertexPointer(3, GL_FLOAT, 0, None)
		glBindBuffer(GL_ARRAY_BUFFER, world.vbo[1])
		glTexCoordPointer(2, GL_FLOAT, 0, None)
		glBindBuffer(GL_ARRAY_BUFFER, world.vbo[2])
		glColorPointer(3, GL_FLOAT, 0, None)
		glDrawArrays(GL_QUADS, 0, world.size.x * world.size.y * 11)

		glPopMatrix()

		#make 2d
		glDisable(GL_DEPTH_TEST)

		levelNames[selected].draw()

		if play.update():
			game(selected)
			return
		elif optionsMenu.update():
			if options():
				return
		elif mainMenu.update():
			main()
			return
		elif prev.update():
			if not transitioning:
				selected = (selected + 2) % 3
				transitioning = True
		elif prov.update():
			if not transitioning:
				selected = (selected + 1) % 3
				transitioning = True
		else:
			transitioning = False

		title.draw()
		play.draw()
		optionsMenu.draw()
		mainMenu.draw()
		prev.draw()
		prov.draw()

		events = pygame.event.get()
		keys = pygame.key.get_pressed()
		for event in events:
			if event.type == pygame.QUIT:
				exit()

		#actualy draw screen
		pygame.display.flip()
		clock.tick(60)

#options panel
def options():
	pygame.mouse.set_visible(True)
	title = Button(Vec2(550, 60), "Options:", True)
	title.texture = assets.options

	transitioning = False

	difficultiesTitle = Button(Vec2(450, 180), " Difficulty:")
	difficulties = [
		Button(Vec2(900, 180), " Normal"),
		Button(Vec2(900, 180), " Extreme"),
	]

	mouseSensativitiesTitle = Button(Vec2(450, 240), " Sensitivity:")
	mouseSensativities = [
		Button(Vec2(900, 240), " Low"),
		Button(Vec2(900, 240), " Medium"),
		Button(Vec2(900, 240), " High")
	]

	musicsTitle = Button(Vec2(450, 300), " music:")
	musics = [
		Button(Vec2(900, 300), " Off"),
		Button(Vec2(900, 300), " Low"),
		Button(Vec2(900, 300), " Medium"),
		Button(Vec2(900, 300), " High")
	]

	volumesTitle = Button(Vec2(450, 360), " Volume:")
	volumes = [
		Button(Vec2(900, 360), " Off"),
		Button(Vec2(900, 360), " Low"),
		Button(Vec2(900, 360), " Medium"),
		Button(Vec2(900, 360), " High")
	]

	resume = Button(Vec2(600, 500), " Resume")

	mainMenu = Button(Vec2(600, 560), " Main Menu")

	while True:
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		#check to make sure the window isn't being closed
		events = pygame.event.get()
		keys = pygame.key.get_pressed()
		for event in events:
			if event.type == pygame.QUIT:
				exit()

		if difficulties[assets.hard].update():
			if not transitioning:
				assets.hard = (assets.hard + 1) % 2
				transitioning = True

		elif mouseSensativities[assets.mouseSensativity].update():
			if not transitioning:
				assets.mouseSensativity = (assets.mouseSensativity + 1) % 3
				transitioning = True

		elif musics[assets.musicVolume].update():
			if not transitioning:
				assets.musicVolume = (assets.musicVolume + 1) % 4
				assets.music.set_volume(assets.musicVolume / 4)
				transitioning = True

		elif volumes[assets.volume].update():
			if not transitioning:
				assets.volume = (assets.volume + 1) % 4
				transitioning = True

		elif resume.update():
			return False

		elif mainMenu.update():
			main()
			return True

		else:
			transitioning = False

		title.draw()
		difficultiesTitle.draw()
		difficulties[assets.hard].draw()
		mouseSensativitiesTitle.draw()
		mouseSensativities[assets.mouseSensativity].draw()
		musicsTitle.draw()
		musics[assets.musicVolume].draw()
		volumesTitle.draw()
		volumes[assets.volume].draw()
		resume.draw()
		mainMenu.draw()

		pygame.display.flip()
		clock.tick(60)

#game running
def game(level):
	world = World("level " + str(level + 1))

	world.mesh(True)

	while True:
		#check to make sure the window isn't being closed
		events = pygame.event.get()
		keys = pygame.key.get_pressed()
		for event in events:
			if event.type == pygame.QUIT:
				exit()
		if keys[K_ESCAPE]:
			if options():
				return

		#update the player
		world.player.control(world, keys, display)
		if world.player.health <= 0:
			failed()
			return
		if world.numEnemies == 0:
			passed()
			return

		#clear the screen
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

		#draw everything
		world.draw()

		#actualy draw screen
		pygame.display.flip()
		clock.tick(60)

def tutorial():
	
	instruction = 0
	transitioning = False

	prev = Button(Vec2(230, 590), " < Back")
	prov = Button(Vec2(990, 590), "       Next >")

	while True:
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		#check to make sure the window isn't being closed
		events = pygame.event.get()
		keys = pygame.key.get_pressed()
		for event in events:
			if event.type == pygame.QUIT:
				exit()

		glPushMatrix()
		glTranslatef(0, 0, -1)
		glScale(2.52, 1.4, 1)
		glBindTexture(GL_TEXTURE_2D, assets.instructions[instruction])
		glBindBuffer(GL_ARRAY_BUFFER, assets.entityVBO[0])
		glVertexPointer(3, GL_FLOAT, 0, None)
		glBindBuffer(GL_ARRAY_BUFFER, assets.entityVBO[1])
		glTexCoordPointer(2, GL_FLOAT, 0, None)
		glBindBuffer(GL_ARRAY_BUFFER, assets.entityVBO[2])
		glColorPointer(3, GL_FLOAT, 0, None)
		glDrawArrays(GL_QUADS, 0, 4 * 12)
		glPopMatrix()

		if prev.update():
			if not transitioning:
				instruction -= 1
				transitioning = True
		elif prov.update():
			if not transitioning:
				instruction += 1
				transitioning = True
		else:
			transitioning = False

		if instruction < 0 or instruction >= 5:
			return

		prev.draw()
		prov.draw()

		pygame.display.flip()
		clock.tick(60)

def passed():
	pygame.mouse.set_visible(True)
	title = Button(Vec2(535, 170), "Level Passed", True)
	title.texture = assets.levelPassed

	mainMenu = Button(Vec2(600, 500), "Main Menu")

	while True:
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		#check to make sure the window isn't being closed
		events = pygame.event.get()
		keys = pygame.key.get_pressed()
		for event in events:
			if event.type == pygame.QUIT:
				exit()

		if mainMenu.update():
			main()
			return

		title.draw()
		mainMenu.draw()

		#actualy draw screen
		pygame.display.flip()
		clock.tick(60)

def failed():
	pygame.mouse.set_visible(True)
	title = Button(Vec2(535, 170), "Level Failed", True)
	title.texture = assets.levelFailed

	mainMenu = Button(Vec2(600, 500), "Main Menu")

	while True:
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		#check to make sure the window isn't being closed
		events = pygame.event.get()
		keys = pygame.key.get_pressed()
		for event in events:
			if event.type == pygame.QUIT:
				exit()

		if mainMenu.update():
			main()
			return

		title.draw()
		mainMenu.draw()

		#actualy draw screen
		pygame.display.flip()
		clock.tick(60)

def main():
	pygame.mouse.set_visible(True)
	title = Button(Vec2(535, 70), "PYDOOM:", True)
	title.texture = assets.title
	play = Button(Vec2(600, 180), " Play")
	optionsMenu = Button(Vec2(600, 240), " Options")
	tutorialMenu = Button(Vec2(600, 300), " Tutorial")
	closeButton = Button(Vec2(600, 360), " Exit")

	while True:
		#clear the screen
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

		world = assets.levelDisplays[0]

		world.player.rotation.y += 0.5
		world.player.rotation.x = 20
		world.player.position.y = 30
		world.player.position.x = 32
		world.player.position.z = 32

		#create transformation matrix
		glEnable(GL_DEPTH_TEST)
		glPushMatrix()
		#shift
		glTranslatef(0, 0, 0)
		#rotate
		glRotatef(world.player.rotation.x, 1, 0, 0)
		glRotatef(world.player.rotation.y, 0, 1, 0)
		#center
		glTranslatef(-world.player.position.x, -world.player.position.y - 0.3, -world.player.position.z)

		#draw the level
		glBindTexture(GL_TEXTURE_2D, world.tileset)
		glBindBuffer(GL_ARRAY_BUFFER, world.vbo[0])
		glVertexPointer(3, GL_FLOAT, 0, None)
		glBindBuffer(GL_ARRAY_BUFFER, world.vbo[1])
		glTexCoordPointer(2, GL_FLOAT, 0, None)
		glBindBuffer(GL_ARRAY_BUFFER, world.vbo[2])
		glColorPointer(3, GL_FLOAT, 0, None)
		glDrawArrays(GL_QUADS, 0, world.size.x * world.size.y * 11)

		glPopMatrix()

		#make 2d
		glDisable(GL_DEPTH_TEST)
		#check to make sure the window isn't being closed
		events = pygame.event.get()
		keys = pygame.key.get_pressed()
		for event in events:
			if event.type == pygame.QUIT:
				exit()

		if play.update():
			select()
		elif optionsMenu.update():
			options()
		elif tutorialMenu.update():
			tutorial()
		elif closeButton.update():
			close()

		title.draw()
		play.draw()
		optionsMenu.draw()
		tutorialMenu.draw()
		closeButton.draw()

		#actualy draw screen
		pygame.display.flip()
		clock.tick(60)

def close():
	print(clock.get_fps())
	pygame.quit()
	quit()

main()