import math
import pygame
import random

from ctypes import *
from mathematics import *
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
import assets

gravity = -0.01

class Item(object):
	def __init__(self):
		pass

	def update(self, use):
		pass

class PlasmaGun(Item):
	def __init__(self):
		super().__init__()
		self.firing = False

	def update(self, world, user, using):
		if using:
			if not self.firing:
				self.firing = True
				lookDir = Vec3(
					math.sin(user.rotation.y * 3.14 / 180) * math.cos(user.rotation.x * 3.14 / 180),
					-math.sin(user.rotation.x * 3.14 / 180),
					-math.cos(user.rotation.y * 3.14 / 180) * math.cos(user.rotation.x * 3.14 / 180))
				world.visuals.append(Bullet(
					Vec3(user.position.x, user.position.y + 0.3, user.position.z) + lookDir,
					lookDir
				))
				assets.bang.play()
		else:
			self.firing = False


class Entity(object):
	def __init__(self, position):
		self.position = position

	def draw(self):
		pass

	def update(self, world):
		pass

class Player(Entity):
	def __init__(self, position, rotation):
		super().__init__(position)
		self.rotation = rotation
		self.velocity = Vec3(0, 0, 0)
		self.grounded = False
		rad = Vec3(0.25, 0.45, 0.25)
		self.rad = rad
		self.faceMesh = (
			Vec3(-rad.x, -rad.y, -rad.z),
			Vec3(-rad.x, -rad.y, rad.z),
			Vec3(-rad.x, rad.y, -rad.z),
			Vec3(-rad.x, rad.y, rad.z),
			Vec3(rad.x, -rad.y, -rad.z),
			Vec3(rad.x, -rad.y, rad.z),
			Vec3(rad.x, rad.y, -rad.z),
			Vec3(rad.x, rad.y, rad.z),
		)
		self.item = PlasmaGun()

	def checkCollision(self, world, delta):
		for point in self.faceMesh:
			if world.checkCollision(self.position + point + delta):
				return True
		return False

	def control(self, world, keys, display):
		deltaPos = Vec3(0, 0, 0)
		deltaRot = Vec3(0, 0, 0)
		if keys[K_w]:
			deltaPos.z += 1
		elif keys[K_s]:
			deltaPos.z -= 1
		if keys[K_d]:
			deltaPos.x += 1
		elif keys[K_a]:
			deltaPos.x -= 1
		if keys[K_SPACE] and self.grounded:
			deltaPos.y += 1
		
		deltaMouse = pygame.mouse.get_pos()
		deltaRot.y = deltaMouse[0] - display[0] // 2
		deltaRot.x = deltaMouse[1] - display[1] // 2
		pygame.mouse.set_pos(display[0] // 2, display[1] // 2)
		pygame.mouse.set_visible(False)

		self.rotation += deltaRot * 0.23
		self.rotation.x = max(min(self.rotation.x, 30), -30)
		dx = (deltaPos.x * math.cos(self.rotation.y * 3.14 / 180) + deltaPos.z * math.sin(self.rotation.y * 3.14 / 180)) * 0.1
		dz = (deltaPos.x * math.sin(self.rotation.y * 3.14 / 180) - deltaPos.z * math.cos(self.rotation.y * 3.14 / 180)) * 0.1

		self.velocity.y += gravity + deltaPos.y * 0.2

		if self.checkCollision(world, Vec3(0, self.velocity.y, 0)):
			if self.velocity.y < 0:
				self.grounded = True
			self.velocity.y *= -0.2
		else:
			self.grounded = False
			self.position.y += self.velocity.y

		if self.checkCollision(world, Vec3(dx, 0, 0)):
			if not self.checkCollision(world, Vec3(dx, 0.5, 0)) and self.grounded:
				self.velocity.y += 0.12
		else:
			self.position.x += dx

		if self.checkCollision(world, Vec3(0, 0, dz)):
			if not self.checkCollision(world, Vec3(0, 0.5, dz)) and self.grounded:
				self.velocity.y += 0.12
		else:
			self.position.z += dz

		usingItem = False
		if pygame.mouse.get_pressed()[0]:
			usingItem = True
		self.item.update(world, self, usingItem)

class Particle(Entity):
	def __init__(self, position, velocity, texture, weight = 1):
		super().__init__(position)
		self.texture = texture
		self.velocity = velocity
		self.rotation = Vec3(0, 0, 0)
		self.vbo = assets.particleVBO
		self.weight = weight

	def draw(self):
		glPushMatrix()
		glTranslatef(self.position.x, self.position.y, self.position.z)
		glRotatef(self.rotation.y, 0, 1, 0)
		glBindTexture(GL_TEXTURE_2D, self.texture)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo[0])
		glVertexPointer(3, GL_FLOAT, 0, None)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo[1])
		glTexCoordPointer(2, GL_FLOAT, 0, None)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo[2])
		glColorPointer(3, GL_FLOAT, 0, None)
		glDrawArrays(GL_QUADS, 0, 4 * 12)
		glPopMatrix()

	def update(self, world):
		toPlayer = Vec3(
			world.player.position.x - self.position.x,
			world.player.position.y - self.position.y,
			world.player.position.z - self.position.z
		)
		if toPlayer.z == 0:
			self.rotation.y = 0
		else:
			self.rotation.y = math.atan(toPlayer.x / toPlayer.z) * 180 / 3.14


		if world.checkCollision(self.position + Vec3(0, self.velocity.y, 0)):
			self.velocity.y *= -0.2
			if abs(self.velocity.y) < 0.003:
				return True
		else:
			self.position.y += self.velocity.y

		self.velocity.y += gravity * self.weight

		if world.checkCollision(self.position + Vec3(self.velocity.x, 0, 0)):
			pass
		else:
			self.position.x += self.velocity.x

		if world.checkCollision(self.position + Vec3(0, 0, self.velocity.z)):
			pass
		else:
			self.position.z += self.velocity.z

