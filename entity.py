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

class Button(object):
	def __init__(self, position, text, underlined = False):
		self.position = position
		self.text = text
		surface = pygame.Surface((512, 512))
		assets.fontBig.set_underline(underlined)
		surface.blit(assets.fontBig.render(text, True, (252, 236, 199)), (0, 200))
		self.texture = assets.toTexture(surface)
		self.hover = False

	def update(self):
		mouse = pygame.mouse.get_pos()
		if (abs(mouse[0] + 70 - self.position.x) < 150 and
			abs(mouse[1] + 15 - self.position.y) < 30):
			self.hover = True
			if pygame.mouse.get_pressed()[0]:
				return True
		else:
			self.hover = False

		return False

	def draw(self):
		#draw menu
		glPushMatrix()
		glTranslatef(
			-2.52 / 2 + self.position.x * 2.52 / 1080,
			1.4 / 2 - self.position.y * 1.4 / 600,
			-1)
		glScale(1, 1, 1)
		glBindTexture(GL_TEXTURE_2D, self.texture)
		glBindBuffer(GL_ARRAY_BUFFER, assets.entityVBO[0])
		glVertexPointer(3, GL_FLOAT, 0, None)
		glBindBuffer(GL_ARRAY_BUFFER, assets.entityVBO[1])
		glTexCoordPointer(2, GL_FLOAT, 0, None)
		glBindBuffer(GL_ARRAY_BUFFER, assets.entityVBO[2])
		glColorPointer(3, GL_FLOAT, 0, None)
		glDrawArrays(GL_QUADS, 0, 4 * 12)

		if self.hover:
			glBindTexture(GL_TEXTURE_2D, assets.highlight)
			glBindBuffer(GL_ARRAY_BUFFER, assets.entityVBO[0])
			glVertexPointer(3, GL_FLOAT, 0, None)
			glBindBuffer(GL_ARRAY_BUFFER, assets.entityVBO[1])
			glTexCoordPointer(2, GL_FLOAT, 0, None)
			glBindBuffer(GL_ARRAY_BUFFER, assets.entityVBO[2])
			glColorPointer(3, GL_FLOAT, 0, None)
			glDrawArrays(GL_QUADS, 0, 4 * 12)

		glPopMatrix()


class Item(object):
	def __init__(self):
		pass

	def update(self, use):
		pass

class PlasmaRifle(Item):
	def __init__(self):
		super().__init__()
		self.firing = False
		self.itemTexture = assets.plasmaRiflePickup

	def update(self, world, user, using):
		if using:
			if not self.firing:
				self.firing = True

				#calculate direction player is looking
				lookDir = Vec3(
					math.sin(user.rotation.y * 3.14 / 180) * math.cos(user.rotation.x * 3.14 / 180),
					-math.sin(user.rotation.x * 3.14 / 180),
					-math.cos(user.rotation.y * 3.14 / 180) * math.cos(user.rotation.x * 3.14 / 180))

				#create a bullet
				world.visuals.append(Bullet(
					Vec3(user.position.x, user.position.y + 0.3, user.position.z) + lookDir,
					lookDir * 0.5, 0.4
				))
				assets.bang.set_volume(assets.volume / 3)
				assets.bang.play()
				world.player.shake.y += 3
				world.player.shake.x += 2
		else:
			self.firing = False

	def draw(self, shake):
		glPushMatrix()
		glTranslatef(1.1 + shake.x / 16, -0.4 + shake.y / 16, -1.2)
		glBindTexture(GL_TEXTURE_2D, assets.plasmaRifle)
		glBindBuffer(GL_ARRAY_BUFFER, assets.entityVBO[0])
		glVertexPointer(3, GL_FLOAT, 0, None)
		glBindBuffer(GL_ARRAY_BUFFER, assets.entityVBO[1])
		glTexCoordPointer(2, GL_FLOAT, 0, None)
		glBindBuffer(GL_ARRAY_BUFFER, assets.entityVBO[2])
		glColorPointer(3, GL_FLOAT, 0, None)
		glDrawArrays(GL_QUADS, 0, 4 * 12)
		glPopMatrix()


