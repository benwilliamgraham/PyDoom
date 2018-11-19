import pygame
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