class Door(Entity):
	def __init__(self, position):
		super().__init__(position)
		self.texture = assets.door
		self.downPos = position.y
		vertices = [
			0, 2, -1,
			0, 0, -1,
			0, 0, 1,
			0, 2, 1
		]
		textureCoords = [
			0, 1,
			0, 0,
			1, 0,
			1, 1
		]
		colors = [1] * 12
		self.vbo = glGenBuffers(3)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo[0])
		glBufferData(GL_ARRAY_BUFFER, len(vertices) * 4, (c_float * len(vertices))(*vertices), GL_STATIC_DRAW)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo[1])
		glBufferData(GL_ARRAY_BUFFER, len(textureCoords) * 4, (c_float * len(textureCoords))(*textureCoords), GL_STATIC_DRAW)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo[2])
		glBufferData(GL_ARRAY_BUFFER, len(colors) * 4, (c_float * len(colors))(*colors), GL_STATIC_DRAW)

	def draw(self):
		glPushMatrix()
		glTranslatef(self.position.x, self.position.y, self.position.z)
		glBindTexture(GL_TEXTURE_2D, self.texture)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo[0])
		glVertexPointer(3, GL_FLOAT, 0, None)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo[1])
		glTexCoordPointer(2, GL_FLOAT, 0, None)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo[2])
		glColorPointer(3, GL_FLOAT, 0, None)
		glDrawArrays(GL_QUADS, 0, 4 * 12)
		glPopMatrix()

	def update(self, world):
		if abs(self.position.x - world.player.position.x) < 2 and abs(self.position.z - world.player.position.z) < 2:
			self.position.y = (self.downPos + 2 + self.position.y * 9) / 10
		else:
			self.position.y = (self.downPos + self.position.y * 9) / 10

class Bullet(Entity):
	def __init__(self, position, velocity):
		super().__init__(position)
		self.texture = assets.bullet
		self.velocity = velocity
		self.rotation = Vec3(0, 0, 0)
		self.vbo = assets.bulletVBO

	def draw(self):
		glPushMatrix()
		glTranslatef(self.position.x, self.position.y, self.position.z)
		glRotatef(self.rotation.y, 0, 1, 0)
		glBindTexture(GL_TEXTURE_2D, self.texture)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo[0])
		glVertexPointer(3, GL_FLOAT, 0, None)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo[1])
		glTexCoordPointer(2, GL_FLOAT, 0, None)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo[2])
		glColorPointer(3, GL_FLOAT, 0, None)
		glDrawArrays(GL_QUADS, 0, 4 * 12)
		glPopMatrix()

	def update(self, world):
		toPlayer = Vec3(
			world.player.position.x - self.position.x,
			world.player.position.y - self.position.y,
			world.player.position.z - self.position.z
		)
		if toPlayer.z == 0:
			self.rotation.y = 0
		else:
			self.rotation.y = math.atan(toPlayer.x / toPlayer.z) * 180 / 3.14

		for entity in world.entities:
			dist = Vec3(
				abs(self.position.x - entity.position.x),
				abs(self.position.y - entity.position.y),
				abs(self.position.z - entity.position.z)
			)
			if (dist.x < entity.rad.x and
				dist.y < entity.rad.y and
				dist.z < entity.rad.z):
				entity.velocity += self.velocity * 2
				return True

		#self.velocity.y += gravity

		if world.checkCollision(self.position + Vec3(0, self.velocity.y, 0)):
			return True
		else:
			self.position.y += self.velocity.y

		if world.checkCollision(self.position + Vec3(self.velocity.x, 0, 0)):
			return True
		else:
			self.position.x += self.velocity.x

		if world.checkCollision(self.position + Vec3(0, 0, self.velocity.z)):
			return True
		else:
			self.position.z += self.velocity.z

		world.visuals.append(
			Particle(
				Vec3(self.position.x, self.position.y, self.position.z), 
				Vec3(random.randint(-1, 1), random.randint(0, 2), random.randint(-1, 1)) * 0.02,
				assets.bullet, -0.6
			)
		)