class PlasmaSMG(Item):
	def __init__(self):
		super().__init__()
		self.itemTexture = assets.plasmaSMGPickup
		self.firing = 0

	def update(self, world, user, using):
		if using:
			if self.firing <= 0:
				self.firing = 3

				#calculate direction player is looking
				lookDir = Vec3(
					math.sin(user.rotation.y * 3.14 / 180) * math.cos(user.rotation.x * 3.14 / 180),
					-math.sin(user.rotation.x * 3.14 / 180),
					-math.cos(user.rotation.y * 3.14 / 180) * math.cos(user.rotation.x * 3.14 / 180))

				#create a bullet
				world.visuals.append(Bullet(
					Vec3(user.position.x, user.position.y + 0.3, user.position.z) + lookDir,
					lookDir * 0.5, 0.4
				))
				assets.bang.set_volume(assets.volume / 3)
				assets.bang.play()
				world.player.shake.y += 2
				world.player.shake.x += 1.5
			else:
				self.firing -= 1
		else:
			self.firing = 0

	def draw(self, shake):
		glPushMatrix()
		glTranslatef(1.1 + shake.x / 16, -0.4 + shake.y / 16, -1.2)
		glBindTexture(GL_TEXTURE_2D, assets.plasmaSMG)
		glBindBuffer(GL_ARRAY_BUFFER, assets.entityVBO[0])
		glVertexPointer(3, GL_FLOAT, 0, None)
		glBindBuffer(GL_ARRAY_BUFFER, assets.entityVBO[1])
		glTexCoordPointer(2, GL_FLOAT, 0, None)
		glBindBuffer(GL_ARRAY_BUFFER, assets.entityVBO[2])
		glColorPointer(3, GL_FLOAT, 0, None)
		glDrawArrays(GL_QUADS, 0, 4 * 12)
		glPopMatrix()


class PlasmaShotgun(Item):
	def __init__(self):
		super().__init__()
		self.itemTexture = assets.plasmaShotgunPickup
		self.firing = 0

	def update(self, world, user, using):
		if self.firing <= 0:
			if using:
				self.firing = 40

				for i in range(4):
					rotY = user.rotation.y + random.randint(-5, 5)
					rotX = user.rotation.x + random.randint(-5, 5)

					#calculate direction player is looking
					lookDir = Vec3(
						math.sin(rotY* 3.14 / 180) * math.cos(rotX * 3.14 / 180),
						-math.sin(rotX * 3.14 / 180),
						-math.cos(rotY * 3.14 / 180) * math.cos(rotX * 3.14 / 180))

					#create a bullet
					world.visuals.append(Bullet(
						Vec3(user.position.x, user.position.y + 0.3, user.position.z) + lookDir,
						lookDir * 0.5, 2.5
					))
				assets.bang.set_volume(assets.volume / 3)
				assets.bang.play()
				world.player.shake.y += 3
				world.player.shake.x += 2
		else:
			if self.firing == 30:
				assets.collect.play(1)
			self.firing = max(0, self.firing - 1)

	def draw(self, shake):
		glPushMatrix()
		glTranslatef(1.1 + shake.x / 16, -0.4 + shake.y / 16, -1.2)
		glBindTexture(GL_TEXTURE_2D, assets.plasmaShotgun)
		glBindBuffer(GL_ARRAY_BUFFER, assets.entityVBO[0])
		glVertexPointer(3, GL_FLOAT, 0, None)
		glBindBuffer(GL_ARRAY_BUFFER, assets.entityVBO[1])
		glTexCoordPointer(2, GL_FLOAT, 0, None)
		glBindBuffer(GL_ARRAY_BUFFER, assets.entityVBO[2])
		glColorPointer(3, GL_FLOAT, 0, None)
		glDrawArrays(GL_QUADS, 0, 4 * 12)
		glPopMatrix()


class Entity(object):
	def __init__(self, position):
		self.position = position

	def update(self, world):
		pass

	def draw(self):
		pass


class Pickup(Entity):
	def __init__(self, position, item):
		super().__init__(position)
		self.texture = item.itemTexture
		self.item = item
		self.rotation = Vec3(0, 0, 0)
		self.yVel = 0.01
		self.centerPos = position.y
		self.vbo = assets.entityVBO
		self.hover = False
		self.timer = 60

	def update(self, world):
		#point towards player
		toPlayer = Vec3(
			world.player.position.x - self.position.x,
			world.player.position.y - self.position.y,
			world.player.position.z - self.position.z
		)
		if toPlayer.z == 0:
			self.rotation.y = 0
		else:
			self.rotation.y = math.atan(toPlayer.x / toPlayer.z) * 180 / 3.14
			if toPlayer.z < 0:
				self.rotation.y += 180

		#hover effect
		self.position.y += self.yVel
		self.yVel += (self.centerPos - self.position.y) * 0.005

		#check if collected
		if self.timer > 0:
			self.timer -= 1
		elif (abs(self.position.x - world.player.position.x) < 2 and
			abs(self.position.y - world.player.position.y) < 2 and
			abs(self.position.z - world.player.position.z) < 2):
			self.hover = True
			if world.player.collecting:
				if world.player.item != None:
					world.visuals.append(Pickup(world.player.position * 1, world.player.item))
				world.player.item = self.item
				world.player.collecting = False
				assets.collect.set_volume(assets.volume / 3)
				assets.collect.play()
				return True
		else:
			self.hover = False

	def draw(self):
		#create and use model matrix
		glPushMatrix()
		glTranslatef(self.position.x, self.position.y, self.position.z)
		glRotatef(self.rotation.y, 0, 1, 0)
		
		#draw
		glBindTexture(GL_TEXTURE_2D, self.texture)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo[0])
		glVertexPointer(3, GL_FLOAT, 0, None)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo[1])
		glTexCoordPointer(2, GL_FLOAT, 0, None)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo[2])
		glColorPointer(3, GL_FLOAT, 0, None)
		glDrawArrays(GL_QUADS, 0, 4 * 12)

		#draw notification
		if self.hover:
			glTranslatef(0, 0.7, 0)
			glBindTexture(GL_TEXTURE_2D, assets.notification)
			glBindBuffer(GL_ARRAY_BUFFER, assets.entityVBO[0])
			glVertexPointer(3, GL_FLOAT, 0, None)
			glBindBuffer(GL_ARRAY_BUFFER, assets.entityVBO[1])
			glTexCoordPointer(2, GL_FLOAT, 0, None)
			glBindBuffer(GL_ARRAY_BUFFER, assets.entityVBO[2])
			glColorPointer(3, GL_FLOAT, 0, None)
			glDrawArrays(GL_QUADS, 0, 4 * 12)

		glPopMatrix()


