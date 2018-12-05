import math
from mathematics import *
import random
from ctypes import *
import pygame
from pygame.locals import *

import assets

from entity import *

from OpenGL.GL import *
from OpenGL.GLU import *

class Column(object):
	def __init__(self, height, texture):
		self.height = height
		self.texture = texture

	def __repr__(self):
		return "Column(" + str(self.height) + ", " + str(self.texture) + ")"

class World(object):
	def __init__(self, filename):

		self.multiplayer = True
 
		self.size, self.columns = eval(
			open("maps/" + filename + ".map", "rt").read()
		)

		self.numEnemies, self.visuals, self.doors, self.entities = eval(
			open("maps/" + filename + ".ent", "rt").read()
		)

		self.vbo = None
		self.tileset = assets.tileset
		self.toLight = Vec3(0.4, 1, 0.7).unit()
		self.player = Player(Vec3(1, 5, 11.5), Vec3(0, 0, 0))

	def __repr__(self):
		return "World(" + str(self.size) + ", " + str(self.columns) + ")"

	def calcNormal(self, face):
		p1 = face[0]
		p2 = face[1]
		p3 = face[2]
		U = Vec3(p2.x - p1.x, p2.y - p1.y, p2.z - p1.z)
		V = Vec3(p3.x - p1.x, p3.y - p1.y, p3.z - p1.z)
		
		normal = Vec3(0, 0, 0)
		normal.x = (U.y * V.z) - (U.z * V.y)
		normal.y = (U.z * V.x) - (U.x * V.z)
		normal.z = (U.x * V.y) - (U.y * V.x)
		
		return normal

	def calcShade(self, point, normal):
		light = (normal.dot(self.toLight) + 5) / 7.0
		step = self.toLight * 0.3
		for i in range(30):
			point += step
			if point.x < 0 or point.x >= self.size.x or point.z < 0 or point.z >= self.size.y:
				break
			if self.columns[int(point.x)][int(point.z)].height >= point.y:
				light *= 0.5
				break

		acid = max((4 - point.y) / 12, 0)

		return [light, light + acid, light]

	def randomize(self):
		for x in range(self.size.x):
			for y in range(self.size.y):
				if self.columns[x][y].texture == 0:
					self.columns[x][y].height += random.randint(0, 3) / 20

	def mesh(self, roof):
		self.randomize()
		vertices = []
		texCoords = []
		colors = []
		for x in range(self.size.x):
			for y in range(self.size.y):
				#top
				height = self.columns[x][y].height
				tex = self.columns[x][y].texture
				newVertices = (
					Vec3(x + 0.5, height, y + 0.5),
					Vec3(x + 0.5, height, y - 0.5),
					Vec3(x - 0.5, height, y - 0.5),
					Vec3(x - 0.5, height, y + 0.5),
				) 
				for vertex in newVertices: 
					vertices.extend(vertex.toList())
				texCoords.extend((
					(tex + 1) / 16, 1,
					tex / 16, 1,
					tex / 16, 7 / 8,
					(tex + 1) / 16, 7 / 8,
				))
				normal = self.calcNormal(newVertices)
				if height >= 0:
					for vertex in newVertices:
						colors.extend(self.calcShade(vertex, normal))
				else:
					colors.extend([1, 1.5, 1] * 4)
				#roof
				if roof:
					newVertices = (
						Vec3(x - 0.5, 5.5, y + 0.5),
						Vec3(x - 0.5, 5.5, y - 0.5),
						Vec3(x + 0.5, 5.5, y - 0.5),
						Vec3(x + 0.5, 5.5, y + 0.5),
					) 
					for vertex in newVertices: 
						vertices.extend(vertex.toList())
					texCoords.extend((
						15 / 16, 1,
						14 / 16, 1,
						14 / 16, 7 / 8,
						15 / 16, 7 / 8,
					))
					acid = max((1 - height) / 12, 0)
					colors.extend([0.3, 0.3 + acid, 0.3] * 4)
				#sides
				for side in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
					nx = x + side[0]
					ny = y + side[1]
					if (nx < 0 or nx >= self.size.x or ny < 0 or ny >= self.size.y):
						continue
					sideHeight = self.columns[nx][ny].height
					drop = sideHeight - height
					if drop >= 0:
						continue
					newVertices = (
						Vec3(x + side[1] / 2 + side[0] / 2, height, y - side[0] / 2 + side[1] / 2),
						Vec3(x - side[1] / 2 + side[0] / 2, height, y + side[0] / 2 + side[1] / 2),
						Vec3(x - side[1] / 2 + side[0] / 2, sideHeight, y + side[0] / 2 + side[1] / 2),
						Vec3(x + side[1] / 2 + side[0] / 2, sideHeight, y - side[0] / 2 + side[1] / 2)
					)
					for vertex in newVertices:
						vertices.extend(vertex.toList())
					texCoords.extend((
						(tex + 1) / 16, 7 / 8,
						tex / 16, 7 / 8,
						tex / 16, (7 + drop) / 8,
						(tex + 1) / 16, (7 + drop) / 8,
					))
					normal = self.calcNormal(newVertices)
					for vertex in newVertices:
						colors.extend(self.calcShade(vertex, normal))


		self.vbo = glGenBuffers(3)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo[0])
		glBufferData(GL_ARRAY_BUFFER, len(vertices) * 4, (c_float * len(vertices))(*vertices), GL_STATIC_DRAW)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo[1])
		glBufferData(GL_ARRAY_BUFFER, len(texCoords) * 4, (c_float * len(texCoords))(*texCoords), GL_STATIC_DRAW)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo[2])
		glBufferData(GL_ARRAY_BUFFER, len(colors) * 4, (c_float * len(colors))(*colors), GL_STATIC_DRAW)

	
	def draw(self):
		#create transformation matrix
		glEnable(GL_DEPTH_TEST)
		glPushMatrix()
		glRotatef(self.player.rotation.x + self.player.shake.y * 0.5, 1, 0, 0)
		glRotatef(self.player.rotation.y + self.player.shake.x * 0.5, 0, 1, 0)
		glTranslatef(-self.player.position.x, -self.player.position.y - 0.3, -self.player.position.z)

		#draw the level
		glBindTexture(GL_TEXTURE_2D, self.tileset)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo[0])
		glVertexPointer(3, GL_FLOAT, 0, None)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo[1])
		glTexCoordPointer(2, GL_FLOAT, 0, None)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo[2])
		glColorPointer(3, GL_FLOAT, 0, None)
		glDrawArrays(GL_QUADS, 0, self.size.x * self.size.y * 11)

		#draw entities
		for ent in range(len(self.entities) - 1, -1, -1):
			if self.entities[ent].update(self) == True:
				self.entities.pop(ent)
			else:
				self.entities[ent].draw()
		for ent in range(len(self.visuals) - 1, -1, -1):
			if self.visuals[ent].update(self) == True:
				self.visuals.pop(ent)
			else:
				self.visuals[ent].draw()
		for ent in range(len(self.doors) - 1, -1, -1):
			self.doors[ent].update(self)
			self.doors[ent].draw()

		#draw gui
		self.player.draw()

	def checkCollision(self, point):
		for door in self.doors:
			if door.checkCollision(point):
				return True
		point = Vec3(round(point.x), point.y, round(point.z))
		return (
			point.x < 0 or point.z < 0 or
			point.x >= self.size.x or point.z >= self.size.y or
			point.y >= 5.5 or
			self.columns[point.x][point.z].height > point.y
		)