class Slime(Entity):
	def __init__(self, position):
		super().__init__(position)
		self.texture = assets.slime
		self.velocity = Vec3(0, 0, 0)
		self.grounded = False
		self.maxSpeed = 0.1
		self.rotation = Vec3(0, 0, 0)
		self.health = 10
		rad = Vec3(0.4, 0.4, 0.4)
		self.rad = rad
		self.faceMesh = (
			Vec3(-rad.x, -rad.y, -rad.z),
			Vec3(-rad.x, -rad.y, rad.z),
			Vec3(-rad.x, rad.y, -rad.z),
			Vec3(-rad.x, rad.y, rad.z),
			Vec3(rad.x, -rad.y, -rad.z),
			Vec3(rad.x, -rad.y, rad.z),
			Vec3(rad.x, rad.y, -rad.z),
			Vec3(rad.x, rad.y, rad.z),
		)
		vertices = [
			-0.5, rad.y, 0,
			-0.5, -rad.y, 0,
			0.5, -rad.y, 0,
			0.5, rad.y, 0
		]
		textureCoords = [
			0, 1,
			0, 0,
			1, 0,
			1, 1
		]
		colors = [1] * 12
		self.vbo = glGenBuffers(3)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo[0])
		glBufferData(GL_ARRAY_BUFFER, len(vertices) * 4, (c_float * len(vertices))(*vertices), GL_STATIC_DRAW)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo[1])
		glBufferData(GL_ARRAY_BUFFER, len(textureCoords) * 4, (c_float * len(textureCoords))(*textureCoords), GL_STATIC_DRAW)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo[2])
		glBufferData(GL_ARRAY_BUFFER, len(colors) * 4, (c_float * len(colors))(*colors), GL_STATIC_DRAW)

	def checkCollision(self, world, delta):
		for point in self.faceMesh:
			if world.checkCollision(self.position + point + delta):
				return True
		return False

	def draw(self):
		glPushMatrix()
		glTranslatef(self.position.x, self.position.y, self.position.z)
		glRotatef(self.rotation.y, 0, 1, 0)
		glBindTexture(GL_TEXTURE_2D, self.texture)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo[0])
		glVertexPointer(3, GL_FLOAT, 0, None)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo[1])
		glTexCoordPointer(2, GL_FLOAT, 0, None)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo[2])
		glColorPointer(3, GL_FLOAT, 0, None)
		glDrawArrays(GL_QUADS, 0, 4 * 12)
		glPopMatrix()

	def update(self, world):
		toPlayer = Vec3(
			world.player.position.x - self.position.x,
			world.player.position.y - self.position.y,
			world.player.position.z - self.position.z
		)
		if toPlayer.z == 0:
			self.rotation.y = 0
		else:
			self.rotation.y = math.atan(toPlayer.x / toPlayer.z) * 180 / 3.14

		dist = abs(toPlayer.x) + abs(toPlayer.y)
		toPlayer = toPlayer.unit()

		if random.randint(0, 50) == 0 and self.grounded:
			self.velocity.x += random.randint(0, 10) / 100 * toPlayer.x
			self.velocity.y += random.randint(10, 20) / 100
			self.velocity.z += random.randint(0, 10) / 100 * toPlayer.z
			assets.squish.set_volume(1 / (dist * dist))
			assets.squish.play()
			for i in range(5):
				world.visuals.append(
					Particle(
						Vec3(self.position.x, self.position.y - 0.4, self.position.z), 
						Vec3(random.randint(-1, 1), random.randint(2, 3), random.randint(-1, 1)) * 0.05,
						assets.slime
					)
				)

		self.velocity.y += gravity

		if self.checkCollision(world, Vec3(0, self.velocity.y, 0)):
			if self.velocity.y < 0:
				self.grounded = True
				self.velocity.x *= 0.4
				self.velocity.z *= 0.4
			self.velocity.y *= -0.2
		else:
			self.grounded = False
			self.position.y += self.velocity.y

		if self.checkCollision(world, Vec3(self.velocity.x, 0, 0)):
			pass
		else:
			self.position.x += self.velocity.x

		if self.checkCollision(world, Vec3(0, 0, self.velocity.z)):
			pass
		else:
			self.position.z += self.velocity.z