class Player(Entity):
	def __init__(self, position, rotation):
		super().__init__(position)
		self.rotation = rotation
		self.velocity = Vec3(0, 0, 0)
		self.grounded = False
		rad = Vec3(0.25, 0.45, 0.25)
		self.rad = rad
		self.health = 10
		self.collecting = False
		self.shake = Vec2(0, 0)

		#create bounding box of points
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
		self.item = None
		self.keys = []

	def checkCollision(self, world, delta):
		for point in self.faceMesh:
			if world.checkCollision(self.position + point + delta):
				return True
		return False

	def control(self, world, keys, display):
		pygame.mouse.set_visible(False)
		deltaPos = Vec3(0, 0, 0)
		deltaRot = Vec3(0, 0, 0)

		#keyboard input
		if keys[K_w]:
			deltaPos.z += 1
		elif keys[K_s]:
			deltaPos.z -= 1
		if keys[K_d]:
			deltaPos.x += 1
		elif keys[K_a]:
			deltaPos.x -= 1

		#jump
		if keys[K_SPACE] and self.grounded:
			deltaPos.y += 1
		
		#mouse input
		deltaMouse = pygame.mouse.get_pos()
		deltaRot.y = deltaMouse[0] - display[0] // 2
		deltaRot.x = deltaMouse[1] - display[1] // 2
		pygame.mouse.set_pos(display[0] // 2, display[1] // 2)

		#update rotation
		self.rotation += deltaRot * 0.1 * ((assets.mouseSensativity + 1) / 2)
		self.rotation.x = max(min(self.rotation.x, 30), -30)
		dx = (deltaPos.x * math.cos(self.rotation.y * 3.14 / 180) + deltaPos.z * math.sin(self.rotation.y * 3.14 / 180)) * 0.1
		dz = (deltaPos.x * math.sin(self.rotation.y * 3.14 / 180) - deltaPos.z * math.cos(self.rotation.y * 3.14 / 180)) * 0.1

		#screen shake
		self.shake.x += -self.shake.x * 1.5
		self.shake.y += -self.shake.y * 1.5

		#update position
		self.velocity.y += gravity + deltaPos.y * 0.2

		#y position update
		if self.checkCollision(world, Vec3(0, self.velocity.y, 0)):
			if self.velocity.y < 0:
				self.grounded = True
			self.velocity.y *= -0.12
		else:
			self.grounded = False
			self.position.y += self.velocity.y

		#x position update
		if self.checkCollision(world, Vec3(dx, 0, 0)):
			if not self.checkCollision(world, Vec3(dx, 0.5, 0)) and self.grounded:
				self.position.y += 0.55
		else:
			self.position.x += dx

		#z position update
		if self.checkCollision(world, Vec3(0, 0, dz)):
			if not self.checkCollision(world, Vec3(0, 0.5, dz)) and self.grounded:
				self.position.y += 0.55
		else:
			self.position.z += dz

		#acid damage
		if self.position.y < 0.4:
			self.health -= 0.06
			assets.hit.set_volume(assets.volume / 3)
			assets.hit.play()
			#create particles
			for i in range(5):
				world.visuals.append(
					Particle(
						Vec3(self.position.x, self.position.y, self.position.z), 
						Vec3(random.randint(-1, 1), random.randint(2, 3), random.randint(-1, 1)) * 0.05,
						assets.slime
					)
				)

		#update player's items
		usingItem = False
		if pygame.mouse.get_pressed()[0]:
			usingItem = True
		if self.item != None:
			self.item.update(world, self, usingItem)

		#collecting items
		self.collecting = pygame.mouse.get_pressed()[2]



	def draw(self):
		#make 2d
		glPopMatrix()
		glDisable(GL_DEPTH_TEST)


		#draw crosshairs
		glPushMatrix()
		glTranslatef(0, 0, -12)
		glBindTexture(GL_TEXTURE_2D, assets.crosshairs)
		glBindBuffer(GL_ARRAY_BUFFER, assets.entityVBO[0])
		glVertexPointer(3, GL_FLOAT, 0, None)
		glBindBuffer(GL_ARRAY_BUFFER, assets.entityVBO[1])
		glTexCoordPointer(2, GL_FLOAT, 0, None)
		glBindBuffer(GL_ARRAY_BUFFER, assets.entityVBO[2])
		glColorPointer(3, GL_FLOAT, 0, None)
		glDrawArrays(GL_QUADS, 0, 4 * 12)
		glPopMatrix()

		#draw keys
		offset = 0
		for key in self.keys:
			glPushMatrix()
			glTranslatef(9.8 + offset, 4.5, -8)
			glBindTexture(GL_TEXTURE_2D, key.texture)
			glBindBuffer(GL_ARRAY_BUFFER, key.vbo[0])
			glVertexPointer(3, GL_FLOAT, 0, None)
			glBindBuffer(GL_ARRAY_BUFFER, key.vbo[1])
			glTexCoordPointer(2, GL_FLOAT, 0, None)
			glBindBuffer(GL_ARRAY_BUFFER, key.vbo[2])
			glColorPointer(3, GL_FLOAT, 0, None)
			glDrawArrays(GL_QUADS, 0, 4 * 12)
			glPopMatrix()
			offset -= 0.2

		#draw health
		glPushMatrix()
		glTranslatef(0, -4, -6)
		glScale(5.1, 1, 1)
		glBindTexture(GL_TEXTURE_2D, assets.bar)
		glBindBuffer(GL_ARRAY_BUFFER, assets.entityVBO[0])
		glVertexPointer(3, GL_FLOAT, 0, None)
		glBindBuffer(GL_ARRAY_BUFFER, assets.entityVBO[1])
		glTexCoordPointer(2, GL_FLOAT, 0, None)
		glBindBuffer(GL_ARRAY_BUFFER, assets.entityVBO[2])
		glColorPointer(3, GL_FLOAT, 0, None)
		glDrawArrays(GL_QUADS, 0, 4 * 12)
		glPopMatrix()

		glPushMatrix()
		glTranslatef((self.health - 10) / 4, -4, -6)
		glScale(self.health / 2, 1, 1)
		glBindTexture(GL_TEXTURE_2D, assets.health)
		glBindBuffer(GL_ARRAY_BUFFER, assets.entityVBO[0])
		glVertexPointer(3, GL_FLOAT, 0, None)
		glBindBuffer(GL_ARRAY_BUFFER, assets.entityVBO[1])
		glTexCoordPointer(2, GL_FLOAT, 0, None)
		glBindBuffer(GL_ARRAY_BUFFER, assets.entityVBO[2])
		glColorPointer(3, GL_FLOAT, 0, None)
		glDrawArrays(GL_QUADS, 0, 4 * 12)
		glPopMatrix()

		if self.item != None:
			self.item.draw(self.shake)


class Particle(Entity):
	def __init__(self, position, velocity, texture, weight = 1):
		super().__init__(position)
		self.texture = texture
		self.velocity = velocity
		self.rotation = Vec3(0, 0, 0)
		self.vbo = assets.particleVBO
		self.weight = weight

	def draw(self):
		#create and use model matrix
		glPushMatrix()
		glTranslatef(self.position.x, self.position.y, self.position.z)
		glRotatef(self.rotation.y, 0, 1, 0)

		#draw
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
		#point towards player
		toPlayer = Vec3(
			world.player.position.x - self.position.x,
			world.player.position.y - self.position.y,
			world.player.position.z - self.position.z
		)
		if toPlayer.z == 0:
			self.rotation.y = 0
		else:
			self.rotation.y = math.atan(toPlayer.x / toPlayer.z) * 180 / 3.14
			if toPlayer.z < 0:
				self.rotation.y += 180

		#update y position
		if world.checkCollision(self.position + Vec3(0, self.velocity.y, 0)):
			self.velocity.y *= -0.2
			if abs(self.velocity.y) < 0.003:
				return True
		else:
			self.position.y += self.velocity.y

		self.velocity.y += gravity * self.weight

		#update x position
		if world.checkCollision(self.position + Vec3(self.velocity.x, 0, 0)):
			pass
		else:
			self.position.x += self.velocity.x

		#update z position
		if world.checkCollision(self.position + Vec3(0, 0, self.velocity.z)):
			pass
		else:
			self.position.z += self.velocity.z

class Door(Entity):
	def __init__(self, position, key, angled, entities):
		super().__init__(position)
		self.texture = assets.door
		self.downPos = position.y
		vertices = []
		self.rad = Vec3(0, 0, 0)
		self.key = key
		self.opening = False
		self.entities = entities

		#create model based upon if is rotated or not
		if angled:
			self.rad = Vec3(0.25, 6, 1)
			vertices = [
				#front
				0.25, 6, -1,
				0.25, 0, -1,
				0.25, 0, 1,
				0.25, 6, 1,
				#back
				-0.25, 6, -1,
				-0.25, 0, -1,
				-0.25, 0, 1,
				-0.25, 6, 1,
				#bottom
				-0.25, 0, -1,
				-0.25, 0, 1,
				0.25, 0, 1,
				0.25, 0, -1,
				#front key
				0.275, 2, -1,
				0.275, 0, -1,
				0.275, 0, 1,
				0.275, 2, 1,
				#back key
				-0.275, 2, -1,
				-0.275, 0, -1,
				-0.275, 0, 1,
				-0.275, 2, 1,
			]
		else:
			self.rad = Vec3(1, 6, 0.25)
			vertices = [
				#front
				-1, 6, 0.25,
				-1, 0, 0.25,
				1, 0, 0.25,
				1, 6, 0.25,
				#back
				-1, 6, -0.25,
				-1, 0, -0.25,
				1, 0, -0.25,
				1, 6, -0.25,
				#bottom
				-1, 0, -0.25,
				1, 0, -0.25,
				1, 0, 0.25,
				-1, 0, 0.25,
				#front key
				-1, 2, 0.275,
				-1, 0, 0.275,
				1, 0, 0.275,
				1, 2, 0.275,
				#back key
				-1, 2, -0.275,
				-1, 0, -0.275,
				1, 0, -0.275,
				1, 2, -0.275,
			]
		textureCoords = [
			#front
			0, 0.75,
			0, 0,
			1, 0,
			1, 0.75,
			#back
			0, 0.75,
			0, 0,
			1, 0,
			1, 0.75,
			#bottom
			1, 0.025,
			0, 0.025,
			0, 0,
			1, 0,
			#front key
			0, 1,
			0, 0.75,
			1, 0.75,
			1, 1,
			#back key
			0, 1,
			0, 0.75,
			1, 0.75,
			1, 1,
		]
		colors = [1] * 12 * 3
		colors += key.color * 8
		self.vbo = glGenBuffers(3)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo[0])
		glBufferData(GL_ARRAY_BUFFER, len(vertices) * 4, (c_float * len(vertices))(*vertices), GL_STATIC_DRAW)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo[1])
		glBufferData(GL_ARRAY_BUFFER, len(textureCoords) * 4, (c_float * len(textureCoords))(*textureCoords), GL_STATIC_DRAW)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo[2])
		glBufferData(GL_ARRAY_BUFFER, len(colors) * 4, (c_float * len(colors))(*colors), GL_STATIC_DRAW)

	def draw(self):
		#create and use model matrix
		glPushMatrix()
		glTranslatef(self.position.x, self.position.y, self.position.z)

		#draw
		glBindTexture(GL_TEXTURE_2D, self.texture)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo[0])
		glVertexPointer(3, GL_FLOAT, 0, None)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo[1])
		glTexCoordPointer(2, GL_FLOAT, 0, None)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo[2])
		glColorPointer(3, GL_FLOAT, 0, None)
		glDrawArrays(GL_QUADS, 0, 4 * 12)

		glPopMatrix()

	def checkCollision(self, point):
		return (
			abs(point.x - self.position.x) <= self.rad.x and
			point.y > self.position.y and
			abs(point.z - self.position.z) <= self.rad.z
		)

	def update(self, world):
		#stay open
		if self.opening:
			self.position.y = (self.downPos + 2 + self.position.y * 9) / 10
		#detect if should open
		elif (abs(self.position.x - world.player.position.x) < 2 and
		 	abs(self.position.z - world.player.position.z) < 2 and
		 	#make sure the player has the correct key
		 	self.key in world.player.keys):
			self.opening = True
			assets.doorOpen.set_volume(assets.volume / 3)
			assets.doorOpen.play()
			world.entities.extend(self.entities)

