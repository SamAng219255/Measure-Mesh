from vector3 import Vector3

class MeshFacet:
	"""A single facet from a mesh."""
	def __init__(self, vertices=[Vector3(0,0,0), Vector3(0,0,0), Vector3(0,0,0)], normal=Vector3(0,0,0), mesh=None, data={}):
		"""
		`vertices` is the facet's vertices as a list of instances of Vector3
		`normal` is the facet's normal as an instance of Vector3
		`mesh` is the facet's parent mesh as Mesh (may be None or omitted, unused by most versions of the class)
		`data` is a dictionary containing additional arbitrary data asociated with the facet
		"""
		self._vertices = vertices
		self._normal = normal
		self.mesh = mesh
		self._data = data

	def __iter__(self):
		return MeshFacetIter(self)
	def __len__(self):
		return len(self._vertices)

	@property
	def vertices(self):
		"""The vertices of the facet as a list of instances of Vector3."""
		return self._vertices
	@vertices.setter
	def vertices(self, new_value):
		"""The vertices of the facet as a list of instances of Vector3."""
		self._vertices = new_value

	@property
	def normal(self):
		"""The normal vector of the facet as a Vector3."""
		return self._normal
	@normal.setter
	def normal(self, new_value):
		"""The normal vector of the facet as a Vector3."""
		self._normal = new_value

	def data(self, data_key=None, value=None):
		"""
		If `data_key` is omitted or None, fetches the facet's arbitary data as a dictionary.
		Otherwise, fetches the arbitrary data value asociated with the vertex with the given key `data_key`.
		If `value` is not omited or None, sets fetched value before fetching.
		"""
		if data_key is None:
			if value is not None:
				self._data = value
			return self._data
		else:
			if value is not None:
				self._data[data_key] = value
			return self._data[data_key]

	def vertex(self, vertex_ind, value=None):
		"""Fetches the vertex with index `vertex_ind` as a Vector3..
		If `value` is not omited or None, sets the vertex to the new value before returning."""
		if value is not None:
			self.vertices[vertex_ind] = value
		return self.vertices[vertex_ind]

	def convert(unknown_facet):
		"""Converts a facet which descends from MeshFacet but is of an arbitrary child class to the current child class."""
		return MeshFacet(unknown_facet.vertices, unknown_facet.normal, unknown_facet.mesh, unknown_facet.data())

	def copy(self):
		"""Creates a copy of the facet."""
		return MeshFacet(self.vertices, self.normal, self.mesh, self.data())

	def add_vertex(self, vertex, ind=None):
		"""Adds the vertex to the facet at the given index. If the index is omitted, adds the vertex to the end.
		`vertex` must be a Vector3 specifying the vertex's position."""
		if ind is None:
			self._vertices.append(vertex)
		else:
			self._vertices.insert(vertex, ind)

	def remove_vertex(self, vertex_ind=None):
		"""Removes the vertex whose index is specified by `vertex_ind` from the facet.
		Returns the removed vertex as a Vector3."""
		self._vertices.pop(vertex_ind)
		

class Mesh:
	"""A 3d mesh with facets.
	Iterable over its facets."""
	def __init__(self, facets=None, meta={}):
		"""
		`facets` is the mesh's facets a list of instances of MeshFacet.
		`meta` is a dictionary containing arbitrary data related to the mesh.
		"""
		self._facets = facets
		self.meta = {}

	@property
	def facets(self):
		"""The facets of the mesh as a list of instances of MeshFacet."""
		return self._facets
	@facets.setter
	def facets(self, new_value):
		"""The facets of the mesh as a list of instances of MeshFacet."""
		self._facets = new_value

	def __iter__(self):
		return MeshIter(self)
	def __len__(self):
		return len(self._facets)

	def facet(self, facet_ind, value=None):
		"""Fetches a single facet referred to by its index, `facet_ind`, as a MeshFacet.
		If `value` is not omited or None, sets the facet to the new value before returning."""
		if value is not None:
			self._facets[facet_ind] = value
		return self._facets[facet_ind]

	def remove_facet(self, facet_ind=-1):
		"""Removes the facet at the given index. If the index is omitted, removes the last facet."""
		return self.facets.pop(facet_ind)

	def add_facet(self, new_facet, facet_ind=None):
		"""Inserts the facet given by `new_facet` at the given index, `facet_ind`. If the index is omitted, adds it to the end."""
		if facet_ind is None:
			return self.facets.append(new_facet)
		else:
			return self.facets.insert(facet_ind, new_facet)


class MeshFacetIter:
	"""An iterable class designated for iterating over the vertices of a mesh facet.
	Generates a series of FacetGetter instances."""
	def __init__(self, facet):
		self.facet = facet
		self.ind = 0

	def __iter__(self):
		return self

	def __next__(self):
		if self.ind >= len(self.facet):
			raise StopIteration
		ret = self.facet.vertex(self.ind)
		self.ind += 1
		return ret

