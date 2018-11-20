import pygame
from ctypes import *
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

def loadTexture(filename):
	img = pygame.image.load(filename)
	data = pygame.image.tostring(img, "RGBA", 1)

	glEnable(GL_TEXTURE_2D)
	textureID = glGenTextures(1)

	glBindTexture(GL_TEXTURE_2D, textureID)
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 
				img.get_width(), img.get_height(),
				0, GL_RGBA, GL_UNSIGNED_BYTE, data)

	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

	return textureID

bullet = loadTexture("assets/bullet.png")
crosshairs = loadTexture("assets/crosshairs.png")
door = loadTexture("assets/door.png")
slime = loadTexture("assets/slime.png")
tileset = loadTexture("assets/tileset.png")
bang = pygame.mixer.Sound("assets/bang.wav")
squish = pygame.mixer.Sound("assets/squish.wav")

#Bullet
vertices = [
	-0.1, 0.2, 0,
	-0.1, 0, 0,
	0.1, 0, 0,
	0.1, 0.2, 0
]
textureCoords = [
	0, 1,
	0, 0,
	1, 0,
	1, 1
]
colors = [1] * 12
bulletVBO = glGenBuffers(3)
glBindBuffer(GL_ARRAY_BUFFER, bulletVBO[0])
glBufferData(GL_ARRAY_BUFFER, len(vertices) * 4, (c_float * len(vertices))(*vertices), GL_STATIC_DRAW)
glBindBuffer(GL_ARRAY_BUFFER, bulletVBO[1])
glBufferData(GL_ARRAY_BUFFER, len(textureCoords) * 4, (c_float * len(textureCoords))(*textureCoords), GL_STATIC_DRAW)
glBindBuffer(GL_ARRAY_BUFFER, bulletVBO[2])
glBufferData(GL_ARRAY_BUFFER, len(colors) * 4, (c_float * len(colors))(*colors), GL_STATIC_DRAW)

#particle
rad = 0.05
vertices = [
	-rad, rad, 0,
	-rad, -rad, 0,
	rad, -rad, 0,
	rad, rad, 0
]
textureCoords = [
	0.49, 0.31,
	0.49, 0.29,
	0.51, 0.29,
	0.51, 0.31
]
colors = [1] * 12
particleVBO = glGenBuffers(3)
glBindBuffer(GL_ARRAY_BUFFER, particleVBO[0])
glBufferData(GL_ARRAY_BUFFER, len(vertices) * 4, (c_float * len(vertices))(*vertices), GL_STATIC_DRAW)
glBindBuffer(GL_ARRAY_BUFFER, particleVBO[1])
glBufferData(GL_ARRAY_BUFFER, len(textureCoords) * 4, (c_float * len(textureCoords))(*textureCoords), GL_STATIC_DRAW)
glBindBuffer(GL_ARRAY_BUFFER, particleVBO[2])
glBufferData(GL_ARRAY_BUFFER, len(colors) * 4, (c_float * len(colors))(*colors), GL_STATIC_DRAW)