class Key(Entity):
	def __init__(self, position, color):
		super().__init__(position)
		self.texture = assets.key
		self.rotation = Vec3(0, 0, 0)
		self.yVel = 0.01
		self.centerPos = position.y
		self.color = color
		self.hover = False

		#create custom colored VBO
		vertices = [
			-0.5, 1, 0,
			-0.5, 0, 0,
			0.5, 0, 0,
			0.5, 1, 0
		]
		textureCoords = [
			0, 1,
			0, 0,
			1, 0,
			1, 1
		]
		colors = color * 4
		self.vbo = glGenBuffers(3)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo[0])
		glBufferData(GL_ARRAY_BUFFER, len(vertices) * 4, (c_float * len(vertices))(*vertices), GL_STATIC_DRAW)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo[1])
		glBufferData(GL_ARRAY_BUFFER, len(textureCoords) * 4, (c_float * len(textureCoords))(*textureCoords), GL_STATIC_DRAW)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo[2])
		glBufferData(GL_ARRAY_BUFFER, len(colors) * 4, (c_float * len(colors))(*colors), GL_STATIC_DRAW)

	def __eq__(self, other):
		return self.color == other.color

	def update(self, world):
		#point towards player
		toPlayer = Vec3(
			world.player.position.x - self.position.x,
			world.player.position.y - self.position.y,
			world.player.position.z - self.position.z
		)
		if toPlayer.z == 0:
			self.rotation.y = 0
		else:
			self.rotation.y = math.atan(toPlayer.x / toPlayer.z) * 180 / 3.14
			if toPlayer.z < 0:
				self.rotation.y += 180

		#hover effect
		self.position.y += self.yVel
		self.yVel += (self.centerPos - self.position.y) * 0.005

		#check if collected
		if (abs(self.position.x - world.player.position.x) < 2 and
			abs(self.position.y - world.player.position.y) < 2 and
			abs(self.position.z - world.player.position.z) < 2):
			self.hover = True
			if world.player.collecting:
				world.player.keys.append(self)
				assets.collect.set_volume(assets.volume / 3)
				assets.collect.play()
				return True
		else:
			self.hover = False

	def draw(self):
		#create and use model matrix
		glPushMatrix()
		glTranslatef(self.position.x, self.position.y, self.position.z)
		glRotatef(self.rotation.y, 0, 1, 0)
		
		#draw
		glBindTexture(GL_TEXTURE_2D, self.texture)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo[0])
		glVertexPointer(3, GL_FLOAT, 0, None)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo[1])
		glTexCoordPointer(2, GL_FLOAT, 0, None)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo[2])
		glColorPointer(3, GL_FLOAT, 0, None)
		glDrawArrays(GL_QUADS, 0, 4 * 12)

		#draw notification
		if self.hover:
			glTranslatef(0, 1.2, 0)
			glBindTexture(GL_TEXTURE_2D, assets.notification)
			glBindBuffer(GL_ARRAY_BUFFER, assets.entityVBO[0])
			glVertexPointer(3, GL_FLOAT, 0, None)
			glBindBuffer(GL_ARRAY_BUFFER, assets.entityVBO[1])
			glTexCoordPointer(2, GL_FLOAT, 0, None)
			glBindBuffer(GL_ARRAY_BUFFER, assets.entityVBO[2])
			glColorPointer(3, GL_FLOAT, 0, None)
			glDrawArrays(GL_QUADS, 0, 4 * 12)

		glPopMatrix()

