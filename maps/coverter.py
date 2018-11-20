import pygame
import random

level = pygame.image.load("map1.png")

size = [24, 12, 24]
heights = []

def toVal(r, g, b):
	if r == 255 and g == 255 and b == 255:
		return 6
	if r == 255 and g == 255:
		return 1
	if r == 255 and b == 255:
		return 8
	if r == 255:
		return 0
	if g == 255 and b == 255:
		return 6
	if g == 255:
		return random.randint(2, 5)
	if b == 255:
		return 7
	return 7

for x in range(size[0]):
	row = []
	for z in range(size[2]):
		row.append((-0.25, 15))
	heights.append(row)

for y in range(size[1]):
	for x in range(size[0]):
		for z in range(size[2]):
			imgX = x
			imgY = (11 - y) * size[2] + z
			pixel = level.get_at((imgX, imgY))
			if pixel.a == 255:
				heights[x][z] = (y / 2, toVal(pixel.r, pixel.g, pixel.b))

world = "World(Vec2(" + str(size[0]) + ", " + str(size[2]) + "), ["
for x in range(size[0]):
	world += "[\n"
	for z in range(size[2]):
		world += "Column" + str(heights[x][z]) + ", "
	world += "\n], "
world += "])"
open("map1.wad", "wt").write(str(world))