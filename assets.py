import pygame
from ctypes import *
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from world import *

#options
hard = 0
mouseSensativity = 1
musicVolume = 1
volume = 3

#texture loading
def loadTexture(filename):
	image = pygame.image.load(filename)
	return toTexture(image)

def toTexture(image):
	data = pygame.image.tostring(image, "RGBA", 1)
	glEnable(GL_TEXTURE_2D)
	textureID = glGenTextures(1)

	glBindTexture(GL_TEXTURE_2D, textureID)
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA,
				image.get_width(), image.get_height(),
				0, GL_RGBA, GL_UNSIGNED_BYTE, data)

	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

	return textureID

bar = loadTexture("assets/bar.png")
bullet = loadTexture("assets/bullet.png")
crosshairs = loadTexture("assets/crosshairs.png")
door = loadTexture("assets/door.png")
health = loadTexture("assets/health.png")
healthPack = loadTexture("assets/healthPack.png")
highlight = loadTexture("assets/highlight.png")
key = loadTexture("assets/key.png")
notification = loadTexture("assets/notification.png")
plasmaRifle = loadTexture("assets/plasmaRifle.png")
plasmaRiflePickup = loadTexture("assets/plasmaRiflePickup.png")
plasmaSMG = loadTexture("assets/plasmaSMG.png")
plasmaSMGPickup = loadTexture("assets/plasmaSMGPickup.png")
plasmaShotgun = loadTexture("assets/plasmaShotgun.png")
plasmaShotgunPickup = loadTexture("assets/plasmaShotgunPickup.png")
slime = loadTexture("assets/slime.png")
skull = loadTexture("assets/skull.png")
tileset = loadTexture("assets/tileset.png")

title = loadTexture("assets/title.png")
options = loadTexture("assets/options.png")
selectLevel = loadTexture("assets/selectLevel.png")

instructions = [
	loadTexture("assets/instructions1.png"),
	loadTexture("assets/instructions2.png"),
	loadTexture("assets/instructions3.png"),
	loadTexture("assets/instructions4.png"),
	loadTexture("assets/instructions5.png"),
]

levelPassed = loadTexture("assets/levelPassed.png")
levelFailed = loadTexture("assets/levelFailed.png")

bang = pygame.mixer.Sound("assets/bang.wav")
doorOpen = pygame.mixer.Sound("assets/doorOpen.wav")
doorClose = pygame.mixer.Sound("assets/doorClose.wav")
hit = pygame.mixer.Sound("assets/hit.wav")
collect = pygame.mixer.Sound("assets/keyGet.wav")
squish = pygame.mixer.Sound("assets/squish.wav")
roar = pygame.mixer.Sound("assets/roar.wav")
music = pygame.mixer.Sound("assets/music.wav")

#Entity
vertices = [
	-0.5, 0.5, 0,
	-0.5, -0.5, 0,
	0.5, -0.5, 0,
	0.5, 0.5, 0
]
textureCoords = [
	0, 1,
	0, 0,
	1, 0,
	1, 1
]
colors = [1] * 12
entityVBO = glGenBuffers(3)
glBindBuffer(GL_ARRAY_BUFFER, entityVBO[0])
glBufferData(GL_ARRAY_BUFFER, len(vertices) * 4, (c_float * len(vertices))(*vertices), GL_STATIC_DRAW)
glBindBuffer(GL_ARRAY_BUFFER, entityVBO[1])
glBufferData(GL_ARRAY_BUFFER, len(textureCoords) * 4, (c_float * len(textureCoords))(*textureCoords), GL_STATIC_DRAW)
glBindBuffer(GL_ARRAY_BUFFER, entityVBO[2])
glBufferData(GL_ARRAY_BUFFER, len(colors) * 4, (c_float * len(colors))(*colors), GL_STATIC_DRAW)

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

fontBig = pygame.font.Font("assets/pixelBadass.ttf", 50)
fontLil = pygame.font.Font("assets/pixelBadass.ttf", 28)

levelDisplays = [
	World("level 1"),
	World("level 2"),
	World("level 3")
]
for world in levelDisplays:
	world.mesh(False)