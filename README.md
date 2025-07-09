# Measure-Mesh
Contains functions and classes for loading, storing, and measuring 3d meshes.

## mmesh
Contains several functions related to acquiring certain measurements of a 3d mesh, namely its volume, surface area, and length on the x, y, and z axies.
The main function `measure_mesh(mesh, volume=False, area=False, length=False)` which takes a Mesh instance (see **mesh**) and calculates the requested properties.
The volume calculation assumes the shape is closed and does not intersect itself. If the shape is not closed or intersects itself, the algorithm's return value is not defined.
Shapes with multiple parts that do not touch do give accurate values.

If mmesh is run directly, it contains a main function which accepts a file path to an obj or stl file from the command line, or requests one if not provided, and prints the model's volume, surface area, and lengths in the x, y, and z axies.

## vector3
Contains a simple class for storing vectors in 3d space called `Vector3`.
The class is an iterable and iterates over its components.
### Vector3
#### Properties
`x`
	Contains the x axis component.
`y`
	Contains the y axis component.
`z`
	Contains the z axis component.
#### Methods
`__init__(self, x, y = None, z = None)`
	Takes x, y, and z values to populate the instance.
	Can take three int or float arguments as separate values. Can also take a single list or dictionary argument containing all three values.

`+` operator
	Alias for the `add` method.

`-` operator
	Alias for the `subtract` method.

`*` operator
	Alias for the `scale` method. Can be used with the Vector3 instance on the right or left of the operator.

`add(vector1, vector2)`
	`vector1` and `vector2` must be instances of Vector3.
	Returns a Vector3 instance that is the sum of the provided vectors.

`copy(vector)`
	`vector` must be an instance of Vector3.
	Creates and returns a copy of the given vector.

`cross(vector1, vector2)`
	`vector1` and `vector2` must be instances of Vector3.
	Computes and returns the cross product of two vectors.

`dot(vector1, vector2)`
	`vector1` and `vector2` must be instances of Vector3.
	Computes and returns the dot product of two vectors.

`equals(vector1, vector2, abs_diff=0, rel_diff=0)`
	`vector1` and `vector2` must be instances of Vector3.
	`abs_diff` and `rel_diff` must be positive real numbers.
	Determines if the two vectors are equal.
	If `abs_diff` is set, determines a maximum absolute difference between each of the components for the vectors to be considered equal.
	If `rel_diff` is set, determines a maximum difference between each of the components for the vectors to be considered equal. This value is given as a coefficient to the average of the values for the two vectors for the given component.
	If both `abs_diff` and `rel_diff` are set, `equals` uses the larger difference.

`mag(vector)`
	An alias of `magnitude(vector)`

`magnitude(vector)`
	`vector` must be an instance of Vector3.
	Computes returns the magnitude of the given vector.
	The magnitude is also cached and only recomputed if one of the components changes.

`norm(vector)`
	`vector` must be an instance of Vector3.
	Computes and returns the norm of the given vector.
	The norm is also cached and only recomputed if one of the components changes.

`scale(vector, scale_factor)`
	`vector` must be an instance of Vector3.
	`scale_factor` must be a real number.
	Returns a version of the given vector that is multiplied by the given scalar.

`subtract(vector1, vector2)`
	`vector1` and `vector2` must be instances of Vector3.
	Returns a Vector3 instance that is the difference of the provided vectors.

`to_dict(vector)`
	`vector` must be an instance of Vector3.
	Converts the given vector to a dictionary.

`to_list(vector)`
	`vector` must be an instance of Vector3.
	Converts the given vector to a list.

## mesh
Contains several classes for storing 3d meshes. 
All included classes and methods include docstrings.
Most operations should only use `Mesh` class `MeshFacet` class and their child classes `MeshPFV`, `MeshIV`, `MeshFacetPFV`, and `MeshFacetIV`.
`Mesh` and `MeshFacet` define the generic properties and methods that all meshes or mesh facets have while their children implement some of these in differing ways.
The "PFV", or "Per Face Values" classes store the coordinates of the vertices as instances of Vector3 in each face while the "IV", or "Indexed Values", store the vertices as integer indexes in each face which reference a list of instances of Vector3 in the parent mesh.
The IV classes occasionally need to compare vectors to determine if it can resuse an index. A tolerance value is stored at `MeshFacetIV.vertex_error_match` which is used as the `rel_diff` argument when comparing vectors using the `equals` method. This value defaults to 0.0001.

The `Mesh` and `MeshFacet` classes are as follows.
### Mesh
`Mesh` has dedicated iterable that it automatically uses when iterating and iterates over its facets.
`Mesh` is compatible with the `len()` function and returns the number of facets in the mesh.
#### Properties
`facets`
	The facets of the mesh as a list of instances of MeshFacet (or a child class).

