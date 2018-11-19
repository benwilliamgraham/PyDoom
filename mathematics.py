class Vec2(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __repr__(self):
		return("Vec2(" + str(self.x) + ", " + str(self.y) + ")")

	def __add__(self, other):
		return Vec2(self.x + other.x, self.y + other.y)

	def __sub__(self, other):
		return Vec2(self.x - other.x, self.y - other.y)

	def __mul__(self, const):
		return Vec2(self.x * const, self.y * const)

	def __div__(self, const):
		return Vec2(self.x / const, self.y / const)


class Vec3(object):
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

	def __repr__(self):
		return("Vec3(" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ")")

	def __add__(self, other):
		return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

	def __sub__(self, other):
		return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

	def __mul__(self, const):
		return Vec3(self.x * const, self.y * const, self.z * const)

	def __div__(self, const):
		return Vec3(self.x / const, self.y / const, self.z / const)

	def dot(self, other):
		return self.x * other.x + self.y * other.y + self.z * other.z

	def unit(self):
		magnitude = (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5
		return Vec3(self.x / magnitude, self.y / magnitude, self.z / magnitude)

	def toList(self):
		return [self.x, self.y, self.z]