class MeshIter:
	"""An iterable class designated for iterating over the facets of a mesh.
	Generates a series of FacetGetter instances."""
	def __init__(self, mesh):
		self.mesh = mesh
		self.ind = 0

	def __iter__(self):
		return self

	def __next__(self):
		if self.ind >= len(self.mesh):
			raise StopIteration
		ret = self.mesh.facet(self.ind)
		self.ind += 1
		return ret


class MeshFacetPFV(MeshFacet):
	"""A single facet from a mesh with a "Per Facet Vertex" format, meaning the vertices are stored as part of the facet like in an STL file."""

	def convert(unknown_facet):
		"""Converts a facet which descends from MeshFacet but is of an arbitrary child class to the current child class."""
		return MeshFacetPFV(unknown_facet.vertices, unknown_facet.normal, unknown_facet.mesh, unknown_facet.data())

class MeshPFV(Mesh):
	"""A 3d mesh with facets with a "Per Facet Vertex" format, meaning the vertices are stored as part of the facet like in an STL file.
	Iterable over its facets."""

	def __init__(self, facets=None, meta={}):
		"""
		`facets` is the mesh's facets a list of instances of MeshFacet.
		`meta` is a dictionary containing arbitrary data related to the mesh.
		"""
		converted_facets = []
		for facet in facets:
			if isinstance(facet, MeshFacetPFV):
				converted_facets.append(facet)
			else:
				converted_facets.append(MeshFacetPFV.convert(facet))
		self._facets = converted_facets
		self.meta = {}

	@property
	def facets(self):
		"""The facets of the mesh as a list of instances of MeshFacet."""
		return self._facets
	@facets.setter
	def facets(self, new_value):
		"""The facets of the mesh as a list of instances of MeshFacet."""
		self._facets = []
		for facet in new_value:
			if isinstance(facet, MeshFacetPFV):
				self._facets.append(facet)
			else:
				self._facets.append(MeshFacetPFV.convert(facet))

	def facet(self, facet_ind, new_value=None):
		"""Fetches a single facet referred to by its index, `facet_ind`, as a MeshFacet.
		If `value` is not omited or None, sets the facet to the new value before returning."""
		if new_value is not None:
			if isinstance(new_value, MeshFacetPFV):
				self._facets[facet_ind] = new_value
			else:
				self._facets[facet_ind] = MeshFacetPFV.convert(new_value)
		return self._facets[facet_ind]

	def add_facet(self, new_facet, facet_ind=None):
		"""Inserts the facet given by `new_facet` at the given index, `facet_ind`. If the index is omitted, adds it to the end."""
		if isinstance(new_facet, MeshFacetPFV):
			return super().add_facet(new_facet, facet_ind)
		return super().add_facet(MeshFacetPFV.convert(new_facet), facet_ind)

