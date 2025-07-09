import re
from vector3 import Vector3
from mesh import MeshFacetIV, MeshIV

def parse_obj(file_path):
	try:
		with open(file_path, 'rt') as fp:
			mesh = MeshIV()
			ptn_arg_split = re.compile(r'\s+')
			for line in fp:
				if line.endswith('\n'):
					line = line[:-1]
				entry = ptn_arg_split.split(line)
				if entry[-1] == '':
					entry.pop()
				arg_count = len(entry)
				if arg_count < 1: # Ignore blank lines
					continue
				match entry[0]:
					case 'v': # Vertex
						if arg_count < 4:
							raise IndexError("parse_obj: Too few vertex arguments in file. File may be malformed. Aborting parse.")
						# Vertex may be scaled by a fourth value
						scale = 1
						if arg_count >= 5:
							scale = float(entry[4])
						mesh.vertices.append(Vector3(float(entry[1]) / scale, float(entry[2]) / scale, float(entry[3]) / scale))
						# Some formats include vertex color data after the scale factor
						if arg_count > 5:
							if 'color_data' not in mesh.meta:
								mesh.meta['color_data'] = {}
							color_data = []
							for arg in entry[5:]:
								try:
									color_data.append(float(arg))
								except ValueError:
									color_data.append(arg)
							mesh.meta['color_data'][len(mesh.vertices) - 1] = color_data
					case 'vt': # Texture Coordinates
						if 'texture_coordinates' not in mesh.meta:
							mesh.meta['texture_coordinates'] = []
						txtr_coord = []
						for arg in entry[1:]:
							try:
								txtr_coord.append(float(arg))
							except ValueError:
								txtr_coord.append(arg)
						mesh.meta['texture_coordinates'].append(txtr_coord)
					case 'vn': # Vertex Normal
						if 'normals' not in mesh.meta:
							mesh.meta['normals'] = []
						normal = []
						errors = False
						for arg in entry[1:]:
							try:
								normal.append(float(arg))
							except ValueError:
								normal.append(arg)
								errors = True
						if len(normal) == 3 and not errors:
							normal = Vector3(normal)
						if len(normal) == 4 and not errors:
							normal = Vector3(normal[:3]) / normal[3]
						mesh.meta['normals'].append(normal)
					case 'vp': # Parameter Space Vertices
						if 'freeform_geometry' not in mesh.meta:
							mesh.meta['freeform_geometry'] = []
						ff_coord = []
						for arg in entry[1:]:
							try:
								ff_coord.append(float(arg))
							except ValueError:
								ff_coord.append(arg)
						mesh.meta['freeform_geometry'].append(ff_coord)
					case 'f': # Face
						vertex_ind = []
						texture_ind = []
						normal_ind = []
						for vertex in entry[1:]:
							indices = vertex.split('/')
							try:
								vertex_ind.append(int(indices[0]) - 1)
							except ValueError:
								try:
									vertex_ind.append(int(indices[0][1:]) - 1)
								except ValueError:
									raise ValueError('parse_obj: Invalid vertex format in face element. File may be malformed. Aborting parse.')
							ind_count = len(indices)
							if ind_count >= 2 and indices[1] != '':
								try:
									texture_ind.append(int(indices[1]) - 1)
								except ValueError:
									try:
										texture_ind.append(int(indices[1][2:]) - 1)
									except ValueError:
										texture_ind.append(None)
							else:
								texture_ind.append(None)
							if ind_count >= 3 and indices[2] != '':
								try:
									normal_ind.append(int(indices[2]) - 1)
								except ValueError:
									try:
										normal_ind.append(int(indices[2][2:]) - 1)
									except ValueError:
										normal_ind.append(None)
							else:
								normal_ind.append(None)
						data = {'texture': texture_ind, 'given_normal': normal_ind}
						mesh.add_facet(MeshFacetIV(vertex_ind, data = data))
						# Normal is calculated later after finished file read.
						# Mesh is not included to prevent vertex reassignment.
						#     (Vertex indices are treated as "floating", without an associated vector, and applied blindly.)
					case 'l': # Line Element
						if 'lines' not in mesh.meta:
							mesh.meta['lines'] = []
						new_line = []
						try:
							for vertex in entry[1:]:
								new_line.append(int(vertex[1:]) - 1)
							mesh.meta.append(new_line)
						except ValueError:
							mesh.meta.append(entry[1:])
					case _: # Store unknown miscellaneous data
						if 'other_tags' not in mesh.meta:
							mesh.meta['other_tags'] = {}
						if entry[0] in mesh.meta['other_tags']:
							mesh.meta['other_tags'][entry[0]].append(entry[1:])
						else:
							mesh.meta['other_tags'][entry[0]] = [entry[1:]]
		for facet in mesh:
			# Detect presence of provided normal value
			has_given_normal = False
			given_normal = Vector3(0,0,0)
			if 'normals' in mesh.meta:
				normal_count = len(mesh.meta['normals'])
				for normal in facet.data('given_normal'):
					if normal is not None and normal < normal_count and isinstance(mesh.meta['normals'][normal], Vector3):
						given_normal += mesh.meta['normals'][normal].norm()
						has_given_normal = True

			# Calculate normal from vertices
			normal = Vector3(0,0,0)
			if len(facet) == 3:
				normal = (facet.vertex(1) - facet.vertex(0)).cross(facet.vertex(2) - facet.vertex(0))
			elif len(facet) > 3:
				mid_point = Vector3(0,0,0)
				for vertex in facet:
					mid_point += vertex
				mid_point /= len(facet)

				vertices = facet.vertices
				for v1, v2 in zip(vertices, vertices[1:] + vertices[:1]):
					normal += (v1 - mid_point).cross(v2 - mid_point).norm()
			normal = normal.norm()

			# If face has a provided normal value, invert calculated normal to match provided normal's facing
			if has_given_normal and given_normal.dot(normal) < 0:
				normal *= -1

			# Assign normal
			facet.normal = normal

		return mesh

	except FileNotFoundError:
		raise FileNotFoundError(f'parse_obj: Failed to locate file "{file_path}" in the current directory.')