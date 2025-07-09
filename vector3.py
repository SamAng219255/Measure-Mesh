from math import sqrt, acos

class Vector3:
	"""A basic 3d vector class with math functions. The class is iterable over its components."""

	_mag = None
	_norm = None
	_str = None

	def __init__(self, x, y = None, z = None):
		"""Takes x, y, and z values to populate the instance.
		Can take three int or float arguments as separate values. Can also take a single list or dictionary argument containing all three values."""
		input_type = type(x)
		if input_type is int or input_type is float:
			if (type(y) is int or type(y) is float) and (type(z) is int or type(z) is float):
				self._x = x
				self._y = y
				self._z = z
			else:
				raise TypeError
		elif input_type is list:
			self._x = x[0]
			self._y = x[1]
			self._z = x[2]
		elif input_type is dict:
			self._x = x['x']
			self._y = x['y']
			self._z = x['z']
		else:
			raise TypeError

	def __iter__(self):
		self._ind = 0
		return self
	def __next__(self):
		self._ind += 1
		match self._ind:
			case 1:
				return (self.x, "x")
			case 2:
				return (self.y, "y")
			case 3:
				return (self.z, "z")
			case _:
				raise StopIteration
	def __len__(self):
		return 3

	def __str__(self):
		if self._str is None:
			self._str = '('
			first = True
			for component, _ in self:
				if first:
					first = False
				else:
					self._str += ', '
				self._str += f"{component:.2f}"
			self._str += ')'
		return self._str

	@property
	def x(self, ):
		return self._x
	@x.setter
	def x(self, newValue):
		self._mag = None
		self._norm = None
		self._str = None
		self._x = newValue
	@property
	def y(self, ):
		return self._y
	@y.setter
	def y(self, newValue):
		self._mag = None
		self._norm = None
		self._str = None
		self._y = newValue
	@property
	def z(self, ):
		return self._z
	@z.setter
	def z(self, newValue):
		self._mag = None
		self._norm = None
		self._str = None
		self._z = newValue

	def copy(self):
		return Vector3(self.x, self.y, self.z)

	def to_list(self):
		return [self.x, self.y, self.z]

	def to_dict(self):
		return {'x': self.x, 'y': self.y, 'z': self.z}

	def equals(vector1, vector2, abs_diff=0, rel_diff=0):
		if isinstance(vector1, Vector3) and isinstance(vector2, Vector3):
			return abs(vector1.x - vector2.x) <= max(abs_diff, rel_diff * vector1.x) and \
			       abs(vector1.y - vector2.y) <= max(abs_diff, rel_diff * vector1.y) and \
			       abs(vector1.z - vector2.z) <= max(abs_diff, rel_diff * vector1.z)
		return False

	def dot(vector1, vector2):
		total = 0
		for (component1, _), (component2, _) in zip(vector1, vector2):
			total += component1 * component2
		return total

	def cross(vector1, vector2):
		newX = vector1.y * vector2.z - vector1.z * vector2.y
		newY = vector1.z * vector2.x - vector1.x * vector2.z
		newZ = vector1.x * vector2.y - vector1.y * vector2.x
		return Vector3(newX, newY, newZ)

	def magnitude(vector):
		if vector._mag is None:
			total = 0
			for (component, _) in vector:
				total += component * component
			vector._mag = sqrt(total)
		return vector._mag
	def mag(vector):
		return vector.magnitude()

	def scale(vector, scale_factor):
		value_array = []
		for component, _ in vector:
			value_array.append(component * scale_factor)
		return Vector3(value_array)

	def add(vector1, vector2):
		value_array = []
		for (component1, _), (component2, _) in zip(vector1, vector2):
			value_array.append(component1 + component2)
		return Vector3(value_array)

	def subtract(vector1, vector2):
		value_array = []
		for (component1, _), (component2, _) in zip(vector1, vector2):
			value_array.append(component1 - component2)
		return Vector3(value_array)
	def sub(vector1, vector2):
		return vector1.subtract(vector2)

	def norm(vector):
		if vector._norm is None:
			mag = vector.mag()
			if mag == 0:
				vector._norm = Vector3(0,0,0)
			else:
				value_array = []
				for component, _ in vector:
					value_array.append(component / mag)
				vector._norm = Vector3(value_array)
		return vector._norm

	def copy(vector):
		new_vector = Vector3(self.x, self.y, self.z)
		if vector._mag is not None:
			new_vector._mag = vector._mag
		if vector._norm is not None:
			new_vector._norm = vector._norm.copy()
		if vector._str is not None:
			new_vector._str = vector._str
		return new_vector

	def __add__(self, other):
		if not isinstance(other, Vector3):
			raise TypeError
		return self.add(other)
	def __sub__(self, other):
		if not isinstance(other, Vector3):
			raise TypeError
		return self.sub(other)
	def __mul__(self, other):
		if not isinstance(other, int) and not isinstance(other, float):
			raise TypeError
		return self.scale(other)
	def __rmul__(self, other):
		return self * other
	def __truediv__(self, other):
		if not isinstance(other, int) and not isinstance(other, float):
			raise TypeError
		return self.scale(1/other)

	def angle_between(vector1, vector2):
		return acos(Vector3.dot(vector1.norm(), vector2.norm()))