class HealthPack(Entity):
	def __init__(self, position):
		super().__init__(position)
		self.texture = assets.healthPack
		self.rotation = Vec3(0, 0, 0)
		self.yVel = 0.01
		self.centerPos = position.y
		self.vbo = assets.entityVBO
		self.hover = False

	def update(self, world):
		#point towards player
		toPlayer = Vec3(
			world.player.position.x - self.position.x,
			world.player.position.y - self.position.y,
			world.player.position.z - self.position.z
		)
		if toPlayer.z == 0:
			self.rotation.y = 0
		else:
			self.rotation.y = math.atan(toPlayer.x / toPlayer.z) * 180 / 3.14
			if toPlayer.z < 0:
				self.rotation.y += 180

		#hover effect
		self.position.y += self.yVel
		self.yVel += (self.centerPos - self.position.y) * 0.005

		#check if collected
		if (abs(self.position.x - world.player.position.x) < 2 and
			abs(self.position.y - world.player.position.y) < 2 and
			abs(self.position.z - world.player.position.z) < 2):
			self.hover = True
			if world.player.collecting:
				world.player.health = min(10, world.player.health + 4)
				assets.collect.set_volume(assets.volume / 3)
				assets.collect.play()
				return True
		else:
			self.hover = False

	def draw(self):
		#create and use model matrix
		glPushMatrix()
		glTranslatef(self.position.x, self.position.y, self.position.z)
		glRotatef(self.rotation.y, 0, 1, 0)
		
		#draw
		glBindTexture(GL_TEXTURE_2D, self.texture)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo[0])
		glVertexPointer(3, GL_FLOAT, 0, None)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo[1])
		glTexCoordPointer(2, GL_FLOAT, 0, None)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo[2])
		glColorPointer(3, GL_FLOAT, 0, None)
		glDrawArrays(GL_QUADS, 0, 4 * 12)

		#draw notification
		if self.hover:
			glTranslatef(0, 0.7, 0)
			glBindTexture(GL_TEXTURE_2D, assets.notification)
			glBindBuffer(GL_ARRAY_BUFFER, assets.entityVBO[0])
			glVertexPointer(3, GL_FLOAT, 0, None)
			glBindBuffer(GL_ARRAY_BUFFER, assets.entityVBO[1])
			glTexCoordPointer(2, GL_FLOAT, 0, None)
			glBindBuffer(GL_ARRAY_BUFFER, assets.entityVBO[2])
			glColorPointer(3, GL_FLOAT, 0, None)
			glDrawArrays(GL_QUADS, 0, 4 * 12)

		glPopMatrix()

