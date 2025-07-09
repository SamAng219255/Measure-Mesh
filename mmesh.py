import sys
import math
from vector3 import Vector3
from mesh import MeshFacet, Mesh
from parse_stl import parse_stl
from parse_obj import parse_obj

def face_tetrahedron_volume(n, v1, v2, v3):
	"""Returns the volume of a tetrahedron whose vertices are at the origin, v1, v2, and v3.
	If the provided normal, `n`, of the face defined by v1, v2, and v3 is pointing towards the origin, the region is concave and subtracted instead."""
	concavity_sign = 1 if v1.dot(n) >= 0 else -1
	# Here, `concavity_sign` measures the 3d concavity of the face, representing a cutout/overhang in the total 3d model.
	return abs(v1.dot(v2.cross(v3)))/6 * concavity_sign

def face_pyramid_volume(face):
	"""Returns the volume of a pyramid whose base is defined by the given shape and whose tip is at the origin.
	If the face's normal is pointing towards the origin, the face represents a concave region and is negative."""
	if not isinstance(face, MeshFacet):
		raise TypeError('face_pyramid_volume: Argument must be an instance of MeshFacet.')
	mid_point = Vector3(0,0,0)
	vertex_count = len(face)
	if vertex_count <= 0:
		return 0
	for vertex in face:
		mid_point += vertex
	mid_point /= vertex_count
	vertices = face.vertices
	if vertex_count < 3:
		return 0
	elif vertex_count == 3:
		return face_tetrahedron_volume(face.normal, vertices[0], vertices[1], vertices[2])
	else:
		majority_concavity = 0
		volume = 0
		for v1, v2 in zip(vertices, vertices[1:] + [vertices[0]]):
			concavity_sign = 1 if (v1 - mid_point).cross(v2 - mid_point).dot(face.normal) >= 0 else -1
			# Here, `concavity_sign` measures the 2d concavity of the segment of the face, representing a cutout/overhang in the face's shape.
			majority_concavity += concavity_sign
			volume += face_tetrahedron_volume(face.normal, mid_point, v1, v2) * concavity_sign
		# If the majority of the face's segments were determined to be concave, the face's vertices were actually ordered in the wrong direction
		# and the concavity is inverted.
		if majority_concavity < 0:
			volume *= -1
		return volume

def triangle_area(p1, p2, p3):
	"""Returns the area of a triangle given by three points."""
	return (p2 - p1).cross(p3 - p1).mag()/2

def polygon_area(vertices):
	"""Returns the volume of a pyramid whose base is defined by the given shape and whose tip is at the origin.
	If the face's normal is pointing towards the origin, the face represents a concave region and is negative."""
	vertex_count = len(vertices)
	if vertex_count < 3:
		return 0
	elif vertex_count == 3:
		return triangle_area(vertices[0], vertices[1], vertices[2])
	else:
		for vertex in vertices:
			mid_point += vertex
		mid_point /= vertex_count

		majority_concavity = 0
		volume = 0
		for v1, v2 in zip(vertices, vertices[1:] + [vertices[0]]):
			concavity_sign = 1 if (v1 - mid_point).cross(v2 - mid_point).dot(mid_point) >= 0 else -1
			# Here, `concavity_sign` measures the 2d concavity of the segment of the face, representing a cutout/overhang in the face's shape.
			majority_concavity += concavity_sign
			area += triangle_area(mid_point, v1, v2) * concavity_sign
		# If the majority of the face's segments were determined to be concave, the face's vertices were actually ordered in the wrong direction
		# and the concavity is inverted.
		if majority_concavity < 0:
			area *= -1
		return area

def measure_mesh(mesh, volume=False, area=False, length=False):
	"""Iterates through the faces of a closed shape define by the given mesh and calculates the total volume, area, and/or lengths in the cardinal axies.
	Non-closed or self-intersecting shapes may give unexpected volumes."""
	if not isinstance(mesh, Mesh):
		raise TypeError('measure_mesh: Argument must be an instance of Mesh.')
	volume_total = 0
	area_total = 0
	minimums = {'x':math.inf,'y':math.inf,'z':math.inf}
	maximums = {'x':0,'y':0,'z':0}

	for face in mesh:
		if volume:
			volume_total += face_pyramid_volume(face)
		if area:
			area_total += polygon_area(face.vertices)
		if length:
			for vertex in face:
				for value, axis in vertex:
					if value < minimums[axis]:
						minimums[axis] = value
					if value > maximums[axis]:
						maximums[axis] = value

	if volume:
		mesh.meta['volume'] = abs(volume_total) # If all the normals were flipped, the volume would be negative but otherwise accurate.
	if area:
		mesh.meta['area'] = area_total
	if length:
		mesh.meta['x_length'] = maximums['x'] - minimums['x']
		mesh.meta['y_length'] = maximums['y'] - minimums['y']
		mesh.meta['z_length'] = maximums['z'] - minimums['z']

def display_round(x):
	"""Rounds `x` to two or more decimal places, such that it contains at least two more places than the 
	most significant digit and has a minimum of at least two decimal places."""
	min_decimal_count = max(0, -math.floor(math.log(x, 10)))
	return round(x, min_decimal_count + 2), min_decimal_count

def main(argc=0, argv=[]):
	"""
		Calculates and prints the volume, surface area, and z, y, and z lengths of a mesh contained within a user provided 3d model file.
		Currently supports .stl and .obj formats.
	"""

	# If a file path is passed with the program call, the program usses the passed value.
	# If not, the program requests a file path to find the model at.
	file_path = ''
	if argc > 1:
		file_path = argv[1]
	else:
		file_path = input('Please provide a valid mesh file (.stl or .obj): ')

	mesh = None
	while mesh is None:
		extension = file_path.split('.')[-1]
		if extension == 'stl':
			mesh = parse_stl(file_path)
		elif extension == 'obj':
			mesh = parse_obj(file_path)
		else:
			print('Invalid format.')
			if argc > 1:
				return
			else:
				file_path = input('Please provide a valid mesh file (.stl or .obj) or leave blank to close: ')
				if file_path.strip() == '':
					return

	measure_mesh(mesh, volume=True, area=True, length=True)

	volume, volume_mdc = display_round(mesh.meta['volume'])
	area, area_mdc = display_round(mesh.meta['area'])
	x_length, x_length_mdc = display_round(mesh.meta['x_length'])
	y_length, y_length_mdc = display_round(mesh.meta['y_length'])
	z_length, z_length_mdc = display_round(mesh.meta['z_length'])

	if volume_mdc < 2: 
		print(f'Volume: {volume:,.2f}')
	else:
		print(f'Volume: {volume:,f}')
	if area_mdc < 2: 
		print(f'Surface Area: {area:,.2f}')
	else:
		print(f'Surface Area: {area:,f}')
	if x_length_mdc < 2: 
		print(f'X Length: {x_length:,.2f}')
	else:
		print(f'X Length: {x_length:,f}')
	if y_length_mdc < 2: 
		print(f'Y Length: {y_length:,.2f}')
	else:
		print(f'Y Length: {y_length:,f}')
	if z_length_mdc < 2: 
		print(f'Z Length: {z_length:,.2f}')
	else:
		print(f'Z Length: {z_length:,f}')

if __name__ == '__main__':
	main(len(sys.argv), sys.argv)