class MeshFacetIV(MeshFacet):
	"""A single facet from a mesh with an "Indexed Vertices" format, meaning the vertices are stored as part of the mesh and the vertices contain indexes to them like in an OBJ file."""

	vertex_error_match = 0.0001

	def __init__(self, vertices=[Vector3(0,0,0), Vector3(0,0,0), Vector3(0,0,0)], normal=Vector3(0,0,0), mesh=None, data={}):
		"""
		`vertices` is the facet's vertices as a list of positive integer indexes or a list of instances of Vector3.
			In the latter case, mesh must be specified.
		`normal` is the facet's normal as an instance of Vector3 or as a positive integer index.
		`mesh` is the facet's parent mesh as an instance of MeshIV
		`data` is a dictionary containing additional arbitrary data asociated with the facet
		"""
		self._normal = normal
		self.mesh = mesh
		self._data = data
		self.vertices = vertices

	@property
	def vertices(self):
		"""The vertices of the facet as a list of instances of Vector3."""
		vertices = []
		for i in range(len(self)):
			vertices.append(self.vertex(i))
		return vertices
	@vertices.setter
	def vertices(self, new_value):
		"""The vertices of the facet as a list of instances of Vector3."""
		self._vertices = []
		for vertex in new_value:
			if isinstance(vertex, Vector3):
				if self.mesh is None:
					raise ValueError("MeshFacetIV.vertices: No mesh provided. Vertices must be integer indexes.")
				self.add_vertex(vertex)
			elif type(vertex) is int:
				self._vertices.append(vertex)
			else:
				raise TypeError

	def vertex(self, vertex_ind, value=None):
		"""Fetches the vertex with index `vertex_ind` as a Vector3.
		If `value` is not omited or None, sets the vertex to the new value before returning."""
		if value is not None:
			if isinstance(value, Vector3):
				self.remove_vertex(vertex_ind)
				self.add_vertex(value, vertex_ind)
			elif type(value) is int:
				self._vertices[vertex_ind] = value
			else:
				raise TypeError
		return self.mesh.vertices[self._vertices[vertex_ind]]

	def convert(unknown_facet, mesh=None):
		"""Converts a facet which descends from MeshFacet but is of an arbitrary child class to the current child class."""
		if mesh is None:
			mesh = unknown_facet.mesh
		return MeshFacetIV(unknown_facet.vertices, unknown_facet.normal, mesh, unknown_facet.data())

	def copy(self, mesh=None):
		"""Creates a copy of the facet.
		If `mesh` is provided, updates the facet's mesh and vertices to reference the new mesh."""
		if mesh is None:
			return MeshFacetIV(self._vertices, self.normal, self.mesh, self.data())
		elif self.mesh is None:
			return MeshFacetIV(self._vertices, self.normal, mesh, self.data())
		else:
			return MeshFacetIV(self._vertices, self.normal, self.mesh, self.data()).swap_mesh(mesh)

	def add_vertex(self, vertex, ind=None):
		"""Adds the vertex to the facet at the given index. If the index is omitted, adds the vertex to the end.
		`vertex` must be a Vector3 specifying the vertex's position."""
		if self.mesh is None:
			raise AttributeError("MeshFacetIV.add_vertex: `mesh` must be defined!")
		match_found = False
		for new_ind in range(len(self.mesh.vertices)):
			if vertex.equals(self.mesh.vertices[new_ind], rel_diff=MeshFacetIV.vertex_error_match):
				match_found = True
				if ind is None:
					self._vertices.append(new_ind)
				else:
					self._vertices.insert(new_ind, ind)
				if self not in self.mesh.reverse_vertex_lookup[new_ind]:
					self.mesh.reverse_vertex_lookup[new_ind].append(self)
				break
		if not match_found:
			new_ind = len(self.mesh.vertices)
			if ind is None:
				self._vertices.append(new_ind)
			else:
				self._vertices.insert(new_ind, ind)
			self.mesh.vertices.append(vertex)
			self.mesh.reverse_vertex_lookup.append([self])

	def remove_vertex(self, vertex_ind=None):
		"""Removes the vertex whose index is specified by `vertex_ind` from the facet.
		Returns the removed vertex as a Vector3."""
		removed_vertex = self._vertices.pop(vertex_ind)
		removed_vertex_pos = self.mesh.vertices[removed_vertex]
		self.mesh.reverse_vertex_lookup[removed_vertex].remove(self)
		if len(self.mesh.reverse_vertex_lookup[removed_vertex]) < 1:
			self.mesh.reverse_vertex_lookup.pop(removed_vertex)
			self.mesh.vertices.pop(removed_vertex)
		return removed_vertex_pos

	def swap_mesh(self, mesh):
		old_vertices = self._vertices
		old_mesh = self.mesh
		self.vertices = []
		self.mesh = mesh
		for original_ind in old_vertices:
			self.add_vertex(old_mesh.vertices[original_ind])
		return self
		

class MeshIV(Mesh):
	"""A 3d mesh with facets with an "Indexed Vertices" format, meaning the vertices are stored as part of the mesh and the vertices contain indexes to them like in an OBJ file.
	Iterable over its facets."""
	def __init__(self, facets=[], meta={}, vertices=[]):
		"""
		`facets` is the mesh's facets a list of instances of MeshFacet.
		`meta` is a dictionary containing arbitrary data related to the mesh.
		"""
		self.vertices = vertices
		self.reverse_vertex_lookup = []
		for vertex in vertices:
			self.reverse_vertex_lookup.append([])
		self.meta = {}
		converted_facets = []
		for facet in facets:
			if isinstance(facet, MeshFacetIV):
				converted_facets.append(facet.copy(self))
			elif isinstance(facet, MeshFacet):
				converted_facets.append(MeshFacetIV.convert(facet, self))
			else:
				raise TypeError('MeshIV.__init__: First argument must be a list of instances of MeshFacet.')
		self._facets = converted_facets

	@property
	def facets(self):
		"""The facets of the mesh as a list of instances of MeshFacet."""
		return self._facets
	@facets.setter
	def facets(self, new_value):
		"""The facets of the mesh as a list of instances of MeshFacet."""
		self._facets = []
		for facet in new_value:
			if isinstance(facet, MeshFacetIV):
				self._facets.append(facet.copy(self))
			else:
				self._facets.append(MeshFacetIV.convert(facet, self))

	def facet(self, facet_ind, new_value=None):
		"""Fetches a single facet referred to by its index, `facet_ind`, as a MeshFacet.
		If `value` is not omited or None, sets the facet to the new value before returning."""
		if new_value is not None:
			if isinstance(new_value, MeshFacetIV):
				self._facets[facet_ind] = new_value.copy(self)
			else:
				self._facets[facet_ind] = MeshFacetIV.convert(new_value, self)
		return self._facets[facet_ind]

	def add_facet(self, new_facet, facet_ind=None):
		"""Inserts the facet given by `new_facet` at the given index, `facet_ind`. If the index is omitted, adds it to the end."""
		if isinstance(new_facet, MeshFacetIV):
			return super().add_facet(new_facet.copy(self), facet_ind)
		return super().add_facet(MeshFacetIV.convert(new_facet, self), facet_ind)