class Bullet(Entity):
	def __init__(self, position, velocity, damage):
		super().__init__(position)
		self.texture = assets.bullet
		self.velocity = velocity
		self.rotation = Vec3(0, 0, 0)
		self.vbo = assets.bulletVBO

	def draw(self):
		#create and use model matrix
		glPushMatrix()
		glTranslatef(self.position.x, self.position.y, self.position.z)
		glRotatef(self.rotation.y, 0, 1, 0)

		#draw
		glBindTexture(GL_TEXTURE_2D, self.texture)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo[0])
		glVertexPointer(3, GL_FLOAT, 0, None)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo[1])
		glTexCoordPointer(2, GL_FLOAT, 0, None)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo[2])
		glColorPointer(3, GL_FLOAT, 0, None)

		glDrawArrays(GL_QUADS, 0, 4 * 12)
		glPopMatrix()

	def explode(self, world, texture):
		for i in range(5):
			world.visuals.append(
				Particle(
					Vec3(self.position.x, self.position.y, self.position.z), 
					Vec3(random.randint(-1, 1), random.randint(2, 3), random.randint(-1, 1)) * 0.05 + 
					self.velocity * 0.3,
					texture
				)
			)

	def update(self, world):
		#point towards player
		toPlayer = Vec3(
			world.player.position.x - self.position.x,
			world.player.position.y - self.position.y,
			world.player.position.z - self.position.z
		)
		if toPlayer.z == 0:
			self.rotation.y = 0
		else:
			self.rotation.y = math.atan(toPlayer.x / toPlayer.z) * 180 / 3.14
			if toPlayer.z < 0:
				self.rotation.y += 180

		#occur in a loop to prevent object jumping
		for i in range(4):
			#check to see if it's hitting any entities
			for entity in world.entities:
				dist = Vec3(
					abs(self.position.x - entity.position.x),
					abs(self.position.y - entity.position.y),
					abs(self.position.z - entity.position.z)
				)
				if (dist.x < entity.rad.x and
					dist.y < entity.rad.y and
					dist.z < entity.rad.z):
					entity.velocity += self.velocity
					entity.health -= 4
					self.explode(world, assets.slime)
					return True

			#y position update
			if world.checkCollision(self.position + Vec3(0, self.velocity.y, 0)):
				self.explode(world, assets.bullet)
				return True
			else:
				self.position.y += self.velocity.y

			#x position update
			if world.checkCollision(self.position + Vec3(self.velocity.x, 0, 0)):
				self.explode(world, assets.bullet)
				return True
			else:
				self.position.x += self.velocity.x

			#z position update
			if world.checkCollision(self.position + Vec3(0, 0, self.velocity.z)):
				self.explode(world, assets.bullet)
				return True
			else:
				self.position.z += self.velocity.z