#### Methods
`__init__(self, facets=None, meta={})`
	`facets` is the mesh's facets a list of instances of MeshFacet.
	`meta` is a dictionary containing arbitrary data related to the mesh.
	Creates an instance of `Mesh`
	`MeshIV` adds an additional argument to this method. (`__init__(self, facets=[], meta={}, vertices=[])`)
	`vertices` is an initial list of vertices to store in the mesh. Required if `facets` uses instances of `MeshFacetIV`.

`add_facet(self, new_facet, facet_ind=None)`
	Inserts the facet given by `new_facet` at the given index, `facet_ind`. If the index is omitted, adds it to the end.
	Supports negative indexes which index from the end of the list of facets.

`facet(self, facet_ind, value=None)`
	Fetches a single facet referred to by its index, `facet_ind`, as a MeshFacet.
	If `value` is not omited or None, sets the facet to the new value before returning.

`remove_facet(self, facet_ind=-1)`
	Removes the facet at the given index. If the index is omitted, removes the last facet.
	Supports negative indexes which index from the end of the list of facets.

### MeshFacet
`MeshFacet` has dedicated iterable that it automatically uses when iterating and iterates over its vertices.
`MeshFacet` is compatible with the `len()` function and returns the number of vertices in the facet.
#### Properties
`normal`
	The normal vector of the facet as a Vector3.

`mesh`
	The facet's parent mesh. May not be set.

`vertices`
	The vertices of the facet as a list of instances of Vector3.
### Methods
`add_vertex(self, vertex, ind=None)`
	Adds the vertex to the facet at the given index. If the index is omitted, adds the vertex to the end.
	`vertex` must be a Vector3 specifying the vertex's position.

`copy(self)`
	Creates a copy of the facet.
	`MeshFacetIV` adds an additional argument to this method. (`copy(self, mesh=None)`)
	If `mesh` is provided, updates the facet copy's mesh and vertices to reference the new mesh.

`convert(unknown_facet)`
	Converts a facet which descends from MeshFacet but is of an arbitrary child class to the current child class.
	`MeshFacetIV` adds an additional argument to this method. (`convert(unknown_facet, mesh=None)`)
	If `mesh` is included, the returned facet uses it instead of the initial facet's parent mesh.

`data(self, data_key=None, value=None)`
	If `data_key` is omitted or None, fetches the facet's arbitary data as a dictionary.
	Otherwise, fetches the arbitrary data value asociated with the vertex with the given key `data_key`.
	If `value` is not omited or None, sets fetched value before fetching.

`remove_vertex(self, vertex_ind=None)`
	Removes the vertex whose index is specified by `vertex_ind` from the facet.
	Returns the removed vertex as a Vector3.

`swap_mesh(self, mesh)`
	Only appears in `MeshFacetIV`.
	Re-indexes the facet's vertices to the new mesh, adding additional entries to the mesh if needed, and returns itself.
	Also updates the facet's `mesh` property to the given mesh.

`vertex(self, vertex_ind, value=None)`
	Fetches the vertex with index `vertex_ind` as a Vector3..
	If `value` is not omited or None, sets the vertex to the new value before returning.

## parse_stl
Contains a handful of functions which are able to read and parse an stl file.
The main three methods are `parse_stl`, `parse_bin_stl`, and `parse_txt_stl`.
`parse_bin_stl` and `parse_txt_stl` take filepath string to a binary or text stl file respectively as an argument and parses the file before returning a `MeshPFV` instance containing the data. The `meta` property includes the file format, whether the file is text or binary, and, in the case of binary files, the header bytes.
`parse_stl` takes a filepath string to any stl file and determines if the file is in text ot binary format before returning the output of the respectively method.

## parse_obj
Contains a single method, `parse_obj`, which takes a filepath string as an argument and parses the file before returning a `MeshIV` instance containing the data.
The `meta` property contains any tags whose data is not otherwise stored in the `MeshIV` class.
Any color data following the end of a vertex is stored under `.mesh['color_data']` in the order they appear as lists of numbers.
Texture Coordiante tags are stored under `.meta['texture_coordinates']` as lists of numbers in the order they appear.
Vertex Normal tags are stored under `.meta['normals']` as instances of `Vector3` where applicable in the order they appear. Otherwise as lists of numbers.
Parameter Space Vertix tags are stored under `.meta['freeform_geometry']` as lists of numbers in the order they appear.
Line Element tags are stored under `.meta['lines']` as 0-based indexes referencing the mesh's list of vertices.
Unknown tags are stored under `.meta['other_tags']['<tag>']` as lists of strings.