class Slime(Entity):
	def __init__(self, position):
		super().__init__(position)
		self.texture = assets.slime
		self.velocity = Vec3(0, 0, 0)
		self.grounded = False
		self.maxSpeed = 0.1
		self.rotation = Vec3(0, 0, 0)
		self.health = 10
		rad = Vec3(0.4, 0.5, 0.4)
		self.rad = rad

		#create bounding box of points
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
		self.vbo = assets.entityVBO

	def checkCollision(self, world, delta):
		for point in self.faceMesh:
			if world.checkCollision(self.position + point + delta):
				return True
		return False

	def draw(self):
		#create and use model matrix
		glPushMatrix()
		glTranslatef(self.position.x, self.position.y, self.position.z)
		glRotatef(self.rotation.y, 0, 1, 0)

		#draw
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
		#calculate direction to player
		toPlayer = Vec3(
			world.player.position.x - self.position.x,
			world.player.position.y - self.position.y,
			world.player.position.z - self.position.z
		)

		#point towards player
		if toPlayer.z == 0:
			self.rotation.y = 0
		else:
			self.rotation.y = math.atan(toPlayer.x / toPlayer.z) * 180 / 3.14
			if toPlayer.z < 0:
				self.rotation.y += 180

		dist = abs(toPlayer.x) + abs(toPlayer.z)
		toPlayer = toPlayer.unit()

		#jump towards player randomly
		if random.randint(0, (2 if assets.hard else 10)) == 0 and self.grounded:
			self.velocity.x += random.randint(0, 10) / (75 if assets.hard else 100) * toPlayer.x
			self.velocity.y += random.randint(10, 20) / 100
			self.velocity.z += random.randint(0, 10) / (75 if assets.hard else 100) * toPlayer.z
			if dist < 20:
				assets.squish.set_volume(assets.volume / 3.0 / dist)
				assets.squish.play()

				#create particles
				for i in range(5):
					world.visuals.append(
						Particle(
							Vec3(self.position.x, self.position.y - 0.4, self.position.z), 
							Vec3(random.randint(-1, 1), random.randint(2, 3), random.randint(-1, 1)) * 0.05,
							assets.slime
						)
					)

		#update position
		self.velocity.y += gravity

		#y position update
		if self.checkCollision(world, Vec3(0, self.velocity.y, 0)):
			if self.velocity.y < 0:
				self.grounded = True
				self.velocity.x *= 0.4
				self.velocity.z *= 0.4
			self.velocity.y *= -0.2
		else:
			self.grounded = False
			self.position.y += self.velocity.y

		#x position update
		if self.checkCollision(world, Vec3(self.velocity.x, 0, 0)):
			pass
		else:
			self.position.x += self.velocity.x

		#z position update
		if self.checkCollision(world, Vec3(0, 0, self.velocity.z)):
			pass
		else:
			self.position.z += self.velocity.z

		#check if hitting player
		if (abs(self.position.x - world.player.position.x) < 1 and
			abs(self.position.y - world.player.position.y) < 1 and
			abs(self.position.z - world.player.position.z) < 1):
			world.player.health -= 0.07
			assets.hit.set_volume(assets.volume)
			assets.hit.play()

		#check if dead
		if self.health <= 0:
			for i in range(15):
				world.visuals.append(
					Particle(
						Vec3(self.position.x, self.position.y, self.position.z), 
						Vec3(random.randint(-1, 1), random.randint(2, 3), random.randint(-1, 1)) * 0.05,
						assets.slime
					)
				)
			world.numEnemies -= 1
			return True


class Skull(Entity):
	def __init__(self, position):
		super().__init__(position)
		self.texture = assets.skull
		self.velocity = Vec3(0, 0, 0)
		self.maxSpeed = 0.1
		self.rotation = Vec3(0, 0, 0)
		self.health = 10
		rad = Vec3(0.4, 0.5, 0.4)
		self.rad = rad
		self.charging = False

		#create bounding box of points
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
		self.vbo = assets.entityVBO

	def checkCollision(self, world, delta):
		for point in self.faceMesh:
			if world.checkCollision(self.position + point + delta):
				return True
		return False

	def draw(self):
		#create and use model matrix
		glPushMatrix()
		glTranslatef(self.position.x, self.position.y, self.position.z)
		glRotatef(self.rotation.y, 0, 1, 0)

		#draw
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
		#calculate direction to player
		toPlayer = Vec3(
			world.player.position.x - self.position.x,
			world.player.position.y - self.position.y,
			world.player.position.z - self.position.z
		)

		#point towards player
		if toPlayer.z == 0:
			self.rotation.y = 0
		else:
			self.rotation.y = math.atan(toPlayer.x / toPlayer.z) * 180 / 3.14
			if toPlayer.z < 0:
				self.rotation.y += 180

		dist = abs(toPlayer.x) + abs(toPlayer.z)
		toPlayer = toPlayer.unit()

		#particle fountain
		if random.randint(0, 3) == 0 and dist < 30:
			world.visuals.append(
				Particle(
					Vec3(self.position.x, self.position.y - 0.4, self.position.z), 
					Vec3(random.randint(-1, 1) * 0.2, random.randint(0, 2) * 0.2, random.randint(-1, 1) * 0.2) * 0.05,
					assets.slime
				)
			)

		#charge player
		if random.randint(0, (90 if assets.hard else 120)) == 0 and not self.charging:
			self.charging = True
			self.velocity += toPlayer * (0.25 if assets.hard else 0.15)
			if dist < 30:
				assets.roar.set_volume(assets.volume * 3.5 / dist)
				assets.roar.play()

		#y position update
		if self.checkCollision(world, Vec3(0, self.velocity.y, 0)):
			self.charging = False
			self.velocity.y *= -0.2
		else:
			self.position.y += self.velocity.y

		#x position update
		if self.checkCollision(world, Vec3(self.velocity.x, 0, 0)):
			self.charging = False
			self.velocity.x *= -0.2
		else:
			self.position.x += self.velocity.x

		#z position update
		if self.checkCollision(world, Vec3(0, 0, self.velocity.z)):
			self.charging = False
			self.velocity.z *= -0.2
		else:
			self.position.z += self.velocity.z

		#check if hitting player
		if (abs(self.position.x - world.player.position.x) < 1 and
			abs(self.position.y - world.player.position.y) < 1 and
			abs(self.position.z - world.player.position.z) < 1):
			world.player.health -= 0.07
			assets.hit.set_volume(assets.volume)
			assets.hit.play()

		#check if dead
		if self.health <= 0:
			for i in range(15):
				world.visuals.append(
					Particle(
						Vec3(self.position.x, self.position.y, self.position.z), 
						Vec3(random.randint(-1, 1), random.randint(2, 3), random.randint(-1, 1)) * 0.05,
						assets.slime
					)
				)
			world.numEnemies -= 1
			return True